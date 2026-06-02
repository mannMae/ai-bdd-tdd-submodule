# 📊 [F01] 모니터링 기능 (Monitoring) - 기술 매핑 및 채점표 (예시)

이 문서는 모니터링 기능의 세부 시나리오가 프론트엔드, 백엔드, AI 모듈의 어떤 아키텍처/디자인 패턴과 매핑되는지 정의하고, 구현 완료 후 규칙 준수 여부를 채점하는 기록서의 예시입니다.

* **상태 (Status)**: `WIP` (진행 중)
* **연관 문서**: [유저플로우(User Flow)](file:///docs/user-flow/monitoring_flow.md) | [거킨 시나리오(BDD)](file:///features/monitoring.feature)

---

## 1. 🗺️ 시나리오-아키텍처 매핑 매트릭스 (Technical Mapping)

### 1) 프론트엔드 (Frontend) 매핑

<table border="1" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th align="left">시나리오</th>
      <th align="left">FE-01</th>
      <th align="left">FE-02</th>
      <th align="left">FE-03</th>
      <th align="left">FE-04</th>
      <th align="left">FE-05</th>
      <th align="left">FE-06</th>
      <th align="left">FE-07</th>
      <th align="left">etc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. 모니터링 시작</b><br><i>(넘버패드 입력 후 시작)</i></td>
      <td>-</td>
      <td>• useStartMonitoring.ts</td>
      <td>• store/useMonitorStore.ts</td>
      <td>• Numpad.tsx</td>
      <td>• MonitoringSetting.tsx<br>• NumpadModal.tsx<br>• Monitoring.tsx</td>
      <td>• apiClient.ts<br>• storage.ts</td>
      <td>-</td>
      <td>-</td>
    </tr>
    <tr>
      <td><b>S02. 시뮬레이션 모드</b><br><i>(시뮬레이션 데이터 구동)</i></td>
      <td>-</td>
      <td>• useSimulate.ts</td>
      <td>• store/useMonitorStore.ts</td>
      <td>• Card.tsx</td>
      <td>• Monitoring.tsx<br>• SimulationPanel.tsx</td>
      <td>• apiClient.ts<br>• timeFormatter.ts</td>
      <td>-</td>
      <td>-</td>
    </tr>
    <tr>
      <td><b>S03. 모니터링 종료</b><br><i>(사용자 강제 종료)</i></td>
      <td>-</td>
      <td>• useStopMonitoring.ts</td>
      <td>• store/useMonitorStore.ts</td>
      <td>• feedback/ConfirmModal.tsx</td>
      <td>• Monitoring.tsx</td>
      <td>• apiClient.ts<br>• storage.ts</td>
      <td>-</td>
      <td>-</td>
    </tr>
  </tbody>
</table>

### 2) 백엔드 (Backend) 매핑

<table border="1" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th align="left">시나리오</th>
      <th align="left">BE-01</th>
      <th align="left">BE-02</th>
      <th align="left">BE-03</th>
      <th align="left">BE-04</th>
      <th align="left">BE-05</th>
      <th align="left">BE-06</th>
      <th align="left">BE-07</th>
      <th align="left">BE-08</th>
      <th align="left">etc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. 모니터링 시작</b><br><i>(넘버패드 입력 후 시작)</i></td>
      <td>• router.py</td>
      <td>• service.py</td>
      <td>• vo.py</td>
      <td>• models.py</td>
      <td>• dependencies.py</td>
      <td>• schemas.py</td>
      <td>• test_monitoring.py</td>
      <td>-</td>
      <td>• database.py [BE-09]</td>
    </tr>
    <tr>
      <td><b>S02. 시뮬레이션 모드</b><br><i>(시뮬레이션 데이터 구동)</i></td>
      <td>• router.py</td>
      <td>• service.py</td>
      <td>• vo.py</td>
      <td>• models.py</td>
      <td>• dependencies.py</td>
      <td>• schemas.py</td>
      <td>• test_monitoring.py</td>
      <td>-</td>
      <td>• database.py [BE-09]</td>
    </tr>
    <tr>
      <td><b>S03. 모니터링 종료</b><br><i>(사용자 강제 종료)</i></td>
      <td>• router.py</td>
      <td>• service.py</td>
      <td>-</td>
      <td>• models.py</td>
      <td>• dependencies.py</td>
      <td>• schemas.py</td>
      <td>• test_monitoring.py</td>
      <td>-</td>
      <td>• database.py [BE-09]</td>
    </tr>
  </tbody>
</table>

### 3) AI 모듈 (AI Module) 매핑

<table border="1" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th align="left">시나리오</th>
      <th align="left">AI-01</th>
      <th align="left">AI-02</th>
      <th align="left">AI-03</th>
      <th align="left">AI-04</th>
      <th align="left">AI-05</th>
      <th align="left">AI-06</th>
      <th align="left">AI-07</th>
      <th align="left">AI-08</th>
      <th align="left">etc</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. 모니터링 시작</b><br><i>(넘버패드 입력 후 시작)</i></td>
      <td>• router.py</td>
      <td>• inference.py</td>
      <td>-</td>
      <td>• processor.py</td>
      <td>• gateway.py</td>
      <td>• value.py</td>
      <td>• test_inference.py</td>
      <td>-</td>
      <td>• bootstrap.py [AI-09]</td>
    </tr>
    <tr>
      <td><b>S02. 시뮬레이션 모드</b><br><i>(시뮬레이션 데이터 구동)</i></td>
      <td>• router.py</td>
      <td>• inference.py</td>
      <td>• process.py</td>
      <td>• processor.py</td>
      <td>• gateway.py</td>
      <td>• value.py</td>
      <td>• test_inference.py</td>
      <td>-</td>
      <td>• bootstrap.py [AI-09]</td>
    </tr>
    <tr>
      <td><b>S03. 모니터링 종료</b><br><i>(사용자 강제 종료)</i></td>
      <td>• router.py</td>
      <td>• inference.py</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>• value.py</td>
      <td>• test_inference.py</td>
      <td>-</td>
      <td>• bootstrap.py [AI-09]</td>
    </tr>
  </tbody>
</table>

---

## 💡 각 영역별 작성 가이드 및 표준 코드 양식 (Code Forms)

> [!IMPORTANT]
> **🚨 AI 에이전트 개발 가이드라인 (RTM 개발 계약)**
> 1. **정답표 및 준수 여부 심사**: 이 RTM(기술 매핑 문서)은 구현 완료 후 사용자가 코드가 잘 작성되었는지 채점하기 위한 정답표이자 규칙 검증 계약서입니다.
> 2. **엄격한 규칙 준수**: 각 컬럼에 정의된 코드유형 ID, 구조적 역할, 그리고 표준 코드 양식을 정확히 준수하여 소스 코드가 작성되어야 합니다.
> 3. **반려 기준**: 다음 사항에 하나라도 해당할 경우, 구현 결과물은 예외 없이 **반려(Reject)** 처리됩니다.
>    - 지정된 기본 디렉토리 경로가 아닌 임의의 위치에 파일을 작성한 경우.
>    - 표준 코드 양식(예: Usecase의 단일 책임 클래스 구조, 불변 VO의 dataclass 선언 등)을 따르지 않고 임의의 아키텍처 및 보일러플레이트로 구현한 경우.
>    - RTM 테이블에 누락되었거나 RTM의 매핑 정보와 다르게 임의로 파일을 임포트하여 의존 관계를 깬 경우.
> 4. **개발 전 필수 확인**: AI 에이전트는 코드를 구현하기 전에 반드시 본 RTM의 가이드 및 코드 양식을 읽고 분석한 뒤, 이에 정확히 부합하는 형태의 프로덕션 코드만을 작성해야 합니다.

---

### 1) 프론트엔드 (Frontend - 코드유형 ID 단위 매핑)

프론트엔드 파일들은 해당하는 **코드유형 ID(FE-01 ~ FE-07)** 및 **etc** 컬럼에 매핑하여 기술하며, 코드 작성 시 [프론트엔드 개발 가이드레일(06-frontend-rules.md)](file:///rules/templates/06-frontend-rules.sample.md)을 준수해야 합니다.

#### ① FE-01 (API Query Hook)
*   **정의**: 서버 데이터를 조회/캐싱하기 위한 TanStack Query용 Custom Query Hook 파일의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: [Frontend Rules - api 표준 코드 양식](file:///rules/templates/06-frontend-rules.sample.md#1-api-react-query-mutation) 및 코드 폼 사전의 `[FE-01]` 스펙을 준수해야 합니다.

#### ② FE-02 (API Fetch/Mutation)
*   **정의**: POST, PUT, DELETE 등 서버 상태를 변경하는 API Fetch/Mutation 모듈 파일의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전의 `[FE-02]` 표준 코드 양식을 준수해야 합니다.

#### ③ FE-03 (Feature Store)
*   **정의**: Zustand 기반 전역 상태 또는 로컬 피처 상태 저장소 파일의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전의 `[FE-03]` 표준 코드 양식을 준수해야 합니다.

#### ④ FE-04 (Controlled Input)
*   **정의**: react-hook-form 및 Zod와 연동되는 공통 Controlled Form Input 컴포넌트의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전의 `[FE-04]` 표준 코드 양식을 준수하여 작성해야 합니다.

#### ⑤ FE-05 (Feature UI Component)
*   **정의**: 폼 컨텍스트, API Hook, UI 컴포넌트들을 조립하여 비즈니스 가치를 완수하는 피처 UI 컴포넌트의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전의 `[FE-05]` 표준 코드 양식을 준수해야 합니다.

#### ⑥ FE-06 (Utility Module)
*   **정의**: 브라우저 저장소 관리 및 비즈니스 공통 연산 등 부수 효과가 없는 순수 함수/객체 헬퍼 파일의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전의 `[FE-06]` 표준 코드 양식을 준수해야 합니다.

#### ⑦ FE-07 (Custom Hook)
*   **정의**: 컴포넌트 생명주기와 연동되거나, UI 동작 상태 및 이벤트를 처리하기 위한 범용 커스텀 훅 파일의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전의 `[FE-07]` 표준 코드 양식을 준수하여 작성해야 합니다.

#### ⑧ etc (기타 파일 및 추가 코드유형)
*   **정의**: 위 1~7번 유형에 속하지 않는 글로벌/공통 파일(`[FE-08] Form Container Wrapper`, `[FE-09] App Provider`, `[FE-10] App Router`, `[FE-11] Domain Types`, `[FE-12] External Library Wrapper` 등), 공통 로직 등의 파일들을 대괄호 접미사와 함께 기재합니다. (단, App Provider와 App Router와 같은 프로젝트 전역 설정 파일은 모든 기능에서 공통으로 당연히 사용되므로 굳이 매번 RTM에 기재하지 않는 것을 권장합니다.)
*   **표준 코드 양식**: 코드 폼 사전에 정의된 각 코드 유형의 표준 코드 양식을 준수하여 작성해야 합니다.

---

### 2) 백엔드 (Backend - 코드유형 ID 단위 매핑)

백엔드 파일들은 해당하는 **코드유형 ID(BE-01 ~ BE-08)** 및 **etc** 컬럼에 매핑하여 기술하며, 코드 작성 시 [백엔드 개발 가이드레일(07-backend-rules.md)](file:///rules/templates/07-backend-rules.sample.md)을 준수해야 합니다.

#### ① BE-01 (routers)
*   **정의**: API 엔드포인트를 정의하고 응답 스펙과 Status Code를 매핑하는 FastAPI APIRouter 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-01]` 스펙을 준수해야 합니다.

#### ② BE-02 (services)
*   **정의**: 단일 비즈니스 규칙 및 Usecase를 조율하는 Stateless 서비스 클래스 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-02]` 스펙을 준수해야 합니다.

#### ③ BE-03 (post_vo)
*   **정의**: 비즈니스 도메인의 무결성 제약조건을 강제하는 불변 값 객체(VO) 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-03]` 스펙을 준수해야 합니다.

#### ④ BE-04 (models)
*   **정의**: SQLAlchemy 기반 DB ORM 테이블 선언적 모델 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-04]` 스펙을 준수해야 합니다.

#### ⑤ BE-05 (dependencies)
*   **정의**: FastAPI Depends에 바인딩할 의존성 주입 및 공용 검증 함수 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-05]` 스펙을 준수해야 합니다.

#### ⑥ BE-06 (schemas)
*   **정의**: 입출력 데이터의 유효성 검증과 직렬화를 담당하는 Pydantic 스키마 DTO 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-06]` 스펙을 준수해야 합니다.

#### ⑦ BE-07 (tests)
*   **정의**: httpx.AsyncClient를 이용하여 백엔드 비즈니스 흐름을 비동기 검증하는 pytest 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-07]` 스펙을 준수해야 합니다.

#### ⑧ BE-08 (utils)
*   **정의**: 날짜 연산, 암호화 헬퍼 등 백엔드 전반에서 공통으로 쓰이는 유틸리티 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-08]` 스펙을 준수해야 합니다.

