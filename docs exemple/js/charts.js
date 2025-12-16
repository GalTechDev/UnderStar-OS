/**
 * ABM-Temp-Analyser - Chart.js Visualizations
 * Graphiques interactifs pour l'analyse de température
 */

// Couleurs du thème
const colors = {
    cold: '#00d4ff',
    coldLight: 'rgba(0, 212, 255, 0.2)',
    hot: '#ff6b35',
    hotLight: 'rgba(255, 107, 53, 0.2)',
    purple: '#8b5cf6',
    purpleLight: 'rgba(139, 92, 246, 0.2)',
    green: '#10b981',
    greenLight: 'rgba(16, 185, 129, 0.2)',
    text: '#e8e8ec',
    textMuted: '#6b7280',
    grid: 'rgba(255, 255, 255, 0.05)'
};

// Configuration globale Chart.js
Chart.defaults.color = colors.textMuted;
Chart.defaults.borderColor = colors.grid;
Chart.defaults.font.family = "'Inter', sans-serif";

/**
 * Génère une courbe de température simulée
 */
function generateTempCurve(gcWeight, startTemp = 20, plateauTemp = -77) {
    const data = [];
    const timeStep = 10; // minutes
    
    // Durée du plateau basée sur le modèle linéaire
    const plateauDuration = 374.36 * gcWeight - 60.51;
    
    // Phase 1: Descente (environ 30 minutes)
    const descentTime = 30;
    for (let t = 0; t <= descentTime; t += timeStep) {
        const progress = t / descentTime;
        const temp = startTemp + (plateauTemp - startTemp) * Math.pow(progress, 0.5);
        data.push({ x: t, y: temp });
    }
    
    // Phase 2: Plateau
    const plateauStart = descentTime;
    const plateauEnd = plateauStart + plateauDuration;
    for (let t = plateauStart; t <= plateauEnd; t += timeStep * 5) {
        // Légères variations autour de -77°C
        const noise = (Math.random() - 0.5) * 1;
        data.push({ x: t, y: plateauTemp + noise });
    }
    
    // Phase 3: Remontée (vitesse ~0.24°C/min)
    const riseSpeed = 0.24;
    const targetTemp = 0;
    let currentTemp = plateauTemp;
    let t = plateauEnd;
    
    while (currentTemp < targetTemp) {
        currentTemp += riseSpeed * timeStep;
        t += timeStep;
        data.push({ x: t, y: Math.min(currentTemp, targetTemp) });
    }
    
    return data;
}

/**
 * Graphique de la courbe de température type
 */
function initCurveChart() {
    const ctx = document.getElementById('curveChart');
    if (!ctx) return;
    
    // Générer des données pour 10kg de GC
    const data10kg = generateTempCurve(10);
    
    new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Température (°C)',
                data: data10kg,
                borderColor: colors.cold,
                backgroundColor: colors.coldLight,
                fill: true,
                tension: 0.4,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: colors.cold,
                borderWidth: 2
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'index'
            },
            plugins: {
                legend: {
                    display: false
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 20, 30, 0.9)',
                    titleColor: colors.text,
                    bodyColor: colors.text,
                    borderColor: colors.cold,
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.y.toFixed(1)}°C`;
                        },
                        title: function(context) {
                            const hours = Math.floor(context[0].parsed.x / 60);
                            const mins = Math.round(context[0].parsed.x % 60);
                            return `T + ${hours}h ${mins}min`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Temps (minutes)',
                        color: colors.textMuted
                    },
                    grid: {
                        color: colors.grid
                    },
                    ticks: {
                        callback: function(value) {
                            const hours = Math.floor(value / 60);
                            return hours > 0 ? `${hours}h` : '0';
                        }
                    }
                },
                y: {
                    title: {
                        display: true,
                        text: 'Température (°C)',
                        color: colors.textMuted
                    },
                    grid: {
                        color: colors.grid
                    },
                    min: -90,
                    max: 30
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            }
        }
    });
}

/**
 * Graphique de régression (Poids vs Durée)
 */
function initRegressionChart() {
    const ctx = document.getElementById('regressionChart');
    if (!ctx) return;
    
    // Données expérimentales
    const experimentalData = [
        { x: 6.1, y: 2220 / 60 },  // 6.1kg -> 37h
        { x: 10, y: 3681 / 60 }   // 10kg -> 61.35h
    ];
    
    // Points de la régression linéaire
    const regressionLine = [];
    for (let weight = 1; weight <= 15; weight += 0.5) {
        const duration = (374.36 * weight - 60.51) / 60; // en heures
        regressionLine.push({ x: weight, y: duration });
    }
    
    new Chart(ctx, {
        type: 'scatter',
        data: {
            datasets: [
                {
                    label: 'Données expérimentales',
                    data: experimentalData,
                    backgroundColor: colors.hot,
                    borderColor: colors.hot,
                    pointRadius: 10,
                    pointHoverRadius: 12
                },
                {
                    label: 'Modèle linéaire (R² = 0.99)',
                    data: regressionLine,
                    type: 'line',
                    borderColor: colors.cold,
                    backgroundColor: 'transparent',
                    borderWidth: 2,
                    borderDash: [5, 5],
                    pointRadius: 0,
                    tension: 0
                }
            ]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            interaction: {
                intersect: false,
                mode: 'nearest'
            },
            plugins: {
                legend: {
                    position: 'top',
                    labels: {
                        usePointStyle: true,
                        padding: 20
                    }
                },
                tooltip: {
                    backgroundColor: 'rgba(20, 20, 30, 0.9)',
                    titleColor: colors.text,
                    bodyColor: colors.text,
                    borderColor: colors.cold,
                    borderWidth: 1,
                    padding: 12,
                    callbacks: {
                        label: function(context) {
                            return `${context.parsed.x} kg → ${context.parsed.y.toFixed(1)} heures`;
                        }
                    }
                }
            },
            scales: {
                x: {
                    title: {
                        display: true,
                        text: 'Poids de Glace Carbonique (kg)',
                        color: colors.textMuted
                    },
                    grid: {
                        color: colors.grid
                    },
                    min: 0,
                    max: 15
                },
                y: {
                    title: {
                        display: true,
                        text: 'Durée du Plateau (heures)',
                        color: colors.textMuted
                    },
                    grid: {
                        color: colors.grid
                    },
                    min: 0
                }
            },
            animation: {
                duration: 1500,
                easing: 'easeOutQuart'
            }
        }
    });
}

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', function() {
    initCurveChart();
    initRegressionChart();
});
