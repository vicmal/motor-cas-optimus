import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
import re

# 1. CONFIGURACIÓN DE LA PÁGINA (SEO MEJORADO)
st.set_page_config(
    page_title="Calculadora de Derivadas e Integrales - Ing. Víctor Malavé",
    page_icon="🤖",
    layout="wide",
    menu_items={
        'About': "# Motor CAS Optimus Prime\nCreado por el Ing. Víctor Hugo Malavé Girón para fines académicos."
    }
)

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
    }
    .titulo-seccion { color: #00e676; font-weight: bold; text-transform: uppercase; }
    .autor { color: #90caf9; font-style: italic; font-size: 1.1em; }
    .alerta-sintaxis {
        background-color: #fff3cd; color: #856404; padding: 10px;
        border-radius: 5px; font-size: 0.85em; border: 1px solid #ffeeba;
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
    st.markdown("<p class='autor'>Autor: <b>Ing. Víctor Hugo Malavé Girón</b></p>", unsafe_allow_html=True)

# --- FUNCIÓN DE LIMPIEZA DE SINTAXIS ---
def corregir_sintaxis(texto):
    texto = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', texto)
    texto = re.sub(r'(\))(\()', r'\1*\2', texto)
    return texto.replace("^", "**")

# 4. BARRA LATERAL
st.sidebar.header("MENÚ DE CÁLCULO")

# --- SECCIÓN DE EJEMPLOS PARA EXAMEN ---
st.sidebar.subheader("📝 Ejemplos para Examen")
ejemplos = {
    "Personalizado": "",
    "Básico: Polinomios": "x^3 - 5*x^2 + 2",
    "Trigonométrico: tan(2x)": "tan(2*x)",
    "Producto: x * cos(x)": "x * cos(x)",
    "Exponencial: e^(-x^2)": "exp(-x^2)",
    "Fracciones: 1/(x^2 + 1)": "1/(x^2 + 1)",
    "Desafío: 1/(2 + cos(x))": "1/(2 + cos(x))"
}
seleccion = st.sidebar.selectbox("Selecciona un reto clásico:", list(ejemplos.keys()))

# Si selecciona un ejemplo, se precarga en el input
input_default = ejemplos[seleccion] if seleccion != "Personalizado" else "tan(2*x)"

st.sidebar.markdown('<div class="alerta-sintaxis">⚠️ Usa * para multiplicar (ej: 2*x)</div>', unsafe_allow_html=True)
input_usuario = st.sidebar.text_input("Función f(x):", value=input_default)
lim_a = st.sidebar.number_input("Límite inferior (a):", value=0.0)
lim_b = st.sidebar.number_input("Límite superior (b):", value=1.0)

if st.sidebar.button("EJECUTAR ANÁLISIS"):
    try:
        x = sp.symbols('x')
        f_limpia = corregir_sintaxis(input_usuario)
        f = sp.sympify(f_limpia)
        
        # OPERACIONES
        derivada = sp.trigsimp(sp.diff(f, x))
        integral_indef = sp.trigsimp(sp.integrate(f, x))
        integral_def = sp.integrate(f, (x, lim_a, lim_b))

        # --- MOSTRAR RESULTADOS ---
        st.subheader("📝 Análisis Simbólico y Numérico")
        
        st.markdown('<div class="pizarra"><div class="titulo-seccion">I. Cálculo Diferencial</div></div>', unsafe_allow_html=True)
        st.latex(f"f'(x) = {sp.latex(derivada)}")
        
        st.markdown('<div class="pizarra"><div class="titulo-seccion">II. Cálculo Integral</div></div>', unsafe_allow_html=True)
        st.latex(f"\\int f(x)dx = {sp.latex(integral_indef)} + C")
        
        st.success(f"**Resultado Integral Definida:** {float(integral_def.evalf()):.4f}")

        # TEORÍA PASO A PASO
        with st.expander("🎓 VER EXPLICACIÓN DEL PROCEDIMIENTO"):
            st.write(f"""
            1. **Derivación:** El motor aplicó reglas de derivación simbólica para obtener f'(x).
            2. **Integración:** Se halló la primitiva mediante el Algoritmo de Risch.
            3. **Evaluación:** Se aplicó el Segundo Teorema Fundamental del Cálculo en el intervalo [{lim_a}, {lim_b}].
            """)

        # GRÁFICA
        st.subheader("📊 Visualización")
        f_num = sp.lambdify(x, f, "numpy")
        x_v = np.linspace(float(lim_a)-2, float(lim_b)+2, 400)
        y_v = f_num(x_v)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x_v, y_v, color="#1E88E5", lw=2)
        ax.fill_between(x_v, y_v, where=(x_v>=lim_a)&(x_v<=lim_b), color='#00e676', alpha=0.3)
        ax.grid(True, linestyle='--', alpha=0.6)
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error CAS: {e}")

# PIE DE PÁGINA PARA SEO
st.markdown("---")
st.markdown("""
<p style='text-align: center; color: gray; font-size: 0.8em;'>
Búsquedas relacionadas: Calculadora de integrales paso a paso, derivada de la tangente, 
regla de la cadena, área bajo la curva, Ing. Víctor Hugo Malavé Girón, Cálculo Infinitesimal.
</p>
""", unsafe_allow_html=True)
