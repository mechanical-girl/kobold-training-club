import pytest
from ktc import app


@pytest.fixture
def client():
    return app.app.test_client()


def test_json_with_proper_mimetype(client):
    response = client.get("/api/environments")
    assert response.status_code == 200
