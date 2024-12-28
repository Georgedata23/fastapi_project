import json
import shutil
from datetime import datetime
import asyncio
import os

import pytest_asyncio
from httpx import AsyncClient, ASGITransport
import pytest
from sqlalchemy import insert, NullPool
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from app.config import settings
from app.database import Base, async_session_maker, engine, get_session
from app.models import Documents, Documents_text
from app.main import app as fastapi_app

engine_2 = create_async_engine(settings.TEST_DATABASE_URL, poolclass=NullPool)
async_session_maker_2 = sessionmaker(bind=engine_2, class_=AsyncSession, expire_on_commit=False)


@pytest_asyncio.fixture(scope="session", autouse=True)
def event_loop(request):

    loop = asyncio.get_event_loop_policy().new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():

    assert settings.MODE == "TEST"

    async with engine_2.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_json(model: str):

        with open(f"for_tests/data_{model}.json", "r", encoding="utf-8") as file:
            return json.load(file)

    docs = open_json("docs")
    docs_text = open_json("docs_text")

    for doc in docs:
        doc["date"] = datetime.strptime(doc["date"], "%Y-%m-%d")

    async with async_session_maker_2() as session:

        add_docs = insert(Documents).values(docs)
        add_docs_text = insert(Documents_text).values(docs_text)

        await session.execute(add_docs)
        await session.execute(add_docs_text)

        await session.commit()

    source_dir = "for_tests/data"
    destination_dir = "app/doc_static/images"

    for filename in os.listdir(source_dir):
        source_file = os.path.join(source_dir, filename)
        shutil.copy(source_file, destination_dir)



@pytest_asyncio.fixture(scope="function", autouse=True)
async def async_db_session():
    async with async_session_maker_2() as session:
        try:
            yield session
        except:
            await session.rollback()
            raise
        finally:
            await session.close()



@pytest_asyncio.fixture(scope="function", autouse=True)
async def client(async_db_session):

    def override():
        yield async_db_session


    fastapi_app.dependency_overrides[get_session] = override

    async with AsyncClient(transport=ASGITransport(app=fastapi_app), base_url="http://test") as clients:
        yield clients





