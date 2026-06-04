---
name: database-conventions
description: SQLAlchemy async session lifecycles, N+1 query prevention (eager loading), soft delete policies, and transaction boundaries (no external HTTP calls inside transactions).
version: 1.0.0
globs: "apps/backend/src/**/models.py, apps/backend/src/**/service.py, apps/backend/src/database.py"
alwaysApply: false
---

# 🗄️ Database Conventions & Transaction Boundary Guidelines

이 스킬은 백엔드 서비스 개발 시 비동기 SQLAlchemy ORM을 안정적으로 사용하고, 데이터 일관성과 성능을 통제하기 위한 규칙을 다룹니다.

---

## 1. 🔄 비동기 세션 생명주기 관리 (Async Session Lifecycle)

1. **단일 세션 범위 준수 (Unit of Work)**:
   - 하나의 HTTP 요청은 단 하나의 비동기 데이터베이스 세션(`AsyncSession`)을 가져야 하며, 단일 트랜잭션 범위 안에서 비즈니스를 완수합니다.
   - 라우터 레벨에서 `Depends(get_db)`를 통해 동일 세션 인스턴스를 주입받아야 하며, 임의로 전역 엔진에서 새 세션을 개설해 사용해서는 안 됩니다.
2. **비동기 컨텍스트 매니저 사용**:
   - `SessionFactory()`를 수동으로 개설할 때는 반드시 `async with` 블록을 통하여 세션이 예외 발생 여부와 무관하게 안전히 클로즈(`close()`)되도록 설계합니다.

---

## 2. 🚧 트랜잭션 경계 규칙 (Transaction Boundary Rules)

1. **외부 API 호출 격리 (Strict Isolation)**:
   - 데이터베이스 트랜잭션 블록(`db.begin()` 또는 `flush() ~ commit()` 구간) 내부에서는 **절대 외부 서드파티 HTTP API 호출이나 Redis 블로킹 연산을 수행해서는 안 됩니다.**
   - 외부 API 응답 지연이 트랜잭션 유휴 시간을 늘려 커넥션 풀 고갈 장애로 이어지는 것을 예방하기 위함입니다.
   - *Good*:
     ```python
     # 1. 외부 API 호출을 먼저 완료
     user_info = await payment_client.verify(token)
     # 2. 트랜잭션 시작 후 쓰기 수행
     async with db.begin():
         model = UserModel(name=user_info["name"])
         db.add(model)
     ```
   - *Bad*:
     ```python
     async with db.begin():
         model = UserModel(name="temp")
         db.add(model)
         # 트랜잭션 내부에서 네트워크 API 통신을 수행하여 락 타임 증가!
         user_info = await payment_client.verify(token) 
         model.name = user_info["name"]
     ```

---

## 3. ⚡ N+1 쿼리 방지 및 조회 최적화 (Query Optimization)

1. **Eager Loading 명시**:
   - 관계형 모델(Relationship)이 정의된 자원을 다대일(M:1) 또는 일대다(1:M)로 조회할 때, 루프 내에서 연관 필드를 참조함으로써 개별 SQL이 발행(N+1 문제)되는 일을 금지합니다.
   - 관계된 테이블은 조회 쿼리 단계에서 `selectinload`(1:N/N:M 관계에 유리) 또는 `joinedload`(N:1 관계에 유리)를 반드시 선언하여 조인 쿼리 한 번으로 데이터를 가져와야 합니다.
   - *Good*:
     ```python
     from sqlalchemy.orm import selectinload
     stmt = select(PostModel).options(selectinload(PostModel.comments))
     result = await db.execute(stmt)
     posts = result.scalars().all()
     ```
   - *Bad*:
     ```python
     stmt = select(PostModel)
     result = await db.execute(stmt)
     posts = result.scalars().all()
     for post in posts:
         print(post.comments) # 각각 comments 조회를 위한 쿼리가 매번 실행되어 N+1 발생!
     ```

---

## 4. 🗑️ Soft Delete (소프트 딜리트) 표준

1. **물리 삭제 금지**:
   - 비즈니스 핵심 사용자 데이터는 데이터 복구 가능성 및 오디팅을 위해 SQL `DELETE` 쿼리로 물리 삭제하는 것을 피하고, `is_deleted` 플래그 필드를 이용해 논리 삭제 처리합니다.
   - 모든 도메인 조회 로직(`BE-DOMAIN-SERVICE` 등)은 기본적으로 `is_deleted == False` 조인 필터를 포함해야 합니다.
