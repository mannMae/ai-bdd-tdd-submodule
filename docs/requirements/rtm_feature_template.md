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
      <th align="left">api/utils<br><sub>src/common</sub></th>
      <th align="left">components<br><sub>src/features/{기능명}/components</sub></th>
      <th align="left">api<br><sub>src/features/{기능명}/api</sub></th>
      <th align="left">store/utils<br><sub>src/features/{기능명}</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• {공통컴포넌트파일명}.tsx</td>
      <td>• {공통클라이언트파일명}.ts</td>
      <td>• {전용컴포넌트파일명}.tsx</td>
      <td>• {전용API통신코드파일명}.ts</td>
      <td>• store/{전용스토어파일명}.ts<br>• utils/{전용유틸파일명}.ts</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• {공통컴포넌트파일명}.tsx</td>
      <td>• {공통클라이언트파일명}.ts</td>
      <td>• {전용컴포넌트파일명}.tsx</td>
      <td>• {전용API통신코드파일명}.ts</td>
      <td>• store/{전용스토어파일명}.ts<br>• utils/{전용유틸파일명}.ts</td>
    </tr>
  </tbody>
</table>

### 2) 백엔드 (Backend) 매핑

<table border="1" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th rowspan="2" align="left">시나리오</th>
      <th colspan="1" align="center">공통 (Common)</th>
      <th colspan="3" align="center">{기능명} 피처 ({Feature})</th>
    </tr>
    <tr>
      <th align="left">middleware/db<br><sub>src/common</sub></th>
      <th align="left">routers<br><sub>src/{기능명}</sub></th>
      <th align="left">services<br><sub>src/{기능명}</sub></th>
      <th align="left">models/deps<br><sub>src/{기능명}</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• middleware/{공통미들웨어파일명}.py<br>• db/{공통DB세션파일명}.py</td>
      <td>• {라우터파일명}.py</td>
      <td>• {유스케이스파일명}.py</td>
      <td>• models.py<br>• dependencies.py</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• db/{공통DB세션파일명}.py</td>
      <td>• {라우터파일명}.py</td>
      <td>• {유스케이스파일명}.py</td>
      <td>• models.py<br>• dependencies.py</td>
    </tr>
  </tbody>
</table>

### 3) AI 모듈 (AI Module) 매핑

<table border="1" style="border-collapse: collapse;">
  <thead>
    <tr>
      <th rowspan="2" align="left">시나리오</th>
      <th colspan="1" align="center">공통 (Common)</th>
      <th colspan="3" align="center">AI 피처 (Prediction)</th>
    </tr>
    <tr>
      <th align="left">base<br><sub>src/common</sub></th>
      <th align="left">routers<br><sub>src/prediction</sub></th>
      <th align="left">models<br><sub>models</sub></th>
      <th align="left">config<br><sub>src/prediction</sub></th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td><b>S01. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>• {공통추론클래스파일명}.py</td>
      <td>• {라우터파일명}.py</td>
      <td>• {모델파일명}.onnx</td>
      <td>• {설정파일명}.py</td>
    </tr>
    <tr>
      <td><b>S02. {시나리오명}</b><br><i>({시나리오 트리거 조건})</i></td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
      <td>-</td>
    </tr>
  </tbody>
</table>

---

## 💡 각 영역별 작성 가이드 및 표준 코드 양식 (Code Forms)

> [!IMPORTANT]
> **🚨 AI 에이전트 개발 가이드라인 (RTM 개발 계약)**
> 1. **정답표 및 준수 여부 심사**: 이 RTM(기술 매핑 문서)은 구현 완료 후 사용자가 코드가 잘 작성되었는지 채점하기 위한 정답표이자 규칙 검증 계약서입니다.
> 2. **엄격한 규칙 준수**: 각 컬럼에 정의된 물리 디렉토리 경로, 구조적 역할, 그리고 하단에 명시된 **[표준 코드 양식(Templates)]**을 정확히 준수하여 소스 코드가 작성되어야 합니다.
> 3. **반려 기준**: 다음 사항에 하나라도 해당할 경우, 구현 결과물은 예외 없이 **반려(Reject)** 처리됩니다.
>    - 지정된 기본 디렉토리 경로가 아닌 임의의 위치에 파일을 작성한 경우.
>    - 표준 코드 양식(예: Usecase의 단일 책임 클래스 구조, 불변 VO의 dataclass 선언 등)을 따르지 않고 임의의 아키텍처 및 보일러플레이트로 구현한 경우.
>    - RTM 테이블에 누락되었거나 RTM의 매핑 정보와 다르게 임의로 파일을 임포트하여 의존 관계를 깬 경우.
> 4. **개발 전 필수 확인**: AI 에이전트는 코드를 구현하기 전에 반드시 본 RTM의 가이드 및 코드 양식을 읽고 분석한 뒤, 이에 정확히 부합하는 형태의 프로덕션 코드만을 작성해야 합니다.

