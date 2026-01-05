import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt

# 1. CONFIGURACIÓN DE LA PÁGINA (Título en la pestaña del navegador)
st.set_page_config(page_title="Calculadora de Integrales Optimus Prime", layout="wide")

# 2. ESTILO CSS PARA LA "PIZARRA"
st.markdown("""
    <style>
    .pizarra {
        background-color: #263238;
        color: #ffffff;
        padding: 20px;
        border-radius: 10px;
        border: 5px solid #455A64;
        font-family: 'Courier New', Courier, monospace;
        margin-bottom: 20px;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO CON IMAGEN Y TÍTULO NUEVO
col1, col2 = st.columns([1, 4])

with col1:
    # Intenta cargar la imagen localmente.
    # Asegúrate de subir tu imagen a GitHub con el nombre 'optimus.png'
    try:
        st.image("optimus.png", width=150)
    except:
        st.write("🤖")  # Icono de respaldo si no encuentra la imagen

with col2:
    st.title("CALCULADORA DE INTEGRALES")
    st.write("Motor de Cálculo Simbólico Avanzado para Ingeniería, desarrollado por Víctor Hugo Malavé Girón")

# 4. ENTRADA DE DATOS
st.sidebar.header("CONFIGURACIÓN DE CÁLCULO")
funcion_input = st.sidebar.text_input("Ingresa la función f(x):", "x^2 * sin(x)")
lim_a = st.sidebar.number_input("Límite inferior (a):", value=0.0)
lim_b = st.sidebar.number_input("Límite superior (b):", value=3.14159)

# Procesar la función para que Python la entienda (cambiar ^ por **)
funcion_python = funcion_input.replace("^", "**")

if st.sidebar.button("EJECUTAR PROCESO"):
    try:
        x = sp.symbols('x')
        f = sp.sympify(funcion_python)

        # CÁLCULOS CAS
        integral_indef = sp.integrate(f, x)
        integral_def = sp.integrate(f, (x, lim_a, lim_b))
        derivada = sp.diff(f, x)  # Añadimos derivada por si quieres verla

        # MOSTRAR RESULTADOS EN LA "PIZARRA"
        st.subheader("Pizarra de Procedimientos")

        with st.container():
            st.markdown(f"""
            <div class="pizarra">
                <h3>ANÁLISIS DE LA FUNCIÓN</h3>
                <p><b>Función original:</b></p>
            </div>
            """, unsafe_allow_html=True)
            st.latex(sp.latex(f))

            st.markdown('<div class="pizarra"><p><b>Antiderivada (Integral Indefinida):</b></p></div>',
                        unsafe_allow_html=True)
            # Simplificamos la respuesta para que no sea tan abrumadora
            st.latex(sp.latex(sp.simplify(integral_indef)) + " + C")

            st.markdown('<div class="pizarra"><p><b>Resultado Numérico (Integral Definida):</b></p></div>',
                        unsafe_allow_html=True)
            st.success(f"El área bajo la curva es: {float(integral_def):.4f}")

        # GRÁFICA
        st.subheader("Visualización Gráfica")
        f_num = sp.lambdify(x, f, "numpy")
        x_vals = np.linspace(float(lim_a) - 2, float(lim_b) + 2, 400)
        y_vals = f_num(x_vals)

        fig, ax = plt.subplots()
        ax.plot(x_vals, y_vals, label=f"f(x) = {funcion_input}", color="blue")
        ax.fill_between(x_vals, y_vals, where=(x_vals >= lim_a) & (x_vals <= lim_b), color='skyblue', alpha=0.4)
        ax.axhline(0, color='black', lw=1)
        ax.axvline(0, color='black', lw=1)
        ax.legend()
        ax.grid(True, linestyle='--')

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error en el procesamiento: {e}")
        st.info("Asegúrate de escribir la función correctamente (ejemplo: x^2 o sin(x))")

