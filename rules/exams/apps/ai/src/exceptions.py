from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class InferenceEngineException(Exception):
    """모델 로딩 실패, 이상치 감지 등 AI 추론 엔진 장애 처리용 예외"""
    def __init__(self, detail: str, model_name: str, status_code: int = 500):
        self.detail = detail
        self.model_name = model_name
        self.status_code = status_code
        super().__init__(detail)

def register_ai_exception_handlers(app: FastAPI):
    """FastAPI 전역 AI 예외 핸들러 바인딩"""
    @app.exception_handler(InferenceEngineException)
    async def ai_inference_exception_handler(request: Request, exc: InferenceEngineException):
        return JSONResponse(
            status_code=exc.status_code,
            content={
                "error": "AI Inference Failed",
                "model": exc.model_name,
                "message": exc.detail
            }
        )
