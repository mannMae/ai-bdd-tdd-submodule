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
      <th rowspan="2" align="left">시나리오</th>
      <th colspan="2" align="center">공통 (Common)</th>
      <th colspan="3" align="center">{기능명} 피처 ({Feature})</th>
    </tr>
    <tr>
      <th align="left">components<br><sub>src/components</sub></th>
      <th align="left">app<br><sub>src/app</sub></th>
      <th align="left">components<br><sub>src/features/{기능명}/components</sub></th>
      <th align="left">api<br><sub>src/features/{기능명}/api</sub></th>
      <th align="left">store<br><sub>src/features/{기능명}/stores</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• {공통컴포넌트파일명}.tsx [FE-04]</td>
      <td>• provider.tsx [FE-06]</td>
      <td>• {전용컴포넌트파일명}.tsx [FE-08]</td>
      <td>• {전용API통신코드파일명}.ts [FE-02]</td>
      <td>• {전용스토어파일명}.ts [FE-03]</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• {공통컴포넌트파일명}.tsx [FE-04]</td>
      <td>• router.tsx [FE-07]</td>
      <td>• {전용컴포넌트파일명}.tsx [FE-08]</td>
      <td>• {전용API통신코드파일명}.ts [FE-02]</td>
      <td>• {전용스토어파일명}.ts [FE-03]</td>
    </tr>
  </tbody>
</table>

### 2) 백엔드 (Backend) 매핑

<table border="1" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th rowspan="2" align="left">시나리오</th>
      <th colspan="1" align="center">공통 (Common)</th>
      <th colspan="7" align="center">{기능명} 피처 ({Feature})</th>
    </tr>
    <tr>
      <th align="left">db<br><sub>src</sub></th>
      <th align="left">routers<br><sub>src/{기능명}</sub></th>
      <th align="left">services<br><sub>src/{기능명}</sub></th>
      <th align="left">post_vo<br><sub>src/{기능명}</sub></th>
      <th align="left">dependencies<br><sub>src/{기능명}</sub></th>
      <th align="left">models<br><sub>src/{기능명}</sub></th>
      <th align="left">schemas<br><sub>src/{기능명}</sub></th>
      <th align="left">tests<br><sub>tests/{기능명}</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• database.py [BE-04]</td>
      <td>• router.py [BE-01]</td>
      <td>• service.py [BE-02]</td>
      <td>• {VO파일명}_vo.py [BE-03]</td>
      <td>• dependencies.py [BE-06]</td>
      <td>• models.py [BE-05]</td>
      <td>• schemas.py [BE-07]</td>
      <td>• test_create_post.py [BE-08]</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• database.py [BE-04]</td>
      <td>• router.py [BE-01]</td>
      <td>• service.py [BE-02]</td>
      <td>• {VO파일명}_vo.py [BE-03]</td>
      <td>• dependencies.py [BE-06]</td>
      <td>• models.py [BE-05]</td>
      <td>• schemas.py [BE-07]</td>
      <td>• test_create_post.py [BE-08]</td>
    </tr>
  </tbody>
</table>

### 3) AI 모듈 (AI Module) 매핑

<table border="1" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th rowspan="2" align="left">시나리오</th>
      <th colspan="1" align="center">공통 (Common)</th>
      <th colspan="7" align="center">AI 피처 (Prediction)</th>
    </tr>
    <tr>
      <th align="left">bootstrap<br><sub>src</sub></th>
      <th align="left">inbound<br><sub>src/inbound</sub></th>
      <th align="left">usecases<br><sub>src/usecases</sub></th>
      <th align="left">workflow<br><sub>src/workflow</sub></th>
      <th align="left">core<br><sub>src/core</sub></th>
      <th align="left">outbound<br><sub>src/outbound</sub></th>
      <th align="left">types<br><sub>src/types</sub></th>
      <th align="left">tests<br><sub>tests</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• bootstrap.py [AI-06]</td>
      <td>• router.py [AI-01]</td>
      <td>• inference.py [AI-02]</td>
      <td>• process.py [AI-03]</td>
      <td>• processor.py [AI-04]</td>
      <td>• gateway.py [AI-05]</td>
      <td>• value.py [AI-07]</td>
      <td>• test_inference.py [AI-08]</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• bootstrap.py [AI-06]</td>
      <td>• router.py [AI-01]</td>
      <td>• inference.py [AI-02]</td>
      <td>• process.py [AI-03]</td>
      <td>• processor.py [AI-04]</td>
      <td>• gateway.py [AI-05]</td>
      <td>• value.py [AI-07]</td>
      <td>• test_inference.py [AI-08]</td>
    </tr>
  </tbody>
</table>

---

## 💡 각 영역별 작성 가이드 및 표준 코드 양식 (Code Forms)

