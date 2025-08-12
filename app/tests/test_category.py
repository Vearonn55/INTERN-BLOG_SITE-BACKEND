import random
import string

def random_string(prefix="category", length=6):
    return f"{prefix}-" + ''.join(random.choices(string.ascii_lowercase, k=length))

def test_create_and_delete_category(client, auth_headers):
    name = random_string("Name")
    slug = random_string("slug")

    # Create category
    res = client.post("/api/categories", headers=auth_headers, json={
        "name": name,
        "slug": slug
    })
    assert res.status_code == 201
    data = res.get_json()
    assert data["name"] == name
    assert data["slug"] == slug
    category_id = data["id"]

    # Delete the same category
    delete_res = client.delete(f"/api/categories/{category_id}", headers=auth_headers)
    assert delete_res.status_code == 200
    assert delete_res.get_json()["message"] == "Category deleted successfully"
