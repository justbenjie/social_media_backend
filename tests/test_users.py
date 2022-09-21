from app import schemas
import pytest
from jose import jwt
from app.config import settings


def test_create_user(client):

    res = client.post(
        "/users/", json={"email": "iamphilipp@gmail.com", "password": "12345"})

    new_user = schemas.UserOut(**res.json())
    assert res.status_code == 201
    assert new_user.email == "iamphilipp@gmail.com"


def test_login_user(test_user, client):
    res = client.post(
        "/login", data={"username": test_user['email'], "password": test_user['password']})

    token = schemas.Token(**res.json())
    payload = jwt.decode(token.access_token, key=settings.secret_key, algorithms=[
                         settings.algorithm])
    id = payload.get("user_id")

    assert res.status_code == 200
    assert token.token_type == "bearer"
    assert id == test_user['id']


@pytest.mark.parametrize("email, password, status_code", [
    ('wrongemail@gmail.com', 'password123', 403),
    ('nesterov@gmail.com', 'wrongpassword', 403),
    ('wrongemail@gmail.com', 'wrongpassword', 403),
    (None, 'password123', 422),
    ('nesterov@gmail.com', None, 422)
])
def test_incorrect_login(test_user, client, email, password, status_code):
    res = client.post(
        "/login", data={"username": email, "password": password})

    assert res.status_code == status_code
    # assert res.json().get('detail') == "Invalid Credentials"
