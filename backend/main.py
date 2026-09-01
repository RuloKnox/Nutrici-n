import os
from fastapi import FastAPI
from dotenv import load_dotenv
import psycopg2
from psycopg2 import OperationalError

load_dotenv()

app = FastAPI(title="Nutrición API")

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            dbname=os.getenv("DB_NAME", "postgres")
        )
        return conn
    except OperationalError as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

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
