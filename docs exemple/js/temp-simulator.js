/**
 * ABM-Temp-Analyser - Temperature Simulator
 * Simulateur interactif de prédiction de durée de plateau
 */

// Couleurs du thème
const simColors = {
    cold: '#00d4ff',
    coldLight: 'rgba(0, 212, 255, 0.3)',
    hot: '#ff6b35',
    hotLight: 'rgba(255, 107, 53, 0.2)',
    text: '#e8e8ec',
    textMuted: '#6b7280',
    grid: 'rgba(255, 255, 255, 0.05)'
};

let simulatorChart = null;

/**
 * Modèle de prédiction basé sur les données expérimentales
 * Durée (minutes) = 374.36 * Poids (kg) - 60.51
 */
function predictPlateauDuration(weightKg) {
    return Math.max(0, 374.36 * weightKg - 60.51);
}

/**
 * Génère les données de courbe pour le simulateur
 */
function generateSimulatedCurve(weightKg) {
    const data = [];
    const phases = [];
    const timeStep = 5; // minutes

    const startTemp = 20;
    const plateauTemp = -77;
    const endTemp = 0;

    // Durée du plateau
    const plateauDuration = predictPlateauDuration(weightKg);

    // Phase 1: Descente rapide (~30 min)
    const descentDuration = 30;
    phases.push({ start: 0, end: descentDuration, name: 'Descente', color: simColors.cold });

    for (let t = 0; t <= descentDuration; t += timeStep) {
        const progress = t / descentDuration;
        const temp = startTemp + (plateauTemp - startTemp) * Math.pow(progress, 0.6);
        data.push({ x: t, y: temp });
    }

    // Phase 2: Plateau à -77°C
    const plateauStart = descentDuration;
    const plateauEnd = plateauStart + plateauDuration;
    phases.push({ start: plateauStart, end: plateauEnd, name: 'Plateau (-77°C)', color: simColors.coldLight });

    for (let t = plateauStart; t <= plateauEnd; t += timeStep * 3) {
        // Stabilité avec micro-variations
        const noise = (Math.random() - 0.5) * 0.5;
        data.push({ x: t, y: plateauTemp + noise });
    }

    // Phase 3: Remontée (~0.24°C/min basé sur les données)
    const riseSpeed = 0.24;
    const riseDuration = (endTemp - plateauTemp) / riseSpeed;
    phases.push({ start: plateauEnd, end: plateauEnd + riseDuration, name: 'Remontée', color: simColors.hotLight });

    let currentTemp = plateauTemp;
    for (let t = plateauEnd; currentTemp < endTemp; t += timeStep) {
        currentTemp += riseSpeed * timeStep;
        data.push({ x: t, y: Math.min(currentTemp, endTemp) });
    }

    return { data, phases, plateauDuration, totalDuration: data[data.length - 1].x };
}

/**
 * Met à jour l'affichage des résultats
 */
function updateResults(weightKg) {
    const plateauMinutes = predictPlateauDuration(weightKg);
    const plateauHours = Math.floor(plateauMinutes / 60);
    const plateauMins = Math.round(plateauMinutes % 60);

    // Durée totale estimée (plateau + remontée de -77°C à 0°C)
    const riseTime = 77 / 0.24; // minutes pour remonter de -77 à 0
    const totalMinutes = plateauMinutes + riseTime + 30; // +30 pour la descente
    const totalHours = Math.round(totalMinutes / 60);

    // Mise à jour de l'affichage
    document.getElementById('weight-value').textContent = weightKg.toFixed(1);
    document.getElementById('duration-hours').textContent = plateauHours;
    document.getElementById('duration-minutes').textContent = plateauMins;
    document.getElementById('total-hours').textContent = totalHours;
}

/**
 * Met à jour le graphique du simulateur
 */
function updateSimulatorChart(weightKg) {
    const { data, plateauDuration, totalDuration } = generateSimulatedCurve(weightKg);

    if (simulatorChart) {
        simulatorChart.data.datasets[0].data = data;

        // Mise à jour des annotations
        const plateauStart = 30;
        const plateauEnd = plateauStart + plateauDuration;

        simulatorChart.options.plugins.annotation = {
            annotations: {
                plateauLine: {
                    type: 'line',
                    yMin: -77,
                    yMax: -77,
                    borderColor: simColors.cold,
                    borderWidth: 1,
                    borderDash: [5, 5],
                    label: {
                        display: true,
                        content: '-77°C (sublimation)',
                        position: 'end',
                        backgroundColor: 'transparent',
                        color: simColors.cold,
                        font: { size: 11 }
                    }
                }
            }
        };

        simulatorChart.update('none');
    }
}

