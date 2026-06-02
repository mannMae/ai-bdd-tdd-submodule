"""
[1. 테스트 대상 유닛 (SUT - System Under Test)]
- 서비스: rules/exams/apps/backend/src/posts/service.py (CreatePostUsecase)
  - 적용 코드 폼 (Code Form): rules/exams/apps/backend/src/posts/service.py (BE-02)
  - State: None (Stateless Service)
  - Actions/Methods: execute(payload: PostCreate, creator_id: str) -> PostModel

[2. 호출/의존하는 유닛 (Dependencies)]
- 값 객체: rules/exams/apps/backend/src/posts/vo.py (PostVO) [BE-03]
- 데이터 모델: rules/exams/apps/backend/src/posts/models.py (PostModel) [BE-05]
- 데이터베이스 세션: sqlalchemy.ext.asyncio.AsyncSession [BE-04]

[3. SUT 동작 규칙 (Business Rules)]
  1. 제목 무결성 보장: 제목이 비어 있는 경우 ValueError가 발생해야 한다.
  2. 글자수 제한: 제목이 100자를 초과하는 경우 ValueError가 발생해야 한다.
  3. 영속화 성공: 제목이 100자 이하이며 내용이 존재하는 경우 DB Session에 add되고 생성된 PostModel을 반환해야 한다.
"""

import pytest
from unittest.mock import AsyncMock
from src.posts.service import CreatePostUsecase
from src.posts.schemas import PostCreate

@pytest.mark.asyncio
async def test_execute_raises_value_error_for_empty_title():
    # Arrange
    mock_db = AsyncMock()
    usecase = CreatePostUsecase(mock_db)
    payload = PostCreate(title="", content="테스트 내용")
    
    # Act & Assert
    with pytest.raises(ValueError, match="제목은 비어 있을 수 없습니다."):
        await usecase.execute(payload, creator_id="test_user")

@pytest.mark.asyncio
async def test_execute_raises_value_error_for_long_title():
    # Arrange
    mock_db = AsyncMock()
    usecase = CreatePostUsecase(mock_db)
    payload = PostCreate(title="a" * 101, content="테스트 내용")
    
    # Act & Assert
    with pytest.raises(ValueError, match="제목은 100자를 초과할 수 없습니다."):
        await usecase.execute(payload, creator_id="test_user")

@pytest.mark.asyncio
async def test_execute_persists_post_model_successfully():
    # Arrange
    mock_db = AsyncMock()
    usecase = CreatePostUsecase(mock_db)
    payload = PostCreate(title="올바른 제목", content="테스트 내용")
    
    # Act
    result = await usecase.execute(payload, creator_id="test_user")
    
    # Assert
    mock_db.add.assert_called_once()
    mock_db.flush.assert_called_once()
    assert result.title == "올바른 제목"
    assert result.content == "테스트 내용"
    assert result.creator_id == "test_user"
