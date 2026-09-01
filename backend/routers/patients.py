from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import PatientCreate, PatientResponse, NutritionResponse, TargetResponse, DailyDietResponse, DietPlanResponse
from database import get_db_connection
from target_calculator import generate_nutrition_target, GoalType
from nutrition_engine import calculate_nutrition_profile
from diet_generator import generate_daily_diet, generate_14_day_plan

router = APIRouter(prefix="/patients", tags=["patients"])

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
def create_patient(patient: PatientCreate):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cur:
            cur.execute("""
                INSERT INTO patients (name, birth_date, gender, height_cm, weight_kg, activity_level)
                VALUES (%s, %s, %s, %s, %s, %s)
                RETURNING *
            """, (
                patient.name, 
                patient.birth_date, 
                patient.gender, 
                patient.height_cm, 
                patient.weight_kg, 
                patient.activity_level
            ))
            new_patient = cur.fetchone()
            conn.commit()
            return new_patient
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        conn.close()

@router.get("/", response_model=List[PatientResponse])
def get_patients():
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM patients ORDER BY id ASC")
            patients = cur.fetchall()
            return patients
    finally:
        conn.close()

@router.get("/{patient_id}", response_model=PatientResponse)
def get_patient(patient_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient = cur.fetchone()
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
            return patient
    finally:
        conn.close()

@router.get("/{patient_id}/nutrition", response_model=NutritionResponse)
def get_patient_nutrition(patient_id: int):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient = cur.fetchone()
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
                
        try:
            nutrition_data = calculate_nutrition_profile(patient)
            return nutrition_data
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
    finally:
        conn.close()

@router.get("/{patient_id}/nutrition-target", response_model=TargetResponse)
def get_patient_nutrition_target(patient_id: int, goal: GoalType = GoalType.MAINTENANCE):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient = cur.fetchone()
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
                
        try:
            nutrition_data = calculate_nutrition_profile(patient)
            tdee = nutrition_data["tdee"]
            target_data = generate_nutrition_target(tdee, goal)
            return target_data
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
    finally:
        conn.close()

@router.get("/{patient_id}/diet", response_model=DailyDietResponse)
def get_patient_diet(patient_id: int, goal: GoalType = GoalType.MAINTENANCE):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient = cur.fetchone()
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
                
        try:
            nutrition_data = calculate_nutrition_profile(patient)
            tdee = nutrition_data["tdee"]
            target_data = generate_nutrition_target(tdee, goal)
            diet_data = generate_daily_diet(target_data)
            return diet_data
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
    finally:
        conn.close()

@router.get("/{patient_id}/diet-plan", response_model=DietPlanResponse)
def get_patient_diet_plan(patient_id: int, goal: GoalType = GoalType.MAINTENANCE):
    conn = get_db_connection()
    if not conn:
        raise HTTPException(status_code=500, detail="Database connection failed")
    
    try:
        with conn.cursor() as cur:
            cur.execute("SELECT * FROM patients WHERE id = %s", (patient_id,))
            patient = cur.fetchone()
            if not patient:
                raise HTTPException(status_code=404, detail="Patient not found")
                
        try:
            nutrition_data = calculate_nutrition_profile(patient)
            tdee = nutrition_data["tdee"]
            target_data = generate_nutrition_target(tdee, goal)
            plan_data = generate_14_day_plan(patient_id, target_data)
            return plan_data
        except ValueError as ve:
            raise HTTPException(status_code=400, detail=str(ve))
    finally:
        conn.close()
