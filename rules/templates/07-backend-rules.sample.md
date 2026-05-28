---
description: FastAPI 백엔드 아키텍처, Pydantic 스키마 검증, 비동기 동시성 제어 및 테스트 가이드레일
glob: "apps/backend/**/*"
---
# 7. 백엔드(FastAPI) 개발 가이드레일

본 가이드는 FastAPI 기반 백엔드 애플리케이션의 도메인 응집성, 확장성, 비동기 이벤트 루프 안정성, 그리고 높은 테스트 용이성을 확보하기 위해 AI 에이전트가 반드시 준수해야 하는 규칙입니다.

---

## 1. 도메인(Bounded Context) 중심 디렉토리 구조 (Project Structure)
모든 백엔드 애플리케이션 코드는 파일 타입(MVC)별 전역 격리가 아닌, 비즈니스 영역에 따라 도메인별로 응집력 있게 격리하는 **Feature-First(도메인 중심)** 구조를 따릅니다.

### ① 디렉토리 구성 표준
```
src/
├── {domain}/            # 예: auth/, posts/, comments/, aws/
│   ├── router.py        # API 엔드포인트 정의
│   ├── schemas.py       # Pydantic 입력/출력 검증 모델 (DTO)
│   ├── models.py        # SQLAlchemy / SQLModel ORM 엔티티
│   ├── service.py       # 도메인 비즈니스 로직
│   ├── dependencies.py  # 라우터 전용 의존성 (Depends)
│   ├── config.py        # 도메인 로컬 BaseSettings 설정
│   ├── constants.py     # 도메인 내 상수 및 비즈니스 에러 코드
│   ├── exceptions.py    # 도메인 전용 커스텀 예외
│   └── utils.py         # 도메인 내 헬퍼 함수
├── config.py            # 전역 BaseSettings 설정
├── models.py            # 공통 Pydantic/ORM 베이스 모델
├── exceptions.py        # 전역 예외 및 Exception Handler
├── database.py          # 데이터베이스 연결 관리 (AsyncSession 팩토리)
└── main.py              # FastAPI 인스턴스 기동 및 Lifespan 설정
```
> [!NOTE]
> Bounded Context 내부의 코드는 해당 폴더 안에서 해결하는 것을 원칙으로 합니다. 불필요하게 타 폴더의 내부 파일을 직접 다중 참조하지 마십시오.

### ② 크로스 도메인(Cross-Domain) 임포트 규칙
- 다른 도메인의 서비스나 상수를 가져올 때는 반드시 **명시적인 모듈 경로**를 지정하여 가져옵니다. 와일드카드(`from src.auth import *`) 사용은 절대 금지합니다.
- 예시:
  ```python
  # 올바른 크로스 도메인 임포트 예시
  from src.auth import constants as auth_constants
  from src.notifications import service as notification_service
  from src.posts.constants import ErrorCode as PostsErrorCode
  ```

---

## 2. Async / Sync 라우터 분기 및 동시성 제어 규칙
FastAPI는 비동기 기반 웹 프레임워크이므로 동기식 블로킹 연산이 이벤트 루프를 장악해 서버 전체를 멈추지 않게 통제해야 합니다.

### ① 실행 방식 결정 규칙
| 작업의 성격 | 라우터 선언 방식 | 실행 및 오프로드 방법 |
| :--- | :--- | :--- |
| **비동기 I/O** (DB, HTTP 호출 등) | `async def` | `await` 키워드를 사용하여 제어권을 양보 |
| **동기 블로킹 I/O** (동기 SDK, Excel 가공 등) | `def` (일반 함수) | FastAPI 내부 스레드풀(Thread Pool)에 자동 위임 |
| **혼합형 I/O** (동작 중 일부만 동기 블로킹) | `async def` | `fastapi.concurrency.run_in_threadpool`로 동기 영역만 래핑 |
| **CPU-bound 무거운 연산** (계산, 영상 압축 등) | `async def` / `def` | Celery, Arq 등 별도 프로세스 백그라운드 태스크 큐로 이관 |

