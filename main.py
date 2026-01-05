import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Optimus Prime CAS - Ing. Víctor Malavé", layout="wide")

# 2. ESTILO CSS
st.markdown("""
    <style>
    .pizarra {
        background-color: #1e1e1e;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border-left: 6px solid #00e676;
        font-family: 'Courier New', Courier, monospace;
        margin-top: 15px;
        margin-bottom: 10px;
    }
    .titulo-seccion { color: #00e676; font-weight: bold; text-transform: uppercase; }
    .autor { color: #90caf9; font-style: italic; font-size: 0.9em; }
    .alerta-sintaxis {
        background-color: #fff3cd;
        color: #856404;
        padding: 10px;
        border-radius: 5px;
        font-size: 0.85em;
        border: 1px solid #ffeeba;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("optimus.png"): st.image("optimus.png", width=120)
    else: st.write("🤖")

with col2:
    st.title("CALCULADORA DE DERIVADAS E INTEGRALES OPTIMUS PRIME")
    st.markdown("<p class='autor'>Desarrollado por: <b>Ing. Víctor Hugo Malavé Girón</b></p>", unsafe_allow_html=True)

# --- FUNCIÓN DE LIMPIEZA DE SINTAXIS ---
def corregir_sintaxis(texto):
    texto = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', texto)
    texto = re.sub(r'(\))(\()', r'\1*\2', texto)
    return texto.replace("^", "**")

# 4. BARRA LATERAL CON ADVERTENCIA
st.sidebar.header("CONFIGURACIÓN")

# RECUADRO DE ADVERTENCIA PEDAGÓGICA
st.sidebar.markdown("""
    <div class="alerta-sintaxis">
        ⚠️ <b>IMPORTANTE:</b> Para productos, usa siempre el asterisco (*). <br>
        Ejemplo: Escribe <b>2*x</b> en lugar de 2x; <b>x*cos(x)</b> en lugar de xcos(x).
    </div>
    """, unsafe_allow_html=True)

input_usuario = st.sidebar.text_input("Ingresa f(x):", "tan(2*x)")
lim_a = st.sidebar.number_input("Límite inferior (a):", value=0.0)
lim_b = st.sidebar.number_input("Límite superior (b):", value=1.0)

if st.sidebar.button("CALCULAR Y EXPLICAR"):
    try:
        x = sp.symbols('x')
        f_limpia = corregir_sintaxis(input_usuario)
        f = sp.sympify(f_limpia)
        
        # OPERACIONES CON SIMPLIFICACIÓN
        derivada = sp.trigsimp(sp.diff(f, x))
        integral_indef = sp.trigsimp(sp.integrate(f, x))
        integral_def = sp.integrate(f, (x, lim_a, lim_b))

        # --- RESULTADOS ---
        st.subheader("📝 Resultados del Análisis")
        
        # DERIVADA
        st.markdown('<div class="pizarra"><div class="titulo-seccion">I. Análisis Diferencial</div></div>', unsafe_allow_html=True)
        st.latex(f"f'(x) = \\frac{{d}}{{dx}}[{sp.latex(f)}] = {sp.latex(derivada)}")
        
        # INTEGRAL
        st.markdown('<div class="pizarra"><div class="titulo-seccion">II. Análisis Integral</div></div>', unsafe_allow_html=True)
        st.latex(f"\\int {sp.latex(f)} dx = {sp.latex(integral_indef)} + C")
        
        st.success(f"**Área bajo la curva en el intervalo [{lim_a}, {lim_b}]:** {float(integral_def):.4f}")

        # EXPLICACIÓN DETALLADA
        with st.expander("📚 VER PROCEDIMIENTO ACADÉMICO"):
            st.markdown("### 1. Derivación")
            st.write(f"Se ha aplicado la derivada simbólica a la función. Resultado: ${sp.latex(derivada)}$.")
            
            st.markdown("### 2. Integración")
            st.write(f"Se ha determinado la primitiva mediante algoritmos CAS. Resultado: ${sp.latex(integral_indef)}$.")

        # GRÁFICA CON CUADRÍCULA
        st.subheader("📊 Visualización")
        f_num = sp.lambdify(x, f, "numpy")
        x_v = np.linspace(float(lim_a)-1, float(lim_b)+1, 400)
        y_v = f_num(x_v)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x_v, y_v, color="#1E88E5", lw=2)
        ax.fill_between(x_v, y_v, where=(x_v>=lim_a)&(x_v<=lim_b), color='#00e676', alpha=0.3)
        ax.grid(True, linestyle='--', alpha=0.6) # CUADRÍCULA
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error: {e}")
