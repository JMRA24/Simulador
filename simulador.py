import math
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Simulador de Física Mecánica", layout="wide")

st.title("Simulador del movimiento de un vehículo en una intersección urbana")
st.markdown(
    """
Este simulador permite analizar cómo cambian la **fuerza centrípeta**, la **energía cinética**,
la **cantidad de movimiento** y la **potencia** cuando varía la velocidad del vehículo.
"""
)

with st.sidebar:
    st.header("Entradas del sistema")
    masa = st.number_input("Masa del vehículo (kg)", min_value=100.0, value=1000.0, step=100.0)
    velocidad = st.slider("Velocidad del vehículo (m/s)", min_value=0.0, max_value=30.0, value=20.0, step=0.1)
    radio = st.number_input("Radio de la curva (m)", min_value=1.0, value=25.0, step=1.0)
    aceleracion = st.number_input("Aceleración en recta (m/s²)", min_value=0.0, value=2.5, step=0.1)
    tiempo = st.number_input("Tiempo de aceleración (s)", min_value=0.1, value=8.0, step=0.1)
    mu = st.number_input("Coeficiente de fricción", min_value=0.1, value=0.7, step=0.05)
    g = 9.8

# Cálculos
fuerza_neta = masa * aceleracion
energia_cinetica = 0.5 * masa * velocidad**2
cantidad_mov = masa * velocidad
fuerza_centripeta = (masa * velocidad**2) / radio if radio > 0 else 0.0
velocidad_segura = math.sqrt(mu * g * radio)
trabajo = fuerza_neta * (0.5 * aceleracion * tiempo**2)
potencia = trabajo / tiempo if tiempo > 0 else 0.0
energia_segura = 0.5 * masa * velocidad_segura**2
energia_a_disipar = max(0.0, energia_cinetica - energia_segura)

col1, col2 = st.columns(2)

with col1:
    st.subheader("Resultados principales")
    st.metric("Fuerza neta en recta", f"{fuerza_neta:,.2f} N")
    st.metric("Energía cinética", f"{energia_cinetica:,.2f} J")
    st.metric("Cantidad de movimiento", f"{cantidad_mov:,.2f} kg·m/s")
    st.metric("Fuerza centrípeta", f"{fuerza_centripeta:,.2f} N")

with col2:
    st.subheader("Condición de seguridad")
    st.metric("Velocidad segura en curva", f"{velocidad_segura:,.2f} m/s")
    st.metric("Velocidad segura en curva", f"{velocidad_segura*3.6:,.2f} km/h")
    st.metric("Energía cinética segura", f"{energia_segura:,.2f} J")
    st.metric("Energía a disipar", f"{energia_a_disipar:,.2f} J")

st.subheader("Interpretación física")
# Comparación segura entre velocidad actual y velocidad segura
velocidad_actual_redondeada = round(velocidad, 2)
velocidad_segura_redondeada = round(velocidad_segura, 2)

# Energía cinética segura
energia_segura = 0.5 * masa * (velocidad_segura ** 2)

# Energía que debería disiparse para llegar a la velocidad segura
energia_a_disipar = max(0.0, round(energia_cinetica - energia_segura, 2))

st.subheader("Interpretación física")

if velocidad_actual_redondeada > velocidad_segura_redondeada:
    st.error(
        f"La velocidad actual de {velocidad_actual_redondeada:.2f} m/s supera la velocidad segura de "
        f"{velocidad_segura_redondeada:.2f} m/s. El vehículo podría perder adherencia en la curva."
    )
else:
    st.success(
        f"La velocidad actual de {velocidad_actual_redondeada:.2f} m/s está dentro del rango seguro para la curva."
    )

st.markdown(
    f"""
- **Fuerza neta en recta:** se obtiene con la segunda ley de Newton, \(F = m \cdot a\).
- **Fuerza centrípeta:** se calcula con \(F_c = \frac{{m v^2}}{{r}}\).
- **Energía cinética:** se calcula con \(E_c = \frac{{1}}{{2}}mv^2\).
- **Cantidad de movimiento:** se calcula con \(p = mv\).
"""
)

st.subheader("Comparación de dos escenarios")
comparacion = pd.DataFrame(
    {
        "Escenario": ["Velocidad actual", "Velocidad segura"],
        "Velocidad (m/s)": [velocidad, velocidad_segura],
        "Velocidad (km/h)": [velocidad * 3.6, velocidad_segura * 3.6],
        "Fuerza centrípeta (N)": [fuerza_centripeta, (masa * velocidad_segura**2) / radio],
        "Energía cinética (J)": [energia_cinetica, energia_segura],
        "Cantidad de movimiento (kg·m/s)": [cantidad_mov, masa * velocidad_segura],
    }
)
st.dataframe(comparacion, use_container_width=True)

st.success("""
Conclusión:

Al reducir la velocidad disminuyen la fuerza centrípeta, 
la energía cinética y la cantidad de movimiento.

Por eso, controlar la velocidad antes de una curva 
mejora la seguridad del vehículo.
""")
