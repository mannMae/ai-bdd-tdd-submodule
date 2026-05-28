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
  from src.auth import constants as auth_constants
  from src.notifications import service as notification_service
  from src.posts.constants import ErrorCode as PostsErrorCode
  ```

### ③ 데이터베이스 테이블 및 컬럼 명명 규칙 (Naming Conventions)
데이터베이스 설계의 일관성과 타 시스템 연동의 용이성을 위해 다음 컨벤션을 준수합니다.
1. **lower_case_snake**: 모든 테이블 및 컬럼 이름은 소문자 스네이크 케이스를 사용합니다.
2. **단수형 테이블 이름**: 복수형(`posts`, `users`) 대신 단수형(`post`, `user`, `user_playlist`)을 사용합니다.
3. **도메인 접두사 그룹화**: 연관된 테이블은 동일한 모듈 접두사로 그룹화합니다. (예: `payment_account`, `payment_bill`)
4. **일관된 접미사 구조**:
   - 일시/시각 타입 컬럼은 `_at` 접미사를 사용합니다. (예: `created_at`, `published_at`)
   - 날짜 타입 컬럼은 `_date` 접미사를 사용합니다. (예: `birth_date`, `due_date`)
   - 외래 키는 타겟 식별자를 명확히 드러내도록 `_id` 접미사를 일관되게 사용합니다. (예: `profile_id`, `post_id`)

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

### ③ BackgroundTasks vs 백그라운드 분산 작업 큐 (Celery / Arq / RQ)
FastAPI 내부의 `BackgroundTasks`는 응답 반환 후 **동일한 워커 프로세스 내에서 실행**되므로 남용 시 서버 리소스를 잠식하거나 유실 위험이 높습니다.
- **BackgroundTasks 사용 기준**: 태스크 수행 시간이 매우 짧고(< 1초), 태스크가 실패하여 유실되더라도 시스템에 치명적이지 않은 무해한 작업(예: 이메일 전송, 단순 로그 기록).
- **분산 작업 큐 사용 기준**: 태스크 수행 시간이 수 초~수 분 이상으로 길거나, CPU 집약적이거나, 실패 시 재시도(Retry), 지연 실행(ETA), cron 예약 실행이 필요한 경우(예: 결제 처리, 대용량 PDF 문서 해석, OCR 파싱).
- *Rule of thumb*: **만약 해당 태스크가 비정상 종료되어 소실되었을 때 개발자에게 긴급 장애 알림(Page)이 발송되어야 하는 중요 작업이라면, 절대 `BackgroundTasks`에 할당하지 말고 분산 작업 큐로 오프로드하십시오.**

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
      model_config = ConfigDict(populate_by_name=True, from_attributes=True)

      @field_serializer("*", when_used="json", check_fields=False)
      def serialize_datetimes(self, value):
          if isinstance(value, datetime):
              if value.tzinfo is None:
                  value = value.replace(tzinfo=ZoneInfo("UTC"))
              return value.strftime("%Y-%m-%dT%H:%M:%S%z")
          return value
  ```

