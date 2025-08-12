# app/tests/test_post.py

import random
import string


def random_string(prefix="post", length=5):
    return f"{prefix}-" + ''.join(random.choices(string.ascii_lowercase, k=length))


def test_create_post(client, auth_headers):
    title = random_string("Title")
    slug = random_string("slug")

    res = client.post("/api/posts", headers=auth_headers, json={
        "title": title,
        "slug": slug,
        "content": "This is the content",
        "published": True,
        "category_id": 1  # Always use category 1
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["title"] == title
    assert data["slug"] == slug


def test_get_all_posts(client):
    res = client.get("/api/posts")
    assert res.status_code == 200
    data = res.get_json()
    assert isinstance(data["posts"], list)
