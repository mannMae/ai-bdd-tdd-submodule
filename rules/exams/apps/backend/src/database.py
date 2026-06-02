from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine

DATABASE_URL = "postgresql+asyncpg://user:pass@localhost:5432/db"

# 1. pool_pre_ping 활성화된 async 엔진 생성
engine = create_async_engine(DATABASE_URL, pool_pre_ping=True)

# 2. expire_on_commit 비활성화된 async 세션 팩토리 생성
SessionFactory = async_sessionmaker(engine, expire_on_commit=False)

# 3. 비동기 세션 생성용 Dependency 함수
async def get_db() -> AsyncSession:
    async with SessionFactory() as session:
        yield session
