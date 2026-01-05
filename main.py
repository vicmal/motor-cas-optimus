import streamlit as st
import sympy as sp
import numpy as np
import matplotlib.pyplot as plt
import os

# 1. CONFIGURACIÓN DE LA PÁGINA
st.set_page_config(page_title="Optimus Prime CAS - Ing. Víctor Malavé", layout="wide")

# 2. ESTILO CSS PARA LA PIZARRA Y CRÉDITOS
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
        font-weight: bold;
        text-transform: uppercase;
        font-size: 1.1em;
    }
    .autor {
        color: #90caf9;
        font-style: italic;
        font-size: 0.9em;
    }
    </style>
    """, unsafe_allow_html=True)

# 3. ENCABEZADO: LOGO, TÍTULO Y CRÉDITOS
col1, col2 = st.columns([1, 5])
with col1:
    if os.path.exists("optimus.png"):
        st.image("optimus.png", width=120)
    else:
        st.write("🤖")

with col2:
    st.title("CALCULADORA DE DERIVADAS E INTEGRALES OPTIMUS PRIME")
    st.markdown("<p class='autor'>Desarrollado por: <b>Ing. Víctor Hugo Malavé Girón</b></p>", unsafe_allow_html=True)
    st.write("### Motor de Cálculo Infinitesimal | Recurso Académico CAS")

# 4. BARRA LATERAL
st.sidebar.header("ENTRADA DE DATOS")
funcion_input = st.sidebar.text_input("Ingresa f(x):", "x^2 * sin(x)")
lim_a = st.sidebar.number_input("Límite inferior (a):", value=0.0)
lim_b = st.sidebar.number_input("Límite superior (b):", value=3.1415)

if st.sidebar.button("CALCULAR Y GENERAR EXPLICACIÓN"):
    try:
        x = sp.symbols('x')
        f = sp.sympify(funcion_input.replace("^", "**"))

        # OPERACIONES CAS
        derivada = sp.diff(f, x)
        integral_indef = sp.integrate(f, x)
        integral_def = sp.integrate(f, (x, lim_a, lim_b))

        # --- SECCIÓN DE RESULTADOS ---
        st.subheader("📝 Resultados del Análisis")

        # DERIVADA
        st.markdown('<div class="pizarra"><div class="titulo-seccion">I. Análisis Diferencial (Derivada)</div></div>',
                    unsafe_allow_html=True)
        st.latex(f"f'(x) = \\frac{{d}}{{dx}}[{sp.latex(f)}] = {sp.latex(derivada)}")

        # INTEGRAL
        st.markdown('<div class="pizarra"><div class="titulo-seccion">II. Análisis Integral (Antiderivada)</div></div>',
                    unsafe_allow_html=True)
        st.latex(f"\\int f(x) dx = \\int {sp.latex(f)} dx = {sp.latex(sp.simplify(integral_indef))} + C")

        # VALOR NUMÉRICO
        st.success(f"**Resultado de la Integral Definida (Área):** {float(integral_def):.4f}")

        # --- SECCIÓN DE TEORÍA ACADÉMICA DETALLADA ---
        with st.expander("📚 EXPLICACIÓN ACADÉMICA DEL PROCEDIMIENTO"):
            st.markdown("### 1. Procedimiento de Derivación")
            st.write(f"""
            Para hallar la derivada de **{funcion_input}**, el motor utiliza el método de **Diferenciación Automática Simbólica**. 
            Dependiendo de la estructura de tu función, se aplican las siguientes reglas:
            - **Regla de la Potencia:** $\\frac{{d}}{{dx}}x^n = nx^{{n-1}}$.
            - **Regla del Producto/Cadena:** Si tu función tiene multiplicaciones o funciones compuestas (como senos o logaritmos), se descompone internamente en operadores elementales.
            """)

            st.markdown("### 2. Procedimiento de Integración")
            st.write(f"""
            La determinación de la antiderivada (integral indefinida) se realiza mediante el **Algoritmo de Risch**. 
            Este proceso es más complejo que la derivación y sigue estos pasos:
            1. **Clasificación:** Se identifica si la función es racional, trigonométrica o exponencial.
            2. **Búsqueda de Primitiva:** Se intenta resolver por métodos clásicos (sustitución, partes o fracciones parciales). Si no es posible, se recurre a funciones especiales.
            3. **Teorema Fundamental:** Una vez obtenida la primitiva $F(x)$, se evalúa en el intervalo $[{lim_a}, {lim_b}]$ mediante la Regla de Barrow: $F({lim_b}) - F({lim_a})$.
            """)
            st.info(
                "Nota: Al igual que en Symbolab, si la integral es muy compleja, el motor garantiza la solución más simplificada posible.")

        # --- SECCIÓN DE GRÁFICA CON CUADRÍCULA ---
        st.subheader("📊 Visualización Geométrica")
        f_num = sp.lambdify(x, f, "numpy")
        x_vals = np.linspace(float(lim_a) - 2, float(lim_b) + 2, 400)
        y_vals = f_num(x_vals)

        fig, ax = plt.subplots(figsize=(10, 5))
        ax.plot(x_vals, y_vals, color="#1E88E5", lw=2, label=f"f(x) = {funcion_input}")
        ax.fill_between(x_vals, y_vals, where=(x_vals >= lim_a) & (x_vals <= lim_b),
                        color='#00e676', alpha=0.3, label="Área de Integración")

        # Configuración de Cuadrícula (Grid) y Estética
        ax.grid(True, which='both', linestyle='--', linewidth=0.5, color='gray', alpha=0.7)
        ax.axhline(0, color='white', lw=1.2)
        ax.axvline(0, color='white', lw=1.2)
        ax.set_facecolor('#1e1e1e')
        fig.patch.set_facecolor('#0e1117')
        ax.tick_params(colors='white', labelsize=10)
        ax.legend()

        st.pyplot(fig)

    except Exception as e:
        st.error(f"Error en el motor CAS: {e}")
