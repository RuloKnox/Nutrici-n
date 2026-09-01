from datetime import date
from typing import Optional

# Factores de actividad basados en la fórmula de Harris-Benedict / Mifflin-St Jeor
ACTIVITY_FACTORS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9
}

def calculate_age(birth_date: date) -> int:
    today = date.today()
    return today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))

def calculate_bmi(weight_kg: float, height_cm: float) -> float:
    if height_cm <= 0:
        raise ValueError("Height must be greater than 0")
    if weight_kg <= 0:
        raise ValueError("Weight must be greater than 0")
    
    height_m = height_cm / 100.0
    return weight_kg / (height_m * height_m)

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str) -> float:
    """
    Usa la ecuación de Mifflin-St Jeor.
    Hombres: (10 x peso en kg) + (6.25 × altura en cm) - (5 × edad en años) + 5
    Mujeres: (10 x peso en kg) + (6.25 × altura en cm) - (5 × edad en años) - 161
    """
    if gender not in ["M", "F"]:
        raise ValueError("Gender must be 'M' or 'F'")
    
    base_bmr = (10 * weight_kg) + (6.25 * height_cm) - (5 * age)
    
    if gender == "M":
        return base_bmr + 5
    else:
        return base_bmr - 161

def calculate_tdee(bmr: float, activity_level: str) -> float:
    if activity_level not in ACTIVITY_FACTORS:
        raise ValueError(f"Activity level must be one of {list(ACTIVITY_FACTORS.keys())}")
    
    return bmr * ACTIVITY_FACTORS[activity_level]

def calculate_nutrition_profile(patient_data: dict) -> dict:
    birth_date = patient_data.get("birth_date")
    weight_kg = patient_data.get("weight_kg")
    height_cm = patient_data.get("height_cm")
    gender = patient_data.get("gender")
    activity_level = patient_data.get("activity_level")
    
    if not all([birth_date, weight_kg, height_cm, gender, activity_level]):
        raise ValueError("Missing required fields for nutrition calculation")
        
    age = calculate_age(birth_date)
    bmi = calculate_bmi(weight_kg, height_cm)
    bmr = calculate_bmr(weight_kg, height_cm, age, gender)
    tdee = calculate_tdee(bmr, activity_level)
    
    return {
        "age": age,
        "bmi": round(bmi, 2),
        "bmr": round(bmr, 2),
        "tdee": round(tdee, 2)
    }
