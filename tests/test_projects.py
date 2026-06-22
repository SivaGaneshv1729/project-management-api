def test_create_project(client):
    client.post("/api/auth/register", json={"email": "proj@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "proj@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    response = client.post(
        "/api/projects",
        json={"name": "New Project", "description": "Test description"},
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["name"] == "New Project"

def test_list_projects(client):
    client.post("/api/auth/register", json={"email": "listproj@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "listproj@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    client.post(
        "/api/projects",
        json={"name": "Project 1"},
        headers=headers
    )
    
    response = client.get("/api/projects", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1
    
def test_update_project(client):
    client.post("/api/auth/register", json={"email": "updateproj@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "updateproj@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = client.post(
        "/api/projects",
        json={"name": "Project 1"},
        headers=headers
    )
    proj_id = proj.json()["id"]
    
    response = client.put(f"/api/projects/{proj_id}", json={"name": "Updated Project"}, headers=headers)
    assert response.status_code == 200
    assert response.json()["name"] == "Updated Project"

def test_delete_project(client):
    client.post("/api/auth/register", json={"email": "delproj@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "delproj@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj = client.post(
        "/api/projects",
        json={"name": "Project to Delete"},
        headers=headers
    )
    proj_id = proj.json()["id"]
    
    response = client.delete(f"/api/projects/{proj_id}", headers=headers)
    assert response.status_code == 204
    
    get_response = client.get(f"/api/projects/{proj_id}", headers=headers)
    assert get_response.status_code == 404
