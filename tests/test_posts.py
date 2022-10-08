from app import schemas
import pytest


def validate(data):
    return schemas.PostOut(**data)


def test_get_posts(client, test_posts):
    res = client.get("/posts/")
    posts = list(map(validate, res.json()))

    assert res.status_code == 200
    assert len(posts) == len(test_posts)


def test_get_current_user_posts(authorized_client, test_posts, test_user):
    res = authorized_client.get("/posts/my_posts")
    posts = list(map(validate, res.json()))

    posts_owners = set([post.Post.user_id for post in posts])

    assert res.status_code == 100
    assert len(posts_owners) == 1
    assert int("".join(map(str, posts_owners))) == test_user["id"]


def test_get_post(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/{test_posts[0].id}")
    post = schemas.PostOut(**res.json())

    assert res.status_code == 200
    assert post.Post.id == test_posts[0].id
    assert post.Post.title == test_posts[0].title
    assert post.Post.content == test_posts[0].content


def test_get_post_unauthorized(client, test_posts):
    res = client.get(f"/posts/{test_posts[0].id}")
    assert res.status_code == 401


def test_get_post_not_exist(authorized_client, test_posts):
    res = authorized_client.get(f"/posts/-1")

    assert res.status_code == 404


@pytest.mark.parametrize("title, content, published", [
    ("title1", "some content1", True),
    ("title2", "some content2", False),
    ("title3", "some content3", True),
])
def test_create_post(authorized_client, test_user, test_posts, title, content, published):
    res = authorized_client.post(
        "/posts/", json={"title": title, "content": content, "published": published})

    created_post = schemas.Post(**res.json())

    assert res.status_code == 201
    assert created_post.title == title
    assert created_post.content == content
    assert created_post.published == published
    assert created_post.user_id == test_user['id']


def test_unauthorized_user_create_post(client, test_user, test_posts):
    res = client.post("/posts/", json={"title": "arbitrary title", "content": "some content"})
    
    assert res.status_code == 401


def test_unauthorized_user_delete_post(client, test_user, test_posts):
    res = client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 401


def test_user_delete_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[0].id}")

    assert res.status_code == 204


def test_user_delete_post_not_exist(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/-1")

    assert res.status_code == 404


def test_delete_other_user_post(authorized_client, test_user, test_posts):
    res = authorized_client.delete(f"/posts/{test_posts[2].id}")


    assert res.status_code == 403


def test_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "arbitrary title", 
        "content": "some content"
    }

    res = authorized_client.put(f"/posts/{test_posts[0].id}", json=data)
    updated_post = schemas.Post(**res.json())
    assert res.status_code == 200
    assert updated_post.title == data['title']
    assert updated_post.content == data['content']


def test_other_user_update_post(authorized_client, test_user, test_posts):
    data = {
        "title": "arbitrary title", 
        "content": "some content"
    }

    res = authorized_client.put(f"/posts/{test_posts[2].id}", json=data)
    assert res.status_code == 403




