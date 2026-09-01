from enum import Enum

class GoalType(str, Enum):
    MAINTENANCE = "maintenance"
    WEIGHT_LOSS = "weight_loss"
    WEIGHT_GAIN = "weight_gain"

def calculate_target_calories(tdee: float, goal: GoalType) -> float:
    if goal == GoalType.WEIGHT_LOSS:
        return tdee - 500.0
    elif goal == GoalType.WEIGHT_GAIN:
        return tdee + 500.0
    return tdee

def calculate_macronutrients(target_calories: float) -> dict:
    """
    Reglas de distribución de macronutrientes:
    - Proteínas: 30% del total calórico (4 kcal/g)
    - Grasas: 30% del total calórico (9 kcal/g)
    - Carbohidratos: 40% del total calórico (4 kcal/g)
    """
    protein_cals = target_calories * 0.30
    fat_cals = target_calories * 0.30
    carb_cals = target_calories * 0.40

    return {
        "protein": {
            "calories": round(protein_cals, 2),
            "grams": round(protein_cals / 4.0, 2),
            "percentage": 30.0
        },
        "fat": {
            "calories": round(fat_cals, 2),
            "grams": round(fat_cals / 9.0, 2),
            "percentage": 30.0
        },
        "carbs": {
            "calories": round(carb_cals, 2),
            "grams": round(carb_cals / 4.0, 2),
            "percentage": 40.0
        }
    }

def generate_nutrition_target(tdee: float, goal: GoalType) -> dict:
    target_calories = calculate_target_calories(tdee, goal)
    
    # Evitar objetivos calóricos peligrosamente bajos
    if target_calories < 1200:
        target_calories = 1200.0

    macros = calculate_macronutrients(target_calories)
    return {
        "goal": goal.value,
        "target_calories": round(target_calories, 2),
        "macros": macros
    }
