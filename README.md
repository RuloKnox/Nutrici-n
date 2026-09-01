# Proyecto de Nutrición

Fundación base para una futura aplicación de nutrición.

## Stack Actual
- **Backend:** Python + FastAPI
- **Base de Datos:** PostgreSQL
- **Frontend:** React (próximamente)

## Estructura
- `/backend`: Servidor de la API.
- `/frontend`: Carpeta preparada para el cliente.
- `/docs`: Documentación del proyecto.

## Requisitos Locales
- Python 3.9+
- PostgreSQL local en ejecución

## Configuración

1. Duplica el archivo `backend/.env.example` y renómbralo a `backend/.env`.
2. Actualiza los valores en `.env` con tus credenciales reales locales de PostgreSQL.

## Cómo iniciar el backend

1. Navega a la carpeta backend:
   ```bash
   cd backend
   ```
2. Activa el entorno virtual:
   ```powershell
   .\venv\Scripts\activate
   ```
3. Ejecuta el servidor:
   ```bash
   uvicorn main:app --reload
   ```

## Verificación

Con el servidor corriendo, puedes visitar:
- Raíz (API status): http://localhost:8000/
- Health Check (API + DB status): http://localhost:8000/health
