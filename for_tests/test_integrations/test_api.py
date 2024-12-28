import pytest
from fastapi.testclient import TestClient


@pytest.mark.parametrize("id, status_code, text", [(1, 200, "La-la-la"),
                                (77, 200, "Текст с данным id не найден, используйте метод get_text для его создания!"),
                                (5, 200, "La-la-la"),
                                ('fff', 422, "La-la-la")])
def test_get_text(client: TestClient, id, status_code, text):
    resp = client.get("/get_text", params={"id_doc": id})
    print(resp.json())
    assert resp.status_code == status_code
    assert resp.content == text








