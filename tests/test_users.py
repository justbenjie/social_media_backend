from app import schemas
from .database import session, client

def test_root(client):

    res = client.get("/")

    assert res.json().get("data") == "Hello"


def test_create_user(client):

    res = client.post(
        "/users/", json={"email": "iamphilipp@gmail.com", "password": "12345"})

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "iamphilipp@gmail.com"
