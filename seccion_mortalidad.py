# ========================================
# SECCIÓN MORTALIDAD - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datos import datos_bolivia
from estilos import render_metric_card, render_section_title

class SeccionMortalidad:
    """Maneja toda la funcionalidad de la sección mortalidad"""
    
    def __init__(self):
        self.df = datos_bolivia.get_datos_mortalidad()
    
    def render_metricas(self):
        """Renderiza las métricas principales de mortalidad"""
        mortalidad_actual = self.df['Mortalidad_General'].iloc[-1]
        esperanza_vida_actual = self.df['Esperanza_Vida'].iloc[-1]
        covid_actual = self.df['Mortalidad_COVID'].iloc[-1]
        
        # Calcular tendencia
        mortalidad_anterior = self.df['Mortalidad_General'].iloc[-2]
        tendencia = "↓" if mortalidad_actual < mortalidad_anterior else "↑"
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card(
                "Mortalidad General", 
                f"{mortalidad_actual:.1f}‰",
                f"2024 {tendencia}"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_metric_card(
                "Esperanza de Vida", 
                f"{esperanza_vida_actual:.1f}",
                "años"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_metric_card(
                "Muertes COVID-19", 
                f"{covid_actual:,.0f}",
                "2024"
            ), unsafe_allow_html=True)
        
        with col4:
            reduccion_covid = ((self.df['Mortalidad_COVID'].iloc[0] - covid_actual) / self.df['Mortalidad_COVID'].iloc[0]) * 100
            st.markdown(render_metric_card(
                "Reducción COVID", 
                f"{reduccion_covid:.1f}%",
                "vs 2020"
            ), unsafe_allow_html=True)
    
    def render_evolucion_temporal(self):
        """Renderiza la evolución temporal de la mortalidad"""
        st.subheader("📈 Evolución de la Mortalidad General")
        
        fig_evolucion = px.line(
            self.df,
            x='Año',
            y='Mortalidad_General',
            markers=True,
            title="Tasa de Mortalidad General (por mil habitantes)",
            color_discrete_sequence=['#e74c3c']
        )
        
        fig_evolucion.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Mortalidad ‰"
        )
        
        st.plotly_chart(fig_evolucion, use_container_width=True)
    
    def render_esperanza_vida(self):
        """Renderiza la evolución de la esperanza de vida"""
        st.subheader("🎯 Evolución de la Esperanza de Vida")
        
        fig_esperanza = px.line(
            self.df,
            x='Año',
            y='Esperanza_Vida',
            markers=True,
            title="Esperanza de Vida al Nacer (años)",
            color_discrete_sequence=['#2ecc71']
        )
        
        fig_esperanza.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Años"
        )
        
        st.plotly_chart(fig_esperanza, use_container_width=True)
    
    def render_covid_evolucion(self):
        """Renderiza la evolución de muertes por COVID-19"""
        st.subheader("🦠 Evolución Muertes por COVID-19")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_covid_line = px.line(
                self.df,
                x='Año',
                y='Mortalidad_COVID',
                markers=True,
                title="Muertes por COVID-19 por Año",
                color_discrete_sequence=['#9b59b6']
            )
            
            fig_covid_line.update_layout(
                height=300,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_covid_line, use_container_width=True)
        
        with col2:
            fig_covid_bar = px.bar(
                self.df,
                x='Año',
                y='Mortalidad_COVID',
                title="Distribución Anual Muertes COVID-19",
                color='Mortalidad_COVID',
                color_continuous_scale='reds'
            )
            
            fig_covid_bar.update_layout(
                height=300,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_covid_bar, use_container_width=True)
    
    def render_analisis_comparativo(self):
        """Renderiza análisis comparativo de indicadores"""
        st.subheader("📊 Análisis Comparativo de Indicadores")
        
        # Normalizar datos para comparación
        df_normalizado = self.df.copy()
        df_normalizado['Mortalidad_Norm'] = (df_normalizado['Mortalidad_General'] - df_normalizado['Mortalidad_General'].min()) / (df_normalizado['Mortalidad_General'].max() - df_normalizado['Mortalidad_General'].min()) * 100
        df_normalizado['Esperanza_Norm'] = (df_normalizado['Esperanza_Vida'] - df_normalizado['Esperanza_Vida'].min()) / (df_normalizado['Esperanza_Vida'].max() - df_normalizado['Esperanza_Vida'].min()) * 100
        
        fig_comparativo = go.Figure()
        
        fig_comparativo.add_trace(go.Scatter(
            x=df_normalizado['Año'],
            y=df_normalizado['Mortalidad_Norm'],
            mode='lines+markers',
            name='Mortalidad (normalizada)',
            line=dict(color='red')
        ))
        
        fig_comparativo.add_trace(go.Scatter(
            x=df_normalizado['Año'],
            y=df_normalizado['Esperanza_Norm'],
            mode='lines+markers',
            name='Esperanza de Vida (normalizada)',
            line=dict(color='green')
        ))
        
        fig_comparativo.update_layout(
            title="Comparación Normalizada: Mortalidad vs Esperanza de Vida",
            xaxis_title="Año",
            yaxis_title="Valor Normalizado (0-100)",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_comparativo, use_container_width=True)
    
    def render_tabla_datos(self):
        """Renderiza tabla con datos detallados"""
        st.subheader("📋 Datos Detallados de Mortalidad")
        
        df_tabla = self.df.copy()
        df_tabla['Cambio_Mortalidad'] = df_tabla['Mortalidad_General'].diff()
        df_tabla['Cambio_Esperanza'] = df_tabla['Esperanza_Vida'].diff()
        
        st.dataframe(
            df_tabla[['Año', 'Mortalidad_General', 'Cambio_Mortalidad', 
                     'Esperanza_Vida', 'Cambio_Esperanza', 'Mortalidad_COVID']],
            use_container_width=True
        )
    
    def render(self, mostrar_covid=True, mostrar_comparativo=True, mostrar_tabla=True):
        """Renderiza toda la sección de mortalidad"""
        st.markdown(render_section_title("Mortalidad y Esperanza de Vida", "⚰️"), unsafe_allow_html=True)
        
        # Métricas
        self.render_metricas()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos principales
        col1, col2 = st.columns(2)
        
        with col1:
            self.render_evolucion_temporal()
        
        with col2:
            self.render_esperanza_vida()
        
        if mostrar_covid:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_covid_evolucion()
        
        if mostrar_comparativo:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_analisis_comparativo()
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_mortalidad = SeccionMortalidad()
