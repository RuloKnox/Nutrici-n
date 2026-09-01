from datetime import date
from nutrition_engine import calculate_age, calculate_bmi, calculate_bmr, calculate_tdee, calculate_nutrition_profile
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_calculate_age():
    today = date.today()
    birth_date = date(today.year - 30, today.month, today.day)
    assert calculate_age(birth_date) == 30

def test_calculate_bmi():
    bmi = calculate_bmi(70, 175)
    assert round(bmi, 2) == 22.86

def test_calculate_bmr():
    # Hombre
    assert calculate_bmr(70, 175, 30, "M") == 1648.75
    # Mujer
    assert calculate_bmr(60, 160, 30, "F") == 1289.0

def test_calculate_tdee():
    assert calculate_tdee(1000, "sedentary") == 1200.0
    assert calculate_tdee(1000, "moderate") == 1550.0

def test_invalid_data():
    with pytest.raises(ValueError):
        calculate_bmi(-10, 175)
    with pytest.raises(ValueError):
        calculate_bmr(70, 175, 30, "X")
    with pytest.raises(ValueError):
        calculate_tdee(1000, "invalid")

def test_api_nutrition_endpoint():
    create_resp = client.post(
        "/patients/",
        json={
            "name": "Nutri Patient",
            "birth_date": "1990-01-01",
            "gender": "M",
            "height_cm": 180,
            "weight_kg": 80,
            "activity_level": "moderate"
        }
    )
    assert create_resp.status_code == 201
    patient_id = create_resp.json()["id"]
    
    resp = client.get(f"/patients/{patient_id}/nutrition")
    assert resp.status_code == 200
    data = resp.json()
    assert "age" in data
    assert "bmi" in data
    assert "bmr" in data
    assert "tdee" in data

def test_api_nutrition_missing_data():
    create_resp = client.post(
        "/patients/",
        json={"name": "Missing Data Patient"}
    )
    patient_id = create_resp.json()["id"]
    
    resp = client.get(f"/patients/{patient_id}/nutrition")
    assert resp.status_code == 400
    assert "Missing required fields" in resp.json()["detail"]

def test_api_nutrition_not_found():
    resp = client.get("/patients/9999/nutrition")
    assert resp.status_code == 404
