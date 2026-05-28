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

## 2. 도메인 데이터 모델링 및 설계 규칙 (`Source` ➔ `Unit` ➔ `Bundle`)
본 프로젝트는 파일 중심의 처리가 아닌 **인입 소스(Source) 중심의 데이터 처리 모델**을 따릅니다. 비정형 데이터 및 문서 데이터를 유연하게 가공하기 위해 다음과 같은 설계 원칙과 단계적 데이터 추상화 모델을 채택해야 합니다.

### ① 핵심 설계 원칙 및 책임 분리
- **Usecase 중심 오케스트레이션**: `usecases` 레이어는 비즈니스 로직에 기반하여 핵심 모델(`core`)과 외부 어댑터(`outbound`) 사이의 상태 전이 및 실행 시점을 제어하고 오케스트레이션합니다.
- **Core의 구조화 타입 의존**: `core` 도메인은 구체적인 파일 포맷(예: Excel, PDF)이나 상세 통신 프로토콜을 다루지 않으며, 오직 내부적으로 규격화된 **값 객체(Value Object / 내부 구조화 타입)**만 다룹니다.
- **Outbound의 물리 처리 위임**: 파일의 실제 바이트(bytes) 파싱, 외부 API/DB 통신, 그리고 수정 사항의 최종 물리적 적용(문서 가공 실행)은 오직 `outbound` 레이어 내부에서만 실행됩니다.
- **구체적인 데이터 구조 지양**: 추상적인 Base Model 클래스를 남용하여 다단계 상속 구조를 만드는 것은 지양하며, 실제 데이터의 흐름과 도메인 요구사항을 반영하는 **명확하고 실질적인 데이터 구조(Actual Data Structure)**로 설계하십시오.

### ② 단계적 데이터 추상화 모델
- **`Source` (입력 원천)**:
  - 시스템에 인입되는 원본 데이터의 형태입니다. 이는 단순 파일(Markdown, PDF, Excel) 뿐만 아니라 이메일(Mail), SAP/외부 API 등 다양한 입력 원천을 모두 객체화한 물리적 포맷입니다.
- **`Unit` (최소 분석 단위)**:
  - `Source` 데이터를 파싱(Parse)하여 얻는 **독립적인 처리 및 검증의 최소 분석 단위**입니다. (예: 문서의 문단, 표의 행/열, 단일 코드 블록 등)
- **`Category` (비즈니스적 분류)**:
  - 개별 `Unit` 또는 이들의 취합체인 `Bundle`이 가지는 비즈니스 의미(Business Meaning, 예: Invoice, Contract 등)를 정의하는 분류 메타데이터입니다.
- **`Bundle` (구조적 취합 패키지)**:
  - 비즈니스 목적에 맞게 여러 `Unit`들을 취합 및 구조화한 최종 결합 데이터 구조입니다.
- **`Edit Intent` (구조화된 수정 명세)**:
  - 가공 및 검증 과정에서 문서 수정이 필요한 경우, `core` 도메인이 최종적으로 생성하는 **구조화된 변경 의도(Edit Intent) 명세 데이터**입니다. 실제 수정 적용은 `outbound`가 수행합니다.

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

## 7. 데이터 검증 및 Value/Boundary 모델링 규칙
AI 모델에 부적절한 데이터가 진입하여 런타임 에러를 발생시키는 것을 방지하고, 도메인 데이터의 정합성을 보장하기 위해 엄격한 검증 및 데이터 격리 규칙을 준수해야 합니다.

- **데이터 검증 및 차원(Shape) 정합성 검증**:
  - AI 모델에 입력되기 전, 유입 데이터의 포맷(예: Base64 이미지 디코딩 유효성)과 차원 수(Numpy Array/Tensor의 Shape)를 조기에 검증하여 모델 단에서 파이썬 데몬 에러가 터지지 않게 방지하십시오.
  - Pydantic 스키마를 사용하여 입력받은 수치 데이터의 최솟값/최댓값 및 크기 조건을 사전에 철저히 검증하십시오. (예: `min_items`, `max_items`, `Field(..., ge=0)`)
