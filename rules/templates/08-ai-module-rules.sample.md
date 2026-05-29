---
description: 로컬 ONNX 기반 ML/DL 추론 API 서버 개발 가이드레일
glob: "apps/ai-server/**/*"
---
# 8. 로컬 ML 추론 (ONNX) 서버 개발 가이드레일

로컬 ONNX 기반의 머신러닝/딥러닝 추론 API를 서빙하는 AI 서버의 안정성, CPU 동시성 성능 확보, OOM(Out of Memory) 예방, 입력값 무결성 및 의존성 관리를 위한 핵심 엔지니어링 가이드레일입니다.

---

## 1. 🔄 ONNX Model 생명주기 관리 (Lifespan)

무거운 AI 모델의 가중치나 런타임 세션(ONNX Runtime Session)을 매 요청(Request)마다 로드하는 행위는 심각한 CPU 병목과 메모리 OOM을 발생시킵니다. 따라서 모델의 기동과 정리는 반드시 서버의 수명 주기와 함께 동기화되어야 합니다.

- **Startup 로딩 (싱글톤 패턴)**: 서버 구동 시점에 모델 가중치를 단 1회 로드하여 메모리에 바인딩하고, 요청 처리 시에는 이미 로딩된 전역 세션을 재사용합니다.
- **FastAPI Lifespan 컨텍스트 매니저 사용 강제**: FastAPI의 `lifespan` 이벤트를 사용하여 Startup 시점에 ONNX Predictor 세션을 생성하고 `app.state`에 할당하며, Shutdown 시점에 명시적으로 메모리 할당 자원을 제거합니다.
- **표준 코드 양식 (FastAPI Lifespan & ONNX Load)**:
  ```python
  from contextlib import asynccontextmanager
  from fastapi import FastAPI
  from src.ml_model.onnx.predictor import ONNXModelPredictor

  @asynccontextmanager
  async def lifespan(app: FastAPI):
      # Startup: 서버 기동 시 설정된 경로를 통해 모델 및 가중치를 1회 로드
      model_dir = "./artifacts"
      onnx_path = "./artifacts/model.onnx"
      app.state.predictor = ONNXModelPredictor.from_artifacts(
          model_dir=model_dir, 
          onnx_path=onnx_path
      )
      yield
      # Shutdown: 서버 종료 시 자원 명시적 해제
      if hasattr(app.state, "predictor"):
          del app.state.predictor
  ```

---

## 2. ⚡ 동시성 제어 및 이벤트 루프 보호 (CPU-bound)

ML 추론 및 데이터 전처리(결측치 보간, Resampling, Outlier filtering, Feature Extraction 등) 과정은 순수 CPU 연산 성능에 의존하는 **대표적인 CPU-bound 블로킹 연산**입니다.

- **FastAPI 비동기 싱글스레드 루프 블로킹 방지**: 
  - 추론 라우터 함수가 내부적으로 `await`를 사용한 I/O 블로킹이 없는 순수 CPU 집약적 연산을 수행한다면, 함수 선언에 `async def`를 쓰지 않고 **일반 `def` 함수로 선언**해야 합니다.
  - 일반 `def` 함수로 선언할 경우 FastAPI는 이 요청 처리를 내부의 별도 백그라운드 스레드 풀(Thread Pool)로 위임하여 비동기 실행하므로, 이벤트 루프가 멈춰 서버 전체가 마비되는 현상을 방지합니다.
- **표준 코드 양식 (CPU-bound 라우터 선언)**:
  ```python
  from fastapi import APIRouter, Depends, Request
  from src.ml_model.schemas import InferenceInput, InferenceResult

  router = APIRouter(prefix="/api/v1/predict", tags=["prediction"])

  @router.post("/", response_model=InferenceResult)
  def predict(payload: InferenceInput, request: Request):
      # Heavy CPU-bound 동기 연산은 일반 def 라우터 내에서 동기식으로 호출합니다.
      # FastAPI가 이 전체 핸들러를 작업 스레드 풀(Thread Pool)에서 동시 실행합니다.
      predictor = request.app.state.predictor
      result = predictor.predict(
          features=payload.features,
          parameters=payload.parameters
      )
      return result
  ```

