from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_read_root():
    response = client.get("/")
    assert response.status_code == 200
    assert response.json()["status"] == "API functioning"

def test_create_patient():
    response = client.post(
        "/patients/",
        json={
            "name": "Test Patient",
            "birth_date": "1990-01-01",
            "gender": "M",
            "height_cm": 175.5,
            "weight_kg": 70.2,
            "activity_level": "moderate"
        }
    )
    assert response.status_code == 201, response.text
    data = response.json()
    assert data["name"] == "Test Patient"
    assert "id" in data

def test_get_patients():
    response = client.get("/patients/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0

def test_get_patient_by_id():
    create_resp = client.post("/patients/", json={"name": "Another Patient"})
    patient_id = create_resp.json()["id"]
    
    response = client.get(f"/patients/{patient_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Another Patient"
