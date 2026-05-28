---
description: AI 모듈 및 머신러닝(ML) 추론 서버 자원 관리, 동시성 처리 및 메모리 누수 방지 가이드레일
glob: "apps/ai-server/**/*"
---
# 8. AI 모듈 및 추론 서버 개발 가이드레일

대용량 AI/ML 모델을 구동하거나 무거운 연산을 처리하는 추론 서버의 성능 최적화, 메모리 OOM(Out of Memory) 방지, 그리고 동시성 병목을 방지하기 위해 AI 에이전트가 반드시 준수해야 하는 규칙입니다.

## 1. AI 모델 생명주기 및 리소스 관리 (OOM 예방)
- **Startup 로딩 (싱글톤 패턴)**: 무거운 AI 모델의 가중치(Weights)나 파이프라인(Pipeline) 객체는 API 요청이 들어올 때(Request handler 내부) 로드하면 안 됩니다. 매 요청마다 파일을 열고 GPU에 할당하는 동작은 극심한 병목과 GPU OOM을 일으킵니다.
- **Lifespan 사용 강제**: FastAPI의 `lifespan` 컨텍스트 매니저를 사용하여 서버 구동 시점에 모델을 단 1회 로드하여 메모리/GPU에 할당하고, 서버 종료 시점에 명시적으로 메모리에서 할당을 해제(del 및 캐시 비우기)하십시오.
  * 올바른 예:
    ```python
    @asynccontextmanager
    async def lifespan(app: FastAPI):
        # Startup: 서버 기동 시 모델을 한 번만 로드하여 app.state에 할당
        app.state.model = HeavyInferenceModel.load("./weights")
        yield
        # Shutdown: 서버 종료 시 자원 회제
        del app.state.model
        if torch.cuda.is_available():
            torch.cuda.empty_cache()
    ```

## 2. 동시성 제어 및 이벤트 루프 블로킹 방지 (성능 보장)
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

## 3. GPU 메모리 관리 및 연산 최적화 (PyTorch 중심)
- **추론 모드 비활성화**: 딥러닝 추론 시 불필요하게 연산 그래프가 생성되고 그래디언트가 메모리에 축적되는 것을 막기 위해, 모든 추론 로직은 반드시 `with torch.no_grad():` 또는 `@torch.inference_mode()` 블록 하위에서 실행되어야 합니다.
- **디바이스 지정**: 모델 가중치와 입력 텐서(`Tensor.to(device)`)의 실행 디바이스(`cuda`, `cpu`, `mps` 등)는 환경 변수나 설정 파일을 기반으로 동적으로 지정될 수 있어야 하며, 임의의 디바이스 문자열을 하드코딩해서는 안 됩니다.

## 4. 데이터 검증 및 차원(Shape) 정합성 검증
- AI 모델에 입력되기 전, 들어오는 데이터의 포맷(예: Base64 이미지 디코딩 유효성)과 차원 수(Numpy Array/Tensor의 Shape)를 조기에 검증하여 모델 단에서 파이썬 데몬 에러가 터지지 않게 방지하십시오.
- Pydantic 스키마를 사용하여 입력받은 수치 데이터의 최솟값/최댓값 및 크기 조건을 사전에 철저히 검증하십시오.
  * 예: `min_items`, `max_items`, `Field(..., ge=0)`
