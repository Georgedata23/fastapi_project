
import pytest
from httpx import AsyncClient
from pydantic import PositiveInt
from sqlalchemy.ext.asyncio import AsyncSession
import json
from sqlalchemy import insert

from app.models import Documents


@pytest.mark.parametrize("id, status_code, text", [(1, 200, "La-la-la"),
                                (77, 404, "Текст с данным id не найден, используйте метод get_text для его создания!"),
                                (5, 200, "La-la-la")])
async def test_get_text(client: AsyncClient, id: PositiveInt, status_code, text):
    resp = await client.get("/get_text", params={"id_doc": id})
    assert resp.status_code == status_code
    assert resp.json() == text



async def test_doc_analyse(client: AsyncClient):
    resp = await client.post("/doc_analyse", params={"id_doc": 98})
    assert resp.status_code == 200
    assert resp.json() == "Текст прочитан и добавлен в БД!"












