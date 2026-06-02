from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse

class DomainException(Exception):
    """비즈니스 룰 위반 시 발생하는 도메인 전용 에러"""
    def __init__(self, message: str, status_code: int = 400):
        self.message = message
        self.status_code = status_code
        super().__init__(message)

def register_exception_handlers(app: FastAPI):
    """FastAPI 전역 예외 처리기 핸들러 등록"""
    @app.exception_handler(DomainException)
    async def domain_exception_handler(request: Request, exc: DomainException):
        return JSONResponse(
            status_code=exc.status_code,
            content={"detail": exc.message}
        )
