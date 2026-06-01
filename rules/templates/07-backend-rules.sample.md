---
description: FastAPI 백엔드 아키텍처, Pydantic 스키마 검증, 비동기 동시성 제어 및 테스트 가이드레일
glob: "apps/backend/**/*"
---
# 7. 백엔드(FastAPI) 개발 가이드레일

본 가이드는 FastAPI 기반 백엔드 애플리케이션의 높은 안정성과 일관성을 확보하기 위해 AI 에이전트가 반드시 준수해야 하는 규칙입니다. 코드의 세부 구현 양식(Boilerplate)은 하단의 **10. RTM 대응 표준 코드 양식**을 참조하십시오.

---

## 1. 도메인(Bounded Context) 중심 디렉토리 구조 (Project Structure)
*   **Feature-First 구조**: 파일 타입별(MVC) 전역 격리가 아닌, 비즈니스 영역에 따라 도메인별로 코드를 응집력 있게 구성합니다.
*   **디렉토리 표준**: `src/{domain}/` 하위에 `router.py` (API), `schemas.py` (DTO), `models.py` (ORM), `service.py` / `usecases/` (비즈니스 로직)을 모아둡니다.
*   **상세 구조 및 규칙**: 세부 디렉토리 구조와 Bounded Context 간 상호 참조 임포트 규칙은 프로젝트의 기본 골격을 유지하며, 하단의 **10. RTM 대응 표준 코드 양식**의 [services] 및 [models/deps] 양식을 준수합니다.

---