/**
 * Initialise le graphique du simulateur
 */
function initSimulatorChart() {
    const ctx = document.getElementById('simulatorChart');
    if (!ctx) return;

    const initialWeight = 5;
    const { data } = generateSimulatedCurve(initialWeight);

    simulatorChart = new Chart(ctx, {
        type: 'line',
        data: {
            datasets: [{
                label: 'Température simulée',
                data: data,
                borderColor: function (context) {
                    const chart = context.chart;
                    const { ctx, chartArea } = chart;
                    if (!chartArea) return simColors.cold;

                    const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                    gradient.addColorStop(0, simColors.cold);
                    gradient.addColorStop(0.5, simColors.cold);
                    gradient.addColorStop(1, simColors.hot);
                    return gradient;
                },
                backgroundColor: function (context) {
                    const chart = context.chart;
                    const { ctx, chartArea } = chart;
                    if (!chartArea) return simColors.coldLight;

                    const gradient = ctx.createLinearGradient(0, chartArea.bottom, 0, chartArea.top);
                    gradient.addColorStop(0, 'rgba(0, 212, 255, 0.2)');
                    gradient.addColorStop(0.5, 'rgba(0, 212, 255, 0.1)');
                    gradient.addColorStop(1, 'rgba(255, 107, 53, 0.1)');
                    return gradient;
                },
                fill: true,
                tension: 0.3,
                pointRadius: 0,
                pointHoverRadius: 6,
                pointHoverBackgroundColor: simColors.cold,
                borderWidth: 3
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
                    backgroundColor: 'rgba(20, 20, 30, 0.95)',
                    titleColor: simColors.text,
                    bodyColor: simColors.text,
                    borderColor: simColors.cold,
                    borderWidth: 1,
                    padding: 12,
                    displayColors: false,
                    callbacks: {
                        title: function (context) {
                            const mins = context[0].parsed.x;
                            const hours = Math.floor(mins / 60);
                            const m = Math.round(mins % 60);
                            return `T + ${hours}h ${m}min`;
                        },
                        label: function (context) {
                            const temp = context.parsed.y;
                            let phase = 'Descente';
                            if (temp <= -75 && temp >= -79) phase = 'Plateau';
                            if (temp > -75) phase = 'Remontée';
                            return [`${temp.toFixed(1)}°C`, `Phase: ${phase}`];
                        }
                    }
                }
            },
            scales: {
                x: {
                    type: 'linear',
                    title: {
                        display: true,
                        text: 'Temps écoulé',
                        color: simColors.textMuted
                    },
                    grid: {
                        color: simColors.grid
                    },
                    ticks: {
                        callback: function (value) {
                            const hours = Math.floor(value / 60);
                            const mins = Math.round(value % 60);
                            if (hours === 0) return `${mins}m`;
                            if (mins === 0) return `${hours}h`;
                            return `${hours}h${mins}`;
                        },
                        maxTicksLimit: 10
                    },
                    min: 0
                },
                y: {
                    title: {
                        display: true,
                        text: 'Température (°C)',
                        color: simColors.textMuted
                    },
                    grid: {
                        color: simColors.grid
                    },
                    min: -90,
                    max: 30,
                    ticks: {
                        callback: function (value) {
                            return value + '°C';
                        }
                    }
                }
            },
            animation: {
                duration: 500,
                easing: 'easeOutQuart'
            }
        }
    });
}

/**
 * Initialise les contrôles du simulateur
 */
function initSimulatorControls() {
    const weightSlider = document.getElementById('weight-slider');
    if (!weightSlider) return;

    // Mise à jour en temps réel
    weightSlider.addEventListener('input', function () {
        const weight = parseFloat(this.value);
        updateResults(weight);
        updateSimulatorChart(weight);
    });

    // Initialisation avec la valeur par défaut
    updateResults(parseFloat(weightSlider.value));
}

// Initialisation au chargement
document.addEventListener('DOMContentLoaded', function () {
    initSimulatorChart();
    initSimulatorControls();
});