- **Value / Boundary 모델의 분리 설계**:
  - **`types/value` (내부 가치 모델)**: 비즈니스 도메인 내부(core)에서만 유통되는 핵심 **값 객체(Value Object)** 타입을 선언하여 비즈니스 논리의 안정성을 보장하십시오.
  - **`types/boundary` (외곽 입출력 DTO)**: 외부 시스템 연동, REST API 요청/응답 시에 사용하는 **입출력 DTO(Data Transfer Object)** 스키마입니다.
  - **유효성 검사 및 변환 흐름**: 시스템 외부에서 인입되는 모든 원시 입력값은 반드시 `boundary` DTO 수준에서 Pydantic 등을 통해 1차 유효성 검증을 마친 후, 안전한 도메인 `value object`로 변환(Mapping)되어 비즈니스 로직에 인입되도록 강제하십시오.

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

---

## 10. 문서 수정 의도(Edit Intent) 및 자동화 격리 규칙 (Edit Intent & Automation)
문서 수정 및 파일 자동화 연동 시, 핵심 논리 계층(`core`)과 구체적인 물리 파일 수정/자동화 도구(`outbound`)의 역할 경계를 엄격히 유지해야 합니다.

- **3단계 역할 분리 원칙**:
  - **`core/edit` (의도 결정)**: 무엇을 어떻게 수정해야 하는지에 대한 변경 사항 자체를 결정하고, 구조화된 **Edit Intent** 객체(수정 의도를 기술하는 데이터 구조)를 생성합니다.
  - **`outbound` (실제 실행)**: 생성된 Edit Intent를 전달받아, 실제 파일 시스템 적용이나 특정 애플리케이션 자동화(RPA, UI Automation 등) 기법으로 변경을 물리적으로 실행합니다.
  - **`usecases` (오케스트레이션)**: Edit Intent의 생성 시점과 실제 실행 어댑터 호출 시점을 논리적으로 연결 및 관리합니다.
- **임포트 및 유출 금지 규칙 (중요)**:
  - **Core 금지 사항**: `core` 레이어는 `openpyxl`(엑셀 핸들링), `COM` 라이브러리, `win32com`, RPA 관련 라이브러리 등 구체적인 파일 가공 및 UI 자동화 라이브러리를 **절대 직접 import해서는 안 됩니다**.
  - **Usecase 금지 사항**: `usecases` 레이어는 `Workbook`, `Worksheet`, 또는 `COM 객체`와 같은 하부 데이터 객체를 직접 참조하거나 가공 로직 내에서 조작해서는 안 됩니다.
  - **Outbound 금지 사항**: 외부 어댑터 내부에서 생성 및 사용되는 UI Automation 객체나 물리 파일 핸들러가 **Outbound 레이어 경계 밖으로 반환되거나 노출되어서는 안 됩니다**.
- **격리된 테스트 전략**:
  - **Edit Intent 검증**: Core 레이어의 수정 의도 도출 알고리즘은 가짜 어댑터를 쓰거나 생성된 Edit Intent(Value Object)의 스펙과 최종 워크플로우 결과를 기준으로 하는 **단위 테스트**로 검증하십시오.
  - **실행기 검증**: 실제 엑셀 파일이나 UI 자동화를 통해 수정 사항을 입히는 실행기(Executor)의 무결성은 통합 테스트(Integration Test)를 별도 구성하여 검증해야 합니다.

---

## 11. 문서화 및 아키텍처 문서 가이드라인 (Documentation Standards)
AI 에이전트 및 모듈 프로젝트의 복잡성을 통제하고 아키텍처 이해도를 높이기 위해 표준 문서화 지침을 유지하십시오.

- **문서화 도구 및 배포 자동화**:
  - 모든 프로젝트 아키텍처 문서는 **MkDocs**(`mkdocs.yml` 기준)로 즉시 사이트 빌드가 가능하도록 구조적으로 작성되어야 하며, CI/CD 파이프라인을 통해 GitHub Pages에 배포할 수 있는 배포 준비(Deploy-ready) 상태를 준수해야 합니다.
- **아키텍처 문서의 물리적 분리 규칙**:
  - 프로젝트의 아키텍처와 흐름을 현행화하기 위해 `docs/` 디렉토리 하위에 아래 표준 문서들을 의무적으로 유지하고 갱신하십시오.
    - `model.md`: `Source`, `Unit`, `Bundle`, `Category` 도메인 데이터 모델 상세 정의서
    - `workflow.md`: 에이전트 워크플로우 및 상태(State)/실행 문맥(Context) 관리 프로세스 설명서
    - `editing.md`: 수정 의도(Edit Intent) 데이터 명세 및 외부 자동화(openpyxl, COM, RPA) 계층 격리 설계서
    - `ecm.md`: 범용 외부 저장소 연동 규격(HMAC 서명, 검색, 업로드/다운로드 헬퍼 등) 연동 가이드
    - `llm.md`: Agent가 사용하는 LLM 아웃바운드 및 프롬프트 파라미터 매핑 구성 설명서
    - `testing.md`: 가짜 어댑터를 남용하지 않는 E2E 및 어댑터 통합 테스트 전략 가이드

