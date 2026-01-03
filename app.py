import time

import scipy.stats
import streamlit as st

st.header('Lanzar una moneda')

# Inicializamos el gráfico con 0.5 (valor esperado de una moneda justa)
chart = st.line_chart([0.5])

def toss_coin(n: int) -> float:
    """Emula n lanzamientos de moneda (Bernoulli p=0.5) y grafica la media acumulada."""
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    outcome_no = 0
    outcome_1_count = 0
    mean = 0.0

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no
        chart.add_rows([mean])
        time.sleep(0.05)  # solo para que se vea el progreso

    return mean

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')
    mean = toss_coin(number_of_trials)
    st.write(f'Resultado final (media): {mean:.4f}')
