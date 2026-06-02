from pydantic_settings import BaseSettings
from pydantic import Field

class ModelSpecs(BaseSettings):
    """모델 파일 경로 및 입출력 차원, 감지 임계치를 관리하는 클래스"""
    model_path: str = Field(default="models/model.onnx")
    input_dimension: int = Field(default=120)
    output_dimension: int = Field(default=2)
    threshold: float = Field(default=0.85)

    class Config:
        env_prefix = "AI_MODEL_"
        env_file = ".env"

model_specs = ModelSpecs()
