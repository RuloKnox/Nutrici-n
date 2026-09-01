class Food:
    def __init__(self, id: str, name: str, calories: float, protein: float, carbs: float, fat: float):
        self.id = id
        self.name = name
        self.calories = calories
        self.protein = protein
        self.carbs = carbs
        self.fat = fat

# Valores por 100g
FOOD_CATALOG = {
    "chicken_breast": Food("chicken_breast", "Pechuga de Pollo", 165, 31.0, 0.0, 3.6),
    "rice_cooked": Food("rice_cooked", "Arroz Blanco Cocido", 130, 2.7, 28.0, 0.3),
    "olive_oil": Food("olive_oil", "Aceite de Oliva", 884, 0.0, 0.0, 100.0),
    "egg_whites": Food("egg_whites", "Claras de Huevo", 52, 11.0, 0.7, 0.2),
    "oats": Food("oats", "Avena", 389, 17.0, 66.0, 7.0),
    "almonds": Food("almonds", "Almendras", 579, 21.0, 22.0, 50.0),
    "fish": Food("fish", "Pescado Blanco", 90, 20.0, 0.0, 1.0),
    "potato": Food("potato", "Papa Cocida", 87, 1.9, 20.0, 0.1),
    "avocado": Food("avocado", "Aguacate", 160, 2.0, 8.5, 14.7)
}
