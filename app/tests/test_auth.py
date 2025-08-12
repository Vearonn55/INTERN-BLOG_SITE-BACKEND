# app/tests/test_auth.py

def test_login_user(client):
    res = client.post("/api/login", json={
        "email": "admin@example.com",
        "password": "securepass"
    })
    assert res.status_code == 200
    assert "access_token" in res.get_json()


def test_get_me(client, auth_headers):
    res = client.get("/api/me", headers=auth_headers)
    assert res.status_code == 200
    data = res.get_json()
    assert data["email"] == "admin@example.com"
    assert data["role"] == "admin"
