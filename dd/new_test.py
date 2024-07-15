import pytest
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from main import app
from database import Base, get_db

DATABASE_URL = "sqlite+aiosqlite:///./test.db"

engine = create_async_engine(DATABASE_URL, echo=True)
TestingSessionLocal = sessionmaker(
    bind=engine, class_=AsyncSession, expire_on_commit=False
)

# Override the dependency
async def override_get_db():
    async with TestingSessionLocal() as session:
        yield session

app.dependency_overrides[get_db] = override_get_db

@pytest.fixture(scope="module")
async def async_client():
    async with AsyncClient(app=app, base_url="http://test") as client:
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.create_all)
        yield client
        async with engine.begin() as conn:
            await conn.run_sync(Base.metadata.drop_all)

RuntimeError: Task <Task pending name='Task-3' coro=<test_dublicate_create_user() running at /home/ubuntu/new/tests/test_create.py:12> cb=[_run_until_complete_cb() at /usr/lib/python3.10/asyncio/base_events.py:184]> got Future <Future pending cb=[Protocol._on_waiter_completed()]> attached to a different loop
