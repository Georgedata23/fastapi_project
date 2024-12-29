import os
from pathlib import Path

import pytest
from httpx import AsyncClient
from pydantic import PositiveInt


@pytest.mark.asyncio
@pytest.mark.parametrize("id, status_code, text", [(1, 200, "La-la-la"),
                                (77, 404, "Текст с данным id не найден, используйте метод get_text для его создания!"),
                                (5, 200, "La-la-la")])
async def test_get_text(client: AsyncClient, id: PositiveInt, status_code, text):
    resp = await client.get("/get_text", params={"id_doc": id})
    assert resp.status_code == status_code
    assert resp.json() == text


@pytest.mark.asyncio
async def test_doc_analyse(client: AsyncClient):
    resp = await client.post("/doc_analyse", params={"id_doc": 98})
    assert resp.status_code == 200
    assert resp.json() == "Текст прочитан и добавлен в БД!"

@pytest.mark.asyncio
async def test_upload_doc(client: AsyncClient):
    test_image_path = Path("for_tests/data_up/abcdef.webp")

    with test_image_path.open("rb") as img_file:
        files = {"file": ("abcdef.webp", img_file, "image/webp")}
        data = {"id_doc": 888}
        resp = await client.post("/upload_doc", files=files, params={"id_doc": 888})
        assert resp.status_code == 200
        assert resp.json() == "Запись и изображение сохранены в БД и на диск!"
    os.remove("app/doc_static/images/888.webp")

@pytest.mark.asyncio
async def test_delete_doc(client: AsyncClient):
    resp = await client.delete("/delete_doc", params={"id_doc": 98})
    assert resp.status_code == 200
    assert resp.json() == "Записи и файл были удалены!"












