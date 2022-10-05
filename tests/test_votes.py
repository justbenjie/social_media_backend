import pytest
from app import models


def test_vote_on_post(authorized_client, test_posts):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id})
    assert res.status_code == 201


def test_vote_twice_on_post(authorized_client, test_posts, test_vote):
    res = authorized_client.post("/vote/", json={"post_id": test_posts[2].id})
    assert res.status_code == 204
