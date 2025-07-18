# ========================================
# SECCIÓN DESEMPLEO - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datos import datos_bolivia
from estilos import render_metric_card, render_section_title

class SeccionDesempleo:
    """Maneja toda la funcionalidad de la sección desempleo EPA Bolivia"""
    
    def __init__(self):
        self.df_tasas, self.df_parados, self.df_historicos = datos_bolivia.get_datos_desempleo()
    
    def render_metricas(self):
        """Renderiza las métricas principales EPA II Trimestre 2024"""
        tasa_total = 2.8
        tasa_hombres = 2.3
        tasa_mujeres = 3.3
        parados_total = 195
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card(
                "Tasa de Desempleo", 
                f"{tasa_total}%",
                "EPA II Trim 2024 🇧🇴"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_metric_card(
                "Desempleo Hombres", 
                f"{tasa_hombres}%",
                "EPA 2024"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_metric_card(
                "Desempleo Mujeres", 
                f"{tasa_mujeres}%",
                "EPA 2024"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_metric_card(
                "Total Parados", 
                f"{parados_total}k",
                "personas desempleadas"
            ), unsafe_allow_html=True)
    
    def render_graficos(self):
        """Renderiza los gráficos de desempleo EPA"""
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📊 Tasa de Paro por Sexo y Edad")
            
            # Preparar datos para el gráfico
            categorias = ['Tasa de\ndesempleo', 'Paro menores\nde 25 años', 'Paro mayores\nde 24 años', 
                         'Paro entre 25\ny 54 años', 'Paro mayores\nde 54 años']
            
            fig_tasas = go.Figure()
            
            # Agregar barras para cada categoría
            fig_tasas.add_trace(go.Bar(
                name='Total',
                x=categorias,
                y=self.df_tasas['Total_%'],
                marker_color='#3498db',
                text=self.df_tasas['Total_%'],
                texttemplate='%{text:.1f}%',
                textposition='outside'
            ))
            
            fig_tasas.add_trace(go.Bar(
                name='Hombres',
                x=categorias,
                y=self.df_tasas['Hombres_%'],
                marker_color='#e74c3c',
                text=self.df_tasas['Hombres_%'],
                texttemplate='%{text:.1f}%',
                textposition='outside'
            ))
            
            fig_tasas.add_trace(go.Bar(
                name='Mujeres',
                x=categorias,
                y=self.df_tasas['Mujeres_%'],
                marker_color='#f39c12',
                text=self.df_tasas['Mujeres_%'],
                texttemplate='%{text:.1f}%',
                textposition='outside'
            ))
            
            fig_tasas.update_layout(
                height=400,
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Tasa de Paro (%)",
                xaxis_tickangle=-45,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig_tasas, use_container_width=True)
        
        with col2:
            st.subheader("� Número de Desempleados")
            
            # Gráfico de parados en miles
            categorias_parados = ['Parados', 'Parados menores\nde 25 años', 'Parados mayores\nde 24 años', 
                                 'Paro entre 25y\n54 años', 'Parados mayores\nde 55 años']
            
            fig_parados = go.Figure()
            
            fig_parados.add_trace(go.Bar(
                name='Total',
                x=categorias_parados,
                y=self.df_parados['Total_miles'],
                marker_color='#3498db',
                text=self.df_parados['Total_miles'],
                texttemplate='%{text}k',
                textposition='outside'
            ))
            
            fig_parados.add_trace(go.Bar(
                name='Hombres',
                x=categorias_parados,
                y=self.df_parados['Hombres_miles'],
                marker_color='#e74c3c',
                text=self.df_parados['Hombres_miles'],
                texttemplate='%{text}k',
                textposition='outside'
            ))
            
            fig_parados.add_trace(go.Bar(
                name='Mujeres',
                x=categorias_parados,
                y=self.df_parados['Mujeres_miles'],
                marker_color='#f39c12',
                text=self.df_parados['Mujeres_miles'],
                texttemplate='%{text}k',
                textposition='outside'
            ))
            
            fig_parados.update_layout(
                height=400,
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Parados (miles)",
                xaxis_tickangle=-45,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig_parados, use_container_width=True)
    
    def render_comparativo_temporal(self):
        """Renderiza comparativo histórico EPA 2022-2024"""
        st.subheader("� Evolución Histórica EPA Bolivia")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Gráfico de evolución de tasas generales
            fig_evolucion = go.Figure()
            
            fig_evolucion.add_trace(go.Bar(
                name='2023',
                x=['Tasa desempleo\n(EPA)', 'Tasa desempleo\nhombres (EPA)', 'Tasa desempleo\nmujeres (EPA)'],
                y=[2.9, 2.6, 3.2],
                marker_color='#3498db',
                text=[2.9, 2.6, 3.2],
                texttemplate='%{text:.1f}%',
                textposition='outside'
            ))
            
            fig_evolucion.add_trace(go.Bar(
                name='2022',
                x=['Tasa desempleo\n(EPA)', 'Tasa desempleo\nhombres (EPA)', 'Tasa desempleo\nmujeres (EPA)'],
                y=[3.3, 2.9, 3.7],
                marker_color='#e74c3c',
                text=[3.3, 2.9, 3.7],
                texttemplate='%{text:.1f}%',
                textposition='outside'
            ))
            
            fig_evolucion.update_layout(
                title="EPA: Paro",
                height=400,
                barmode='group',
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Tasa de Paro (%)",
                xaxis_tickangle=0,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            
            st.plotly_chart(fig_evolucion, use_container_width=True)
        
        with col2:
            # Tabla de datos históricos detallados
            st.subheader("📋 Datos Históricos Detallados")
            
            # Preparar datos para mostrar
            datos_tabla = {
                '': ['Tasa de desempleo (EPA)', 'Tasa de desempleo hombres (EPA)', 
                     'Tasa de desempleo mujeres (EPA)', 'Paro menores de 25 años',
                     'Paro hombres menores de 25', 'Paro mujeres menores de 25',
                     'Paro mayores de 24 años', 'Paro hombres mayores de 24',
                     'Paro mujeres mayores de 24 años', 'Paro entre 25 y 54 años',
                     'Paro hombres entre 25 y 54', 'Paro mujeres entre 25 y 54',
                     'Paro mayores de 54 años', 'Paro hombres mayores de 54',
                     'Paro mujeres mayores de 54'],
                '2023': ['2,9%', '2,6%', '3,2%', '4,6%', '4,3%', '5,0%', '2,4%', '2,2%', 
                        '2,7%', '2,9%', '2,4%', '3,4%', '1,1%', '1,4%', '0,8%'],
                '2022': ['3,3%', '2,9%', '3,7%', '5,6%', '5,2%', '6,1%', '2,7%', '2,3%',
                        '3,1%', '3,1%', '2,5%', '3,8%', '1,3%', '1,6%', '0,9%']
            }
            
            df_tabla_historica = pd.DataFrame(datos_tabla)
            st.dataframe(df_tabla_historica, use_container_width=True, hide_index=True)
    
    def render_tabla_datos(self):
        """Renderiza tabla con datos detallados EPA II Trimestre 2024"""
        st.subheader("� EPA - Paro Bolivia II Trimestre 2024")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("📈 Tasas de Paro (%)")
            # Mostrar tabla de tasas
            df_tasas_display = self.df_tasas.copy()
            df_tasas_display.columns = ['', 'Total', 'Hombres', 'Mujeres']
            df_tasas_display['Total'] = df_tasas_display['Total'].apply(lambda x: f"{x}%")
            df_tasas_display['Hombres'] = df_tasas_display['Hombres'].apply(lambda x: f"{x}%")
            df_tasas_display['Mujeres'] = df_tasas_display['Mujeres'].apply(lambda x: f"{x}%")
            
            st.dataframe(df_tasas_display, use_container_width=True, hide_index=True)
        
        with col2:
            st.subheader("👥 Parados (miles)")
            # Mostrar tabla de parados
            df_parados_display = self.df_parados.copy()
            df_parados_display.columns = ['', 'Total', 'Hombres', 'Mujeres']
            df_parados_display['Total'] = df_parados_display['Total'].apply(lambda x: f"{x} k")
            df_parados_display['Hombres'] = df_parados_display['Hombres'].apply(lambda x: f"{x} k")
            df_parados_display['Mujeres'] = df_parados_display['Mujeres'].apply(lambda x: f"{x} k")
            
            st.dataframe(df_parados_display, use_container_width=True, hide_index=True)
    
    def render(self, mostrar_comparativo=True, mostrar_tabla=True):
        """Renderiza toda la sección de desempleo EPA Bolivia"""
        st.markdown(render_section_title("Empleo y Paro", "💼"), unsafe_allow_html=True)
        
        # Métricas principales EPA
        self.render_metricas()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos principales por sexo y edad
        self.render_graficos()
        
        if mostrar_comparativo:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_comparativo_temporal()
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_desempleo = SeccionDesempleo()
