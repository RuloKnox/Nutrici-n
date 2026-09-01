from catalog import FOOD_CATALOG
from typing import Dict, Any

def create_meal(name: str, target_p: float, target_c: float, target_f: float, p_food_id: str, c_food_id: str, f_food_id: str) -> dict:
    p_food = FOOD_CATALOG[p_food_id]
    c_food = FOOD_CATALOG[c_food_id]
    f_food = FOOD_CATALOG[f_food_id]
    
    # 1. Calcular cantidad de fuente de proteína
    amount_p = (target_p / p_food.protein) * 100 if p_food.protein > 0 else 0
    
    # 2. Calcular carbohidratos restantes y cantidad de fuente de carbohidratos
    c_from_p = (amount_p / 100) * p_food.carbs
    remaining_c = max(0, target_c - c_from_p)
    amount_c = (remaining_c / c_food.carbs) * 100 if c_food.carbs > 0 else 0
    
    # 3. Calcular grasas restantes y cantidad de fuente de grasas
    f_from_p = (amount_p / 100) * p_food.fat
    f_from_c = (amount_c / 100) * c_food.fat
    remaining_f = max(0, target_f - f_from_p - f_from_c)
    amount_f = (remaining_f / f_food.fat) * 100 if f_food.fat > 0 else 0
    
    foods = []
    for food, amount in [(p_food, amount_p), (c_food, amount_c), (f_food, amount_f)]:
        if amount > 0:
            foods.append({
                "name": food.name,
                "amount_g": round(amount, 1),
                "calories": round((amount / 100) * food.calories, 1),
                "protein": round((amount / 100) * food.protein, 1),
                "carbs": round((amount / 100) * food.carbs, 1),
                "fat": round((amount / 100) * food.fat, 1)
            })
            
    meal_cals = sum(f["calories"] for f in foods)
    meal_p = sum(f["protein"] for f in foods)
    meal_c = sum(f["carbs"] for f in foods)
    meal_f = sum(f["fat"] for f in foods)
    
    return {
        "name": name,
        "foods": foods,
        "total_calories": round(meal_cals, 1),
        "total_protein": round(meal_p, 1),
        "total_carbs": round(meal_c, 1),
        "total_fat": round(meal_f, 1)
    }

def generate_daily_diet(target_data: dict, day_index: int = 1) -> dict:
    macros = target_data["macros"]
    target_p = macros["protein"]["grams"]
    target_c = macros["carbs"]["grams"]
    target_f = macros["fat"]["grams"]
    
    # Dividir en 3 comidas iguales
    meal_p = target_p / 3
    meal_c = target_c / 3
    meal_f = target_f / 3
    
    # Rotación simple para variedad
    if day_index % 3 == 0:
        breakfast = create_meal("Desayuno", meal_p, meal_c, meal_f, "egg_whites", "potato", "avocado")
        lunch = create_meal("Comida", meal_p, meal_c, meal_f, "fish", "rice_cooked", "olive_oil")
        dinner = create_meal("Cena", meal_p, meal_c, meal_f, "chicken_breast", "oats", "almonds")
    elif day_index % 2 == 0:
        breakfast = create_meal("Desayuno", meal_p, meal_c, meal_f, "egg_whites", "oats", "almonds")
        lunch = create_meal("Comida", meal_p, meal_c, meal_f, "fish", "potato", "olive_oil")
        dinner = create_meal("Cena", meal_p, meal_c, meal_f, "chicken_breast", "rice_cooked", "avocado")
    else:
        breakfast = create_meal("Desayuno", meal_p, meal_c, meal_f, "egg_whites", "oats", "almonds")
        lunch = create_meal("Comida", meal_p, meal_c, meal_f, "chicken_breast", "rice_cooked", "olive_oil")
        dinner = create_meal("Cena", meal_p, meal_c, meal_f, "fish", "potato", "avocado")
    
    meals = [breakfast, lunch, dinner]
    
    total_cals = sum(m["total_calories"] for m in meals)
    total_p = sum(m["total_protein"] for m in meals)
    total_c = sum(m["total_carbs"] for m in meals)
    total_f = sum(m["total_fat"] for m in meals)
    
    diff_cals = total_cals - target_data["target_calories"]
    diff_p = total_p - target_p
    diff_c = total_c - target_c
    diff_f = total_f - target_f
    
    return {
        "target": target_data,
        "meals": meals,
        "totals": {
            "calories": round(total_cals, 1),
            "protein": round(total_p, 1),
            "carbs": round(total_c, 1),
            "fat": round(total_f, 1)
        },
        "diff": {
            "calories": round(diff_cals, 1),
            "protein": round(diff_p, 1),
            "carbs": round(diff_c, 1),
            "fat": round(diff_f, 1)
        }
    }

def generate_14_day_plan(patient_id: int, target_data: dict) -> dict:
    days = []
    for day_index in range(1, 15):
        daily = generate_daily_diet(target_data, day_index)
        daily["day"] = day_index
        days.append(daily)
        
    return {
        "patient_id": patient_id,
        "target": target_data,
        "days": days
    }
