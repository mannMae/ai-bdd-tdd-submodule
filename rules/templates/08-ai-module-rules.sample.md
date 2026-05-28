---
description: AI 모듈, LLM 에이전트 설계, 리소스 관리, 동시성, 평가(Evals) 및 의존성 관리 가이드레일
glob: "apps/ai-server/**/*"
---
# 8. AI 모듈 및 에이전트 서버 개발 가이드레일

대용량 AI/ML 모델 구동, LLM 오케스트레이션(에이전트) 설계, 성능 최적화, 메모리 OOM(Out of Memory) 방지, 동시성 관리, 프롬프트 품질 평가, 그리고 현대적 Python 패키징 표준을 보장하기 위해 AI 에이전트가 반드시 준수해야 하는 규칙입니다.

---

## 1. 에이전트 오케스트레이션 아키텍처 (Architecture)
AI 모듈 및 에이전트 서버는 단순한 선형 파이프라인(Linear Pipeline) 대신 **`Usecase + Workflow` 중심의 오케스트레이션 설계**를 권장합니다. 요청의 복잡한 비즈니스 흐름을 구조화하기 위해 다음과 같이 레이어를 구분하여 개발하십시오.

- **① Inbound (진입점 레이어)**:
  - 사용자 또는 외부 시스템의 입력을 받는 레이어입니다.
  - **FastAPI**(REST API/WebSocket), **Streamlit**(데모 UI), **CLI**(로컬 스크립트) 등 다양한 엔드포인트를 노출하지만, 비즈니스 로직을 직접 포함하지 않고 Usecase를 트리거하는 역할만 수행합니다.
- **② Usecase (기능 단위 레이어)**:
  - 애플리케이션의 핵심 비즈니스 유스케이스(예: 문서 요약, 규칙 검증, 텍스트 편집 등)를 수행하는 순수한 논리적 실행 단위입니다.
  - 외부 인프라와 격리되어 동작하며, 필요 시 `Workflow`를 조합하여 호출합니다.
- **③ Workflow (상태 관리 오케스트레이션 레이어)**:
  - 하나의 요청이 실행되는 동안 유지되는 **실행 문맥(Execution Context)과 상태(State)**를 제어합니다.
  - 여러 Usecase와 Core 컴포넌트를 호출하면서 분기, 반복, 병렬 처리 등의 제어 흐름을 stateful하게 조율합니다.
- **④ Core (AI 추론 및 도메인 핵심 레이어)**:
  - 실제 로컬 AI 모델 추론(PyTorch 등) 또는 외부 LLM API(OpenAI, Anthropic 등) 호출을 직접 처리하는 물리적 레이어입니다.
  - `source ➔ unit ➔ bundle`과 같은 도메인 단위 모델링 구조를 가집니다.
- **⑤ Outbound (외부 연동 레이어)**:
  - 가공 완료된 최종 산출물 파일 저장(S3, 로컬 스토리지), 데이터베이스 영속화, 외부 웹훅 API 연동 등 외부 인프라에 쓰기 작업을 수행합니다.

---

## 2. 도메인 데이터 모델링 규칙 (`Source` ➔ `Unit` ➔ `Bundle`)
비정형 텍스트 및 문서 데이터를 유연하게 처리하고 AI 가공 파이프라인의 완성도를 높이기 위해 다음과 같은 **단계적 데이터 모델링**을 채택해야 합니다.

- **`Source` (원시 데이터 객체)**:
  - 입력받은 원본 데이터 또는 파싱되지 않은 전체 텍스트 파일(예: Markdown, PDF, CSV 원본)을 의미합니다.
- **`Unit` (분석/가공의 최소 독립 단위)**:
  - `Source`에서 추출한 논리적 구성 요소이자 분석의 기본 단위입니다. (예: 문서의 개별 '문단', 표의 '행/열', 단일 코드 '블록' 등)
  - 각 `Unit`은 독립적으로 AI 모델의 검증 및 변환(수정) 처리를 받을 수 있어야 합니다.
- **`Bundle` (가공된 Unit의 패키지)**:
  - 처리 완료된 여러 `Unit`들을 원래의 순서대로 정렬하거나 최종 구조화한 상태의 집합체입니다.
  - 최종적으로 사용자에게 반환되거나 `Outbound` 레이어를 거쳐 파일로 저장되는 포맷입니다.

