from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_home_route():
    response = client.get("/")
    assert response.status_code == 200
    assert "Alert Management System" in response.json()["message"]


def test_alerts_require_api_key():
    response = client.get("/alerts")
    assert response.status_code == 401


def test_operator_can_list_alerts():
    response = client.get("/alerts", headers={"X-API-Key": "operator-key"})
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) >= 1


def test_summary_route():
    response = client.get("/alerts/summary", headers={"X-API-Key": "operator-key"})
    assert response.status_code == 200
    body = response.json()
    assert "total_alerts" in body
    assert "open" in body
    assert "critical" in body


def test_operator_cannot_delete_alert():
    response = client.delete("/alerts/1", headers={"X-API-Key": "operator-key"})
    assert response.status_code == 403


def test_admin_can_create_and_delete_alert():
    payload = {
        "title": "Test Alert",
        "description": "Created during automated test",
        "severity": "LOW",
        "source": "QA Test",
    }

    create_response = client.post(
        "/alerts",
        json=payload,
        headers={"X-API-Key": "admin-key"},
    )
    assert create_response.status_code == 200
    created_alert = create_response.json()
    assert created_alert["title"] == payload["title"]

    delete_response = client.delete(
        f"/alerts/{created_alert['id']}",
        headers={"X-API-Key": "admin-key"},
    )
    assert delete_response.status_code == 200
