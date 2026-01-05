import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os
import re
import random

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(
    page_title="Optimus Prime CAS - Ing. Víctor Malavé",
    page_icon="🤖",
    layout="wide"
)

# 2. ESTILO CSS PARA PIZARRA Y COMPONENTES
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
        box-shadow: 2px 2px 10px rgba(0,0,0,0.5);
    }
    .titulo-seccion { color: #00e676; font-weight: bold; text-transform: uppercase; font-size: 1.1em; }
    .autor { color: #90caf9; font-style: italic; font-size: 1.1em; }
    .alerta-sintaxis {
        background-color: #fff3cd; color: #856404; padding: 10px;
        border-radius: 5px; font-size: 0.85em; border: 1px solid #ffeeba;
        margin-bottom: 15px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("optimus.png"):
        st.image("optimus.png", width=120)
    else:
        st.write("🤖")

with col2:
    st.title("CALCULADORA DE DERIVADAS E INTEGRALES OPTIMUS PRIME")
    st.markdown("<p class='autor'>Autor: <b>Ing. Víctor Hugo Malavé Girón</b></p>", unsafe_allow_html=True)
    st.write("### Motor CAS para Ingeniería y Docencia")

# --- BANCO DE DATOS DE EJERCICIOS ---
BANCO_EJERCICIOS = {
    "Polinomio de Grado 3": "x^3 - 4*x^2 + x",
    "Trigonométrica: tan(2x)": "tan(2*x)",
    "Producto: x^2 * exp(x)": "x^2 * exp(x)",
    "Racional: 1/(x^2 + 1)": "1/(x^2 + 1)",
    "Desafío: 1/(2 + cos(x))": "1/(2 + cos(x))",
    "Raíz y Logaritmo": "log(x) / sqrt(x)",
    "Cíclica: exp(x)*cos(x)": "exp(x)*cos(x)",
    "Potencia: (2*x + 3)^4": "(2*x + 3)^4"
}

# Lógica de ejemplos aleatorios por sesión
if 'ejemplos_del_dia' not in st.session_state:
    nombres_aleatorios = random.sample(list(BANCO_EJERCICIOS.keys()), 4)
    st.session_state.ejemplos_del_dia = {k: BANCO_EJERCICIOS[k] for k in nombres_aleatorios}

# --- FUNCIÓN DE LIMPIEZA DE SINTAXIS ---
def corregir_sintaxis(texto):
    # Inserta '*' entre número y letra (ej: 2x -> 2*x)
    texto = re.sub(r'(\d)([a-zA-Z\(])', r'\1*\2', texto)
    # Inserta '*' entre paréntesis (ej: (x)(x) -> (x)*(x))
    texto = re.sub(r'(\))(\()', r'\1*\2', texto)
    return texto.replace("^", "**")

# 4. BARRA LATERAL
st.sidebar.header("MENÚ DE CONTROL")

# Sección de ejemplos aleatorios
st.sidebar.subheader("📝 Retos para Examen")
opciones = ["Personalizado"] + list(st.session_state.ejemplos_del_dia.keys())
seleccion = st.sidebar.selectbox("Selecciona un reto clásico:", opciones)

input_default = st.session_state.ejemplos_del_dia[seleccion] if seleccion != "Personalizado" else "tan(2*x)"

st.sidebar.markdown("""
    <div class="alerta-sintaxis">
        ⚠️ <b>Sintaxis:</b> Usa siempre el asterisco (*) para multiplicar.<br>
        Ejemplo: <b>3*x*sin(x)</b>
    </div>
    """, unsafe_allow_html=True)

input_usuario = st.sidebar.text_input("Ingresa la función f(x):", value=input_default)
lim_a = st.sidebar.number_input("Límite inferior (a):", value=0.0)
lim_b = st.sidebar.number_input("Límite superior (b):", value=1.0)

if st.sidebar.button("EJECUTAR ANÁLISIS COMPLETO"):
    try:
        x = sp.symbols('x')
        f_limpia = corregir_sintaxis(input_usuario)
        f = sp.sympify(f_limpia)
        
        # CÁLCULOS CAS
        derivada = sp.trigsimp(sp.diff(f, x))
        integral_indef = sp.trigsimp(sp.integrate(f, x))
        integral_def = sp.integrate(f, (x, lim_a, lim_b))

        # --- RESULTADOS ---
        st.subheader("📝 Resultados del Análisis")
        
        # DERIVADA
        st.markdown('<div class="pizarra"><div class="titulo-seccion">I. Cálculo Diferencial</div></div>', unsafe_allow_html=True)
        st.latex(f"f'(x) = \\frac{{d}}{{dx}}[{sp.latex(f)}] = {sp.latex(derivada)}")
        
        # INTEGRAL
        st.markdown('<div class="pizarra"><div class="titulo-seccion">II. Cálculo Integral</div></div>', unsafe_allow_html=True)
        st.latex(f"\\int {sp.latex(f)} dx = {sp.latex(integral_indef)} + C")
        
        # VALOR NUMÉRICO
        st.success(f"**Resultado de la Integral Definida:** {float(integral_def.evalf()):.4f}")

        # --- SECCIÓN DE FUNDAMENTOS TEÓRICOS (REINTEGRADA) ---
        with st.expander("🎓 VER FUNDAMENTOS TEÓRICOS Y PROCEDIMIENTO"):
            st.markdown("### 1. Determinación de la Derivada")
            st.write(f"""
            Para calcular $f'(x)$, el motor aplica reglas de derivación sobre **${sp.latex(f)}$**. 
            Dependiendo de la forma, se utiliza la **Regla de la Cadena**, el **Producto** o la **Potencia**. 
            El resultado se somete a una simplificación trigonométrica para mostrar la forma más elegante.
            """)
            
            st.markdown("### 2. Determinación de la Integral")
            st.write(f"""
            La antiderivada se obtiene mediante el **Algoritmo de Risch**, un método algebraico que decide si una función tiene una integral elemental.
            
            Para el valor numérico de **{float(integral_def.evalf()):.4f}**, se aplicó el **Segundo Teorema Fundamental del Cálculo**:
            """)
            st.latex(r"\int_{a}^{b} f(x) dx = F(b) - F(a)")
            st.write(f"Donde $F(x)$ es la antiderivada evaluada en los límites ${lim_a}$ y ${lim_b}$.")

        # --- GRÁFICA ---
        st.subheader("📊 Visualización Geométrica")
        f_num = sp.lambdify(x, f, "numpy")
        x_v = np.linspace(float(lim_a)-2, float(lim_b)+2, 400)
        y_v = f_num(x_v)
        
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x_v, y_v, color="#1E88E5", lw=2, label="f(x)")
        ax.fill_between(x_v, y_v, where=(x_v>=lim_a)&(x_v<=lim_b), color='#00e676', alpha=0.3, label="Área")
        ax.grid(True, linestyle='--', alpha=0.5)
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error en el Motor CAS: {e}")

# FOOTER SEO
st.markdown("---")
st.markdown("<p style='text-align: center; color: gray;'>Optimizado para Ingeniería | Desarrollado por Víctor Malavé</p>", unsafe_allow_html=True)