---

## 3. 프롬프트 관리 및 품질 평가 (Evaluation - `evals/` 구축)
AI 모델 및 에이전트의 안정성과 응답 품질 신뢰성을 보장하기 위해 프롬프트 템플릿을 격리하고 정량적 평가 파이프라인을 구축하십시오.

- **프롬프트 템플릿 격리**:
  - Python 소스 코드 파일 내부에 수십 줄의 프롬프트 문자열을 직접 인라인 코드로 하드코딩하지 마십시오.
  - 프롬프트는 반드시 독립된 텍스트/마크다운 파일(`.txt`, `.md`, `.json`, `.yaml`) 또는 프롬프트 전역 관리 모듈(예: `src/[app_name]/prompts/`)로 분리하여 관리하십시오.
- **평가 디렉토리 (`evals/`) 구성 및 회귀 방지**:
  - 프로젝트 루트에 `evals/` 디렉토리를 구축하여 품질 평가 스크립트와 검증 데이터셋을 관리하십시오.
  - 평가 데이터셋(Golden Dataset)을 구성하고, 에이전트의 성능 지표(예: Accuracy, BLEU, ROUGE, 또는 GPT-4를 판사로 사용하는 LLM-as-a-judge 점수)를 산출하는 평가 코드를 작성하십시오.
  - 주요 프롬프트 템플릿이나 오케스트레이션 로직이 변경될 때마다 이 평가 도구를 가동하여 이전 대비 성능이 저하되는 회귀(Regression) 현상을 사전에 방지하십시오.

---

## 4. AI 모델 생명주기 및 리소스 관리 (OOM 예방)
- **Startup 로딩 (싱글톤 패턴)**: 무거운 AI 모델의 가중치(Weights)나 파이프라인(Pipeline) 객체는 API 요청이 들어올 때(Request handler 내부) 로드하면 안 됩니다. 매 요청마다 파일을 열고 GPU에 할당하는 동작은 극심한 병목과 GPU OOM을 일으킵니다.
- **Lifespan 사용 강제**: FastAPI의 `lifespan` 컨텍스트 매니저를 사용하여 서버 구동 시점에 모델을 단 1회 로드하여 메모리/GPU에 할당하고, 서버 종료 시점에 명시적으로 메모리에서 할당을 해제(del 및 캐시 비우기)하십시오.
  * 올바른 예:
    ```python
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: 서버 기동 시 모델을 한 번만 로드하여 app.state에 할당
        app.state.model = HeavyInferenceModel.load("./weights")
        yield
        # Shutdown: 서버 종료 시 자원 해제
        del app.state.model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    ```

---

## 5. 동시성 제어 및 이벤트 루프 블로킹 방지 (성능 보장)
- **동기식 추론 연산 처리**: AI 모델 추론 연산(CPU-bound 또는 GPU-bound 동기 연산)은 Python의 이벤트 루프(Single-threaded Event Loop)를 차단하여 서버 전체를 먹통으로 만들기 쉽습니다.
- **라우터 선언 규칙**: 
  - 추론 로직을 담고 있는 라우터 함수가 내부적으로 `await`를 쓸 수 없는 동기식 함수라면, 함수 선언에 `async def`를 쓰지 말고 일반 `def`로 정의하십시오. FastAPI가 이 함수를 별도의 작업 스레드 풀(Thread Pool)에서 동시 실행하여 이벤트 루프 블로킹을 차단합니다.
  * 올바른 예:
    ```python
    @router.post("/predict")
    def predict(payload: PredictRequest, app = Depends(get_app)):
        # CPU/GPU Heavy 동기 연산은 일반 def 함수 내에서 안전하게 실행
        result = app.state.model.infer(payload.input_data)
        return result
    ```
  - 만약 꼭 `async def` 함수 안에서 동기 연산을 실행해야 한다면, 반드시 `asyncio.to_thread` 또는 `anyio.to_thread.run_sync` 등을 사용하여 백그라운드 스레드로 연산을 위임하십시오.

---

