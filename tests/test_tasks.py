def test_create_task(client):
    client.post("/api/auth/register", json={"email": "task@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "task@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj_resp = client.post(
        "/api/projects",
        json={"name": "Project for Task"},
        headers=headers
    )
    proj_id = proj_resp.json()["id"]

    response = client.post(
        f"/api/projects/{proj_id}/tasks",
        json={"title": "New Task", "description": "Task desc", "status": "TODO"},
        headers=headers
    )
    assert response.status_code == 201
    assert response.json()["title"] == "New Task"

def test_list_tasks(client):
    client.post("/api/auth/register", json={"email": "listtask@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "listtask@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj_resp = client.post(
        "/api/projects",
        json={"name": "Project for Task list"},
        headers=headers
    )
    proj_id = proj_resp.json()["id"]

    client.post(
        f"/api/projects/{proj_id}/tasks",
        json={"title": "Task 1"},
        headers=headers
    )
    
    response = client.get(f"/api/projects/{proj_id}/tasks", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) >= 1

def test_update_task(client):
    client.post("/api/auth/register", json={"email": "updatetask@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "updatetask@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj_resp = client.post(
        "/api/projects",
        json={"name": "Project for Update Task"},
        headers=headers
    )
    proj_id = proj_resp.json()["id"]

    task_resp = client.post(
        f"/api/projects/{proj_id}/tasks",
        json={"title": "Task to Update"},
        headers=headers
    )
    task_id = task_resp.json()["id"]
    
    response = client.put(
        f"/api/tasks/{task_id}",
        json={"title": "Updated Task", "status": "IN_PROGRESS"},
        headers=headers
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Task"
    assert response.json()["status"] == "IN_PROGRESS"

def test_delete_task(client):
    client.post("/api/auth/register", json={"email": "deltask@example.com", "password": "password123"})
    login_resp = client.post("/api/auth/login", json={"email": "deltask@example.com", "password": "password123"})
    token = login_resp.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    proj_resp = client.post(
        "/api/projects",
        json={"name": "Project for Delete Task"},
        headers=headers
    )
    proj_id = proj_resp.json()["id"]

    task_resp = client.post(
        f"/api/projects/{proj_id}/tasks",
        json={"title": "Task to Delete"},
        headers=headers
    )
    task_id = task_resp.json()["id"]
    
    response = client.delete(f"/api/tasks/{task_id}", headers=headers)
    assert response.status_code == 204
    
    get_response = client.get(f"/api/tasks/{task_id}", headers=headers)
    assert get_response.status_code == 404
