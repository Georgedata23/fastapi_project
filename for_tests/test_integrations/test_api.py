from httpx import AsyncClient
import pytest

@pytest.mark.parametrize("id, status_code", [(1, 200),
                                (77, 200),
                                (5, 200),
                                ('fff', 422)])
async def test_get_text(aclient: AsyncClient, id, status_code):
    response = await aclient.get("/get_text", params={"id_doc": id})
    assert response.status_code == status_code







