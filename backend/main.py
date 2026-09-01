import os
from fastapi import FastAPI
from dotenv import load_dotenv

from database import get_db_connection, init_db
from routers import patients

load_dotenv()

# Inicializar BD
init_db()

app = FastAPI(title="Nutrición API")

app.include_router(patients.router)



@app.get("/")
def read_root():
    return {"message": "Hello World", "status": "API functioning"}

@app.get("/health")
def health_check():
    conn = get_db_connection()
    if conn:
        conn.close()
        return {"api": "ok", "database": "connected"}
    else:
        return {"api": "ok", "database": "disconnected"}