## 6. GPU 메모리 관리 및 연산 최적화 (PyTorch 중심)
- **추론 모드 비활성화**: 딥러닝 추론 시 불필요하게 연산 그래프가 생성되고 그래디언트가 메모리에 축적되는 것을 막기 위해, 모든 추론 로직은 반드시 `with torch.no_grad():` 또는 `@torch.inference_mode()` 블록 하위에서 실행되어야 합니다.
- **디바이스 지정**: 모델 가중치와 입력 텐서(`Tensor.to(device)`)의 실행 디바이스(`cuda`, `cpu`, `mps` 등)는 환경 변수나 설정 파일을 기반으로 동적으로 지정될 수 있어야 하며, 임의의 디바이스 문자열을 하드코딩해서는 안 됩니다.

---

## 7. 데이터 검증 및 차원(Shape) 정합성 검증
- AI 모델에 입력되기 전, 들어오는 데이터의 포맷(예: Base64 이미지 디코딩 유효성)과 차원 수(Numpy Array/Tensor의 Shape)를 조기에 검증하여 모델 단에서 파이썬 데몬 에러가 터지지 않게 방지하십시오.
- Pydantic 스키마를 사용하여 입력받은 수치 데이터의 최솟값/최댓값 및 크기 조건을 사전에 철저히 검증하십시오.
  * 예: `min_items`, `max_items`, `Field(..., ge=0)`

---

## 8. 패키지 및 의존성 관리 표준 (`uv` & `pyproject.toml`)
- **최신 툴체인 사용**: 의존성 설치 속도 향상과 일관된 실행 환경을 보장하기 위해 파이썬 패키징 도구인 **`uv`**를 적극 사용하십시오.
- **표준 메타데이터 선언**: 패키지 정보와 사용되는 라이브러리는 `requirements.txt` 단일 파일 대신 **`pyproject.toml`** 표준 파일에 명시적으로 선언하십시오.
- **잠금 파일 관리**: 빌드 및 배포 안정성을 위해 `uv.lock` 또는 `poetry.lock` 파일을 레포지토리에 커밋하여 관리하고, 실행 환경의 라이브러리 버전을 고정(Pinning)하여 사용할 수 있게 강제하십시오.

---

## 9. 외부 인프라 및 Outbound 연동 격리 규칙 (Outbound Isolation)
AI 모듈이 외부 파일 저장소나 문서 관리 시스템(ECM 등)과 연동할 때, 기술 상세가 비즈니스 로직과 결합하지 않도록 철저한 격리 규칙을 준수해야 합니다.

- **역할 경계 준수 (Rule of Isolation)**:
  - 외부 스토리지나 API 연동 모듈(예: `docflow_agent/outbound/external/ecm.py`)은 **단순한 데이터 송수신(HTTP 요청, 서명, 업로드/다운로드, 로컬 임시 저장)의 기술적 실행만 담당**해야 합니다.
  - 비즈니스 카테고리 판단, 번들 조합, 수정 의도(Edit Intent) 생성이나 비즈니스 검증 규칙 등의 비즈니스 로직은 Outbound 모듈이 절대 알면 안 되며, 이는 오직 `core` 및 `usecases` 레이어에서만 다루어야 합니다.
- **클라이언트 추상화 및 벤더 독립성 (Vendor-agnostic)**:
  - 특정 외부 시스템 벤더의 SDK에 강하게 의존하지 말고, 범용 HTTP 클라이언트 및 설정 파라미터(`base_url`, `timeout`, `endpoints path` 등)를 가지는 추상 클라이언트 구조를 채택하십시오.
  - 기본 엔드포인트 경로(예: search: `/documents/search`, upload: `/documents/upload` 등)를 지정하되, 인스턴스 생성 시 벤더 규격에 맞게 동적으로 오버라이드할 수 있도록 설계해야 합니다.
- **보안 및 서명 로직의 캡슐화**:
  - API 서명 생성(HMAC-SHA256), 요청 본문 무결성 검증(SHA-256 Digest 생성), 커스텀 보안 헤더(`X-ECM-Signature`, `X-ECM-Content-SHA256` 등) 주입과 같은 하부 통신 및 보안 규격은 클라이언트 단에서 캡슐화하여 자동 처리되도록 구성하십시오.
  - 상위 레이어(`usecases`)는 외부 서버와의 직접 통신 상태를 제어하지 않고, 오직 추상화된 데이터 모델(`EcmAuth`, `EcmSearchQuery`, `EcmDocument` 등)만을 사용하여 클라이언트의 함수를 호출해야 합니다.
