# Memoria del Proyecto - Nutrición

## Propósito
Aplicación de nutrición con módulos futuros para nutriólogos (cálculo dietético, expedientes) y pacientes (tracker, chatbot, supermercado).

## Stack
- **Backend:** Python + FastAPI
- **Base de Datos:** PostgreSQL
- **Frontend:** React (preparado para web/móvil)

## Estructura Principal
- `/backend`: API REST con FastAPI.
- `/frontend`: Aplicación cliente (por inicializar).
- `/docs`: Documentación técnica y reglas.

## Comandos de Desarrollo
Backend:
- Activar entorno: `.\backend\venv\Scripts\activate` (Windows)
- Iniciar servidor: `uvicorn main:app --reload` (desde la carpeta `backend`)

## Convenciones y Límites Actuales
- Arquitectura simple, evitando microservicios y capas abstractas prematuras.
- Conexión a base de datos validada mediante endpoint `/health`.
- No hay modelos de dominio, autenticación ni lógica clínica implementada todavía.
- Las variables de entorno (.env) no deben subirse a Git.

## Reglas de Git
- Commits pequeños, descriptivos y centrados en la iteración actual.
- No incluir secretos reales en el historial.
