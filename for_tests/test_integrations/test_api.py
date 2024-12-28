
import pytest
from httpx import AsyncClient
from pydantic import PositiveInt


@pytest.mark.parametrize("id, status_code, text", [(1, 200, "La-la-la"),
                                (77, 404, "Текст с данным id не найден, используйте метод get_text для его создания!"),
                                (5, 200, "La-la-la")])
async def test_get_text(client: AsyncClient, id: PositiveInt, status_code, text):
    resp = await client.get("/get_text", params={"id_doc": id})
    assert resp.status_code == status_code
    assert resp.json() == text


@pytest.mark.parametrize("id, status_code, text", [(12, 200, "Текст прочитан и добавлен в БД!")])
async def test_doc_analyse(client: AsyncClient, id: PositiveInt, status_code, text):
    resp = await client.get("/doc_analyse", params={"id_doc": id})
    assert resp.status_code == status_code
    # assert resp.content == text











