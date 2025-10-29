import pytest
from fastapi.testclient import TestClient
from src import app as app_module


client = TestClient(app_module.app)


def test_get_activities_returns_expected_structure():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    assert isinstance(data, dict)
    assert "Chess Club" in data
    chess = data["Chess Club"]
    assert "participants" in chess and isinstance(chess["participants"], list)


def test_signup_and_remove_participant_flow():
    activity = "Chess Club"
    email = "pytest_user@example.com"

    # ensure email not present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]

    # sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # verify present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email in resp.json()[activity]["participants"]

    # remove
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # verify removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]


def test_duplicate_signup_returns_400():
    activity = "Programming Class"
    email = "dup_user@example.com"

    # first signup should succeed
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    # second signup should fail with 400
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400
    assert "already" in resp.json().get("detail", "").lower()
import pytest
from fastapi.testclient import TestClient
from src import app as app_module


client = TestClient(app_module.app)


def test_get_activities_returns_expected_structure():
    resp = client.get("/activities")
    assert resp.status_code == 200
    data = resp.json()
    # basic contract: activities is a dict and contains known keys
    assert isinstance(data, dict)
    assert "Chess Club" in data
    chess = data["Chess Club"]
    assert "participants" in chess and isinstance(chess["participants"], list)


def test_signup_and_remove_participant_flow():
    activity = "Chess Club"
    email = "pytest_user@example.com"

    # ensure email not present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]

    # sign up
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Signed up" in resp.json().get("message", "")

    # verify present
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email in resp.json()[activity]["participants"]

    # remove
    resp = client.delete(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200
    assert "Removed" in resp.json().get("message", "")

    # verify removed
    resp = client.get("/activities")
    assert resp.status_code == 200
    assert email not in resp.json()[activity]["participants"]


def test_duplicate_signup_returns_400():
    activity = "Programming Class"
    email = "dup_user@example.com"

    # first signup should succeed
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 200

    # second signup should fail with 400
    resp = client.post(f"/activities/{activity}/signup", params={"email": email})
    assert resp.status_code == 400
    assert "already" in resp.json().get("detail", "").lower()
