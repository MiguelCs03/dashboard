# ========================================
# SECCIÓN FECUNDIDAD - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datos import datos_bolivia
from estilos import render_metric_card, render_section_title

class SeccionFecundidad:
    """Maneja toda la funcionalidad de la sección fecundidad Bolivia"""
    
    def __init__(self):
        self.df_departamental, self.df_historicos, self.df_edad_madre = datos_bolivia.get_datos_fecundidad()
    
    def render_metricas(self):
        """Renderiza las métricas principales de fecundidad 2024"""
        tasa_fecundidad_nacional = 2.5  # TFG Nacional 2024
        nacimientos_total = self.df_departamental['Nacimientos_2024'].sum()
        mortalidad_infantil_nacional = 22.9  # Por mil nacidos vivos
        tasa_natalidad_nacional = 18.2  # Por mil habitantes
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card(
                "Tasa Fecundidad Global", 
                f"{tasa_fecundidad_nacional}",
                "hijos por mujer 🇧🇴"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_metric_card(
                "Nacimientos 2024", 
                f"{nacimientos_total:,.0f}",
                "total nacional"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_metric_card(
                "Mortalidad Infantil", 
                f"{mortalidad_infantil_nacional}‰",
                "por mil nacidos vivos"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_metric_card(
                "Tasa de Natalidad", 
                f"{tasa_natalidad_nacional}‰",
                "por mil habitantes"
            ), unsafe_allow_html=True)
    
    def render_graficos(self, departamentos_seleccionados=None):
        """Renderiza los gráficos de fecundidad por departamento"""
        if departamentos_seleccionados:
            df_filtrado = self.df_departamental[self.df_departamental['Departamento'].isin(departamentos_seleccionados)]
        else:
            df_filtrado = self.df_departamental
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("👶 Tasa Fecundidad Global por Departamento")
            
            fig_fecundidad = px.bar(
                df_filtrado.sort_values('Tasa_Fecundidad_Global'),
                x='Tasa_Fecundidad_Global',
                y='Departamento',
                orientation='h',
                color='Tasa_Fecundidad_Global',
                color_continuous_scale='viridis',
                text='Tasa_Fecundidad_Global',
                title="Hijos por mujer por departamento"
            )
            
            fig_fecundidad.update_traces(texttemplate='%{text:.1f}', textposition='outside')
            fig_fecundidad.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Tasa de Fecundidad Global",
                yaxis_title="",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_fecundidad, use_container_width=True)
        
        with col2:
            st.subheader("⚰️ Mortalidad Infantil por Departamento")
            
            fig_mortalidad = px.bar(
                df_filtrado.sort_values('Mortalidad_Infantil_x1000'),
                x='Mortalidad_Infantil_x1000',
                y='Departamento',
                orientation='h',
                color='Mortalidad_Infantil_x1000',
                color_continuous_scale='reds',
                text='Mortalidad_Infantil_x1000',
                title="Por mil nacidos vivos"
            )
            
            fig_mortalidad.update_traces(texttemplate='%{text:.1f}‰', textposition='outside')
            fig_mortalidad.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Mortalidad Infantil (‰)",
                yaxis_title="",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_mortalidad, use_container_width=True)
    
    def render_evolucion_historica(self):
        """Renderiza la evolución histórica de indicadores de fecundidad"""
        st.subheader("📈 Evolución Histórica de Indicadores (2010-2024)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Evolución de la Tasa de Fecundidad Global
            fig_tfg = px.line(
                self.df_historicos,
                x='Año',
                y='Tasa_Fecundidad_Global',
                markers=True,
                title="Evolución Tasa de Fecundidad Global",
                color_discrete_sequence=['#e74c3c']
            )
            
            fig_tfg.update_traces(
                mode='lines+markers+text',
                text=self.df_historicos['Tasa_Fecundidad_Global'],
                texttemplate='%{text:.1f}',
                textposition='top center'
            )
            
            fig_tfg.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Hijos por mujer",
                yaxis=dict(range=[2.0, 4.0])
            )
            
            st.plotly_chart(fig_tfg, use_container_width=True)
        
        with col2:
            # Evolución de la Mortalidad Infantil
            fig_mi = px.line(
                self.df_historicos,
                x='Año',
                y='Mortalidad_Infantil_x1000',
                markers=True,
                title="Evolución Mortalidad Infantil",
                color_discrete_sequence=['#3498db']
            )
            
            fig_mi.update_traces(
                mode='lines+markers+text',
                text=self.df_historicos['Mortalidad_Infantil_x1000'],
                texttemplate='%{text:.1f}‰',
                textposition='top center'
            )
            
            fig_mi.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Por mil nacidos vivos",
                yaxis=dict(range=[20, 45])
            )
            
            st.plotly_chart(fig_mi, use_container_width=True)
    
    def render_fecundidad_por_edad(self):
        """Renderiza análisis de fecundidad por edad de la madre"""
        st.subheader("👩‍🍼 Fecundidad por Edad de la Madre")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras de tasas por edad
            fig_edad = px.bar(
                self.df_edad_madre,
                x='Grupo_Edad',
                y='Tasa_Fecundidad_2024',
                title="Tasa de Fecundidad por Grupo de Edad (2024)",
                color='Tasa_Fecundidad_2024',
                color_continuous_scale='viridis',
                text='Tasa_Fecundidad_2024'
            )
            
            fig_edad.update_traces(texttemplate='%{text}‰', textposition='outside')
            fig_edad.update_layout(
                height=350,
                showlegend=False,
                xaxis_title="Edad de la Madre",
                yaxis_title="Tasa por mil mujeres del grupo",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_edad, use_container_width=True)
        
        with col2:
            # Distribución porcentual de nacimientos
            fig_distribucion = px.pie(
                self.df_edad_madre,
                values='Porcentaje_Nacimientos',
                names='Grupo_Edad',
                title="Distribución de Nacimientos por Edad Materna (%)"
            )
            
            fig_distribucion.update_traces(textposition='inside', textinfo='percent+label')
            fig_distribucion.update_layout(
                height=350,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_distribucion, use_container_width=True)
    
    def render_comparativo_natalidad(self):
        """Renderiza comparativo de natalidad departamental"""
        st.subheader("🏥 Tasa de Natalidad por Departamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de barras de natalidad
            fig_natalidad = px.bar(
                self.df_departamental.sort_values('Tasa_Natalidad_x1000', ascending=False),
                x='Departamento',
                y='Tasa_Natalidad_x1000',
                color='Tasa_Natalidad_x1000',
                color_continuous_scale='blues',
                title="Tasa de Natalidad por Departamento (‰)",
                text='Tasa_Natalidad_x1000'
            )
            
            fig_natalidad.update_traces(texttemplate='%{text:.1f}‰', textposition='outside')
            fig_natalidad.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Departamento",
                yaxis_title="Por mil habitantes",
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_natalidad, use_container_width=True)
        
        with col2:
            # Gráfico de dispersión: Fecundidad vs Mortalidad Infantil
            fig_correlacion = px.scatter(
                self.df_departamental,
                x='Tasa_Fecundidad_Global',
                y='Mortalidad_Infantil_x1000',
                size='Nacimientos_2024',
                color='Tasa_Natalidad_x1000',
                hover_name='Departamento',
                title="Fecundidad vs Mortalidad Infantil",
                color_continuous_scale='reds'
            )
            
            fig_correlacion.update_layout(
                height=400,
                xaxis_title="Tasa de Fecundidad Global",
                yaxis_title="Mortalidad Infantil (‰)",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_correlacion, use_container_width=True)
    
    def render_tabla_datos(self):
        """Renderiza tablas con datos detallados"""
        st.subheader("📊 Datos Detallados de Fecundidad")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Datos por Departamento 2024**")
            df_display = self.df_departamental.copy()
            df_display['Nacimientos_2024'] = df_display['Nacimientos_2024'].apply(lambda x: f"{x:,}")
            df_display.columns = ['Departamento', 'TFG', 'Nacimientos', 'Mort. Infantil ‰', 'Natalidad ‰']
            st.dataframe(df_display, use_container_width=True, hide_index=True)
        
        with col2:
            st.markdown("**Evolución Histórica Nacional**")
            df_historicos_display = self.df_historicos.copy()
            df_historicos_display.columns = ['Año', 'TFG', 'Natalidad ‰', 'Mort. Infantil ‰']
            st.dataframe(df_historicos_display, use_container_width=True, hide_index=True)
    
    def render(self, departamentos_seleccionados=None, mostrar_correlacion=True, mostrar_tabla=True):
        """Renderiza toda la sección de fecundidad"""
        st.markdown(render_section_title("Fecundidad y Natalidad", "👶"), unsafe_allow_html=True)
        
        # Métricas principales
        self.render_metricas()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Evolución histórica
        self.render_evolucion_historica()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos principales por departamento
        self.render_graficos(departamentos_seleccionados)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Fecundidad por edad de la madre
        self.render_fecundidad_por_edad()
        
        if mostrar_correlacion:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_comparativo_natalidad()
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_fecundidad = SeccionFecundidad()
