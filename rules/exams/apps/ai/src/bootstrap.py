from src.outbound.gateway import ModelGateway
from src.core.processor import FeatureExtractor
from src.usecases.inference import InferenceUsecase

class DIContainer:
    def __init__(self):
        # 1. 무거운 가중치 모델 로딩 및 게이트웨이 어댑터 초기화 (1회만 캐싱)
        self.model_gateway = ModelGateway(model_path="models/model.onnx")
        self.extractor = FeatureExtractor()
        
        # 2. Usecase 서비스에 조립 의존성 주입
        self.inference_usecase = InferenceUsecase(
            model_gateway=self.model_gateway,
            extractor=self.extractor
        )

# 전역 컨테이너 인스턴스 싱글톤 관리
container = DIContainer()
