# ========================================
# BOLIVIA DASHBOARD - VERSIÓN DE PRUEBA
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
import numpy as np

# ========================================
# CONFIGURACIÓN INICIAL
# ========================================
st.set_page_config(
    page_title="🇧🇴 Bolivia Dashboard",
    page_icon="🇧🇴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ========================================
# DATOS DE EJEMPLO - BOLIVIA
# ========================================
# Datos poblacionales reales
departamentos_data = {
    'Departamento': ['Santa Cruz', 'La Paz', 'Cochabamba', 'Potosí', 'Chuquisaca', 'Tarija', 'Oruro', 'Beni', 'Pando'],
    'Población_2024': [4000143, 2706359, 2005373, 823517, 576153, 482196, 494178, 421196, 110436],
    'Población_2012': [2655084, 2706359, 1758143, 823517, 576153, 482196, 494178, 421196, 110436],
    'Superficie_km2': [370621, 133985, 55631, 118218, 51524, 37623, 53588, 213564, 63827],
    'Densidad': [10.8, 20.2, 36.0, 7.0, 11.2, 12.8, 9.2, 2.0, 1.7]
}

df_bolivia = pd.DataFrame(departamentos_data)
df_bolivia['Crecimiento_%'] = ((df_bolivia['Población_2024'] / df_bolivia['Población_2012']) - 1) * 100

# Datos de alfabetización por año
años_alfabetizacion = {
    'Año': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Alfabetización_%': [95.37, 95.45, 95.52, 95.60, 95.68, 95.75, 95.83, 95.90, 95.98, 96.06],
    'Analfabetismo_%': [4.63, 4.55, 4.48, 4.40, 4.32, 4.25, 4.17, 4.10, 4.02, 3.94]
}

df_alfabetizacion = pd.DataFrame(años_alfabetizacion)

# ========================================
# CSS PERSONALIZADO
# ========================================
st.markdown("""
<style>
    /* Importar fuente moderna */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
    
    /* Estilos generales */
    .main {
        font-family: 'Inter', sans-serif;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 0;
    }
    
    /* Container principal */
    .main .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        background: rgba(255, 255, 255, 0.95);
        border-radius: 15px;
        margin: 1rem;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    
    /* Cards de métricas */
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem;
        border-radius: 15px;
        text-align: center;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
        transition: transform 0.3s ease;
        margin: 0.5rem 0;
    }
    
    .metric-card:hover {
        transform: translateY(-5px);
    }
    
    .metric-number {
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0.5rem 0;
    }
    
    .metric-label {
        font-size: 0.9rem;
        opacity: 0.9;
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 600;
    }
    
    /* Sidebar */
    .css-1d391kg {
        background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
    }
    
    .css-1d391kg .css-1vq4p4l {
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# ========================================
# SIDEBAR
# ========================================
with st.sidebar:
    st.markdown("## 🇧🇴 Bolivia Stats")
    st.markdown("---")
    
    # Selector de vista
    vista = st.selectbox(
        "🔍 Selecciona Vista:",
        ["📊 Dashboard Principal", "📈 Análisis Temporal", "🗺️ Análisis Regional"]
    )
    
    st.markdown("---")
    
    # Filtros
    st.markdown("### ⚙️ Filtros")
    departamentos_seleccionados = st.multiselect(
        "Departamentos:",
        df_bolivia['Departamento'].tolist(),
        default=['Santa Cruz', 'La Paz', 'Cochabamba']
    )
    
    mostrar_densidad = st.checkbox("Mostrar densidad poblacional", True)
    
    st.markdown("---")
    st.markdown("📅 **Datos actualizados:** Censo 2024")
    st.markdown("📊 **Fuente:** INE Bolivia")

# ========================================
# TÍTULO PRINCIPAL
# ========================================
st.markdown("""
<div style='text-align: center; padding: 2rem 0;'>
    <h1 style='color: #2c3e50; font-size: 3rem; margin-bottom: 0;'>🇧🇴 BOLIVIA</h1>
    <h2 style='color: #7f8c8d; font-size: 1.2rem; font-weight: 300;'>Dashboard Estadístico Nacional</h2>
</div>
""", unsafe_allow_html=True)

# ========================================
# MÉTRICAS PRINCIPALES
# ========================================
col1, col2, col3, col4 = st.columns(4)

poblacion_total = df_bolivia['Población_2024'].sum()
superficie_total = df_bolivia['Superficie_km2'].sum()
densidad_promedio = poblacion_total / superficie_total

with col1:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Población Total</div>
        <div class="metric-number">{poblacion_total:,.0f}</div>
        <div style="font-size: 0.8rem;">Censo 2024</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Departamentos</div>
        <div class="metric-number">9</div>
        <div style="font-size: 0.8rem;">Divisiones admin.</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Superficie</div>
        <div class="metric-number">{superficie_total:,.0f}</div>
        <div style="font-size: 0.8rem;">km²</div>
    </div>
    """, unsafe_allow_html=True)

with col4:
    st.markdown(f"""
    <div class="metric-card">
        <div class="metric-label">Alfabetización</div>
        <div class="metric-number">96.1%</div>
        <div style="font-size: 0.8rem;">2024</div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

# ========================================
# CONTENIDO PRINCIPAL SEGÚN VISTA
# ========================================

if vista == "📊 Dashboard Principal":
    
    # FILA DE GRÁFICOS PRINCIPALES
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("📊 Población por Departamento 2024")
        
        df_filtrado = df_bolivia[df_bolivia['Departamento'].isin(departamentos_seleccionados)] if departamentos_seleccionados else df_bolivia
        
        fig_barras = px.bar(
            df_filtrado.sort_values('Población_2024', ascending=True),
            x='Población_2024',
            y='Departamento',
            orientation='h',
            color='Población_2024',
            color_continuous_scale='viridis',
            text='Población_2024'
        )
        
        fig_barras.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_barras.update_layout(
            height=400,
            showlegend=False,
            xaxis_title="Población",
            yaxis_title="",
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_barras, use_container_width=True)
    
    with col2:
        st.subheader("🥧 Distribución Poblacional")
        
        fig_pie = px.pie(
            df_filtrado,
            values='Población_2024',
            names='Departamento',
            color_discrete_sequence=px.colors.qualitative.Set3
        )
        
        fig_pie.update_traces(textposition='inside', textinfo='percent+label')
        fig_pie.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_pie, use_container_width=True)

elif vista == "📈 Análisis Temporal":
    
    st.subheader("📈 Evolución de la Alfabetización 2015-2024")
    
    col1, col2 = st.columns(2)
    
    with col1:
        fig_alfabetizacion = px.line(
            df_alfabetizacion,
            x='Año',
            y='Alfabetización_%',
            markers=True,
            title="Tasa de Alfabetización (%)",
            color_discrete_sequence=['#2ecc71']
        )
        
        fig_alfabetizacion.update_layout(
            height=300,
            yaxis=dict(range=[94, 97]),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_alfabetizacion, use_container_width=True)
    
    with col2:
        fig_analfabetismo = px.line(
            df_alfabetizacion,
            x='Año',
            y='Analfabetismo_%',
            markers=True,
            title="Tasa de Analfabetismo (%)",
            color_discrete_sequence=['#e74c3c']
        )
        
        fig_analfabetismo.update_layout(
            height=300,
            yaxis=dict(range=[3, 5]),
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_analfabetismo, use_container_width=True)

elif vista == "🗺️ Análisis Regional":
    
    st.subheader("🗺️ Análisis por Densidad Poblacional")
    
    if mostrar_densidad:
        fig_scatter = px.scatter(
            df_bolivia,
            x='Superficie_km2',
            y='Población_2024',
            size='Densidad',
            color='Densidad',
            hover_name='Departamento',
            title="Relación Superficie vs Población (Tamaño = Densidad)",
            color_continuous_scale='viridis'
        )
        
        fig_scatter.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Tabla de datos
    st.subheader("📋 Datos Detallados")
    st.dataframe(
        df_bolivia[['Departamento', 'Población_2024', 'Superficie_km2', 'Densidad']],
        use_container_width=True
    )

# ========================================
# FOOTER CON EXPORTACIONES REALES
# ========================================
st.markdown("---")

col1, col2, col3, col4 = st.columns(4)

# Preparar datos para exportación
datos_exportacion = df_bolivia.to_csv(index=False)
datos_json = df_bolivia.to_json(orient='records', indent=2)

# Preparar Excel con múltiples hojas
import io
def crear_excel():
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        # Hoja 1: Datos principales
        df_bolivia.to_excel(writer, sheet_name='Datos_Bolivia', index=False)
        
        # Hoja 2: Datos de alfabetización
        df_alfabetizacion.to_excel(writer, sheet_name='Alfabetizacion', index=False)
        
        # Hoja 3: Resumen estadístico
        resumen = pd.DataFrame({
            'Métrica': ['Población Total', 'Superficie Total (km²)', 'Densidad Promedio (hab/km²)', 'Departamentos'],
            'Valor': [poblacion_total, superficie_total, round(densidad_promedio, 2), 9]
        })
        resumen.to_excel(writer, sheet_name='Resumen', index=False)
    
    return output.getvalue()

with col1:
    # Exportar CSV
    st.download_button(
        label="📥 Descargar CSV",
        data=datos_exportacion,
        file_name="bolivia_datos.csv",
        mime="text/csv",
        use_container_width=True
    )

with col2:
    # Exportar Excel con múltiples hojas
    excel_data = crear_excel()
    st.download_button(
        label="📊 Descargar Excel",
        data=excel_data,
        file_name="bolivia_dashboard_completo.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col3:
    # Generar reporte en texto
    reporte = f"""
REPORTE BOLIVIA 2024
====================

Población Total: {poblacion_total:,.0f} habitantes
Superficie Total: {superficie_total:,.0f} km²
Densidad Promedio: {densidad_promedio:.2f} hab/km²

DEPARTAMENTOS:
{'-'*40}
"""
    for _, row in df_bolivia.iterrows():
        reporte += f"{row['Departamento']}: {row['Población_2024']:,.0f} habitantes\n"
    
    st.download_button(
        label="📱 Descargar Reporte",
        data=reporte,
        file_name="bolivia_reporte.txt",
        mime="text/plain",
        use_container_width=True
    )

with col4:
    # Información del link online
    if st.button("🔗 Info Link Online", use_container_width=True):
        st.info("""
        🌐 **Para crear link online:**
        1. Sube tu código a GitHub
        2. Conecta en streamlit.io
        3. ¡Listo! Link permanente
        
        💡 **Próximo paso:** Te enseño cómo
        """)

# EXPORTACIÓN DE GRÁFICOS
st.markdown("### 📊 Exportar Gráficos Individuales")

export_col1, export_col2 = st.columns(2)

with export_col1:
    if st.button("📊 Exportar Gráfico Principal", use_container_width=True):
        try:
            # Crear el gráfico para exportar
            df_para_grafico = df_bolivia.sort_values('Población_2024', ascending=True)
            fig_export = px.bar(
                df_para_grafico,
                x='Población_2024',
                y='Departamento',
                orientation='h',
                title="Población por Departamento - Bolivia 2024"
            )
            
            # Exportar como HTML
            html_string = fig_export.to_html(include_plotlyjs='cdn')
            
            st.download_button(
                label="⬇️ Descargar Gráfico HTML",
                data=html_string,
                file_name="grafico_poblacion_bolivia.html",
                mime="text/html"
            )
            
        except Exception as e:
            st.error(f"Error al exportar: {e}")

with export_col2:
    if st.button("🥧 Exportar Gráfico Circular", use_container_width=True):
        try:
            # Crear gráfico circular para exportar
            fig_pie_export = px.pie(
                df_bolivia,
                values='Población_2024',
                names='Departamento',
                title="Distribución Poblacional - Bolivia 2024"
            )
            
            # Exportar como HTML
            html_pie = fig_pie_export.to_html(include_plotlyjs='cdn')
            
            st.download_button(
                label="⬇️ Descargar Gráfico Circular",
                data=html_pie,
                file_name="grafico_circular_bolivia.html",
                mime="text/html"
            )
            
        except Exception as e:
            st.error(f"Error al exportar: {e}")

# Footer
st.markdown("""
<div style='text-align: center; padding: 2rem 0; color: #7f8c8d;'>
    <p><strong>Dashboard Bolivia 2024</strong> | Creado con Python + Streamlit | Datos: INE Bolivia</p>
</div>
""", unsafe_allow_html=True)