---

## 3. 🛡️ 핵심 ML 알고리즘 무결성 보존 및 캡슐화 격리

연구팀 등 외부에서 검증 및 전달받은 핵심 ML/DL 분석/추론 알고리즘 코드는 수식의 미세한 변화로도 예측 성능이 뒤틀릴 수 있으므로 직접 수정을 엄격히 금지하고, 완벽히 캡슐화하여 보호합니다.

- **핵심 알고리즘 코드의 완벽한 보존**:
  - 수학적 가공, 피처 추출, 모델 추론 로직 등 핵심 알고리즘은 전용 모듈(예: `src/ml_model/` 등) 내부에 격리하여 보존하며, 해당 소스 코드 내부 연산 흐름이나 가중치는 단 한 줄도 임의로 수정해서는 안 됩니다.
- **외곽 통신 및 인프라 레이어 분리**:
  - FastAPI 라우터, 의존성 주입 등 외부 통신 레이어에서만 동시성 성능 확보(스레드 풀 위임 등) 및 리소스 수명 주기 관리를 수행하고, 핵심 알고리즘은 오직 호출 대상으로만 활용합니다.
  - 이를 통해 서버 인프라 및 통신 구조를 튜닝하더라도 알고리즘의 무결성과 결과의 등가성(Equivalence)은 100% 보장되어야 합니다.

---

## 4. 🔍 입력 데이터 유효성 검증 및 전처리 무결성

추론 로직 진입 전에 비정상적인 값(NaN, Inf, 잘못된 데이터 규격)이나 비어있는 데이터가 유입되어 추론 엔진에서 치명적인 런타임 에러(IndexError, ValueError 등)가 발생하는 것을 철저히 차단해야 합니다.

- **Pydantic 스키마 기반 1차 검증**:
  - `InferenceInput` 등의 DTO 스펙 선언 시 Pydantic을 활용하여 데이터의 타입, 범위, 차원(Shape), 필수 필드 포함 상태 등을 사전 검증합니다.
- **전처리 파이프라인(Preprocessing) 내부 2차 검증 및 보정**:
  - 입력 데이터에 NaN/Inf가 포함되어 있을 경우를 대비하여 유효성 검증 및 보간 로직을 거쳐 지정된 기본값으로 복구 및 대체합니다.
  - 전처리 과정에서 보간이나 보정이 발생한 경우 최종 출력의 `warnings` 필드에 해당 사실을 명시적으로 기록합니다.
  - 입력 배열의 길이가 일치하지 않거나 설정 파라미터가 모델 환경 설정과 다를 경우 422 Unprocessable Entity 에러(또는 구체적 Exception)를 즉시 반환하고 연산을 중단합니다.

---

## 5. 📦 패키지 및 의존성 고정 (uv)

개발 환경과 프로덕션 환경의 라이브러리 불일치로 인한 런타임 추론 결함을 미연에 방지하기 위해 패키지 의존성을 명확하게 선언하고 고정하여 사용해야 합니다.

- **표준 빌드 메타데이터 (`pyproject.toml`) 사용**:
  - `requirements.txt`와 같은 임의의 텍스트 파일 대신 파이썬 현대 패키지 표준인 `pyproject.toml`을 생성하여 패키지 이름, 파이썬 버젼 요구사항, 의존성 패키지(예: `onnxruntime`, `pydantic`, `numpy`, `scipy` 등)를 명확히 구조적으로 기재합니다.
- **`uv` 패키징 도구체인 도입**:
  - 패키지 종속성의 빠른 싱크와 빌드 관리를 위해 **`uv`**를 표준 도구로 적용하고, 프로젝트 루트에 `uv.lock` 파일을 동봉하여 배포 환경의 모든 종속 버전을 일관되게 동결(Pinning)합니다.
