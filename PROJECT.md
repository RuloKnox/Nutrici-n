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

## Motor Nutricional Base
- **Fórmula BMR**: Mifflin-St Jeor (diferente para hombre y mujer).
- **Cálculo de TDEE**: BMR * Factor de actividad.
- **Unidades**: Peso en kg, Altura en cm, Edad en años.
- **Factores de actividad**: Sedentario (1.2), Ligero (1.375), Moderado (1.55), Activo (1.725), Muy activo (1.9).
- **Objetivos Calóricos**: Mantenimiento (TDEE), Pérdida de peso (TDEE - 500 kcal), Ganancia de peso (TDEE + 500 kcal). Se aplica un límite mínimo de seguridad de 1200 kcal.
- **Macronutrientes**:
  - Proteínas: 30% del objetivo calórico (4 kcal/g)
  - Grasas: 30% del objetivo calórico (9 kcal/g)
  - Carbohidratos: 40% del objetivo calórico (4 kcal/g)
- **Generador de Dieta Mínimo**:
  - Catálogo de alimentos en memoria (hardcoded) para la primera iteración.
  - Estructura: 3 comidas (Desayuno, Comida, Cena).
  - Estrategia: Asignación lineal determinista. Reparte los macros objetivo equitativamente entre las comidas y asigna alimentos puros de forma algorítmica para intentar cuadrar.
- **Limitaciones Actuales**: El cálculo se hace bajo demanda (on-the-fly) sin persistencia en base de datos. No incluye ajustes por objetivos, macros, patologías médicas o catálogo completo de alimentos.
