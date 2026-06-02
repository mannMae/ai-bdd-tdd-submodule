from pydantic import BaseModel
from dataclasses import dataclass

# 1. Inbound/Outbound API 경계용 Pydantic DTO (types/boundary)
class PredictionRequest(BaseModel):
    data: list[float]

class PredictionResponse(BaseModel):
    result: str

# 2. Core 내부 비즈니스 룰 및 제어용 frozen dataclass VO (types/value)
@dataclass(frozen=True)
class TensorConfigVO:
    input_dim: int
    output_dim: int
