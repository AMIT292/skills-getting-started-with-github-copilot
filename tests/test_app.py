import pytest
from fastapi.testclient import TestClient
from src.app import app
from urllib.parse import quote

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Soccer Team" in data

def test_signup_for_activity_success():
    activity = "Chess Club"
    url = f"/activities/{quote(activity)}/signup"
    response = client.post(url, params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json()["message"]
    # Clean up
    cleanup_url = f"/activities/{quote(activity)}/unregister"
    client.delete(cleanup_url, params={"email": "testuser@mergington.edu"})

def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    activity = "Chess Club"
    url = f"/activities/{quote(activity)}/signup"
    response = client.post(url, params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_nonexistent_activity():
    activity = "Nonexistent"
    url = f"/activities/{quote(activity)}/signup"
    response = client.post(url, params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    activity = "Art Club"
    signup_url = f"/activities/{quote(activity)}/signup"
    unregister_url = f"/activities/{quote(activity)}/unregister"
    # First, sign up
    client.post(signup_url, params={"email": "removeuser@mergington.edu"})
    response = client.delete(unregister_url, params={"email": "removeuser@mergington.edu"})
    assert response.status_code == 200
    assert "Removed removeuser@mergington.edu from Art Club" in response.json()["message"]

def test_unregister_from_activity_not_found():
    activity = "Art Club"
    url = f"/activities/{quote(activity)}/unregister"
    response = client.delete(url, params={"email": "notfound@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

def test_unregister_from_nonexistent_activity():
    activity = "Nonexistent"
    url = f"/activities/{quote(activity)}/unregister"
    response = client.delete(url, params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