#### ⑨ etc
*   **정의**: 1~8번 유형 이외의 파일(예: `[BE-09] Database Session Manager`, `[BE-10] External Client`, `[BE-11] Custom Exception`, `[BE-12] Config Settings` 등, 유형 번호 표기 필수)을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전에 정의된 각 코드 유형의 표준 코드 양식을 준수하여 작성해야 합니다.

---

### 3) AI 모듈 (AI Module - 코드유형 ID 단위 매핑)

AI 모듈 파일들은 해당하는 **코드유형 ID(AI-01 ~ AI-08)** 및 **etc** 컬럼에 매핑하여 기술하며, 코드 작성 시 [로컬 ML 추론 서버 개발 가이드레일(08-ai-module-rules.md)](file:///rules/templates/08-ai-module-rules.sample.md)을 준수해야 합니다.

#### ① AI-01 (inbound)
*   **정의**: 외부 추론 요청을 수신하는 APIRouter 진입점 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-01]` 스펙을 준수해야 합니다.

#### ② AI-02 (usecases)
*   **정의**: 추론 전/후처리 및 모델 호출 게이트웨이를 조율하는 오케스트레이터 클래스 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-02]` 스펙을 준수해야 합니다.

#### ③ AI-03 (workflow)
*   **정의**: LangGraph 기반 다단계 추론 체인 및 에이전트 상태 제어 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-03]` 스펙을 준수해야 합니다.

#### ④ AI-04 (core)
*   **정의**: 특징(Feature) 추출, 텐서 가공, 수학적 연산 및 비즈니스 룰 후처리를 수행하는 Pure Python 모듈 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-04]` 스펙을 준수해야 합니다.

