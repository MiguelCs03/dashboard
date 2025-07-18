# ========================================
# SECCIÓN POBLACIÓN - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datos import datos_bolivia
from estilos import render_metric_card, render_section_title

class SeccionPoblacion:
    """Maneja toda la funcionalidad de la sección población"""
    
    def __init__(self):
        self.df = datos_bolivia.get_datos_poblacion()
        self.df_historica = datos_bolivia.get_evolucion_poblacion_historica()
        self.df_tasas = datos_bolivia.get_tasas_crecimiento_intercensal()
    
    def render_metricas(self):
        """Renderiza las métricas principales de población - Censo 2024"""
        poblacion_total = 11312620  # Dato oficial del censo
        superficie_total = self.df['Superficie_km2'].sum()
        densidad_promedio = poblacion_total / superficie_total
        departamento_mayor = self.df.loc[self.df['Población_2024'].idxmax(), 'Departamento']
        crecimiento_total = poblacion_total - 10059856  # vs censo 2012
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card(
                "Población Total", 
                f"{poblacion_total:,}",
                "Censo 2024 🇧🇴"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_metric_card(
                "Crecimiento 2012-2024", 
                f"+{crecimiento_total:,}",
                "habitantes"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_metric_card(
                "Densidad Nacional", 
                f"{densidad_promedio:.2f}",
                "hab/km²"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_metric_card(
                "Departamento Mayor", 
                departamento_mayor,
                f"{self.df.loc[self.df['Población_2024'].idxmax(), 'Población_2024']:,} hab."
            ), unsafe_allow_html=True)
    
    def render_graficos(self, departamentos_seleccionados=None):
        """Renderiza los gráficos de población"""
        if departamentos_seleccionados:
            df_filtrado = self.df[self.df['Departamento'].isin(departamentos_seleccionados)]
        else:
            df_filtrado = self.df
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.subheader("📊 Población por Departamento 2024")
            
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
    
    def render_tabla_datos(self):
        """Renderiza tabla con datos detallados"""
        st.subheader("📋 Datos Detallados de Población - Censo 2024")
        
        # Mostrar datos del censo con todas las métricas
        df_display = self.df.copy()
        
        # Formatear números para mejor visualización
        columnas_formato = ['Población_2024', 'Población_2012', 'Superficie_km2', 'Crecimiento_Absoluto']
        for col in columnas_formato:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"{x:,}")
        
        # Formatear porcentajes
        columnas_porcentaje = ['Crecimiento_%', 'Participación_%']
        for col in columnas_porcentaje:
            if col in df_display.columns:
                df_display[col] = df_display[col].apply(lambda x: f"{x:.2f}%")
        
        # Formatear densidad
        if 'Densidad' in df_display.columns:
            df_display['Densidad'] = df_display['Densidad'].apply(lambda x: f"{x:.2f}")
        
        st.dataframe(
            df_display[['Departamento', 'Población_2024', 'Población_2012', 'Crecimiento_Absoluto',
                       'Crecimiento_%', 'Participación_%', 'Superficie_km2', 'Densidad']],
            use_container_width=True
        )
    
    def render_comparativo_2012_2024(self):
        """Renderiza comparativo específico entre censos 2012 y 2024"""
        st.subheader("🔄 Comparativo Censos 2012 vs 2024")
        
        # Preparar datos para el gráfico comparativo
        df_comparativo = self.df.melt(
            id_vars=['Departamento'],
            value_vars=['Población_2012', 'Población_2024'],
            var_name='Año',
            value_name='Población'
        )
        df_comparativo['Año'] = df_comparativo['Año'].str.replace('Población_', '')
        
        fig_comparativo = px.bar(
            df_comparativo,
            x='Departamento',
            y='Población',
            color='Año',
            barmode='group',
            title="Comparación Poblacional 2012 vs 2024 por Departamento",
            color_discrete_sequence=['#3498db', '#e74c3c']
        )
        
        fig_comparativo.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45,
            yaxis_title="Población (habitantes)"
        )
        
        st.plotly_chart(fig_comparativo, use_container_width=True)
        
        # Tabla con detalles de crecimiento
        st.subheader("📊 Detalle de Crecimiento por Departamento")
        
        df_crecimiento = self.df[['Departamento', 'Población_2012', 'Población_2024', 
                                 'Crecimiento_Absoluto', 'Crecimiento_%', 'Participación_%']].copy()
        df_crecimiento = df_crecimiento.sort_values('Crecimiento_%', ascending=False)
        
        # Formatear números para mejor visualización
        df_display = df_crecimiento.copy()
        df_display['Población_2012'] = df_display['Población_2012'].apply(lambda x: f"{x:,}")
        df_display['Población_2024'] = df_display['Población_2024'].apply(lambda x: f"{x:,}")
        df_display['Crecimiento_Absoluto'] = df_display['Crecimiento_Absoluto'].apply(lambda x: f"+{x:,}")
        df_display['Crecimiento_%'] = df_display['Crecimiento_%'].apply(lambda x: f"{x:.2f}%")
        df_display['Participación_%'] = df_display['Participación_%'].apply(lambda x: f"{x:.2f}%")
        
        st.dataframe(df_display, use_container_width=True)
    
    def render_evolucion_historica(self):
        """Renderiza la evolución poblacional histórica 1950-2024"""
        st.subheader("📈 Evolución Poblacional de Bolivia (1950-2024)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de evolución poblacional
            fig_evolucion = px.bar(
                self.df_historica,
                x='Año',
                y='Población',
                title="Población Total",
                color='Población',
                color_continuous_scale='blues',
                text='Población'
            )
            
            # Formatear texto en las barras
            fig_evolucion.update_traces(
                texttemplate='%{text:,.0f}',
                textposition='outside'
            )
            
            fig_evolucion.update_layout(
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Población (habitantes)",
                showlegend=False
            )
            
            st.plotly_chart(fig_evolucion, use_container_width=True)
        
        with col2:
            # Gráfico de tasas de crecimiento intercensal
            fig_tasas = go.Figure()
            
            # Agregar la línea con marcadores
            fig_tasas.add_trace(go.Scatter(
                x=self.df_tasas['Período'],
                y=self.df_tasas['Tasa_Crecimiento'],
                mode='lines+markers+text',
                text=self.df_tasas['Tasa_Crecimiento'],
                texttemplate='%{text:.3f}',
                textposition='top center',
                line=dict(color='#e74c3c', width=3),
                marker=dict(color='#e74c3c', size=8),
                name='Tasa de Crecimiento'
            ))
            
            fig_tasas.update_layout(
                title="Tasa Crecimiento Intercensal (%)",
                height=400,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                xaxis_title="Período Intercensal",
                yaxis_title="Tasa de Crecimiento (%)",
                yaxis=dict(
                    range=[0, 3.0],
                    tickmode='linear',
                    tick0=0,
                    dtick=0.5
                ),
                xaxis=dict(
                    type='category',
                    tickangle=0
                ),
                showlegend=False
            )
            
            st.plotly_chart(fig_tasas, use_container_width=True)
    
    def render(self, departamentos_seleccionados=None, mostrar_tabla=True, 
               mostrar_comparativo=True, mostrar_historica=True):
        """Renderiza toda la sección de población"""
        st.markdown(render_section_title("Población", "👥"), unsafe_allow_html=True)
        
        # Métricas principales del Censo 2024
        self.render_metricas()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Evolución histórica
        if mostrar_historica:
            self.render_evolucion_historica()
            st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos principales por departamento
        self.render_graficos(departamentos_seleccionados)
        
        # Comparativo 2012 vs 2024
        if mostrar_comparativo:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_comparativo_2012_2024()
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_poblacion = SeccionPoblacion()
