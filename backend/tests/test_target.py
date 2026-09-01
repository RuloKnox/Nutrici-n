from target_calculator import calculate_target_calories, calculate_macronutrients, generate_nutrition_target, GoalType
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_calculate_target_calories():
    tdee = 2000.0
    assert calculate_target_calories(tdee, GoalType.MAINTENANCE) == 2000.0
    assert calculate_target_calories(tdee, GoalType.WEIGHT_LOSS) == 1500.0
    assert calculate_target_calories(tdee, GoalType.WEIGHT_GAIN) == 2500.0

def test_calculate_macronutrients():
    # Para 2000 kcal
    # protein: 30% = 600 kcal = 150g
    # fat: 30% = 600 kcal = 66.67g
    # carbs: 40% = 800 kcal = 200g
    macros = calculate_macronutrients(2000.0)
    assert macros["protein"]["calories"] == 600.0
    assert macros["protein"]["grams"] == 150.0
    assert macros["protein"]["percentage"] == 30.0
    
    assert macros["fat"]["calories"] == 600.0
    assert round(macros["fat"]["grams"], 1) == 66.7
    
    assert macros["carbs"]["calories"] == 800.0
    assert macros["carbs"]["grams"] == 200.0

    total_cals = macros["protein"]["calories"] + macros["fat"]["calories"] + macros["carbs"]["calories"]
    assert total_cals == 2000.0

def test_minimum_calories_safety():
    # Un TDEE muy bajo
    target = generate_nutrition_target(1500.0, GoalType.WEIGHT_LOSS)
    # Deberia ser 1000 pero el limite es 1200
    assert target["target_calories"] == 1200.0

def test_api_nutrition_target():
    # Create patient
    create_resp = client.post(
        "/patients/",
        json={
            "name": "Target Patient",
            "birth_date": "1990-01-01",
            "gender": "F",
            "height_cm": 160,
            "weight_kg": 60,
            "activity_level": "sedentary"
        }
    )
    assert create_resp.status_code == 201
    patient_id = create_resp.json()["id"]

    # Test maintenance
    resp = client.get(f"/patients/{patient_id}/nutrition-target?goal=maintenance")
    assert resp.status_code == 200
    data = resp.json()
    assert data["goal"] == "maintenance"
    assert "target_calories" in data
    assert "macros" in data
    assert "protein" in data["macros"]

    # Test weight loss
    resp_loss = client.get(f"/patients/{patient_id}/nutrition-target?goal=weight_loss")
    assert resp_loss.status_code == 200
    assert resp_loss.json()["target_calories"] < data["target_calories"]

def test_api_nutrition_target_invalid_goal():
    create_resp = client.post("/patients/", json={"name": "Goal Patient", "birth_date": "1990-01-01", "gender": "F", "height_cm": 160, "weight_kg": 60, "activity_level": "sedentary"})
    patient_id = create_resp.json()["id"]
    resp = client.get(f"/patients/{patient_id}/nutrition-target?goal=invalid_goal")
    assert resp.status_code == 422 # Validation error from FastAPI enum
