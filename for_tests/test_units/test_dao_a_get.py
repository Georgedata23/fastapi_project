from sqlalchemy.ext.asyncio import AsyncSession


from app.dao import DocTextDAO


async def test_getter(async_db_session: AsyncSession):
    text = await DocTextDAO.getter_text(id_doc=1, session=async_db_session)
    assert text.body.decode('utf-8').strip('"') == "La-la-la"


async def test_getter_2(async_db_session: AsyncSession):
    text = await DocTextDAO.getter_text(id_doc=23, session=async_db_session)
    assert text.body.decode('utf-8').strip('"') == "Текст с данным id не найден, используйте метод get_text для его создания!"