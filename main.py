import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Optimus Prime CAS", layout="wide")

# 2. ESTILO CSS PARA LA "PIZARRA" PROFESIONAL
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
    .titulo-seccion {
        color: #00e676;
        text-transform: uppercase;
        letter-spacing: 1px;
        font-size: 1.1em;
        margin-bottom: 10px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO: IMAGEN + TÍTULO
col1, col2 = st.columns([1, 5])

with col1:
    # Intenta cargar el archivo que vas a subir a GitHub
    if os.path.exists("optimus.png"):
        st.image("optimus.png", width=120)
    else:
        st.write("🤖")  # Respaldo visual si no encuentra el archivo
        st.caption("Esperando logo...")

with col2:
    st.title("CALCULADORA DE INTEGRALES OPTIMUS PRIME")
    st.write("### Motor CAS de Ingeniería | Análisis Simbólico")
    st.write("### Desarrollado por Ing. Víctor Hugo Malavé Girón")

# 4. BARRA LATERAL (CONFIGURACIÓN)
st.sidebar.header("CONFIGURACIÓN DE CÁLCULO")
funcion_input = st.sidebar.text_input("Ingresa la función f(x):", "x^3 * cos(x)")
lim_a = st.sidebar.number_input("Límite inferior (a):", value=0.0)
lim_b = st.sidebar.number_input("Límite superior (b):", value=3.14159)

# Procesamiento de la cadena para Python
f_prep = funcion_input.replace("^", "**")

if st.sidebar.button("EJECUTAR PROCESO"):
    try:
        x = sp.symbols('x')
        f = sp.sympify(f_prep)

        # --- CÁLCULOS CAS ---
        derivada = sp.diff(f, x)
        integral_indef = sp.integrate(f, x)
        integral_def = sp.integrate(f, (x, lim_a, lim_b))

        # --- SECCIÓN 1: DERIVADAS ---
        st.subheader("1. Análisis de Derivación")
        st.markdown(f"""
        <div class="pizarra">
            <div class="titulo-seccion">Derivada Resultante f'(x):</div>
        </div>
        """, unsafe_allow_html=True)
        st.latex(sp.latex(derivada))

        # --- SECCIÓN 2: INTEGRACIÓN ---
        st.subheader("2. Análisis de Integración")

        st.markdown('<div class="pizarra"><div class="titulo-seccion">Antiderivada (Integral Indefinida):</div></div>',
                    unsafe_allow_html=True)
        # Simplificación automática para mejorar la lectura
        st.latex(sp.latex(sp.simplify(integral_indef)) + " + C")

        st.markdown('<div class="pizarra"><div class="titulo-seccion">Resultado Numérico (Área):</div></div>',
                    unsafe_allow_html=True)
        st.success(f"El valor de la integral definida es: {float(integral_def):.4f}")

        # --- SECCIÓN 3: BOTÓN DE TEORÍA (EXPANDER) ---
        st.write("---")
        with st.expander("🎓 VER FUNDAMENTOS TEÓRICOS"):
            st.markdown(f"""
            ### ¿Cómo se resolvió este problema?
            Para llegar a este resultado, el motor **Optimus Prime** aplicó los siguientes procesos internos:

            * **Diferenciación:** Se aplicaron reglas de cadena, producto o cociente según la estructura de la función para hallar la derivada.
            * **Integración Simbólica:** El motor utilizó algoritmos de **Risch** y **Heuristic** para encontrar la primitiva.
            * **Evaluación:** Se aplicó el *Segundo Teorema Fundamental del Cálculo*: $\int_{{a}}^{{b}} f(x) dx = F(b) - F(a)$.
            * **Simplificación:** El resultado se procesó algebraicamente para mostrar la expresión más reducida posible.
            """)

        # --- SECCIÓN 4: GRÁFICA ---
        st.subheader("3. Visualización de la Curva")
        f_num = sp.lambdify(x, f, "numpy")
        x_vals = np.linspace(float(lim_a) - 2, float(lim_b) + 2, 400)
        y_vals = f_num(x_vals)

        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(x_vals, y_vals, label="f(x)", color="#1E88E5", lw=2.5)
        ax.fill_between(x_vals, y_vals, where=(x_vals >= lim_a) & (x_vals <= lim_b),
                        color='#00e676', alpha=0.3, label="Área Calculada")
        ax.axhline(0, color='white', alpha=0.3)
        ax.axvline(0, color='white', alpha=0.3)
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white')
        ax.legend()
        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error en el motor CAS: {e}")
        st.info("Sugerencia: Revisa que la función esté bien escrita (ej. x^2 o 3*x).")
