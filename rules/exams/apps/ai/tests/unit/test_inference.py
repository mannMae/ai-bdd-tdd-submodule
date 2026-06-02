"""
[1. 테스트 대상 유닛 (SUT - System Under Test)]
- 서비스: rules/exams/apps/ai/src/usecases/inference.py (InferenceUsecase)
  - 적용 코드 폼 (Code Form): rules/exams/apps/ai/src/usecases/inference.py (AI-02)
  - State: None (Stateless Usecase)
  - Actions/Methods: execute(request: PredictionRequest) -> PredictionResponse

[2. 호출/의존하는 유닛 (Dependencies)]
- 어댑터: rules/exams/apps/ai/src/outbound/gateway.py (ModelGateway) [AI-05]
- 도메인 코어: rules/exams/apps/ai/src/core/processor.py (FeatureExtractor) [AI-04]
- 타입: rules/exams/apps/ai/src/types/value.py (PredictionRequest) [AI-07]

[3. SUT 동작 규칙 (Business Rules)]
  1. 전처리 정상 호출: 입력 데이터 특징 추출이 올바르게 numpy array로 변환되어 모델에 전달되어야 한다.
  2. 위험 판정: 모델 출력이 0.85인 경우 '위험' 판정이 최종 리턴되어야 한다.
  3. 정상 판정: 모델 출력이 0.3인 경우 '정상' 판정이 최종 리턴되어야 한다.
"""

import pytest
from unittest.mock import AsyncMock
import numpy as np
from src.usecases.inference import InferenceUsecase
from src.core.processor import FeatureExtractor
from src.types.value import PredictionRequest

@pytest.mark.asyncio
async def test_usecase_returns_danger_for_high_score():
    # Arrange
    mock_gateway = AsyncMock()
    # 0.85 점수 반환 설정
    mock_gateway.predict.return_value = np.array([[0.85]], dtype=np.float32)
    
    extractor = FeatureExtractor()
    usecase = InferenceUsecase(model_gateway=mock_gateway, extractor=extractor)
    request = PredictionRequest(data=[120.0, 130.0, 140.0])
    
    # Act
    response = await usecase.execute(request)
    
    # Assert
    assert response.result == "위험"
    mock_gateway.predict.assert_called_once()

@pytest.mark.asyncio
async def test_usecase_returns_normal_for_low_score():
    # Arrange
    mock_gateway = AsyncMock()
    # 0.3 점수 반환 설정
    mock_gateway.predict.return_value = np.array([[0.3]], dtype=np.float32)
    
    extractor = FeatureExtractor()
    usecase = InferenceUsecase(model_gateway=mock_gateway, extractor=extractor)
    request = PredictionRequest(data=[120.0, 130.0, 140.0])
    
    # Act
    response = await usecase.execute(request)
    
    # Assert
    assert response.result == "정상"
    mock_gateway.predict.assert_called_once()
