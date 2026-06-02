from typing import Annotated
from fastapi import Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from .models import PostModel

# 1. JWT 토큰을 파싱하여 인가를 수행하는 Mock Dependency (비동기 수행 선호)
async def valid_active_user() -> dict:
    # 실서비스에서는 JWT 검증 후 유저 반환
    return {"user_id": "test_user_id"}

# 2. Path 파라미터로 유입된 ID 기반 리소스 검증 및 리소스를 획득하는 의존성
async def valid_post_id(
    post_id: int,
    db: Annotated[AsyncSession, Depends(get_db)]
) -> PostModel:
    post = await db.get(PostModel, post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="존재하지 않는 게시글입니다."
        )
    return post

# 3. 다른 의존성을 체이닝(Chaining)하여 도메인 소유권을 판단하는 의존성
async def valid_owned_post(
    post: Annotated[PostModel, Depends(valid_post_id)],
    user: Annotated[dict, Depends(valid_active_user)]
) -> PostModel:
    if post.creator_id != user["user_id"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="이 리소스에 대한 수정 권한이 없습니다."
        )
    return post
