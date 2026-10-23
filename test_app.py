import pytest
import app as app_module


@pytest.fixture
def client(tmp_path, monkeypatch):
    # Use a temporary database so tests never touch your real data
    monkeypatch.setattr(app_module, "DB_NAME", str(tmp_path / "test.db"))
    app_module.init_db()
    app_module.app.config["TESTING"] = True
    return app_module.app.test_client()


def test_list_tasks_empty(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert response.get_json() == []


def test_add_task(client):
    response = client.post("/tasks", json={"title": "Learn Flask"})
    assert response.status_code == 201
    assert response.get_json()["title"] == "Learn Flask"
    assert len(client.get("/tasks").get_json()) == 1


def test_add_task_without_title_fails(client):
    response = client.post("/tasks", json={})
    assert response.status_code == 400


def test_update_task(client):
    task_id = client.post("/tasks", json={"title": "Write tests"}).get_json()["id"]
    response = client.put(f"/tasks/{task_id}", json={"done": True})
    assert response.status_code == 200
    assert client.get("/tasks").get_json()[0]["done"] == 1


def test_update_missing_task_returns_404(client):
    response = client.put("/tasks/999", json={"done": True})
    assert response.status_code == 404


def test_delete_task(client):
    task_id = client.post("/tasks", json={"title": "Temp"}).get_json()["id"]
    response = client.delete(f"/tasks/{task_id}")
    assert response.status_code == 204
    assert client.get("/tasks").get_json() == []