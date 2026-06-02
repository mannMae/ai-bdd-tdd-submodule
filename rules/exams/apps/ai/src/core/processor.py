import numpy as np

# 1. 외부 의존성(SDK, IO, 네트워크)이 일절 배제된 Pure Python 연산 컴포넌트
class FeatureExtractor:
    def extract_features(self, raw_data: list[float]) -> np.ndarray:
        # 입력 데이터 검증 및 shape 변환 (1, -1)
        if not raw_data:
            raise ValueError("특징을 추출할 원시 신호 데이터가 비어 있습니다.")
        return np.array(raw_data, dtype=np.float32).reshape(1, -1)

    def postprocess(self, model_output: np.ndarray) -> str:
        # 모델 출력 점수(float)를 비즈니스 규칙에 근거하여 판단 분류
        score = float(model_output[0][0])
        if score > 0.8:
            return "위험"
        elif score > 0.4:
            return "경고"
        return "정상"