---

## 12. LLM 연동 및 에코시스템 격리 규칙 (LLM Outbound & Configuration)
AI 에이전트가 사용하는 대형 언어 모델(LLM)에 대한 결합도를 차단하고 유연하게 교체할 수 있도록 연동 및 설정 규격을 격리하여 설계해야 합니다.

- **LLM Outbound 격리 원칙 (Model Agnostic & Stub 지원)**:
  - LangGraph 노드, Tool, 또는 Usecase 로직 내부에서 특정 LLM Provider(OpenAI, Gemini 등)의 API나 모델 세부사항에 직접 결합(Binding)되지 않도록 `outbound/external/llm.py` 형태의 어댑터 레이어로 격리하십시오.
  - **로컬 테스트(Stub) 강제**: 로컬 개발 및 테스트 시 외부 API 호출 없이도 독립 실행이 가능하도록 모의 응답을 반환하는 기본 `stub` 동작 모델을 내장해야 합니다.
  - **결정권 격리**: LLM은 문서 해석 보조, 요약(`summarize_document`), 단순 질의응답(`ask_document_question`) 등의 **보조 연산에만 사용**되어야 하며, 비즈니스 검증 규칙이나 최종 판정 로직 등 **Business Rule의 핵심 결정권(Source of Truth)을 LLM이 갖게 해서는 안 됩니다**. 핵심 결정권은 반드시 `core` 단독 파이썬 코드로 제어하십시오.
- **환경변수 및 설정 규격 표준화**:
  - 설정 구조는 `DOCFLOW_AGENT_` (또는 프로젝트 prefix)로 시작하는 명확한 환경 변수 계층을 준수하고, Pydantic-settings 등의 중첩 클래스 매핑에 호환되도록 던더(`__`) 구분자 구조를 사용해야 합니다.
  - API Key 등 보안 크리덴셜 정보는 런타임 파일 fallback 대신 **오직 환경 변수 또는 보안 주입 프로세스로만 관리**되어야 합니다.
- **일관된 에러 분류 및 API 매핑**:
  - LLM 연동 중 발생하는 실패는 아래와 같이 명확히 정의된 커스텀 예외 타입으로 래핑하여 상위로 전달하십시오.
    - **Quota 초과 / 일시적 차단**: `LlmQuotaExceededError` ➔ HTTP `429 Too Many Requests` (재시도 수행하지 않음)
    - **일시적 Rate Limit**: `LlmRateLimitError` ➔ HTTP `503 Service Unavailable` (지정된 백오프/재시도 정책 가동)
    - **기타 네트워크 및 Provider 실패**: `LlmRequestError` ➔ HTTP `503 Service Unavailable`
- **의존성 팩 관리**:
  - 각 LLM Provider별 필수 패키지(예: `langchain-openai`, `langchain-google-genai` 등)는 `pyproject.toml`에 선택적(Optional) 의존성 세트나 그룹으로 명시하여, 불필요한 패키지가 배포 환경에 남용되지 않도록 관리하십시오.

---

## 13. 추상 인터페이스 배제 기반 테스팅 전략 (Testing Without Abstract Adapters)
불필요한 조기 추상화와 오버헤드를 막기 위해, 본 프로젝트는 의존성 격리를 목적으로 한 명시적 인터페이스(Abstract Class)를 선제적으로 설계하지 않는 것을 원칙으로 합니다. 

### ① 기본 입장 및 테스트 가능성 확보
- 복잡성의 중심은 다중 구현체 지원을 위한 인터페이스 추상화가 아닌, 문서 해석 및 비즈니스 검증 논리 자체입니다.
- 무분별한 인터페이스 정의는 코드양과 파일 탐색 비용만 증가시킵니다. 대신 구체 모듈을 직접 호출하여 테스트하되, 호출 경계(Seam)에서 테스트 도구를 활용하여 제어합니다.
- 테스트 가능성은 다음 설계를 통해 확보하십시오:
  - 상태가 존재하지 않는 순수 함수 중심의 **`core`**
  - 얇은 제어 흐름만 담는 **`usecases`**
  - 실행 문맥과 상태 전이를 전담 관리하는 **`workflow`**
  - 단일 책임을 갖는 작은 함수와 전용 클라이언트로 분리된 **`outbound`**
  - 표준 라이브러리 및 테스트 러너의 **`monkeypatch`**, **`fake response`**, **`tmp_path`** 등의 로컬 모킹 도구 적극 활용

