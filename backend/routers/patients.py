from fastapi import APIRouter, HTTPException, status
from typing import List
from schemas import PatientCreate, PatientResponse, NutritionResponse
from database import get_db_connection
from nutrition_engine import calculate_nutrition_profile

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
