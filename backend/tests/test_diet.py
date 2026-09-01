from diet_generator import generate_daily_diet, create_meal
from target_calculator import generate_nutrition_target, GoalType
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_meal():
    meal = create_meal("Test", 30, 40, 15, "chicken_breast", "rice_cooked", "olive_oil")
    assert meal["name"] == "Test"
    assert len(meal["foods"]) > 0
    # The naive allocation should be very close to the targets
    assert abs(meal["total_protein"] - 30) < 5
    assert abs(meal["total_carbs"] - 40) < 5
    assert abs(meal["total_fat"] - 15) < 5

def test_generate_daily_diet():
    target = generate_nutrition_target(2000, GoalType.MAINTENANCE)
    diet = generate_daily_diet(target)
    
    assert len(diet["meals"]) == 3
    assert diet["totals"]["calories"] > 0
    # Diff should be calculated correctly, though naive algo might have larger deviations due to trace macros
    assert "protein" in diet["diff"]
    assert "carbs" in diet["diff"]
    assert "fat" in diet["diff"]
    assert abs(diet["diff"]["protein"]) < 50
    assert abs(diet["diff"]["carbs"]) < 50
    assert abs(diet["diff"]["fat"]) < 50

def test_api_diet_endpoint():
    create_resp = client.post(
        "/patients/",
        json={
            "name": "Diet Patient",
            "birth_date": "1990-01-01",
            "gender": "M",
            "height_cm": 180,
            "weight_kg": 80,
            "activity_level": "moderate"
        }
    )
    patient_id = create_resp.json()["id"]
    
    resp = client.get(f"/patients/{patient_id}/diet?goal=weight_loss")
    assert resp.status_code == 200
    data = resp.json()
    
    assert "target" in data
    assert "meals" in data
    assert "totals" in data
    assert "diff" in data
    assert len(data["meals"]) == 3
    
    # Verificamos que contenga alimentos
    assert len(data["meals"][0]["foods"]) > 0
