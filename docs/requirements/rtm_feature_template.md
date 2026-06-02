# 📊 [{F01}] {기능명} (Feature) - 기술 매핑 및 채점표

이 문서는 {기능명}의 세부 시나리오가 프론트엔드, 백엔드, AI 모듈의 어떤 아키텍처/디자인 패턴과 매핑되는지 정의하고, 구현 완료 후 규칙 준수 여부를 채점하는 기록서의 템플릿입니다.

* **상태 (Status)**: `WIP` (진행 중)
* **연관 문서**: [유저플로우(User Flow)](file:///docs/user-flow/{기능명}_flow.md) | [거킨 시나리오(BDD)](file:///features/{기능명}.feature)

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
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• {전용API조회파일명}.ts</td>
      <td>• {전용API통신코드파일명}.ts</td>
      <td>• {전용스토어파일명}.ts</td>
      <td>• {공통컴포넌트파일명}.tsx</td>
      <td>• {전용컴포넌트파일명}.tsx</td>
      <td>• {전용유틸파일명}.ts</td>
      <td>• {전용커스텀훅파일명}.ts</td>
      <td>• provider.tsx [FE-09]</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• {전용API조회파일명}.ts</td>
      <td>• {전용API통신코드파일명}.ts</td>
      <td>• {전용스토어파일명}.ts</td>
      <td>• {공통컴포넌트파일명}.tsx</td>
      <td>• {전용컴포넌트파일명}.tsx</td>
      <td>-</td>
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
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• router.py</td>
      <td>• service.py</td>
      <td>• {VO파일명}_vo.py</td>
      <td>• models.py</td>
      <td>• dependencies.py</td>
      <td>• schemas.py</td>
      <td>• test_create_post.py</td>
      <td>• utils.py</td>
      <td>• database.py [BE-09]</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• router.py</td>
      <td>• service.py</td>
      <td>• {VO파일명}_vo.py</td>
      <td>• models.py</td>
      <td>• dependencies.py</td>
      <td>• schemas.py</td>
      <td>• test_create_post.py</td>
      <td>• utils.py</td>
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
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• router.py</td>
      <td>• inference.py</td>
      <td>• process.py</td>
      <td>• processor.py</td>
      <td>• gateway.py</td>
      <td>• value.py</td>
      <td>• test_inference.py</td>
      <td>• utils.py</td>
      <td>• bootstrap.py [AI-09]</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• router.py</td>
      <td>• inference.py</td>
      <td>• process.py</td>
      <td>• processor.py</td>
      <td>• gateway.py</td>
      <td>• value.py</td>
      <td>• test_inference.py</td>
      <td>• utils.py</td>
      <td>• bootstrap.py [AI-09]</td>
    </tr>
  </tbody>
</table>

---

## 💡 각 영역별 작성 가이드 및 표준 코드 양식 (Code Forms)

> [!IMPORTANT]
> **🚨 AI 에이전트 RTM 행-열 계약 (Row-Column Enforcement Contract)**
> 1. **행(Row)-열(Column) 결합 의무**: 이 RTM 문서의 행(시나리오 = 구현해야 할 컨텐츠)과 열(코드유형 ID = 구현의 레퍼런스)은 강력한 실행 규격 계약서입니다.
> 2. **코드 폼(Code Form) 상속 필수**: 셀에 기재된 소스 코드를 생성/수정할 때, 에이전트는 해당하는 **열의 코드 폼 번호([Code Form])의 구조 및 보일러플레이트를 반드시 100% 모방(상속)하여 작성**해야 합니다. 임의의 아키텍처나 구조 편차를 적용하는 것을 엄격히 금지합니다.
> 3. **반려(Reject) 사유**: 아래 사항 위반 시 즉시 작업은 반려됩니다:
>    - 지정된 열의 기본 물리 디렉토리가 아닌 다른 임의의 경로에 파일을 생성한 경우.
>    - 표준 코드 폼(예: `services` 열 ➔ 단일 책임 Usecase 클래스 구조, `models` 열 ➔ frozen VO dataclass 등)에 위배되는 방식으로 freestyle 코딩을 한 경우.
>    - RTM에 명시되지 않은 파일 또는 의존성을 임의로 추가하여 도메인 간의 단방향 결합을 깨뜨린 경우.
> 4. **개발 전 필수 조치**: 에이전트는 코딩 시작 전에 RTM 매핑 매트릭스의 열별 `[Code Form]` 레퍼런스를 개발 가이드레일 파일에서 직접 로드하여 숙지해야 합니다.

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
*   **표준 코드 양식**: 코드 폼 사전의 `[FE-07]` 표준 코드 양식을 준수해야 합니다.

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
