import json
from datetime import datetime
import asyncio

import pytest
from sqlalchemy import insert, NullPool
from fastapi.testclient import TestClient
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
# from app.main import get_session
from app.database import Base, async_session_maker, engine, get_session
from app.models import Documents, Documents_text
from app.main import app as fastapi_app

engine = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)


@pytest.fixture(scope="session", autouse=True)
def event_loop(request):

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():

    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_json(model: str):

        with open(f"for_tests/data_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    docs = open_json("docs")
    docs_text = open_json("docs_text")

    for doc in docs:
        doc["date"] = datetime.strptime(doc["date"], "%Y-%m-%d")

    async with async_session_maker() as session:

        add_docs = insert(Documents).values(docs)
        add_docs_text = insert(Documents_text).values(docs_text)

        await session.execute(add_docs)
        await session.execute(add_docs_text)

        await session.commit()


# @pytest.fixture
# async def async_db_session():
#     async with async_session_maker() as session:
#         yield session



@pytest.fixture(scope="function")
def client():

    def override():


    fastapi_app.dependency_overrides[get_session] = override
    with TestClient(app=fastapi_app, base_url="http://test") as clients:
        yield clients





