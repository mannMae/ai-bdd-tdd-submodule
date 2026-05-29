# 📊 [F01] 모니터링 기능 (Monitoring) - 기술 매핑 및 채점표

이 문서는 모니터링 기능의 세부 시나리오가 프론트엔드, 백엔드, AI 모듈의 어떤 아키텍처/디자인 패턴과 매핑되는지 정의하고, 구현 완료 후 규칙 준수 여부를 채점하는 기록서입니다.

* **상태 (Status)**: `WIP` (진행 중)
* **연관 문서**: [유저플로우(User Flow)](file:///docs/user-flow/monitoring_flow.md) | [거킨 시나리오(BDD)](file:///features/monitoring.feature)

---

## 1. 🗺️ 시나리오-아키텍처 매핑 매트릭스 (Technical Mapping)

| 시나리오 | [FE] UI | [FE] API (HTTP/WS) | [FE] 상태/스토어 | [FE] 브라우저/유틸 | ┃ | [BE] API (HTTP/WS) | [BE] 아키텍처/인프라 | [BE] DB 테이블 | [BE] 도메인 (Usecase/VO) | ┃ | [AI] API/입출력 | [AI] 모델/설정 | ┃ | 글로벌 |
| :--- | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :--- | :--- | :---: | :--- | :--- | :---: | :--- |
| **S01. 모니터링 시작**<br>*(넘버패드 입력 후 시작)* | `MonitoringSetting` ➔ `(NumpadModal)` ➔ `Monitoring` | WS (`Send: START`) | `useMonitorStore` | `LocalStorage` (인증 토큰 로드) | **┃** | WS (`START` 수신) | Redis Pub/Sub 메시지 발행 | `monitor_session` | • `StartMonitoringUsecase`<br>• `FetalDataVO` | **┃** | `predict_window`<br>(IN: `fhr, toco` ➔ OUT: `risk_probability, risk_label`) | `model.onnx`<br>(use_research_outlier_filter: true) | **┃** | JWT 인증 전파 |
| **S02. 시뮬레이션 모드**<br>*(시뮬레이션 데이터 구동)* | `Monitoring` ➔ `(SimulationPanel)` | WS (`Send: SIMULATE`) | `useMonitorStore` | `timeFormatter.ts` (시간 포맷 유틸) | **┃** | WS (`SIMULATE` 수신) | DB 트랜잭션 비동기 처리 | `simulation_log` | • `StartSimulationUsecase`<br>• `SimulationVO` | **┃** | `predict_window`<br>(IN: `fhr, toco` ➔ OUT: `risk_probability, risk_label`) | `model.onnx`<br>(use_research_outlier_filter: false) | **┃** | JWT 인증 전파 |
| **S03. 모니터링 종료**<br>*(사용자 강제 종료)* | `Monitoring` ➔ `(ConfirmModal)` ➔ `Menu` | HTTP POST<br>(`/api/v1/monitor/stop`) | `useMonitorStore` | `SessionStorage` (임시 세션 제거) | **┃** | HTTP POST<br>(`/api/v1/monitor/stop`) | Redis Pub/Sub 메시지 발행 | `monitor_session`<br>(Status 업데이트) | • `StopMonitoringUsecase` | **┃** | - | - | **┃** | JWT 인증 전파 |

---

## 💡 각 영역별 작성 가이드 및 표준 코드 양식 (Code Forms)

이 가이드는 RTM 각 컬럼에 들어갈 기술 요소의 정의와, 실제 코드로 구현할 때 반드시 따라야 하는 **표준 코드 양식(Templates)**을 정의합니다. (해당없음은 `-`로 표기)

---

### 1) 프론트엔드 (Frontend - 4단계 레이어 분리)

프론트엔드 역시 백엔드와 마찬가지로 흐름을 **화면(UI) ➔ 통신(API) ➔ 상태(스토어) ➔ 도구(브라우저/유틸)**의 4단계 컬럼으로 완벽히 분리하여 기술합니다.

#### ① [FE] UI
*   **정의**: 시나리오 수행 시 사용자에게 렌더링되거나 전환되는 UI 흐름을 기재합니다. 
    *   **UI 전환/이동이 일어나는 경우**: `이전UI ➔ 이동할UI` 형태로 변화를 명시합니다. (예: `MonitoringSetting ➔ Monitoring`)
    *   **화면 이동 과정 중 팝업/모달/서브패널 등이 등장하는 경우**: 괄호 `(SubUI)`를 사용하여 흐름 사이에 명시합니다. (예: `MonitoringSetting ➔ (NumpadModal) ➔ Monitoring`, `Monitoring ➔ (SimulationPanel)`)

#### ② [FE] API (HTTP/WS)
*   **정의**: 프론트엔드에서 발송하는 HTTP 요청 메서드/경로 또는 WebSocket 발송 이벤트.
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

#### ③ [FE] 상태/스토어
*   **정의**: 전역 상태 관리(Zustand 등) 스토어 및 데이터 흐름 상태 정의.
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

#### ④ [FE] 브라우저/유틸
*   **정의**: 브라우저 저장소(LocalStorage, SessionStorage, Cookie)나 브라우저 Native API, 혹은 범용 계산/파싱을 수행하는 공통/도메인 유틸리티 함수(`utils`)를 기술합니다.
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

### 2) 백엔드 (Backend - 4단계 레이어 분리)

백엔드 개발 흐름을 **게이트(API) ➔ 장치(아키텍처/인프라) ➔ 저장소(DB 테이블) ➔ 두뇌(도메인)**의 4개 컬럼으로 완벽히 분리하여 기술합니다.

#### ① [BE] API (HTTP/WS)
*   **정의**: 백엔드가 외부 요청을 받아들이는 게이트웨이 관문.
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

#### ② [BE] 아키텍처/인프라
*   **정의**: 시스템을 구동하는 기술 뼈대 및 미들웨어/프레임워크 연동 규칙.
*   **표준 코드 양식 (비동기 DB 커넥션 / Redis 연동 등)**:
    ```python
    # 비동기 트랜잭션 관리 구조 양식
    async with async_session_maker() as session:
        async with session.begin():
            # 안전한 DB 트랜잭션 수행 보장 블록
            await repository.save(session, entity)
    ```

#### ③ [BE] DB 테이블
*   **정의**: 데이터가 적재, 수정, 또는 조회되는 데이터베이스 물리 테이블명.
    *   *예시*: `monitor_session`, `simulation_log`

#### ④ [BE] 도메인 (Usecase/VO)
*   **정의**: 데이터 가공, 상태 계산 등 순수 비즈니스 규칙 처리 레이어 (Usecase/Service & Value Object).
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

    # VO (Value Object): 데이터 무결성을 보장하는 불변 값 객체
    from dataclasses import dataclass

    @dataclass(frozen=True)
    class FetalDataVO:
        heart_rate: int
    ```

---

### 3) AI 모듈 (AI Module - 2단계 레이어 분리)

AI 모듈 역시 복잡한 데이터 분석 처리가 얽히므로, 백엔드와 일관되게 **게이트(API) ➔ 두뇌(모델/파이프라인)**의 2개 컬럼으로 구성합니다.

#### ① [AI] API/입출력
*   **정의**: AI 엔진 서버가 제공하는 HTTP/gRPC 연동 규격 및 입출력 명세.
*   **표준 코드 양식 (AI Inference Router)**:
    ```python
    @router.post("/predict", response_model=PredictResponse)
    async def predict_endpoint(payload: PredictRequest):
        prediction = await ai_model.predict(payload.features)
        return PredictResponse(prediction=prediction)
    ```

#### ② [AI] 모델/설정
*   **정의**: 실제 추론을 수행하는 인공지능 신경망 모델 정보(ONNX)와 가중치 파일, 그리고 추론 파라미터 설정을 기재합니다.
    *   *내용*: 추론 모델 종류 및 가중치 버전(LSTM v1.5), 데이터 정규화 및 슬라이딩 윈도우 규칙 등.
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

---

### 4) 글로벌
*   **정의**: JWT 보안 검증 규칙, 공통 에러 응답 규격, 다중 컨텍스트 간 데이터 포맷 규칙.

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