> [!IMPORTANT]
> **🚨 AI 에이전트 RTM 행-열 계약 (Row-Column Enforcement Contract)**
> 1. **행(Row)-열(Column) 결합 의무**: 이 RTM 문서의 행(시나리오 = 구현해야 할 컨텐츠)과 열(물리적 디렉토리 및 표준 코드 폼 = 구현의 레퍼런스)은 강력한 실행 규격 계약서입니다.
> 2. **코드 폼(Code Form) 상속 필수**: 셀에 기재된 소스 코드를 생성/수정할 때, 에이전트는 해당하는 **열의 코드 폼 번호([Code Form])의 구조 및 보일러플레이트를 반드시 100% 모방(상속)하여 작성**해야 합니다. 임의의 아키텍처나 구조 편차를 적용하는 것을 엄격히 금지합니다.
> 3. **반려(Reject) 사유**: 아래 사항 위반 시 즉시 작업은 반려됩니다:
>    - 지정된 열의 기본 물리 디렉토리가 아닌 다른 임의의 경로에 파일을 생성한 경우.
>    - 표준 코드 폼(예: `services` 열 ➔ 단일 책임 Usecase 클래스 구조, `models` 열 ➔ frozen VO dataclass 등)에 위배되는 방식으로 freestyle 코딩을 한 경우.
>    - RTM에 명시되지 않은 파일 또는 의존성을 임의로 추가하여 도메인 간의 단방향 결합을 깨뜨린 경우.
> 4. **개발 전 필수 조치**: 에이전트는 코딩 시작 전에 RTM 매핑 매트릭스의 열별 `[Code Form]` 레퍼런스를 개발 가이드레일 파일에서 직접 로드하여 숙지해야 합니다.

---

### 1) 프론트엔드 (Frontend - 디렉토리 단위 매핑)

