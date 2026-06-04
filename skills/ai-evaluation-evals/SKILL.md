---
name: ai-evaluation-evals
description: ML/AI 모델 추론의 재현성을 확보하기 위한 시드 고정 규칙과 모델 평가 테스트 메트릭 및 속도 성능 검증 기준을 정의합니다.
version: 1.0.0
globs: apps/ai/tests/**/test_*.py, apps/ai/src/**/processor.py
---

# 📊 AI Model Evaluation Metrics & Reproducibility Guidelines

이 스킬은 AI 모듈 개발 및 가중치 업데이트 시, 추론 결과가 일관되게 재현되고 성능 및 반응 속도가 프로덕션 요구사항을 상회하는지 지속적으로 평가하기 위한 규칙입니다.

---

## 1. 🎯 난수 시드 고정 및 결정론적 추론 (Seed Pinning)

1. **글로벌 난수 제어 (Deterministic Inference)**:
   - ML 추론 연산(`AI-DOMAIN-CORE` 등) 또는 임베딩 가공 시 텐서의 초기값 설정, 무작위 드롭아웃, 또는 가공 분할 로직에서 예측 불가능한 결과 차이가 나지 않도록 난수 시드를 명시적으로 고정해야 합니다.
   - NumPy, PyTorch, Python 내장 random 라이브러리 및 TensorFlow가 사용되는 경우, 연산 전역에서 아래와 같은 시드 고정 설정을 반드시 거쳐야 합니다.
   - *Good*:
     ```python
     import random
     import numpy as np
     
     def pin_global_seeds(seed: int = 42):
         random.seed(seed)
         np.random.seed(seed)
         # PyTorch 사용 시 추가:
         # torch.manual_seed(seed)
         # torch.backends.cudnn.deterministic = True
     ```

---

## 2. ⚡ Latency & Threshold Performance Evals (성능 및 반응 속도 검증)

1. **추론 속도(Latency) 단위 테스트 검증**:
   - AI 추론 Usecase와 모델 어댑터를 검증하는 단위 테스트(`AI-DOMAIN-TEST`) 작성 시, 기능 정상 작동 검증 외에 **평균 추론 대기 시간(Latency) 임계치 검증**을 Assert 문에 반드시 통합합니다.
   - *Good*:
     ```python
     import time
     import pytest
     
     @pytest.mark.asyncio
     async def test_inference_latency_guardrail(client):
         start_time = time.perf_counter()
         
         response = await client.post("/predict", json={"data": [0.1] * 120})
         
         elapsed_time = time.perf_counter() - start_time
         assert response.status_code == 200
         # 추론 대기 시간이 200ms 이내여야 함을 가드레일로 강제
         assert elapsed_time < 0.20, f"Inference took too long: {elapsed_time}s"
     ```

---

## 3. 📈 AI 모델 평가지표 검증 (ML Model Evals)

1. **테스트 데이터셋 검증**:
   - 가중치 엔진을 업데이트한 경우, 고정된 골든 테스트 데이터셋(Golden Dataset)을 로드하여 모델의 핵심 평가지표(Accuracy, Precision, Recall 등)를 검증합니다.
   - 코드 리팩토링이나 의존성 라이브러리 버전 업데이트가 모델 추론 품질의 퇴행(Regression)을 일으키지 않았는지 단위 테스트 수준에서 단언문으로 강제합니다.
   - *Good*:
     ```python
     def test_model_accuracy_regression_guard():
         golden_dataset = load_golden_eval_dataset() # 테스트 데이터셋 로드
         predictions = run_batch_evaluation(golden_dataset)
         
         accuracy = calculate_accuracy(predictions, golden_dataset)
         # 모델 정확도가 최소 85% 이상 유지되어야 함을 빌드 가드로 선언
         assert accuracy >= 0.85, f"Model accuracy degraded to {accuracy}"
     ```
