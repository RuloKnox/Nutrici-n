import os
import psycopg2
from psycopg2 import OperationalError
from psycopg2.extras import RealDictCursor

def get_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=os.getenv("DB_PORT", "5432"),
            user=os.getenv("DB_USER", "postgres"),
            password=os.getenv("DB_PASSWORD", "postgres"),
            dbname=os.getenv("DB_NAME", "postgres"),
            cursor_factory=RealDictCursor
        )
        return conn
    except OperationalError as e:
        print(f"Error conectando a la base de datos: {e}")
        return None

def init_db():
    conn = get_db_connection()
    if conn:
        try:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS patients (
                        id SERIAL PRIMARY KEY,
                        name VARCHAR(255) NOT NULL,
                        birth_date DATE,
                        gender VARCHAR(50),
                        height_cm REAL,
                        weight_kg REAL,
                        activity_level VARCHAR(50)
                    )
                """)
            conn.commit()
        except Exception as e:
            print(f"Error inicializando la base de datos: {e}")
        finally:
            conn.close()