#### ⑤ AI-05 (outbound)
*   **정의**: 실제 모델 가중치(ONNX/Torch) 구동 또는 외부 LLM API 통신을 수행하는 Gateway/Adapter 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-05]` 스펙을 준수해야 합니다.

#### ⑥ AI-06 (types)
*   **정의**: API 입출력 Pydantic DTO 및 내부 도메인 값 VO 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-06]` 스펙을 준수해야 합니다.

#### ⑦ AI-07 (tests)
*   **정의**: pytest 기반 모의 어댑터 및 추론 파이프라인 단언 검증 테스트 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-07]` 스펙을 준수해야 합니다.

#### ⑧ AI-08 (utils)
*   **정의**: 텍스트 정규화, 텐서 연산 등 AI 파이프라인 전반에서 공통으로 쓰이는 유틸리티 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[AI-08]` 스펙을 준수해야 합니다.

#### ⑨ etc
*   **정의**: 1~8번 유형 이외의 파일(예: `[AI-09] Bootstrap & DI Container`, `[AI-10] Prompt Templates`, `[AI-11] AI Custom Exception`, `[AI-12] Model Config & Specs` 등, 유형 번호 표기 필수)을 기재합니다.
*   **표준 코드 양식**: 코드 폼 사전에 정의된 각 코드 유형의 표준 코드 양식을 준수하여 작성해야 합니다.

