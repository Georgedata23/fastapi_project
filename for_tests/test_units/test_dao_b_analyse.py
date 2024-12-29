

from fastapi import HTTPException
import pytest
from pytest import raises
from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao import DocTextDAO
from app.models import Documents
from app.tasks.tasks import img_to_text


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


async def test_img_to_text():
    assert isinstance(img_to_text(10000), str) == True