## 2. Async / Sync 라우터 분기 및 동시성 제어 규칙
*   **비동기 I/O**: DB 조회, HTTP 외부 호출 등 I/O 대기가 발생하는 작업은 반드시 `async def`와 `await`를 사용합니다.
*   **동기 블로킹 금지**: `async def` 내부에서 동기식 블로킹 함수(`time.sleep`, `requests.get`, 동기 DB 세션 등)를 실행하여 이벤트 루프를 마비시키는 행위를 절대 금지합니다.
*   **동기 작업 오프로딩**: 불가피하게 동기 라이브러리를 호출할 때는 일반 `def` 라우터로 선언(FastAPI가 스레드풀로 오프로드)하거나, `fastapi.concurrency.run_in_threadpool`로 감싸서 실행합니다.
*   **코드 양식**: [10. RTM 대응 표준 코드 양식 - ④ dependencies](#dependencies)를 참고하십시오.

---

## 3. Pydantic v2 DTO 및 도메인별 BaseSettings 규칙
*   **Pydantic v2 규칙 준수**: 모델 직렬화 시 `.dict()` 대신 `.model_dump()` 또는 `.model_dump_json()`을 사용하며, 커스텀 직렬화는 `@field_serializer` 데코레이터를 적용합니다.
*   **도메인별 BaseSettings 분리**: 전역 환경 설정 파일 하나에 모든 설정을 밀어넣지 말고, 도메인 패키지 하위의 `config.py`에 `env_prefix`를 부여한 개별 `BaseSettings`를 선언합니다.
*   **DTO/VO 분리**: API 입출력용 DTO 스키마(`schemas.py`)와 비즈니스 연산용 값 객체(VO)를 엄격히 분리하여 사용합니다. DTO에서 데이터를 검증한 후, 서비스 레이어 진입 시 즉시 VO 객체로 매핑합니다.
*   **코드 양식**: [10. RTM 대응 표준 코드 양식 - ② services](#services) 및 [③ models/deps](#modelsdeps)를 참고하십시오.

---

## 4. 의존성 주입 (Annotated & Chained Dependencies)
*   **Annotated 구문 표준화**: 디폴트 인자 기반의 Depends 사용을 금지하며, 반드시 `Annotated[Type, Depends(dependency_function)]` 양식을 준수합니다.
*   **비즈니스 유효성 검사용 Depends**: 단순 DB 세션 주입을 넘어, ID 존재 여부 확인이나 권한 검증 등 비즈니스 제약 검사를 라우터 바디가 아닌 `Depends` 의존성 함수로 격리하여 재사용합니다.
*   **코드 양식**: [10. RTM 대응 표준 코드 양식 - ① routers](#routers)를 참고하십시오.

---

## 5. 데이터베이스 키 명명 규칙 및 Alembic 마이그레이션 규칙
*   **SQLAlchemy Metadata 컨벤션**: 외래키(FK), 유니크(UQ), 인덱스(IX) 등이 DBMS에 따라 다르게 생성되지 않도록 명시적인 `naming_convention`을 지정합니다.
*   **Alembic 정적 마이그레이션**: 마이그레이션 파일이 런타임 변수에 영향받지 않게 작성하며, 반드시 롤백(`downgrade()`)이 완벽히 지원되도록 작성합니다. 파일명은 `alembic.ini` 설정에 맞춰 날짜와 slug가 포함되게 자동 템플릿화합니다.
*   **코드 양식**: [10. RTM 대응 표준 코드 양식 - ④ dependencies](#dependencies)를 참고하십시오.

---

## 6. 비동기 테스트 및 개발 표준 (Testing & Standards)
*   **BDD-TDD 프로세스 흐름**: 모든 백엔드 테스트 작성 및 개발은 [04. 테스트 작성 원칙](file:///rules/04-test-rules.md)을 엄격히 준수합니다. `유저플로우 ➔ 시나리오 ➔ 통합테스트 ➔ 유닛테스트 ➔ 유닛 코드` 순서를 지키고, 통합 테스트 상단 주석에 협력 유닛과 해당 유닛들의 동작 규칙(Behavior Rules)을 정의한 뒤, 단위 테스트 단계에서는 정의된 규칙에 대해서만 테스트하고 코드로 구현합니다.
*   **비동기 테스트 클라이언트**: httpx와 ASGITransport를 조합한 비동기 API 테스트 클라이언트(`httpx.AsyncClient`) 구성을 표준으로 사용합니다.
*   **트랜잭션 롤백 격리**: 테스트 DB 오염을 막기 위해, 각 테스트 수행 시 트랜잭션을 시작하고 테스트 종료 시 항상 롤백을 수행하는 Pytest Fixture를 강제 적용합니다.
*   **의존성 오버라이드**: 모킹 시 외부 연동 모듈이나 인증 로직은 `app.dependency_overrides`를 활용하여 모의 객체로 간소하게 대체합니다.
*   **코드 양식**: [10. RTM 대응 표준 코드 양식 - ④ dependencies](#dependencies)를 참고하십시오.


---

## 7. API 문서 및 Swagger 제어 규칙
*   **openapi_url 제어**: Production 배포 환경에서는 Swagger UI 및 OpenAPI 명세서가 외부에 노출되지 않도록 `openapi_url`을 `None`으로 차등 설정합니다.
*   **다중 응답 명세화**: 정상 응답 외에 201 Created, 202 Accepted 등의 특수 응답 상태와 발생 가능한 비즈니스 예외 규격을 라우터 데코레이터의 `responses` 파라미터에 명확히 명세합니다.
*   **코드 양식**: [10. RTM 대응 표준 코드 양식 - ① routers](#routers)를 참고하십시오.

---

## 8. FastAPI Lifespan을 통한 전역 리소스 및 커넥션 관리
*   **싱글톤 리소스 관리**: HTTP 비동기 클라이언트(`httpx.AsyncClient`), 외부 커넥션, 대형 리소스는 API 요청마다 개별 생성하지 않고, 반드시 FastAPI `lifespan` 시점에 1회 초기화하여 `app.state`에 저장하고 사용 후 안전하게 해제합니다.
*   **코드 양식**: [10. RTM 대응 표준 코드 양식 - ④ dependencies](#dependencies)를 참고하십시오.

---

## 9. AI 에이전트 안티패턴 체크리스트 (자가 점검용)

에이전트는 코드 작성 완료 후 아래 체크리스트를 활용해 구현에 위반 사항이 없는지 검토하고, 이를 자가 채점표에 증거와 함께 반영하십시오.

| 안티패턴 (우려되는 구현) | 왜 잘못되었는가? | 올바른 대안 및 해결 방안 |
| :--- | :--- | :--- |
| `requests.get(...)` 등을 `async def` 내부에 사용 | 이벤트 루프를 마비시켜 전체 서버 처리를 지연시킵니다. | `httpx.AsyncClient`를 쓰거나 `run_in_threadpool`로 래핑하십시오. |
| `time.sleep`을 `async def`에 사용 | 위와 같이 메인 스레드를 블로킹합니다. | `asyncio.sleep`을 사용하십시오. |
| `from jose import jwt` 임포트 | 관리되지 않는 레거시 라이브러리입니다. | `PyJWT` (`import jwt` 사용)를 적용하십시오. |
| `model_config = ConfigDict(json_encoders={...})` | Pydantic v2에서 폐기된 속성입니다. | `@field_serializer` 데코레이터를 선언해 처리하십시오. |
| `def get_user(id: int = Depends(...))` | 디폴트 인자 기반 DI는 유연성과 가독성이 떨어집니다. | `user: Annotated[User, Depends(...)]` 표준 양식을 적용하십시오. |
| 라우터 바디 전체를 `try: ... except Exception:`으로 감싸기 | 에러의 근본적 추적을 방해하고 500 에러를 200 응답으로 둔갑시킬 수 있습니다. | 구체적 예외만 캐치하고, 적절한 상태 코드를 담은 `HTTPException`을 내던지십시오. |
| 중요한 알림/정합성 처리를 `BackgroundTasks`에 할당 | 큐가 프로세스 내에서 돌기 때문에 유실 시 재시도가 불가능하며 유실 위험이 큽니다. | 외부 분산 작업 큐(Celery 등)로 오프로드하십시오. |
| 다른 도메인의 심층 내부 모듈 임포트 (`from src.auth.service.user import ...`) | 도메인 간 강한 결합을 유발합니다. | 서비스 외곽 패키지 경로로 임포트 범위를 제한하십시오. (`from src.auth import service`) |
| 전역 `BaseSettings` 하나에 모든 설정 채우기 | 관리가 복잡해지고 모듈별 환경 설정 격리가 되지 않습니다. | 각 도메인 폴더별로 `BaseSettings`를 다중 분리 정의해 사용하십시오. |
| 통합 테스트 작성 시 데이터베이스 모킹(Mocking) 수행 | 실제 DB 동작과의 괴리로 인해 프로덕션 에러 확률을 높입니다. | 로컬 도커 DB를 띄우거나 테스트용 데이터베이스 연결을 `dependency_overrides`로 오버라이드하십시오. |

---

## 10. RTM 대응 표준 코드 양식 (RTM Code Templates)

이 섹션은 RTM(기술 매핑 문서)의 Backend 컬럼에 기재된 소스 코드를 생성할 때 AI 에이전트가 반드시 준수해야 하는 표준 코드 양식(Boilerplate)을 정의합니다.

<div id="routers"></div>

### ① routers (FastAPI Router Endpoint)
백엔드 API 라우터는 외부 요청 DTO 스키마를 수용하고, DI를 활용하여 단일 Usecase를 주입받아 비동기로 실행합니다.
```python
from fastapi import APIRouter, Depends, status
from typing import Annotated
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/monitor", tags=["monitoring"])

# API 요청/응답 DTO 스키마 정의
class StartRequest(BaseModel):
    heart_rate: int

class StartResponse(BaseModel):
    status: str

@router.post("/start", response_model=StartResponse, status_code=status.HTTP_200_OK)
async def start_monitoring(
    payload: StartRequest,
    usecase: Annotated[StartMonitoringUsecase, Depends(get_start_usecase)]
):
    # 단일 책임 Usecase를 의존성 주입받아 비동기로 실행
    return await usecase.execute(payload)
```

<div id="services"></div>

### ② services (단일 책임 Usecase & 불변 값 객체 VO)
비즈니스 로직은 단일 책임의 Usecase 클래스에 격리하며, 입력 DTO를 도메인의 무결성이 보장되는 불변 값 객체(VO)로 변환하여 처리합니다.
```python
# DTO (Pydantic Schema) 및 VO (Value Object) 임포트 가정
class StartMonitoringUsecase:
    def __init__(self, repository: MonitorRepository):
        self.repository = repository

    async def execute(self, request_dto: StartRequest) -> StartResponse:
        # 1. DTO를 도메인 불변 객체(VO)로 즉시 변환하여 무결성 보장
        input_vo = FetalDataVO(heart_rate=request_dto.heart_rate)
        
        # 2. 비즈니스 로직 연산 후 반환 DTO 구조 리턴
        return StartResponse(status="success")
```

<div id="modelsdeps"></div>

### ③ models/deps (불변 값 객체 VO)
비즈니스 도메인의 값을 캡슐화하고 데이터 무결성을 보장하기 위해 파이썬 `dataclass`를 frozen 상태로 선언합니다.
```python
from dataclasses import dataclass

@dataclass(frozen=True)
class FetalDataVO:
    heart_rate: int
```

<div id="dependencies"></div>

### ④ dependencies (비동기 DB 커넥션 및 미들웨어)
FastAPI 의존성 주입에 필요한 리소스 생성 흐름 및 트랜잭션 범위는 Context Manager 기반 비동기 블록 구조로 관리합니다.
```python
# 비동기 트랜잭션 및 DB 세션 관리 표준 구조
async def get_db_session():
    async with async_session_maker() as session:
        async with session.begin():
            # 안전한 DB 트랜잭션 수행 보장을 위해 yield 또는 DB 세션 전달
            yield session
```
