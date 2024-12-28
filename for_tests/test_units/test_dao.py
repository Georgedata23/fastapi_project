from fastapi import HTTPException, UploadFile
from httpx import AsyncClient
from pydantic import PositiveInt
import pytest
from pytest import raises
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao import DocTextDAO, DocumentsDAO
from app.models import Documents_text, Documents


async def test_getter(client: AsyncClient, async_db_session: AsyncSession):
    text = await DocTextDAO.getter_text(id_doc=1, session=async_db_session)
    assert text.body.decode('utf-8').strip('"') == "La-la-la"


async def test_getter_2(client: AsyncClient, async_db_session: AsyncSession):
    text = await DocTextDAO.getter_text(id_doc=23, session=async_db_session)
    assert text.body.decode('utf-8').strip('"') == "Текст с данным id не найден, используйте метод get_text для его создания!"



@pytest.mark.parametrize("id",[33, 510])
async def test_analyse(id, async_db_session: AsyncSession):

    await async_db_session.execute(insert(Documents).values(id=id,
                                                        path="app/doc_static/images"))
    await async_db_session.commit()
    response = await DocTextDAO.analyse(id_doc=id, session=async_db_session)
    assert response.body.decode('utf-8').strip('"') == "Текст прочитан и добавлен в БД!"


async def test_found_or_no():
    with raises(HTTPException) as exc:
        DocTextDAO.found_or_no(333)
    assert exc.value.detail == "Файл не найден!"


async def test_analyse_error(async_db_session: AsyncSession):
    with raises(HTTPException) as exc:
        assert await DocTextDAO.analyse(id_doc=1, session=async_db_session) == 200
    assert exc.value.detail == "Текст не был добавлен в БД!"



async def test_upload(async_db_session: AsyncSession):
    with open("for_tests/data_up/abcdef.webp", "wb+") as file_up:
        f = UploadFile(file_up)
        result = await DocumentsDAO.upload(id_doc=117, file_uploaded=f, session=async_db_session)
        assert result.status_code == 200
        assert result.body.decode('utf-8').strip('"') == "Запись и изображение сохранены в БД и на диск!"