프론트엔드 파일들은 실제 프로젝트 디렉토리 구조(`components`, `api`, `store`, `utils`)에 맞추어 매핑하여 기술하며, 코드 작성 시 [프론트엔드 개발 가이드레일(06-frontend-rules.md)](file:///rules/templates/06-frontend-rules.sample.md)을 준수해야 합니다.

#### ① components
*   **정의**: 시나리오 수행 시 렌더링되거나 활성화되는 최상위 UI 컴포넌트의 **순수 파일명**을 기재합니다. (헤더에 기본 경로가 지정되어 있으므로 경로 및 마크다운 링크 제외)
    *   *작성법*: 화면 이동 순서나 전환 흐름(➔) 기호는 사용하지 않고, 해당 시나리오를 구성하는 최상위 컴포넌트의 **순수 파일명**들만 목록 형태로 나열합니다.

#### ② api
*   **정의**: 프론트엔드에서 발송하는 HTTP 요청 메서드/경로 또는 WebSocket 발송 이벤트를 정의하는 API custom hook 또는 클라이언트 모듈의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식**: [Frontend Rules - api 표준 코드 양식](file:///rules/templates/06-frontend-rules.sample.md#1-api-react-query-mutation)을 준수하여 작성해야 합니다.

#### ③ store/utils
*   **정의**: Zustand 등 전역 상태 관리 스토어 및 브라우저 저장소 연동, 헬퍼 함수 파일의 **순수 파일명**들을 기재합니다. (기본 경로 하위의 상대 경로로 표기)
*   **표준 코드 양식**: [Frontend Rules - store 및 utils 표준 코드 양식](file:///rules/templates/06-frontend-rules.sample.md#2-store-zustand-store)을 준수하여 작성해야 합니다.

---

### 2) 백엔드 (Backend - 디렉토리 단위 매핑)

백엔드 파일들은 실제 프로젝트 디렉토리 구조(`db`, `routers`, `services`, `post_vo`, `dependencies`, `models`)에 맞추어 매핑하여 기술하며, 코드 작성 시 [백엔드 개발 가이드레일(07-backend-rules.md)](file:///rules/templates/07-backend-rules.sample.md)을 준수해야 합니다.

#### ① routers
*   **정의**: 백엔드가 외부 요청을 받아들이는 라우터 인터페이스 **순수 파일명** 및 HTTP/WS 엔드포인트 명세.
*   **표준 코드 양식**: [Backend Rules - routers 표준 코드 양식](file:///rules/templates/07-backend-rules.sample.md#routers)을 준수하여 작성해야 합니다.

#### ② services
*   **정의**: 단일 비즈니스 규칙 및 Usecase를 수행하는 서비스 비즈니스 클래스 정의 파일의 **순수 파일명**.
*   **표준 코드 양식**: [Backend Rules - services 표준 코드 양식](file:///rules/templates/07-backend-rules.sample.md#services)을 준수하여 작성해야 합니다.

#### ③ post_vo
*   **정의**: 비즈니스 정책 및 무결성 제약조건을 검증하는 Immutable 값 객체(VO) 정의 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-03]` 표준 코드 양식을 준수하여 작성해야 합니다.

#### ④ dependencies
*   **정의**: FastAPI의 의존성 주입(`Depends`)을 위한 팩토리 함수 정의 파일의 **순수 파일명**.

#### ⑤ models
*   **정의**: 데이터베이스 테이블 스키마에 매핑되는 SQLAlchemy ORM 모델 정의 파일의 **순수 파일명**.
*   **표준 코드 양식**: 코드 폼 사전의 `[BE-05]` 표준 코드 양식을 준수하여 작성해야 합니다.

---

### 3) AI 모듈 (AI Module - 디렉토리 단위 매핑)

AI 모듈 파일들은 실제 프로젝트 디렉토리 구조(`routers`, `models`, `config`)에 맞추어 매핑하여 기술하며, 코드 작성 시 [로컬 ML 추론 서버 개발 가이드레일(08-ai-module-rules.md)](file:///rules/templates/08-ai-module-rules.sample.md)을 준수해야 합니다.

#### ① base
*   **정의**: 공통 추론 base 클래스 및 전처리 유틸 클래스의 **순수 파일명**들을 기재합니다.
*   **표준 코드 양식**: [AI Module Rules - base 표준 코드 양식](file:///rules/templates/08-ai-module-rules.sample.md#base)을 준수하여 작성해야 합니다.

#### ② routers
*   **정의**: AI 엔진 서버가 제공하는 HTTP/gRPC 연동 라우터 파일의 **순수 파일명** 및 입출력 명세.
*   **표준 코드 양식**: [AI Module Rules - routers 표준 코드 양식](file:///rules/templates/08-ai-module-rules.sample.md#routers)을 준수하여 작성해야 합니다.

#### ③ models
*   **정의**: 실제 추론을 수행하는 머신러닝/인공지능 모델 및 가중치 파일(예: ONNX)의 **순수 파일명**.
*   **표준 코드 양식**: [AI Module Rules - models 표준 코드 양식](file:///rules/templates/08-ai-module-rules.sample.md#models)을 참고하십시오.

#### ④ config
*   **정의**: 추론용 슬라이딩 윈도우 크기, 이상치 필터(Outlier Filter) 유무 등 모델 구동 설정 파라미터 파일의 **순수 파일명**.
*   **표준 코드 양식**: [AI Module Rules - config 표준 코드 양식](file:///rules/templates/08-ai-module-rules.sample.md#config)을 준수하여 작성해야 합니다.

---

## 2. 🛡️ 엔지니어링 룰 자가 채점표 (Convention Self-Grading)

구현을 완료한 후, AI 에이전트는 작성한 코드가 각 템플릿의 가이드레일을 준수했는지 스스로 체크하고 물리적 증거(코드 링크)를 제시해야 합니다.

### [S01] {시나리오명} 채점
*   **[프론트엔드] Feature-First 구조 준수 (06-FE 1조)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: {증거 설명 및 링크 기재, 예: 컴포넌트가 `src/features/{기능명}/components/Numpad.tsx`에 생성됨.}
*   **[백엔드] Async 비동기 동시성 규칙 (07-BE 2조)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: {증거 설명 및 링크 기재, 예: [router.py:L45](file:///apps/backend/src/{기능명}/router.py#L45)}
*   **[백엔드] Depends 의존성 주입 표준 (07-BE 4조)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: {증거 설명 및 링크 기재, 예: [dependencies.py:L12](file:///apps/backend/src/{기능명}/dependencies.py#L12)}

### [S02] {시나리오명} 채점
*   **[백엔드] DTO 및 VO 분리 흐름 (07-BE 3조 3항)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: {증거 설명 및 링크 기재}
*   **[백엔드] 롤백 기반 테스트 격리 (07-BE 6조 2항)**
    *   [ ] **결과**: `Pending` / `Pass` / `Fail`
    *   [ ] **증거**: {증거 설명 및 링크 기재}

---

## 3. 📂 검증 물리 증거 (Verification Evidence)

이 시나리오를 검증하기 위해 생성/수정된 파일의 실제 경로 링크입니다.

### ① 설계 및 테스트 스펙 (Specification)
*   **BDD 시나리오**: [{기능명}.feature](file:///features/{기능명}.feature)
*   **유저플로우 다이어그램**: [{기능명}_flow.md](file:///docs/user-flow/{기능명}_flow.md)

### ② 프론트엔드 변경 파일 (Frontend)
*   **컴포넌트**: [{컴포넌트파일명}.tsx](file:///apps/frontend/src/features/{기능명}/components/{컴포넌트파일명}.tsx)
*   **통합 테스트**: [{테스트파일명}.test.tsx](file:///apps/frontend/src/features/{기능명}/tests/{테스트파일명}.test.tsx)

### ③ 백엔드 변경 파일 (Backend)
*   **API 라우터**: [{라우터파일명}.py](file:///apps/backend/src/{기능명}/{라우터파일명}.py)
*   **비즈니스 서비스**: [{서비스파일명}.py](file:///apps/backend/src/{기능명}/{서비스파일명}.py)
*   **통합 테스트**: [{테스트파일명}.py](file:///apps/backend/tests/{테스트파일명}.py)
