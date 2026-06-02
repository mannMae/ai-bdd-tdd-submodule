from datetime import datetime
from zoneinfo import ZoneInfo
from pydantic import BaseModel, Field, field_serializer, ConfigDict

# 1. 전역 datetime 포맷 규칙을 내장한 Custom BaseModel (Pydantic v2 표준)
class CustomModel(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    @field_serializer("*", when_used="json", check_fields=False)
    def _serialize_datetimes(self, value):
        if isinstance(value, datetime):
            if value.tzinfo is None:
                value = value.replace(tzinfo=ZoneInfo("UTC"))
            return value.strftime("%Y-%m-%dT%H:%M:%S%z")
        return value

# 2. Input DTO: 게시글 생성 시 필요한 필드 및 제약 조건 검증
class PostCreate(BaseModel):
    title: str = Field(min_length=1, max_length=100)
    content: str = Field(min_length=1)

# 3. Output DTO: 클라이언트로 반환할 직렬화 스키마
class PostResponse(CustomModel):
    id: int
    title: str
    content: str
    creator_id: str

# 4. 공통 에러 반환 스키마
class ErrorResponse(BaseModel):
    detail: str