### ② 도메인별 BaseSettings 분리 선언
- 단일 글로벌 `.env` 파일에 백엔드의 모든 설정을 단일 클래스로 로드하지 마십시오.
- **도메인 격리성**을 위해 각 도메인 패키지 하위의 `config.py`에 전용 `BaseSettings`를 선언하고, `env_prefix`를 부여하여 격리하여 선언합니다.
  ```python
  # src/auth/config.py
  from pydantic_settings import BaseSettings, SettingsConfigDict

  class AuthSettings(BaseSettings):
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

### ③ Pydantic 내 `ValueError` 발생 및 API 자동 매핑 규칙
- Pydantic 스키마 내의 `field_validator` 등에서 특정 제약 조건을 충족하지 못해 `ValueError`를 발생시키면, FastAPI가 이를 자동으로 감지하여 클라이언트에게 규격화된 **422 Unprocessable Entity (ValidationError)** JSON 응답을 반환합니다. 억지로 비즈니스 예외로 래핑하여 던지지 마십시오.
  ```python
  from pydantic import BaseModel, field_validator
  import re

  class ProfileCreateSchema(BaseModel):
      username: str
      password: str

      @field_validator("password", mode="after")
      @classmethod
      def validate_strength(cls, v: str) -> str:
          if not re.match(r"^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$", v):
              raise ValueError("비밀번호는 최소 8자 이상이며 영문과 숫자를 포함해야 합니다.")
          return v
  ```

### ④ 직렬화 성능 오버헤드 인지 규칙
- FastAPI 라우터가 Pydantic 모델 인스턴스(객체)를 그대로 반환하면, 내부적으로 `jsonable_encoder`를 통해 dict로 파싱한 후 다시 `response_model` 스펙에 맞추어 검증하고 JSON으로 변환합니다.
- 즉, **Pydantic 인스턴스 생성이 2번 발생**하는 불필요한 성능 오버헤드가 동반됩니다. 성능이 극도로 민감한 API 엔드포인트에서는 Pydantic 객체를 직접 반환하는 대신, dict 또는 Raw SQL 반환값(Mapping) 구조를 리턴하는 것을 고려하십시오.

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
  DatabaseSessionDep = Annotated[AsyncSession, Depends(get_db_session)]

  @router.get("/users/me")
  async def read_users_me(db: DatabaseSessionDep):
      return {"status": "active"}
  ```

### ② 의존성 체이닝(Dependency Chaining) 및 캐시 활용
- FastAPI의 의존성 주입은 기본적으로 한 번의 HTTP 요청 내에서 실행 결과를 캐싱합니다. 여러 의존성에서 동일한 DB 세션 또는 현재 유저 정보(`get_current_user`)를 호출하더라도 캐싱을 통해 1회만 연산이 수행되므로 안심하고 체이닝하여 작성하십시오.

### ③ 데이터 유효성 검사 도구로서의 Depends 활용 (Beyond DI)
- Pydantic은 단순 데이터 스키마 유효성만 검증할 뿐, 데이터베이스 조회나 외부 API 호출 등이 수반되는 비즈니스적 제약 조건 검증은 수행하지 못합니다.
- **데이터베이스 제약 조건 검사(ID 존재 여부, 권한 검증 등) 로직은 라우터 바디가 아닌 `Depends` 의존성 함수로 격리하십시오.** 이를 통해 여러 라우터 엔드포인트 간의 중복 검사 로직을 방지하고 테스트 작성을 단순화할 수 있습니다.
  ```python
  # dependencies.py
  async def get_valid_post(post_id: int, db: DatabaseSessionDep) -> Post:
      post = await service.get_post_by_id(db, post_id)
      if not post:
          raise PostNotFoundException()  # 404 HTTP Exception
      return post

  # router.py
  @router.get("/posts/{post_id}", response_model=PostResponse)
  async def get_post(post: Annotated[Post, Depends(get_valid_post)]):
      # 이미 존재 여부가 검증된 post 객체가 안전하게 주입됩니다.
      return post

  @router.put("/posts/{post_id}", response_model=PostResponse)
  async def update_post(
      update_data: PostUpdate,
      post: Annotated[Post, Depends(get_valid_post)],
      db: DatabaseSessionDep
  ):
      return await service.update(db, post.id, update_data)
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
  ```

### ② SQL-first, Pydantic-second 규칙
- 데이터베이스 스키마와 관련된 모든 정의 및 제약조건은 SQLAlchemy / SQLModel ORM 스키마 수준에서 완벽하게 정의해야 합니다. Pydantic의 데이터 직렬화 속성은 ORM 정의를 따르는 보조적 요소여야 합니다.
- 데이터베이스 조인 및 데이터 결합 연산 등은 CPython 수준에서 복잡하게 연산하기보다 SQL 및 DB Query 단에서 해결하는 것이 속도와 처리 비용 측면에서 극도로 유리합니다.