### ② 아키텍처 계층별 테스트 대상 및 가이드
- **Usecases 테스트**:
  - `usecases`는 오케스트레이션 역할만 수행하므로 외부 RDBMS, Vector Store, Queue 등의 경계를 가벼운 인메모리(In-memory) 또는 페이크(Fake) 클래스로 대체하여 로직의 흐름을 검증합니다.
  - *주요 검증 대상*: Artifact의 결합 및 조립 순서, 외부 포트/LLM 호출 흐름, 지원하지 않는 흐름(Unsupported flow) 진입 시의 처리 상태 등.
- **Workflow 테스트**:
  - `workflow` 테스트 시 LangGraph 등 오케스트레이션 프레임워크 자체의 라이브러리 동작을 검사하지 마십시오.
  - *주요 검증 대상*: 비즈니스 라우팅 분기 조건(route 선택), 단계 전이(state transition), 산출물 레퍼런스(artifact ref) 생성 규칙, 상태 값 안정성(state safety) 및 승인/반려/재개(human-in-the-loop pending/approve/resume) 흐름 등 **도메인 시나리오 흐름**을 검증합니다.
- **Outbound 테스트**:
  - 외부 연동 어댑터(`outbound`)의 테스트는 추상 인터페이스 모킹이 아닌, **외부 부작용(Side Effect)을 로컬 환경으로 우회(Redirection)**시켜 검증합니다.
  - *주요 검증 패턴*: HTTP API 호출은 `urlopen` 및 HTTP Client에 대한 `monkeypatch` 사용, 파일 가공 시 `tmp_path` 피처 활용, 인메모리 가짜 객체(Fake Class) 및 로컬 모의 DB 환경 활용.
- **Inbound 테스트**:
  - 엔드포인트(`inbound`)는 Usecase 호출 및 예외 번역(Error Translation) 역할만 수행하는 얇은 레이어입니다.
  - API 프레임워크 제공 `test client`를 사용하여 입력 유효성 검증 실패(422) 및 정상 호출 경로에 대한 최소한의 정상/실패 상태 코드 위주로 가볍게 테스트하십시오.

### ③ 호출 접점(Seam)의 제어 지점
인터페이스가 없더라도 다음 Seam 위치에서 `monkeypatch` 또는 fake 객체를 주입하여 테스트 시나리오를 온전히 통제할 수 있습니다:
- Usecase가 Outbound 함수를 직접 import하여 호출하는 지점
- Outbound가 외부 시스템/표준 라이브러리 함수를 직접 호출하는 지점
- 시스템 환경 변수 및 설정(`settings`)을 로드하는 지점

### ④ 추상 인터페이스(Abstract Adapter) 도입 검토 조건
기본은 도입하지 않는 것이나, 아래 조건 중 하나 이상 충족 시에 한해 예외적으로 인터페이스 설계를 도입할 수 있습니다:
1. 동일한 Usecase가 여러 상이한 외부 프로바이더를 런타임에 동적으로 변경하며 장기간 운영해야 할 때
2. 테스트 Setup에 필요한 런타임 바인딩이 너무 복잡해져서 테스트 셋업 코드가 감당할 수 없을 만큼 비대해질 때
3. 다수의 서로 다른 구체 클래스 구현체가 동일한 인터페이스 계약(Contract)을 명백히 따르고 반복 구현해야 할 때
그 전까지는 **구체 모듈 + 작은 함수 + `monkeypatch`** 구성의 단순함이 가장 유지보수와 가독성에 유리합니다.

---

## 13. 추상 인터페이스 배제 기반 테스팅 전략 (Testing Without Abstract Adapters)
불필요한 조기 추상화와 오버헤드를 막기 위해, 본 프로젝트는 의존성 격리를 목적으로 한 명시적 인터페이스(Abstract Class)를 선제적으로 설계하지 않는 것을 원칙으로 합니다. 

