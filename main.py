import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import random # Importamos para la aleatoriedad

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Optimus Prime CAS - Ing. Víctor Malavé", layout="wide")

# 2. ESTILO CSS
st.markdown("""
    <style>
    .pizarra { background-color: #1e1e1e; color: #ffffff; padding: 20px; border-radius: 10px; border-left: 6px solid #00e676; }
    .titulo-seccion { color: #00e676; font-weight: bold; text-transform: uppercase; }
    .autor { color: #90caf9; font-style: italic; font-size: 1.1em; }
    .alerta-sintaxis { background-color: #fff3cd; color: #856404; padding: 10px; border-radius: 5px; font-size: 0.85em; }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("optimus.png"): st.image("optimus.png", width=120)
    else: st.write("🤖")

with col2:
    st.title("CALCULADORA DE DERIVADAS E INTEGRALES OPTIMUS PRIME")
    st.markdown("<p class='autor'>Autor: <b>Ing. Víctor Hugo Malavé Girón</b></p>", unsafe_allow_html=True)

# --- BANCO DE DATOS DE EJERCICIOS (EL "ALMACÉN") ---
BANCO_EJERCICIOS = {
    "Polinomio de Grado 3": "x^3 - 4*x^2 + x",
    "Trigonométrica Básica": "sin(x) + cos(x)",
    "Regla de la Cadena": "tan(3*x^2)",
    "Producto Complejo": "x^2 * exp(x)",
    "Logarítmica": "log(x^2 + 1)",
    "Racionalizante": "1/(sqrt(x) + 1)",
    "Fracciones Parciales": "1/(x^2 - 1)",
    "Cíclica": "exp(x) * sin(x)",
    "Potencia Compuesta": "(x + 1)^5",
    "Inversa Trigonométrica": "atan(x)",
    "Desafío Weierstrass": "1/(2 + cos(x))",
    "Gaussiana": "exp(-x^2)"
}

# --- LÓGICA DE ACTUALIZACIÓN ---
# Usamos session_state para que los ejemplos no cambien CADA vez que haces clic en un botón, 
# sino solo cuando refrescas la página (F5) o entras de nuevo.
if 'ejemplos_del_dia' not in st.session_state:
    nombres_aleatorios = random.sample(list(BANCO_EJERCICIOS.keys()), 5)
    st.session_state.ejemplos_del_dia = {k: BANCO_EJERCICIOS[k] for k in nombres_aleatorios}

# 4. BARRA LATERAL
st.sidebar.header("MENÚ DE CÁLCULO")

# SECCIÓN DINÁMICA
st.sidebar.subheader("📝 Retos Clásicos Aleatorios")
opciones = ["Personalizado"] + list(st.session_state.ejemplos_del_dia.keys())
seleccion = st.sidebar.selectbox("Elige un desafío (se actualiza al refrescar):", opciones)

input_default = st.session_state.ejemplos_del_dia[seleccion] if seleccion != "Personalizado" else "x^2"

st.sidebar.markdown('<div class="alerta-sintaxis">⚠️ Usa * para multiplicar (ej: 2*x)</div>', unsafe_allow_html=True)
input_usuario = st.sidebar.text_input("Función f(x):", value=input_default)
lim_a = st.sidebar.number_input("Límite inferior (a):", value=0.0)
lim_b = st.sidebar.number_input("Límite superior (b):", value=1.0)

# --- PROCESO Y RESULTADOS (Mantenemos la lógica anterior corregida) ---
def corregir_sintaxis(texto):
    texto = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', texto)
    return texto.replace("^", "**")

if st.sidebar.button("EJECUTAR ANÁLISIS"):
    try:
        x = sp.symbols('x')
        f = sp.sympify(corregir_sintaxis(input_usuario))
        
        derivada = sp.trigsimp(sp.diff(f, x))
        integral_indef = sp.trigsimp(sp.integrate(f, x))
        integral_def = sp.integrate(f, (x, lim_a, lim_b))

        st.subheader("📝 Análisis Simbólico")
        st.markdown('<div class="pizarra"><div class="titulo-seccion">I. Derivada</div></div>', unsafe_allow_html=True)
        st.latex(f"f'(x) = {sp.latex(derivada)}")
        
        st.markdown('<div class="pizarra"><div class="titulo-seccion">II. Integral</div></div>', unsafe_allow_html=True)
        st.latex(f"\\int f(x)dx = {sp.latex(integral_indef)} + C")
        
        st.success(f"**Resultado Numérico:** {float(integral_def.evalf()):.4f}")

        # GRÁFICA CON CUADRÍCULA
        st.subheader("📊 Visualización")
        f_num = sp.lambdify(x, f, "numpy")
        x_v = np.linspace(float(lim_a)-2, float(lim_b)+2, 400)
        y_v = f_num(x_v)
        fig, ax = plt.subplots(figsize=(10, 3))
        ax.plot(x_v, y_v, color="#1E88E5", lw=2)
        ax.fill_between(x_v, y_v, where=(x_v>=lim_a)&(x_v<=lim_b), color='#00e676', alpha=0.3)
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")

st.markdown("---")
st.caption("Nota: La lista de ejemplos cambia aleatoriamente cada vez que reinicias la aplicación.")
