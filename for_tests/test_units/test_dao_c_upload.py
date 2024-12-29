import os

from fastapi import HTTPException, UploadFile
from pytest import raises
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao import DocumentsDAO
from app.models import Documents


async def test_upload(async_db_session: AsyncSession):
    with open("for_tests/data_up/abcdef.webp", "wb+") as file_up:
        f = UploadFile(file_up)
        result = await DocumentsDAO.upload(id_doc=117, file_uploaded=f, session=async_db_session)
        assert result.status_code == 200
        assert result.body.decode('utf-8').strip('"') == "Запись и изображение сохранены в БД и на диск!"
    os.remove("app/doc_static/images/117.webp")


async def test_upload_2(async_db_session: AsyncSession):
    with open("for_tests/data_up/abcdef.webp", "wb+") as file_up:
        f = UploadFile(file_up)
        result = await DocumentsDAO.upload(id_doc=1, file_uploaded=f, session=async_db_session)
        assert result.status_code == 200
        assert result.body.decode('utf-8').strip('"') == "Данный id занят, попробуйте другой!"


async def test_upload_3(async_db_session: AsyncSession):
    await async_db_session.execute(insert(Documents).values(id=101,
                                                            path="app/doc_static/images"))
    with raises(HTTPException) as exc:
        with open("for_tests/data_up/abcdef.webp", "wb+") as file_up:
            f = UploadFile(file_up)
            result = await DocumentsDAO.upload(id_doc=101, file_uploaded=f, session=async_db_session)
    assert exc.value.detail == "Ошибка во время добавления записи в БД, попробуйте позже!"
