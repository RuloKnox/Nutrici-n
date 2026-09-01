from pydantic import BaseModel
from typing import Optional
from datetime import date
from enum import Enum
from datetime import date

class PatientBase(BaseModel):
    name: str
    birth_date: Optional[date] = None
    gender: Optional[str] = None
    height_cm: Optional[float] = None
    weight_kg: Optional[float] = None
    activity_level: Optional[str] = None

class PatientCreate(PatientBase):
    pass

class PatientResponse(PatientBase):
    id: int

class NutritionResponse(BaseModel):
    age: int
    bmi: float
    bmr: float
    tdee: float

class MacroDetail(BaseModel):
    calories: float
    grams: float
    percentage: float

class Macros(BaseModel):
    protein: MacroDetail
    fat: MacroDetail
    carbs: MacroDetail

class GoalTypeSchema(str, Enum):
    MAINTENANCE = "maintenance"
    WEIGHT_LOSS = "weight_loss"
    WEIGHT_GAIN = "weight_gain"

class TargetResponse(BaseModel):
    goal: GoalTypeSchema
    target_calories: float
    macros: Macros

class FoodSchema(BaseModel):
    name: str
    amount_g: float
    calories: float
    protein: float
    carbs: float
    fat: float

class MealSchema(BaseModel):
    name: str
    foods: list[FoodSchema]
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fat: float

class DietTotals(BaseModel):
    calories: float
    protein: float
    carbs: float
    fat: float

class DailyDietResponse(BaseModel):
    target: TargetResponse
    meals: list[MealSchema]
    totals: DietTotals
    diff: DietTotals
