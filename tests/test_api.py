from fastapi.testclient import TestClient

from app.main import app


client = TestClient(app)


def test_health() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_frontend_index() -> None:
    response = client.get("/")
    assert response.status_code == 200
    assert "车机语义测试台" in response.text


def test_parse_navigation() -> None:
    response = client.post(
        "/v1/dialogue/parse",
        json={"query": "导航去北京南站", "session_id": "test"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["accepted"] is True
    assert payload["intent"] == "NAVIGATE"
    assert payload["slots"]["destination"] == "北京南站"


def test_reject_empty_query() -> None:
    response = client.post(
        "/v1/dialogue/parse",
        json={"query": "   ", "session_id": "test"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["accepted"] is False
    assert payload["intent"] == "UNKNOWN"


def test_cockpit_apply_updates_climate() -> None:
    response = client.post(
        "/v1/cockpit/apply",
        json={"query": "打开空调", "session_id": "cockpit-test"},
    )
    assert response.status_code == 200
    payload = response.json()
    assert payload["dialogue"]["intent"] == "VEHICLE_CONTROL"
    assert payload["state"]["climate_on"] is True
    assert payload["modules"][-1]["status"] == "updated"


def test_tool_registry_endpoint() -> None:
    response = client.get("/v1/mcp/tools")
    assert response.status_code == 200
    assert "query_weather" in response.json()["tools"]


def test_sample_evaluation_endpoint() -> None:
    response = client.get("/v1/evaluation/sample")
    assert response.status_code == 200
    payload = response.json()
    assert payload["accuracy"] >= 0.75
    assert payload["total"] == 4.0