---

## 2. 🛡️ 엔지니어링 룰 자가 채점표 (Convention Self-Grading)

구현을 완료한 후, AI 에이전트는 작성한 코드가 각 템플릿의 가이드레일을 준수했는지 스스로 체크하고 물리적 증거(코드 링크)를 제시해야 합니다.

### [S01] 모니터링 시작 시나리오 채점
*   **[프론트엔드] Feature-First 구조 준수 (06-FE 1조)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: 컴포넌트가 `src/features/monitoring/components/Numpad.tsx`에 응집력 있게 생성됨.
*   **[백엔드] Async 비동기 동시성 규칙 (07-BE 2조)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: `async def` 라우터 내부에서 동기 Redis 블로킹을 방지하기 위해 `aioredis` 비동기 메시지 발행을 구현함. ([router.py:L45](file:///apps/backend/src/monitoring/router.py#L45))
*   **[백엔드] Depends 의존성 주입 표준 (07-BE 4조)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: `Annotated[AsyncSession, Depends(get_db_session)]` 구문을 사용하여 타입 안정성을 확보함. ([dependencies.py:L12](file:///apps/backend/src/monitoring/dependencies.py#L12))

### [S02] 시뮬레이션 모드 시나리오 채점
*   **[백엔드] DTO 및 VO 분리 흐름 (07-BE 3조 3항)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: 인입 데이터는 Pydantic 스키마인 `SimulationRequest`로 받고, 내부 시뮬레이터 연산 시에는 불변 객체인 `SimulationVO`로 변환하여 처리함. ([service.py:L82](file:///apps/backend/src/monitoring/service.py#L82))
*   **[백엔드] 롤백 기반 테스트 격리 (07-BE 6조 2항)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: 시뮬레이션 실행 시 적재되는 테스트 데이터를 격리하기 위해 `pytest` DB 트랜잭션 롤백 피스처를 적용함. ([test_simulation.py:L15](file:///apps/backend/tests/test_simulation.py#L15))

---

## 3. 📂 검증 물리 증거 (Verification Evidence)

이 시나리오를 검증하기 위해 생성/수정된 파일의 실제 경로 링크입니다.

### ① 설계 및 테스트 스펙 (Specification)
*   **BDD 시나리오**: [monitoring.feature](file:///features/monitoring.feature)
*   **유저플로우 다이어그램**: [monitoring_flow.md](file:///docs/user-flow/monitoring_flow.md)

### ② 프론트엔드 변경 파일 (Frontend)
*   **컴포넌트**: [Numpad.tsx](file:///apps/frontend/src/features/monitoring/components/Numpad.tsx)
*   **통합 테스트**: [Numpad.test.tsx](file:///apps/frontend/src/features/monitoring/tests/Numpad.test.tsx)

### ③ 백엔드 변경 파일 (Backend)
*   **API 라우터**: [router.py](file:///apps/backend/src/monitoring/router.py)
*   **비즈니스 서비스**: [service.py](file:///apps/backend/src/monitoring/service.py)
*   **통합 테스트**: [test_monitoring.py](file:///apps/backend/tests/test_monitoring.py)
