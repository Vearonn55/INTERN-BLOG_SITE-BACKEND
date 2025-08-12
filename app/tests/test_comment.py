# app/tests/test_comment.py

import random
import string


def random_string(prefix="comment", length=6):
    return f"{prefix}-" + ''.join(random.choices(string.ascii_lowercase, k=length))


def test_create_and_delete_comment(client, auth_headers):
    # Create comment
    comment_res = client.post(f"/api/comments/1", headers=auth_headers, json={
        "content": "Nice post!"
    })
    assert comment_res.status_code == 201
    comment_data = comment_res.get_json()
    comment_id = comment_data["id"]
    print(comment_id)

    # Delete comment
    delete_res = client.delete(f"/api/comments/{comment_id}", headers=auth_headers)
    assert delete_res.status_code == 200
    assert delete_res.json["message"] == "Comment deleted successfully"
