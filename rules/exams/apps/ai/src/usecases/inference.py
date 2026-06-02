from src.types.value import PredictionRequest, PredictionResponse
from src.core.processor import FeatureExtractor
from src.outbound.gateway import ModelGateway

# 1. 비즈니스 룰 및 전처리를 Core/Outbound에 격리하고 실행 순서만 제어
class InferenceUsecase:
    def __init__(self, model_gateway: ModelGateway, extractor: FeatureExtractor):
        self.model_gateway = model_gateway
        self.extractor = extractor

    async def execute(self, request: PredictionRequest) -> PredictionResponse:
        # 1. 입력 데이터를 core 전처리용 구조로 변환
        features = self.extractor.extract_features(request.data)
        
        # 2. Outbound Gateway를 활용해 ML 추론 수행
        raw_prediction = await self.model_gateway.predict(features)
        
        # 3. 모델 출력 후처리 판정
        processed_data = self.extractor.postprocess(raw_prediction)
        return PredictionResponse(result=processed_data)
