# ========================================
# BOLIVIA DASHBOARD - VERSIÓN MODULAR
# ========================================

import streamlit as st
import pandas as pd

# Importar módulos del dashboard
from config import APP_CONFIG, SECCIONES_VISIBLES
from estilos import get_css_styles
from datos import datos_bolivia
from utilidades import exportador

# Importar secciones
from seccion_poblacion import seccion_poblacion
from seccion_desempleo import seccion_desempleo
from seccion_fecundidad import seccion_fecundidad
from seccion_mortalidad import seccion_mortalidad
from seccion_datos_electorales import seccion_datos_electorales
from seccion_educacion import seccion_educacion

# ========================================
# CONFIGURACIÓN INICIAL
# ========================================
st.set_page_config(
    page_title=APP_CONFIG['titulo'],
    page_icon=APP_CONFIG['icono'],
    layout=APP_CONFIG['layout'],
    initial_sidebar_state="expanded"
)

# ========================================
# CSS PERSONALIZADO
# ========================================
st.markdown(get_css_styles(), unsafe_allow_html=True)

# ========================================
# SIDEBAR
# ========================================
with st.sidebar:
    st.markdown("## 🇧🇴 Bolivia Stats")
    st.markdown("---")
    
    # Selector de secciones
    st.markdown("### 📊 Secciones Disponibles")
    
    secciones_activas = {}
    for seccion, visible in SECCIONES_VISIBLES.items():
        if visible:
            secciones_activas[seccion] = st.checkbox(
                {
                    'poblacion': '👥 Población',
                    'desempleo': '💼 Desempleo',
                    'fecundidad': '👶 Fecundidad',
                    'mortalidad': '⚰️ Mortalidad',
                    'datos_electorales': '🗳️ Datos Electorales',
                    'educacion': '📚 Educación'
                }.get(seccion, seccion.title()),
                value=True
            )
    
    st.markdown("---")
    
    # Filtros generales
    st.markdown("### ⚙️ Filtros")
    departamentos_seleccionados = st.multiselect(
        "Departamentos:",
        datos_bolivia.departamentos,
        default=['Santa Cruz', 'La Paz', 'Cochabamba']
    )
    
    # Opciones de visualización
    st.markdown("### 🎛️ Opciones")
    mostrar_tablas = st.checkbox("📊 Mostrar tablas detalladas", True)
    mostrar_graficos_adicionales = st.checkbox("📈 Mostrar gráficos adicionales", True)
    mostrar_evolucion_historica = st.checkbox("🕐 Mostrar evolución histórica", True)
    
    st.markdown("---")
    st.markdown("📅 **Datos actualizados:** 2024")
    st.markdown("📊 **Fuente:** INE Bolivia")

# ========================================
# TÍTULO PRINCIPAL
# ========================================
st.markdown(f"""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='color: #2c3e50; font-size: 3rem; margin-bottom: 0;'>{APP_CONFIG['icono']} BOLIVIA</h1>
    <h2 style='color: #7f8c8d; font-size: 1.2rem; font-weight: 300;'>{APP_CONFIG['subtitulo']}</h2>
</div>
""", unsafe_allow_html=True)

# ========================================
# RENDERIZADO DE SECCIONES
# ========================================

# Función helper para separar secciones
def separar_seccion():
    st.markdown("---")
    st.markdown("<br>", unsafe_allow_html=True)

# Renderizar secciones activas
if secciones_activas.get('poblacion', False):
    seccion_poblacion.render(
        departamentos_seleccionados=departamentos_seleccionados,
        mostrar_tabla=mostrar_tablas,
        mostrar_comparativo=mostrar_graficos_adicionales,  # Comparativo como gráfico adicional
        mostrar_historica=mostrar_evolucion_historica  # Control específico para evolución
    )
    separar_seccion()

if secciones_activas.get('desempleo', False):
    seccion_desempleo.render(
        mostrar_comparativo=mostrar_graficos_adicionales,
        mostrar_tabla=mostrar_tablas  # Control de tablas
    )
    separar_seccion()

if secciones_activas.get('fecundidad', False):
    seccion_fecundidad.render(
        departamentos_seleccionados=departamentos_seleccionados,
        mostrar_correlacion=mostrar_graficos_adicionales,
        mostrar_tabla=mostrar_tablas  # Control de tablas
    )
    separar_seccion()

if secciones_activas.get('mortalidad', False):
    seccion_mortalidad.render(
        mostrar_covid=mostrar_graficos_adicionales,
        mostrar_comparativo=mostrar_graficos_adicionales,
        mostrar_tabla=mostrar_tablas  # Control de tablas
    )
    separar_seccion()

if secciones_activas.get('datos_electorales', False):
    seccion_datos_electorales.render(
        departamentos_seleccionados=departamentos_seleccionados,
        mostrar_depuracion=mostrar_graficos_adicionales,
        mostrar_nuevos=mostrar_graficos_adicionales,
        mostrar_comparativo=mostrar_graficos_adicionales,
        mostrar_tabla=mostrar_tablas  # Control de tablas
    )
    separar_seccion()

if secciones_activas.get('educacion', False):
    seccion_educacion.render(
        departamentos_seleccionados=departamentos_seleccionados,
        mostrar_niveles=mostrar_graficos_adicionales,
        mostrar_universitaria=mostrar_graficos_adicionales,
        mostrar_brechas=mostrar_graficos_adicionales,
        mostrar_tabla=mostrar_tablas  # Control de tablas
    )
    separar_seccion()

# ========================================
# EXPORTACIÓN DE DATOS
# ========================================
st.markdown("---")

# Preparar datos para exportación
datos_exportacion = {}

if secciones_activas.get('poblacion', False):
    datos_exportacion['Poblacion'] = datos_bolivia.get_datos_poblacion()

if secciones_activas.get('desempleo', False):
    df_tasas, df_parados, df_historicos = datos_bolivia.get_datos_desempleo()
    datos_exportacion['Desempleo_Tasas'] = df_tasas
    datos_exportacion['Desempleo_Parados'] = df_parados
    datos_exportacion['Desempleo_Historicos'] = df_historicos

if secciones_activas.get('fecundidad', False):
    datos_exportacion['Fecundidad'] = datos_bolivia.get_datos_fecundidad()

if secciones_activas.get('mortalidad', False):
    datos_exportacion['Mortalidad'] = datos_bolivia.get_datos_mortalidad()

if secciones_activas.get('datos_electorales', False):
    datos_exportacion['Datos_Electorales'] = datos_bolivia.get_datos_electorales()

if secciones_activas.get('educacion', False):
    temporal, departamental = datos_bolivia.get_datos_educacion()
    datos_exportacion['Educacion_Temporal'] = temporal
    datos_exportacion['Educacion_Departamental'] = departamental

# Renderizar botones de exportación
if datos_exportacion:
    exportador.render_botones_exportacion(datos_exportacion, "bolivia")

# ========================================
# FOOTER
# ========================================
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #7f8c8d;'>
    <p><strong>Dashboard Bolivia 2024</strong> | Creado con Python + Streamlit | Datos: INE Bolivia</p>
    <p>Estructura modular - Fácil modificación y mantenimiento</p>
</div>
""", unsafe_allow_html=True)