### ③ Alembic 정적 마이그레이션 및 파일 템플릿
1. **정적이고 가역적인 마이그레이션**: 마이그레이션 파일이 런타임에 동적으로 변경되는 외부 변수에 영향받아서는 안 됩니다. 또한 모든 마이그레이션은 `upgrade()`와 `downgrade()`가 모두 완벽히 구현되어 롤백이 완벽히 지원되어야 합니다.
2. **파일명 템플릿 표준화**: 마이그레이션 생성 시 날짜와 마이그레이션 목적을 직관적으로 확인할 수 있도록 `alembic.ini` 파일에 다음 템플릿 구성을 강제 적용합니다.
   ```ini
   # alembic.ini
   file_template = %%(year)d-%%(month).2d-%%(day).2d_%%(slug)s
   ```
   * 생성 예시: `2026-05-28_add_user_profile_table.py`

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

### ③ 의존성 오버라이드(`dependency_overrides`)를 통한 모킹 간소화
- 테스트 코드에서 내부 모듈을 복잡하게 monkeypatch하거나 mocking하지 마십시오.
- FastAPI가 자체 제공하는 `app.dependency_overrides`를 활용하여 외부 연동 클라이언트나 인증 검사 로직(예: JWT 파서)을 테스트용 Fake/Stub 객체로 완벽히 대체하여 테스트 격리성을 유지하십시오.
  ```python
  from src.auth.dependencies import parse_jwt_data
  from src.main import app
  import pytest

  def fake_jwt_parser():
      return {"user_id": 1, "role": "admin"}

  @pytest.fixture(autouse=True)
  def override_dependencies():
      # 테스트 기동 시 JWT 파서를 가짜 파서로 대체
      app.dependency_overrides[parse_jwt_data] = fake_jwt_parser
      yield
      # 테스트 완료 후 원상 복구
      app.dependency_overrides.clear()
  ```

### ④ Ruff 스타일 가이딩 강제
- 코드 스타일 일관성을 보장하기 위해 기존의 `black`, `isort`, `autoflake`, `flake8`을 단일 도구로 완벽히 대체하는 **`ruff`**를 린터 및 포맷터로 강제합니다. 모든 PR 빌드 시 린트 오류가 없을 것을 준수해야 합니다.

---

## 7. API 문서 및 Swagger 제어 규칙
API 문서화(Swagger UI)는 개발 편의성을 대폭 높여주지만, 프로덕션 환경의 정보 노출 방지를 위해 엄격히 제어되어야 합니다.

### ① openapi_url 환경별 차등 비활성화
- 로컬(`local`) 및 스테이징(`staging`) 환경을 제외한 운영(Production) 배포 환경에서는 Swagger UI와 OpenAPI 명세 문서가 외부에 노출되지 않도록 `openapi_url` 설정을 명시적으로 비활성화해야 합니다.
  ```python
  # src/main.py
  from fastapi import FastAPI
  from src.config import settings

  SHOW_DOCS_ENVIRONMENTS = {"local", "staging"}

  app_configs = {"title": "Docflow Backend API"}

  # 운영 환경에서는 OpenAPI 스펙 제공 주소를 비활성화하여 문서 노출 차단
  if settings.ENVIRONMENT not in SHOW_DOCS_ENVIRONMENTS:
      app_configs["openapi_url"] = None
      app_configs["docs_url"] = None
      app_configs["redoc_url"] = None

  app = FastAPI(**app_configs)
  ```

### ② 라우터 데코레이터 내 다중 응답(HTTP Status Codes) 명세화
- API 문서의 가독성과 프론트엔드 코드 생성 자동화 도구의 신뢰성을 극대화하기 위해, 정상 응답 이외에 발생 가능한 특수 응답 규격(예: 201 Created, 202 Accepted)이나 도메인 오류 상황에 대해 `responses` 파라미터를 사용해 Pydantic 스키마를 정밀하게 명세하십시오.
  ```python
  from fastapi import APIRouter, status

  router = APIRouter()

  @router.post(
      "/items",
      response_model=ItemDefaultResponse,
      status_code=status.HTTP_201_CREATED,
      responses={
          status.HTTP_200_OK: {
              "model": ItemSuccessResponse,
              "description": "기존에 매칭되는 리소스가 존재하여 정상 수정됨"
          },
          status.HTTP_202_ACCEPTED: {
              "model": ItemAcceptedResponse,
              "description": "생성 요청이 수락되어 백그라운드 큐에서 처리 중"
          }
      }
  )
  async def create_item(payload: ItemCreateSchema):
      pass
  ```
