import streamlit as st
import numpy as np
import sympy as sp
import matplotlib.pyplot as plt
from sympy.integrals.manualintegrate import manualintegrate, integral_steps

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Optimus Prime: Motor CAS", layout="wide")

# --- ESTILOS CSS PERSONALIZADOS ---
st.markdown("""
    <style>
    .main { background: radial-gradient(circle, #1a2a3a 0%, #050a0f 100%); color: #ecf0f1; }
    h1 { text-shadow: 2px 2px 4px black; color: #e74c3c; font-weight: bold; text-align: center; margin-bottom: 20px; }
    .pizarra {
        background-color: #fdf6e3; color: #073642; padding: 30px; 
        border-radius: 12px; border: 8px solid #856404;
        font-family: 'serif'; margin-top: 20px;
        box-shadow: 10px 10px 20px rgba(0,0,0,0.6);
        line-height: 1.6;
    }
    .paso-titulo { color: #b58900; font-weight: bold; border-bottom: 1px solid #eee; margin-top: 15px; }
    </style>
    """, unsafe_allow_html=True)

# --- TÍTULO ---
st.markdown("<h1>🤖 OPTIMUS PRIME: MOTOR CAS DEFINITIVE V10</h1>", unsafe_allow_html=True)

# --- SIDEBAR ---
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/4712/4712139.png", width=100)  # Icono de robot
    st.header("Configuración de Cálculo")
    func_input = st.text_input("Ingresa f(x):", value="(x^4 + 2*x^2 + 2*x + 1) / (x^2 + 1)^2")

    col1, col2 = st.columns(2)
    with col1:
        lim_a = st.number_input("Límite a:", value=0.0)
    with col2:
        lim_b = st.number_input("Límite b:", value=3.1416)

    btn_ejecutar = st.button("EJECUTAR PROCESO", type="primary", use_container_width=True)
    st.info("Soporta: log(x), exp(x), sin(x), sqrt(x), potencias ^ o **")


# --- FUNCIONES DE APOYO PARA EL "PASO A PASO" ---
def obtener_pasos(expr, var):
    """Genera una explicación simplificada basada en el árbol de pasos de SymPy"""
    steps = integral_steps(expr, var)

    def format_step(step, level=0):
        lines = []
        indent = "&nbsp;" * (level * 4)

        if hasattr(step, 'substep'):
            lines.append(f"<div class='paso-titulo'>Aplicando: {type(step).__name__}</div>")
            lines.append(format_step(step.substep, level + 1))
        elif hasattr(step, 'substeps'):
            lines.append(f"<div class='paso-titulo'>Estrategia: {type(step).__name__}</div>")
            for s in step.substeps:
                lines.append(format_step(s, level + 1))
        else:
            # Caso base: mostrar la regla aplicada
            regla = type(step).__name__.replace("Rule", "")
            lines.append(f"{indent} • Regla de <b>{regla}</b>")
        return "".join(lines)

    return format_step(steps)


# --- LÓGICA PRINCIPAL ---
if btn_ejecutar:
    try:
        x = sp.symbols('x')
        # Limpieza de entrada
        expr_clean = func_input.replace("^", "**")
        f_sym = sp.sympify(expr_clean)

        # Cálculos Analíticos
        integral_indef = sp.integrate(f_sym, x)
        area_exacta = sp.integrate(f_sym, (x, lim_a, lim_b))

        # Descomposición (Fracciones Parciales)
        f_descompuesta = sp.apart(f_sym) if f_sym.is_rational_function() else f_sym

        # Mostrar Resultados
        tab1, tab2 = st.tabs(["📝 Pizarra de Procedimiento", "📊 Análisis Gráfico"])

        with tab1:
            st.markdown('<div class="pizarra">', unsafe_allow_html=True)
            st.write("### 📜 Memoria de Cálculo Detallada")

            # Paso 1: Análisis
            st.write("#### 1. Análisis de la Función")
            st.latex(rf"f(x) = {sp.latex(f_sym)}")

            # Paso 2: Estrategia (Fracciones Parciales / Sustitución)
            if f_sym != f_descompuesta:
                st.write("#### 2. Simplificación por Fracciones Parciales")
                st.write("La función es racional, descomponiendo el denominador:")
                st.latex(rf"f(x) = {sp.latex(f_descompuesta)}")

            # Paso 3: El "Paso a Paso" automático
            st.write("#### 3. Algoritmo de Integración")
            try:
                explicacion = obtener_pasos(f_sym, x)
                st.markdown(explicacion, unsafe_allow_html=True)
            except:
                st.write("Se aplicó integración directa por reglas fundamentales.")

            # Paso 4: Resultado final
            st.write("#### 4. Antiderivada Final")
            st.latex(rf"F(x) = {sp.latex(integral_indef)} + C")

            # Paso 5: Evaluación de límites
            st.write("#### 5. Evaluación de la Integral Definida")
            st.latex(rf"\int_{{{lim_a}}}^{{{lim_b}}} f(x) dx = {sp.latex(area_exacta)}")

            st.markdown('</div>', unsafe_allow_html=True)

        with tab2:
            st.metric("Área Aproximada", f"{float(area_exacta.evalf()):.6f} u²")

            # Generar datos para el gráfico
            f_num = sp.lambdify(x, f_sym, modules=['numpy'])
            x_range = np.linspace(float(lim_a) - 1, float(lim_b) + 1, 500)
            y_range = f_num(x_range)

            fig, ax = plt.subplots(figsize=(10, 5))
            fig.patch.set_facecolor('#1a2a3a')
            ax.set_facecolor('#1a2a3a')

            # Dibujar área y función
            ax.plot(x_range, y_range, color='#3498db', label=f"f(x)")
            x_fill = np.linspace(float(lim_a), float(lim_b), 200)
            ax.fill_between(x_fill, f_num(x_fill), color='#e74c3c', alpha=0.4, label="Área bajo la curva")

            # Estilo de ejes
            ax.axhline(0, color='white', linewidth=0.8)
            ax.axvline(0, color='white', linewidth=0.8)
            ax.tick_params(colors='white')
            for spine in ax.spines.values(): spine.set_color('white')
            ax.legend()
            st.pyplot(fig)

    except Exception as e:
        st.error(f"Error en el Motor CAS: {e}")
else:
    st.info("Ingrese una función y presione el botón para iniciar el análisis.")
