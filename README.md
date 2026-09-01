# Proyecto de Nutrición

Base técnica del proyecto de una aplicación de nutrición.

## Requisitos previos

- Python 3.9+
- PostgreSQL
- Node.js (para el frontend futuro)

## Configuración y ejecución local

### 1. Base de datos (PostgreSQL)
Asegúrate de tener PostgreSQL instalado y en ejecución en tu máquina local.
Puedes configurar las credenciales en el archivo `backend/.env` (basado en `backend/.env.example`).

### 2. Backend (FastAPI)

1. Navega al directorio backend:
   ```bash
   cd backend
   ```
2. Crea y activa un entorno virtual (opcional pero recomendado):
   ```bash
   python -m venv venv
   # En Windows:
   venv\Scripts\activate
   # En macOS/Linux:
   source venv/bin/activate
   ```
3. Instala las dependencias:
   ```bash
   pip install -r requirements.txt
   ```
4. Ejecuta el servidor de desarrollo:
   ```bash
   uvicorn main:app --reload
   ```
5. Verifica que funciona visitando `http://localhost:8000` en tu navegador.
