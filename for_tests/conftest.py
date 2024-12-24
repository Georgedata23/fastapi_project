import json
from datetime import datetime
import asyncio

import pytest
from sqlalchemy import insert

from app.config import settings
from app.database import Base, async_session_maker, engine
from app.models import Documents, Documents_text


# @pytest.fixture(scope="session") # Заменили с помощью asyncio_default_fixture_loop_scope в pytest.ini
# def event_loop(request):
#
#     loop = asyncio.get_event_loop_policy().new_event_loop()
#     yield loop
#     loop.close()


@pytest.fixture(autouse=True, scope="session")
async def prepare_database():

    assert settings.MODE == "TEST"

    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)

    def open_mock_json(model: str):

        with open(f"for_tests/data_{model}.json", "r") as file:
            return json.load(file)

    docs = open_mock_json("docs")
    docs_text = open_mock_json("docs_text")

    for doc in docs:
        doc["date"] = datetime.strptime(doc["date"], "%Y-%m-%d")

    async with async_session_maker() as session:

        add_docs = insert(Documents).values(docs)
        add_docs_text = insert(Documents_text).values(docs_text)

        await session.execute(add_docs)
        await session.execute(add_docs_text)

        await session.commit()