### ② 올바른 동시성 제어 예제
```python
import asyncio
import time
from fastapi import APIRouter
from fastapi.concurrency import run_in_threadpool

router = APIRouter()

# ❌ 나쁜 예: async def 내에서 동기식 time.sleep을 실행하여 전체 이벤트 루프를 마비시킴
@router.get("/bad-ping")
async def bad_ping():
    time.sleep(5)  # 5초 동안 전 서버의 모든 요청 처리가 블로킹됨
    return {"pong": True}

#  올바른 예 1: 비동기 논블로킹 I/O 처리
@router.get("/async-ok")
async def async_ok():
    await asyncio.sleep(5)  # 대기 시간 동안 이벤트 루프가 다른 클라이언트 요청을 처리함
    return {"pong": True}

#  올바른 예 2: 동기 I/O는 일반 def로 선언하여 스레드풀에서 안전하게 실행
@router.get("/sync-ok")
def sync_ok():
    time.sleep(5)  # 스레드가 대기하므로 메인 이벤트 루프는 정상 작동함
    return {"pong": True}

#  올바른 예 3: async def 내부에서 불가피하게 동기 라이브러리를 호출할 때 
@router.get("/wrap-sync")
async def wrap_sync(item_id: str):
    # run_in_threadpool을 사용해 특정 동기 처리만 스레드풀로 전송
    result = await run_in_threadpool(legacy_sync_library.fetch_data, item_id)
    return result
```

---

## 3. Pydantic v2 DTO 및 도메인별 BaseSettings 규칙
Pydantic v2 API를 적극 활용하여 강력한 데이터 정합성 검증과 최신 직렬화 모범 사례를 적용하십시오.

### ① Pydantic v2 준수 가이드레일
- 구형 v1의 `.dict()` 메서드는 폐기되었습니다. 모델 덤프 시 반드시 `.model_dump()` 또는 `.model_dump_json()`을 사용하십시오.
- `json_encoders` 옵션은 더 이상 사용되지 않습니다. 커스텀 포맷 직렬화는 `@field_serializer` 데코레이터를 사용해야 합니다.
- **Datetime 공통 포맷 보장을 위한 Custom Base Model 예시**:
  ```python
  from datetime import datetime
  from zoneinfo import ZoneInfo
  from pydantic import BaseModel, ConfigDict, field_serializer

  class CustomBaseModel(BaseModel):
      # ORM 객체의 속성을 Pydantic에서 쉽게 읽을 수 있도록 지원
      model_config = ConfigDict(populate_by_name=True, from_attributes=True)

      @field_serializer("*", when_used="json", check_fields=False)
      def serialize_datetimes(self, value):
          if isinstance(value, datetime):
              # Timezone 정보가 없는 naive datetime의 경우 UTC 강제 지정
              if value.tzinfo is None:
                  value = value.replace(tzinfo=ZoneInfo("UTC"))
              return value.strftime("%Y-%m-%dT%H:%M:%S%z")
          return value
  ```

### ② 도메인별 BaseSettings 분리 선언
- 단일 글로벌 `.env` 파일에 백엔드의 수백 개 설정을 다 쑤셔 넣고 단일 클래스로 로드하지 마십시오.
- **도메인 격리성**을 위해 각 도메인 패키지 하위의 `config.py`에 전용 `BaseSettings`를 선언하고, `env_prefix`를 부여하여 격리하여 선언합니다.
  ```python
  # src/auth/config.py
  from pydantic_settings import BaseSettings, SettingsConfigDict

  class AuthSettings(BaseSettings):
      # AUTH_ 접두사가 붙은 환경변수만 읽어들이며 매핑되지 않는 무관한 변수는 ignore 처리
      model_config = SettingsConfigDict(
          env_prefix="AUTH_", 
          env_file=".env", 
          extra="ignore"
      )

      JWT_SECRET: str
      JWT_ALGORITHM: str = "HS256"
      ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

  auth_settings = AuthSettings()
  ```

---

## 4. 의존성 주입 (Annotated & Chained Dependencies)
의존성 주입 체계를 구형 디폴트 인자 주입 방식에서 가독성과 타입 안정성이 뛰어난 `Annotated` 형식으로 일원화합니다.

### ① Annotated 구문 표준화
- `Annotated[Type, Depends(dependency_function)]` 방식을 의무화합니다.
- 예시:
  ```python
  from typing import Annotated
  from fastapi import APIRouter, Depends
  from sqlalchemy.ext.asyncio import AsyncSession
  from src.database import get_db_session

  router = APIRouter()

  # 타입 정의를 통해 재사용성과 가독성을 높입니다.
  DatabaseSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

  @router.get("/users/me")
  async def read_users_me(db: DatabaseSessionDep):
      # db 객체는 타입 추론이 가능하여 자동완성 및 정적 분석 혜택을 온전히 받습니다.
      return {"status": "active"}
  ```

