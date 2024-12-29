
from fastapi import HTTPException
import pytest
from pytest import raises
from sqlalchemy.ext.asyncio import AsyncSession

from app.dao import DocumentsDAO



@pytest.mark.parametrize("id", [1, 5, 7])
async def test_delete(id, async_db_session: AsyncSession):
    text = await DocumentsDAO.delete(id_doc=id, session=async_db_session)
    assert text.status_code == 200
    assert text.body.decode('utf-8').strip('"') == "Записи и файл были удалены!"


async def test_check_available():
    with raises(HTTPException) as exc:
        text = await DocumentsDAO.check_available_file(2)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Изображение с id: 2 не найдено!"


async def test_remove_exception():
    with raises(HTTPException) as exc:
        await DocumentsDAO.remove_and_exception(12345)
    assert exc.value.status_code == 404
    assert exc.value.detail == "Кто-то изменил/удалил файл во время выполнения запроса, записи стёрты!"
