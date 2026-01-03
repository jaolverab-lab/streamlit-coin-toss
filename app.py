import time

import pandas as pd
import scipy.stats
import streamlit as st

st.header('Lanzar una moneda')

# Estado de la sesión
if 'experiment_no' not in st.session_state:
    st.session_state['experiment_no'] = 0

if 'df_experiment_results' not in st.session_state:
    st.session_state['df_experiment_results'] = pd.DataFrame(
        {
            'no': pd.Series(dtype='int'),
            'iteraciones': pd.Series(dtype='int'),
            'media': pd.Series(dtype='float'),
        }
    )

# Placeholder para actualizar el gráfico sin usar add_rows (deprecado)
chart_placeholder = st.empty()

def toss_coin(n: int) -> float:
    """Emula n lanzamientos (Bernoulli p=0.5) y actualiza la media acumulada."""
    trial_outcomes = scipy.stats.bernoulli.rvs(p=0.5, size=n)

    outcome_no = 0
    outcome_1_count = 0
    means = [0.5]  # arrancamos en el valor esperado

    for r in trial_outcomes:
        outcome_no += 1
        if r == 1:
            outcome_1_count += 1

        mean = outcome_1_count / outcome_no
        means.append(mean)

        # Redibuja el gráfico con la serie actual
        chart_placeholder.line_chart(means)
        time.sleep(0.05)

    return means[-1]

number_of_trials = st.slider('¿Número de intentos?', 1, 1000, 10)
start_button = st.button('Ejecutar')

if start_button:
    st.write(f'Experimento con {number_of_trials} intentos en curso.')

    st.session_state['experiment_no'] += 1
    mean = toss_coin(number_of_trials)

    # Agregar fila sin concat (evita FutureWarning)
    st.session_state['df_experiment_results'].loc[len(st.session_state['df_experiment_results'])] = [
        st.session_state['experiment_no'],
        int(number_of_trials),
        float(mean),
    ]

    st.write(f'Resultado final (media): {mean:.4f}')

st.subheader('Histórico de experimentos')

col1, col2 = st.columns([1, 3])
with col1:
    clear_button = st.button("Limpiar historial")

if clear_button:
    st.session_state['experiment_no'] = 0
    st.session_state['df_experiment_results'] = st.session_state['df_experiment_results'].iloc[0:0]
    st.success("Historial limpiado.")

st.dataframe(st.session_state['df_experiment_results'], width='stretch')

