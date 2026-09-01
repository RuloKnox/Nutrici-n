import React, { useState, useEffect } from 'react';
import axios from 'axios';
import './PlanNutricional.css';

const PlanNutricional = () => {
    const [planData, setPlanData] = useState(null);
    const [loading, setLoading] = useState(true);
    const [error, setError] = useState(null);
    const [selectedDay, setSelectedDay] = useState(1);
    
    const patientId = 1; 
    const goal = "weight_loss";

    useEffect(() => {
        const fetchPlan = async () => {
            try {
                // Hacemos el ping para ver si el paciente existe, sino mostrar mensaje amigable.
                // En un app real, primero aseguramos que existe. Por ahora, fetch directo.
                const response = await axios.get(`http://localhost:8000/patients/${patientId}/diet-plan?goal=${goal}`);
                setPlanData(response.data);
                setLoading(false);
            } catch (err) {
                console.error(err);
                if (err.response && err.response.status === 404) {
                    setError("Paciente no encontrado. Por favor, crea primero un paciente en el backend usando Swagger (http://localhost:8000/docs).");
                } else {
                    setError("Error cargando el plan. Asegúrate de que el backend de FastAPI esté corriendo en http://localhost:8000.");
                }
                setLoading(false);
            }
        };
        fetchPlan();
    }, [patientId, goal]);

    if (loading) return <div className="loading">Cargando Plan Nutricional de 14 Días...</div>;
    if (error) return <div className="error">{error}</div>;
    if (!planData) return null;

    const currentDayData = planData.days.find(d => d.day === selectedDay);

    return (
        <div className="plan-container">
            <header className="plan-header">
                <h1>PLAN NUTRICIONAL</h1>
                <h2>Paciente #{planData.patient_id}</h2>
                <div className="target-info">
                    <p><strong>Objetivo:</strong> {planData.target.goal === 'weight_loss' ? 'Perder peso' : planData.target.goal === 'weight_gain' ? 'Ganar peso' : 'Mantener'}</p>
                    <p><strong>Calorías objetivo:</strong> {planData.target.target_calories} kcal</p>
                    <p>
                        <strong>Proteínas:</strong> {planData.target.macros.protein.grams} g | 
                        <strong> Carbohidratos:</strong> {planData.target.macros.carbs.grams} g | 
                        <strong> Grasas:</strong> {planData.target.macros.fat.grams} g
                    </p>
                </div>
            </header>

            <div className="days-nav">
                {planData.days.map(d => (
                    <button 
                        key={d.day} 
                        className={selectedDay === d.day ? 'active' : ''}
                        onClick={() => setSelectedDay(d.day)}
                    >
                        Día {d.day}
                    </button>
                ))}
            </div>

            {currentDayData && (
                <div className="day-content">
                    <h3>DÍA {currentDayData.day}</h3>
                    
                    <div className="meals-container">
                        {currentDayData.meals.map((meal, idx) => (
                            <div key={idx} className="meal-card">
                                <h4>{meal.name.toUpperCase()}</h4>
                                <ul>
                                    {meal.foods.map((food, fIdx) => (
                                        <li key={fIdx}>
                                            <span className="food-name">- {food.name}</span>
                                            <span className="food-amount">{food.amount_g}g</span>
                                            <span className="food-macros">({food.calories} kcal | P: {food.protein}g C: {food.carbs}g G: {food.fat}g)</span>
                                        </li>
                                    ))}
                                </ul>
                                <div className="meal-totals">
                                    Subtotal: {meal.total_calories} kcal (P: {meal.total_protein}g C: {meal.total_carbs}g G: {meal.total_fat}g)
                                </div>
                            </div>
                        ))}
                    </div>

                    <div className="daily-totals">
                        <h4>TOTAL DEL DÍA</h4>
                        <div className="totals-grid">
                            <div className="total-item">
                                <span className="value">{currentDayData.totals.calories}</span>
                                <span className="label">kcal</span>
                            </div>
                            <div className="total-item">
                                <span className="value">{currentDayData.totals.protein}</span>
                                <span className="label">g proteína</span>
                            </div>
                            <div className="total-item">
                                <span className="value">{currentDayData.totals.carbs}</span>
                                <span className="label">g carbohidratos</span>
                            </div>
                            <div className="total-item">
                                <span className="value">{currentDayData.totals.fat}</span>
                                <span className="label">g grasa</span>
                            </div>
                        </div>
                    </div>
                </div>
            )}
        </div>
    );
};

export default PlanNutricional;
