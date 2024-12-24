from fastapi import Depends
from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.testclient import TestClient

from app.dao import DocTextDAO
from app.database import get_session
from app.main import app
from for_tests.conftest import session


async def test_getter_test(aclient: AsyncClient, session: AsyncSession):

    def get_session_override():
        return session

    app.dependency_overrides[get_session] = get_session_override

    response = await aclient.get("/get_text", params={"id_doc": 1})
    app.dependency_overrides.clear()
    response = response.json()
    # text = await DocTextDAO.getter_text(id_doc=1, session=session)
    assert response["text"] == "La-la"