### ② 의존성 체이닝(Dependency Chaining) 및 캐시 활용
- FastAPI의 의존성 주입은 기본적으로 한 번의 HTTP 요청 내에서 실행 결과를 캐싱합니다. 여러 의존성에서 동일한 DB 세션 또는 현재 유저 정보(`get_current_user`)를 호출하더라도 캐싱을 통해 1회만 연산이 수행되므로 안심하고 체이닝하여 작성하십시오.
  ```python
  # 의존성 체이닝 예시
  async def get_active_user(
      current_user: Annotated[User, Depends(get_current_user)]
  ) -> User:
      if not current_user.is_active:
          raise UserInactiveException()
      return current_user

  # 라우터 수준에서는 활성화된 유저 정보만 바로 바인딩
  @router.get("/dashboard")
  async def get_dashboard(user: Annotated[User, Depends(get_active_user)]):
      return {"data": "ok"}
  ```

---

## 5. 데이터베이스 키 명명 규칙 및 Alembic 마이그레이션 규칙
데이터베이스 마이그레이션 도중 예기치 못한 제약 조건 충족 오류나 정합성 불일치를 방지하고, 모든 타겟 데이터베이스(PostgreSQL, SQLite, MySQL 등)에서 일관된 마이그레이션 동작을 보장해야 합니다.

### ① SQLAlchemy Metadata 명명 규칙(Naming Convention) 지정
- 외래키, 인덱스, 유니크 제약조건 등의 이름이 DBMS에 따라 제각각으로 생성되는 것을 원천 차단하기 위해 SQLAlchemy의 `MetaData` 생성 시 아래 컨벤션을 명시해야 합니다.
  ```python
  # src/models.py 또는 database.py
  from sqlalchemy import MetaData

  POSTGRES_NAMING_CONVENTION = {
      "ix": "ix_%(column_0_label)s",
      "uq": "uq_%(table_name)s_%(column_0_name)s",
      "ck": "ck_%(table_name)s_%(constraint_name)s",
      "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
      "pk": "pk_%(table_name)s"
  }

  metadata = MetaData(naming_convention=POSTGRES_NAMING_CONVENTION)
  # 이후 선언되는 Base 모델이 위 metadata를 사용하도록 설계합니다.
  ```

### ② SQL-first, Pydantic-second 규칙
- 데이터베이스 스키마와 관련된 모든 정의 및 제약조건은 SQLAlchemy / SQLModel ORM 스키마 수준에서 완벽하게 정의해야 합니다. Pydantic의 데이터 직렬화 속성은 ORM 정의를 따르는 보조적 요소여야 합니다.
- Alembic 마이그레이션 생성 시 `alembic revision --autogenerate` 스크립트를 사용하여 마이그레이션 파일을 만들고, 반드시 업그레이드(`upgrade()`)와 다운그레이드(`downgrade()`) 코드 모두가 정상 작동하는지 마이그레이션 파일을 실행하여 확인하십시오.

---

## 6. 비동기 테스트 및 도구 규칙 (Day 0 Async Testing)
백엔드 기능의 견고함을 입증하기 위해, 테스트 클라이언트는 처음부터 비동기로 설계하여 동기/비동기 호출 충돌을 방지합니다.

### ① 비동기 테스트 클라이언트 구성 규칙 (httpx & ASGITransport)
- `httpx.AsyncClient`와 `httpx.ASGITransport`를 사용하여 서버 프로세스를 실제로 띄우지 않고 메모리 내에서 ASGI 앱과 연동하여 고성능 비동기 API 요청 테스트를 수행합니다.
  ```python
  import pytest
  from httpx import AsyncClient, ASGITransport
  from src.main import app

  @pytest.fixture
  async def async_client():
      # ASGITransport를 사용해 인프로세스 ASGI 루프로 요청 처리
      transport = ASGITransport(app=app)
      async with AsyncClient(transport=transport, base_url="http://test") as ac:
          yield ac

  @pytest.mark.asyncio
  async def test_get_health(async_client: AsyncClient):
      response = await async_client.get("/health")
      assert response.status_code == 200
      assert response.json() == {"status": "ok"}
  ```

### ② 데이터베이스 격리를 위한 트랜잭션 롤백(Rollback) 테스트 패턴
- 테스트 중에 데이터베이스에 데이터를 삽입/삭제하더라도 다른 테스트나 실 DB에 영향을 미치지 않도록, 개별 테스트 시작 시 데이터베이스 트랜잭션을 시작하고 테스트 종료 시 무조건 `rollback`을 수행하는 Pytest Fixture를 강제합니다.

### ③ Ruff 스타일 가이딩 강제
- 코드 스타일 일관성을 보장하기 위해 기존의 `black`, `isort`, `autoflake`, `flake8`을 단일 도구로 완벽히 대체하는 **`ruff`**를 린터 및 포맷터로 강제합니다. 모든 PR 빌드 시 린트 오류가 없을 것을 준수해야 합니다.
