from fastapi import APIRouter, Depends, status
from typing import Annotated
from src.bootstrap import container
from src.types.value import PredictionRequest, PredictionResponse

router = APIRouter(prefix="/predict", tags=["predict"])

# 1. API 요청 수신 및 비동기 추론 처리 위임
@router.post(
    "",
    response_model=PredictionResponse,
    status_code=status.HTTP_200_OK,
    summary="Fetal Heart Rate 추론 검사"
)
async def predict_heart_rate(
    payload: PredictionRequest,
    usecase = Depends(lambda: container.inference_usecase)
):
    # 2. 파싱 및 비즈니스 연산 없이 Usecase 즉시 호출
    result = await usecase.execute(payload)
    return result
