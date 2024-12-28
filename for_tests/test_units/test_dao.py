from httpx import AsyncClient
from pydantic import PositiveInt
import pytest
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao import DocTextDAO



async def test_getter(client: AsyncClient, async_db_session: AsyncSession):
    text = await DocTextDAO.getter_text(id_doc=1, session=async_db_session)
    assert text.body.decode('utf-8').strip('"') == "La-la-la"


async def test_getter_2(client: AsyncClient, async_db_session: AsyncSession):
    text = await DocTextDAO.getter_text(id_doc=23, session=async_db_session)
    assert text.body.decode('utf-8').strip('"') == "Текст с данным id не найден, используйте метод get_text для его создания!"

# @pytest.mark.parametrize("id",[33, 510])
async def test_analyse(async_db_session: AsyncSession):
    response = await DocTextDAO.analyse(id_doc=5, session=async_db_session)
    assert response.body.decode('utf-8').strip('"') == "Текст прочитан и добавлен в БД!"