### ① 기본 입장 및 테스트 가능성 확보
- 복잡성의 중심은 다중 구현체 지원을 위한 인터페이스 추상화가 아닌, 문서 해석 및 비즈니스 검증 논리 자체입니다.
- 무분별한 인터페이스 정의는 코드양과 파일 탐색 비용만 증가시킵니다. 대신 구체 모듈을 직접 호출하여 테스트하되, 호출 경계(Seam)에서 테스트 도구를 활용하여 제어합니다.
- 테스트 가능성은 다음 설계를 통해 확보하십시오:
  - 상태가 존재하지 않는 순수 함수 중심의 **`core`**
  - 얇은 제어 흐름만 담는 **`usecases`**
  - 실행 문맥과 상태 전이를 전담 관리하는 **`workflow`**
  - 단일 책임을 갖는 작은 함수와 전용 클라이언트로 분리된 **`outbound`**
  - 표준 라이브러리 및 테스트 러너의 **`monkeypatch`**, **`fake response`**, **`tmp_path`** 등의 로컬 모킹 도구 적극 활용

### ② 아키텍처 계층별 테스트 대상 및 가이드
- **Usecases 테스트**:
  - `usecases`는 오케스트레이션 역할만 수행하므로 외부 RDBMS, Vector Store, Queue 등의 경계를 가벼운 인메모리(In-memory) 또는 페이크(Fake) 클래스로 대체하여 로직의 흐름을 검증합니다.
  - *주요 검증 대상*: Artifact의 결합 및 조립 순서, 외부 포트/LLM 호출 흐름, 지원하지 않는 흐름(Unsupported flow) 진입 시의 처리 상태 등.
- **Workflow 테스트**:
  - `workflow` 테스트 시 LangGraph 등 오케스트레이션 프레임워크 자체의 라이브러리 동작을 검사하지 마십시오.
  - *주요 검증 대상*: 비즈니스 라우팅 분기 조건(route 선택), 단계 전이(state transition), 산출물 레퍼런스(artifact ref) 생성 규칙, 상태 값 안정성(state safety) 및 승인/반려/재개(human-in-the-loop pending/approve/resume) 흐름 등 **도메인 시나리오 흐름**을 검증합니다.
- **Outbound 테스트**:
  - 외부 연동 어댑터(`outbound`)의 테스트는 추상 인터페이스 모킹이 아닌, **외부 부작용(Side Effect)을 로컬 환경으로 우회(Redirection)**시켜 검증합니다.
  - *주요 검증 패턴*: HTTP API 호출은 `urlopen` 및 HTTP Client에 대한 `monkeypatch` 사용, 파일 가공 시 `tmp_path` 피처 활용, 인메모리 가짜 객체(Fake Class) 및 로컬 모의 DB 환경 활용.
- **Inbound 테스트**:
  - 엔드포인트(`inbound`)는 Usecase 호출 및 예외 번역(Error Translation) 역할만 수행하는 얇은 레이어입니다.
  - API 프레임워크 제공 `test client`를 사용하여 입력 유효성 검증 실패(422) 및 정상 호출 경로에 대한 최소한의 정상/실패 상태 코드 위주로 가볍게 테스트하십시오.

### ③ 호출 접점(Seam)의 제어 지점
인터페이스가 없더라도 다음 Seam 위치에서 `monkeypatch` 또는 fake 객체를 주입하여 테스트 시나리오를 온전히 통제할 수 있습니다:
- Usecase가 Outbound 함수를 직접 import하여 호출하는 지점
- Outbound가 외부 시스템/표준 라이브러리 함수를 직접 호출하는 지점
- 시스템 환경 변수 및 설정(`settings`)을 로드하는 지점

### ④ 추상 인터페이스(Abstract Adapter) 도입 검토 조건
기본은 도입하지 않는 것이나, 아래 조건 중 하나 이상 충족 시에 한해 예외적으로 인터페이스 설계를 도입할 수 있습니다:
1. 동일한 Usecase가 여러 상이한 외부 프로바이더를 런타임에 동적으로 변경하며 장기간 운영해야 할 때
2. 테스트 Setup에 필요한 런타임 바인딩이 너무 복잡해져서 테스트 셋업 코드가 감당할 수 없을 만큼 비대해질 때
3. 다수의 서로 다른 구체 클래스 구현체가 동일한 인터페이스 계약(Contract)을 명백히 따르고 반복 구현해야 할 때
그 전까지는 **구체 모듈 + 작은 함수 + `monkeypatch`** 구성의 단순함이 가장 유지보수와 가독성에 유리합니다.