---

### 1) 프론트엔드 (Frontend - 디렉토리 단위 매핑)

프론트엔드 파일들은 실제 프로젝트 디렉토리 구조(`components`, `api`, `store`, `utils`)에 맞추어 매핑하여 기술합니다.

#### ① components
*   **정의**: 시나리오 수행 시 렌더링되거나 활성화되는 최상위 UI 컴포넌트의 **순수 파일명**을 기재합니다. (헤더에 기본 경로가 지정되어 있으므로 경로 및 마크다운 링크 제외)
    *   *작성법*: 화면 이동 순서나 전환 흐름(➔) 기호는 사용하지 않고, 해당 시나리오를 구성하는 최상위 컴포넌트의 **순수 파일명**들만 목록 형태로 나열합니다.

#### ② api
*   **정의**: 프론트엔드에서 발송하는 HTTP 요청 메서드/경로 또는 WebSocket 발송 이벤트를 정의하는 API custom hook 또는 클라이언트 모듈의 **순수 파일명**을 기재합니다.
*   **표준 코드 양식 (HTTP Axios Client / WS Send)**:
    ```typescript
    // HTTP API 호출 훅 양식
    export const useStartMonitoring = () => {
      return useMutation({
        mutationFn: async (payload: StartRequest) => {
          const { data } = await apiClient.post<StartResponse>('/api/v1/monitor/start', payload);
          return data;
        }
      });
    };
    ```

#### ③ store
*   **정의**: Zustand 등 전역 상태 관리 스토어의 **순수 파일명** 및 상태 값 정의. (파일 표기 시 `store/useMonitorStore.ts`와 같이 기본 경로 하위의 상대 경로로 표기)
*   **표준 코드 양식 (Zustand Store)**:
    ```typescript
    import { create } from 'zustand';

    interface MonitorState {
      isMonitoring: boolean;
      startMonitoring: () => void;
      stopMonitoring: () => void;
    }

    export const useMonitorStore = create<MonitorState>((set) => ({
      isMonitoring: false,
      startMonitoring: () => set({ isMonitoring: true }),
      stopMonitoring: () => set({ isMonitoring: false }),
    }));
    ```

#### ④ utils
*   **정의**: 브라우저 저장소(LocalStorage, SessionStorage, Cookie) 연동 파일 또는 공통 포맷터 등의 순수 유틸리티 헬퍼 함수 파일의 **순수 파일명**을 기재합니다. (파일 표기 시 `utils/storage.ts`와 같이 기본 경로 하위의 상대 경로로 표기)
*   **표준 코드 양식 (Storage Wrapper / Helper Function)**:
    ```typescript
    // 1. Browser Storage Util: 브라우저 저장소 관리 양식
    export const storage = {
      get: (key: string): string | null => localStorage.getItem(key),
      set: (key: string, value: string): void => localStorage.setItem(key, value),
      remove: (key: string): void => localStorage.removeItem(key),
    };

    // 2. Pure Helper: 비즈니스 연산 유틸 함수 양식
    export const formatSecondsToMinutes = (seconds: number): string => {
      const mins = Math.floor(seconds / 60);
      const secs = seconds % 60;
      return `${mins}:${secs.toString().padStart(2, '0')}`;
    };
    ```

---

### 2) 백엔드 (Backend - 디렉토리 단위 매핑)

백엔드 파일들은 실제 프로젝트 디렉토리 구조(`routers`, `services`, `models`, `dependencies`)에 맞추어 매핑하여 기술합니다.

