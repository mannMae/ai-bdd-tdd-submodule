---
description: FastAPI 백엔드 아키텍처, Pydantic 스키마 검증 및 데이터 흐름 가이드레일
glob: "apps/backend/**/*"
---
# 7. 백엔드(FastAPI) 개발 가이드레일

FastAPI 백엔드 서버의 견고한 구조, 보안 향상, 그리고 API 명세의 명확성을 유지하기 위해 AI 에이전트가 반드시 준수해야 하는 규칙입니다.

## 1. 아키텍처 및 레이어드 패턴 (Layered Architecture)
모든 백엔드 코드는 관심사의 분리(Separation of Concerns)를 달성하기 위해 아래 구조를 엄격히 따릅니다.

- **API/Router Layer (`src/api/`)**: HTTP 요청 수신, 인증 검증, 응답 반환만을 담당합니다. 이 계층에 복잡한 비즈니스 로직이나 DB 직접 쿼리를 배치하지 마십시오.
- **Service Layer (`src/services/`)**: 핵심 비즈니스 로직, 데이터 계산, 외부 연동(AI 모델 호출, 서드파티 API) 등을 담당합니다.
- **Data/Repository Layer (`src/models/` 또는 `src/repository/`)**: 데이터베이스 모델 정의 및 데이터 직접 조작(CRUD)을 담당합니다.

```
src/
├── api/             # API 엔드포인트 정의 (APIRouter)
│   ├── v1/          # API 버저닝 분수
│   └── dependencies.py # 공통 의존성 주입 (DB 세션, 인증 등)
├── schemas/         # Pydantic DTO (Request/Response 검증 모델)
├── services/        # 비즈니스 로직 및 외부 모듈 연동
├── models/          # 데이터베이스 ORM 엔티티 (SQLAlchemy, SQLModel 등)
└── main.py          # 애플리케이션 진입점 및 전역 설정
```

## 2. DTO 패턴 준수 및 Pydantic 활용 규칙
- **데이터베이스 모델 반환 금지**: 데이터베이스 ORM 객체(예: SQLAlchemy Entity)를 API 응답으로 직접 반환하거나 클라이언트로부터 직접 받지 마십시오.
- **반환형 강제**: 모든 라우터 데코레이터에는 반드시 `response_model`을 명시해야 합니다.
  * 올바른 예: `@router.post("/items", response_model=ItemResponseSchema)`
- **스키마 구분**: 입력 데이터 검증용 `{Action}RequestSchema`와 출력 데이터 제어용 `{Action}ResponseSchema`를 분리하여 작성하십시오. 이를 통해 비밀번호나 내부 상태값 등 민감한 정보가 API를 통해 외부에 노출되는 것을 사전에 차단하십시오.

## 3. 의존성 주입 (Dependency Injection) 규칙
- 데이터베이스 세션, 환경 설정(Config), 현재 로그인한 유저 정보 등 모든 리소스 및 컨텍스트는 FastAPI의 의존성 주입 도구인 `Depends`를 사용하여 라우터 또는 필요한 위치에 주입하십시오.
- 글로벌 변수로 DB 커넥션 풀을 들고 와 인라인으로 세션을 생성하는 것을 금지합니다.
  * 올바른 예:
    ```python
    @router.get("/profile", response_model=UserProfileResponse)
    def get_profile(
        current_user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
    ):
        return current_user
    ```

## 4. 예외 처리 및 응답 형식 표준화
- 예외 상황이 발생했을 때 예외를 콘솔에 `print`만 하거나 날것의 500 에러를 던지지 마십시오.
- 사전에 정의된 커스텀 예외(`HTTPException` 상속)를 던지고, 전역 Exception Handler를 구현하여 클라이언트에게 규격화된 에러 JSON 포맷을 반환하십시오.
  * 예시 응답 규격:
    ```json
    {
      "success": false,
      "error": {
        "code": "USER_NOT_FOUND",
        "message": "해당 사용자를 찾을 수 없습니다."
      }
    }
    ```
- 로깅 시에는 Python 표준 `logging` 라이브러리를 활용하여 구조화된 로그를 남겨야 합니다.
