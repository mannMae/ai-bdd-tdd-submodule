from typing import Annotated
from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from src.database import get_db
from .schemas import PostCreate, PostResponse, ErrorResponse
from .dependencies import valid_active_user, valid_owned_post
from .service import CreatePostUsecase
from .models import PostModel

router = APIRouter(prefix="/posts", tags=["posts"])

# 1. POST 엔드포인트: 명확한 response_model과 status_code, 다중 에러 응답 설계 기술
@router.post(
    "",
    response_model=PostResponse,
    status_code=status.HTTP_201_CREATED,
    summary="게시글 작성",
    responses={
        status.HTTP_400_BAD_REQUEST: {"model": ErrorResponse, "description": "제목 혹은 내용 누락"},
        status.HTTP_401_UNAUTHORIZED: {"model": ErrorResponse, "description": "인증 정보 없음"}
    }
)
async def create_post(
    payload: PostCreate,
    db: Annotated[AsyncSession, Depends(get_db)],
    current_user: Annotated[dict, Depends(valid_active_user)]
):
    # 2. Usecase 서비스 레이어 호출 및 데이터 생성
    usecase = CreatePostUsecase(db)
    new_post = await usecase.execute(payload, creator_id=current_user["user_id"])
    
    # 3. 변경 사항 커밋 (트랜잭션 확정)
    await db.commit()
    return new_post

# 3. GET 엔드포인트: 다른 의존성 검증기를 활용하여 리소스를 주입받음
@router.get(
    "/{post_id}",
    response_model=PostResponse,
    status_code=status.HTTP_200_OK,
    summary="게시글 조회",
    responses={
        status.HTTP_404_NOT_FOUND: {"model": ErrorResponse, "description": "게시글 없음"}
    }
)
async def get_post(
    post: Annotated[PostModel, Depends(valid_owned_post)]
):
    return post