#### ① routers
*   **정의**: 백엔드가 외부 요청을 받아들이는 라우터 인터페이스 **순수 파일명** 및 HTTP/WS 엔드포인트 명세.
*   **표준 코드 양식 (FastAPI Router Endpoint)**:
    ```python
    from fastapi import APIRouter, Depends, status
    from typing import Annotated

    router = APIRouter(prefix="/api/v1/monitor", tags=["monitoring"])

    @router.post("/start", response_model=StartResponse, status_code=status.HTTP_200_OK)
    async def start_monitoring(
        payload: StartRequest,
        usecase: Annotated[StartMonitoringUsecase, Depends(get_start_usecase)]
    ):
        return await usecase.execute(payload)
    ```

#### ② services
*   **정의**: 단일 비즈니스 규칙 및 Usecase를 수행하는 서비스 비즈니스 클래스 정의 파일의 **순수 파일명**.
*   **표준 코드 양식 (단일 책임 Usecase & 불변 값 객체 VO)**:
    ```python
    # Usecase: 하나의 비즈니스 작업만 완결성 있게 처리하는 단일 책임 클래스
    class StartMonitoringUsecase:
        def __init__(self, repository: MonitorRepository):
            self.repository = repository

        async def execute(self, request_dto: StartRequest) -> StartResponse:
            # 1. DTO를 도메인 불변 객체(VO)로 변환
            input_vo = FetalDataVO(heart_rate=request_dto.heart_rate)
            # 2. 비즈니스 로직 연산 후 반환
            return StartResponse(status="success")
    ```

#### ③ models
*   **정의**: 데이터베이스 ORM 모델 정의 파일의 **순수 파일명** 및 불변 값 객체(VO) 정의.
*   **표준 코드 양식 (불변 값 객체 VO)**:
    ```python
    # VO (Value Object): 데이터 무결성을 보장하는 불변 값 객체
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class FetalDataVO:
        heart_rate: int
    ```

#### ④ dependencies
*   **정의**: FastAPI의 `Depends` 의존성 주입 **순수 파일명** 및 미들웨어, Redis, RabbitMQ 등 외부 인프라 연동 파일의 **순수 파일명**.
*   **표준 코드 양식 (비동기 DB 커넥션 / Redis 연동 등)**:
    ```python
    # 비동기 트랜잭션 관리 구조 양식
    async with async_session_maker() as session:
        async with session.begin():
            # 안전한 DB 트랜잭션 수행 보장 블록
            await repository.save(session, entity)
    ```

---

### 3) AI 모듈 (AI Module - 디렉토리 단위 매핑)

AI 모듈 파일들은 실제 프로젝트 디렉토리 구조(`routers`, `models`, `config`)에 맞추어 매핑하여 기술합니다.

#### ① routers
*   **정의**: AI 엔진 서버가 제공하는 HTTP/gRPC 연동 라우터 파일의 **순수 파일명** 및 입출력 명세.
*   **표준 코드 양식 (AI Inference Router)**:
    ```python
    @router.post("/predict", response_model=PredictResponse)
    async def predict_endpoint(payload: PredictRequest):
        prediction = await ai_model.predict(payload.features)
        return PredictResponse(prediction=prediction)
    ```

#### ② models
*   **정의**: 실제 추론을 수행하는 머신러닝/인공지능 모델 및 가중치 파일(예: ONNX)의 **순수 파일명**과 추론 전처리 파이프라인 파일의 **순수 파일명**.
*   **표준 코드 양식 (ML Model Predictor Wrapper & Preprocessor)**:
    ```python
    # Model Predictor: 추론 수행 및 전처리 파이프라인 래퍼
    class FetalDecelModel:
        def __init__(self, model_path: str):
            self.model = self.load_model(model_path)

        def load_model(self, path: str):
            # ONNX Runtime 가중치 로드
            return onnxruntime.InferenceSession(path)

        def preprocess(self, raw_signals: list[float]) -> list[float]:
            # 1. 데이터 노멀라이제이션 및 슬라이딩 윈도우 피처 추출
            normalized = [s / 100.0 for s in raw_signals]
            return normalized

        def predict(self, raw_signals: list[float]) -> float:
            features = self.preprocess(raw_signals)
            inputs = {self.model.get_inputs()[0].name: [features]}
            outputs = self.model.run(None, inputs)
            return float(outputs[0][0])
    ```

#### ③ config
*   **정의**: 추론용 슬라이딩 윈도우 크기, 이상치 필터(Outlier Filter) 유무 등 모델 구동 설정 파라미터 파일의 **순수 파일명**.

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
