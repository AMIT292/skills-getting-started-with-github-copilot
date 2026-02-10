import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert "Chess Club" in data
    assert "Soccer Team" in data

def test_signup_for_activity_success():
    response = client.post("/activities/Chess Club/signup", params={"email": "testuser@mergington.edu"})
    assert response.status_code == 200
    assert "Signed up testuser@mergington.edu for Chess Club" in response.json()["message"]
    # Clean up
    client.delete("/activities/Chess Club/unregister", params={"email": "testuser@mergington.edu"})

def test_signup_for_activity_already_signed_up():
    email = "michael@mergington.edu"
    response = client.post("/activities/Chess Club/signup", params={"email": email})
    assert response.status_code == 400
    assert response.json()["detail"] == "Student already signed up for this activity"

def test_signup_for_nonexistent_activity():
    response = client.post("/activities/Nonexistent/signup", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"

def test_unregister_from_activity_success():
    # First, sign up
    client.post("/activities/Art Club/signup", params={"email": "removeuser@mergington.edu"})
    response = client.delete("/activities/Art Club/unregister", params={"email": "removeuser@mergington.edu"})
    assert response.status_code == 200
    assert "Removed removeuser@mergington.edu from Art Club" in response.json()["message"]

def test_unregister_from_activity_not_found():
    response = client.delete("/activities/Art Club/unregister", params={"email": "notfound@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found in this activity"

def test_unregister_from_nonexistent_activity():
    response = client.delete("/activities/Nonexistent/unregister", params={"email": "someone@mergington.edu"})
    assert response.status_code == 404
    assert response.json()["detail"] == "Activity not found"
