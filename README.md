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

## Verificación y Ejecución Local

Para ejecutar el sistema completo en local, necesitas abrir dos terminales:

### 1. Iniciar Backend (FastAPI)
```bash
cd backend
.\venv\Scripts\python -m uvicorn main:app --reload
```
- **API URL:** http://localhost:8000
- **Swagger Docs:** http://localhost:8000/docs
*(Nota: Para probar el frontend, primero debes crear al menos un paciente usando el endpoint POST `/patients/` en Swagger).*

### 2. Iniciar Frontend (React)
```bash
cd frontend
npm run dev
```
- **Frontend URL:** http://localhost:5173
- Aquí podrás visualizar el plan de 14 días.

## Pruebas Backend

Para ejecutar las pruebas automatizadas del backend:
```bash
cd backend
.\venv\Scripts\pytest
```
