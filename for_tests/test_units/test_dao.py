from httpx import AsyncClient
from sqlalchemy.ext.asyncio import AsyncSession


from app.dao import DocTextDAO



async def test_getter(client: AsyncClient, async_db_session: AsyncSession):
    text = await DocTextDAO.getter_text(id_doc=1, session=async_db_session)
    print(text.body)
    assert text.body.decode('utf-8').strip('"') == "La-la-la"