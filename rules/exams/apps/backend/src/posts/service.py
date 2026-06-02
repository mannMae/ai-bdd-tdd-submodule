from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import PostCreate
from .vo import PostVO
from .models import PostModel

# 1. 단일 책임 원칙(Single Responsibility)을 준수하는 Usecase 비즈니스 클래스
class CreatePostUsecase:
    # 2. 의존할 데이터베이스 세션 생성자 주입 (Stateless)
    def __init__(self, db: AsyncSession):
        self.db = db

    async def execute(self, payload: PostCreate, creator_id: str) -> PostModel:
        # 3. DTO 데이터를 도메인 규칙을 보장하는 불변 VO로 강제 변환
        vo = PostVO(title=payload.title, content=payload.content)
        
        # 4. 검증 완료된 VO 데이터로 ORM 객체 매핑 및 영속화
        model = PostModel(
            title=vo.title,
            content=vo.content,
            creator_id=creator_id
        )
        self.db.add(model)
        await self.db.flush()
        return model
