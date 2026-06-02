import numpy as np

# Mocking ONNX Session for local testability
class DummySession:
    def run(self, output_names, input_feed):
        # 모의 출력 점수 0.85 리턴
        return [np.array([[0.85]], dtype=np.float32)]

class ModelGateway:
    def __init__(self, model_path: str):
        # 1. 파일 및 바이너리 연산은 Outbound 내에만 머뭄
        self.model_path = model_path
        # 실환경: self.session = ort.InferenceSession(model_path)
        self.session = DummySession()

    async def predict(self, input_tensor: np.ndarray) -> np.ndarray:
        # 2. 비동기 래퍼 혹은 threadpool 위임 추론
        # 실환경: raw_output = self.session.run(None, {input_name: input_tensor})
        raw_output = self.session.run(None, None)
        return raw_output[0]

    async def call_llm(self, prompt: str) -> str:
        # 3. LLM API 외부 HTTP 통신 캡슐화
        # 실환경: openai.ChatCompletion.create(...) 등
        return f"LLM parsed answer for: {prompt}"
