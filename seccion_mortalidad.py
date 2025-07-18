# ========================================
# SECCIÓN MORTALIDAD - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from datos import datos_bolivia
from estilos import render_metric_card, render_section_title

class SeccionMortalidad:
    """Maneja toda la funcionalidad de la sección mortalidad"""
    
    def __init__(self):
        self.df = datos_bolivia.get_datos_mortalidad()
    
    def render_metricas(self):
        """Renderiza las métricas principales de mortalidad"""
        mortalidad_actual = self.df['Tasa_Mortalidad'].iloc[-1]
        esperanza_vida_actual = self.df['Esperanza_Vida'].iloc[-1]
        defunciones_actual = self.df['Defunciones'].iloc[-1]
        
        # Calcular tendencia
        mortalidad_anterior = self.df['Tasa_Mortalidad'].iloc[-2]
        tendencia = "↓" if mortalidad_actual < mortalidad_anterior else "↑"
        
        # Reducción de 4,950 muertes vs 2022
        reduccion_2022 = 92765 - 87815
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card(
                "Tasa de Mortalidad", 
                f"{mortalidad_actual:.2f}‰",
                f"2023 {tendencia} vs 2022"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_metric_card(
                "Defunciones 2023", 
                f"{defunciones_actual:,.0f}",
                "personas"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_metric_card(
                "Reducción vs 2022", 
                f"{reduccion_2022:,.0f}",
                "menos muertes"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_metric_card(
                "Ranking Mundial", 
                "95°",
                "subió 12 posiciones"
            ), unsafe_allow_html=True)
    
    def render_evolucion_temporal(self):
        """Renderiza la evolución temporal de la mortalidad"""
        st.subheader("📈 Evolución de la Tasa de Mortalidad 2012-2023")
        
        fig_evolucion = px.line(
            self.df,
            x='Año',
            y='Tasa_Mortalidad',
            markers=True,
            title="Tasa de Mortalidad General (por mil habitantes) - Bolivia",
            color_discrete_sequence=['#e74c3c']
        )
        
        # Añadir línea de tendencia pre-pandemia
        df_pre_pandemia = self.df[self.df['Año'] <= 2019]
        fig_evolucion.add_scatter(
            x=df_pre_pandemia['Año'],
            y=df_pre_pandemia['Tasa_Mortalidad'].rolling(window=3).mean(),
            mode='lines',
            name='Tendencia pre-pandemia',
            line=dict(dash='dash', color='blue', width=2)
        )
        
        # Destacar picos de pandemia
        fig_evolucion.add_vrect(
            x0=2019.5, x1=2021.5,
            fillcolor="rgba(255,0,0,0.1)",
            layer="below",
            line_width=0,
            annotation_text="Período pandemia",
            annotation_position="top left"
        )
        
        fig_evolucion.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            yaxis_title="Tasa de Mortalidad ‰",
            annotations=[
                dict(
                    x=2023, y=7.17,
                    text="7.17‰<br>(2023)<br>Ranking 95°",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="green"
                ),
                dict(
                    x=2013, y=7.78,
                    text="7.78‰<br>(2013)",
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor="orange"
                )
            ]
        )
        
        st.plotly_chart(fig_evolucion, use_container_width=True)
        
        # Información adicional
        st.info("💡 **Análisis**: Bolivia mejoró 12 posiciones en el ranking mundial de mortalidad (del 107° al 95°). La tasa cayó de 7.68‰ en 2022 a 7.17‰ en 2023, con 4,950 muertes menos.")
    
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
    
    def render_defunciones_evolucion(self):
        """Renderiza la evolución del número de defunciones"""
        st.subheader("⚰️ Evolución del Número de Defunciones")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_defunciones = px.line(
                self.df,
                x='Año',
                y='Defunciones',
                markers=True,
                title="Número Total de Defunciones por Año",
                color_discrete_sequence=['#9b59b6']
            )
            
            fig_defunciones.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Número de Defunciones"
            )
            
            st.plotly_chart(fig_defunciones, use_container_width=True)
        
        with col2:
            # Calcular variación anual
            df_variacion = self.df.copy()
            df_variacion['Variacion_Anual'] = df_variacion['Defunciones'].pct_change() * 100
            
            fig_variacion = px.bar(
                df_variacion[1:],  # Excluir primer año sin variación
                x='Año',
                y='Variacion_Anual',
                title="Variación Anual de Defunciones (%)",
                color='Variacion_Anual',
                color_continuous_scale='RdYlBu_r'
            )
            
            fig_variacion.update_layout(
                height=350,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                yaxis_title="Variación %"
            )
            
            st.plotly_chart(fig_variacion, use_container_width=True)
    
    def render_analisis_comparativo(self):
        """Renderiza análisis comparativo de indicadores"""
        st.subheader("📊 Análisis Comparativo: Mortalidad vs Esperanza de Vida")
        
        # Crear figura con dos ejes Y
        fig_comparativo = go.Figure()
        
        # Eje izquierdo - Tasa de Mortalidad
        fig_comparativo.add_trace(go.Scatter(
            x=self.df['Año'],
            y=self.df['Tasa_Mortalidad'],
            mode='lines+markers',
            name='Tasa de Mortalidad (‰)',
            line=dict(color='red', width=3),
            yaxis='y'
        ))
        
        # Eje derecho - Esperanza de Vida
        fig_comparativo.add_trace(go.Scatter(
            x=self.df['Año'],
            y=self.df['Esperanza_Vida'],
            mode='lines+markers',
            name='Esperanza de Vida (años)',
            line=dict(color='green', width=3),
            yaxis='y2'
        ))
        
        fig_comparativo.update_layout(
            title="Relación Inversa: Mortalidad vs Esperanza de Vida (2012-2023)",
            xaxis_title="Año",
            yaxis=dict(
                title="Tasa de Mortalidad (‰)",
                side="left",
                color="red"
            ),
            yaxis2=dict(
                title="Esperanza de Vida (años)",
                side="right",
                overlaying="y",
                color="green"
            ),
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            legend=dict(x=0.02, y=0.98)
        )
        
        st.plotly_chart(fig_comparativo, use_container_width=True)
        
        # Correlación
        correlacion = self.df['Tasa_Mortalidad'].corr(self.df['Esperanza_Vida'])
        st.info(f"📈 **Correlación**: {correlacion:.3f} - {'Relación inversa fuerte' if correlacion < -0.5 else 'Relación inversa moderada' if correlacion < -0.3 else 'Relación inversa débil'} entre mortalidad y esperanza de vida.")
    
    def render_tabla_datos(self):
        """Renderiza tabla con datos detallados"""
        st.subheader("📋 Datos Históricos de Mortalidad INE Bolivia")
        
        df_tabla = self.df.copy()
        df_tabla['Cambio_Tasa'] = df_tabla['Tasa_Mortalidad'].diff().round(2)
        df_tabla['Cambio_Esperanza'] = df_tabla['Esperanza_Vida'].diff().round(1)
        
        # Formatear columnas
        df_mostrar = df_tabla.copy()
        df_mostrar['Defunciones'] = df_mostrar['Defunciones'].apply(lambda x: f"{x:,.0f}")
        df_mostrar['Tasa_Mortalidad'] = df_mostrar['Tasa_Mortalidad'].apply(lambda x: f"{x:.2f}‰")
        df_mostrar['Esperanza_Vida'] = df_mostrar['Esperanza_Vida'].apply(lambda x: f"{x:.1f}")
        df_mostrar['Cambio_Tasa'] = df_mostrar['Cambio_Tasa'].apply(lambda x: f"{x:+.2f}‰" if pd.notna(x) else "-")
        
        st.dataframe(
            df_mostrar[['Año', 'Defunciones', 'Tasa_Mortalidad', 'Cambio_Tasa', 
                       'Esperanza_Vida']].rename(columns={
                'Defunciones': 'Total Defunciones',
                'Tasa_Mortalidad': 'Tasa Mortalidad',
                'Cambio_Tasa': 'Δ Tasa',
                'Esperanza_Vida': 'Esperanza Vida'
            }),
            use_container_width=True
        )
    
    def render(self, mostrar_defunciones=True, mostrar_comparativo=True, mostrar_tabla=True):
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
        
        if mostrar_defunciones:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_defunciones_evolucion()
        
        if mostrar_comparativo:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_analisis_comparativo()
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_mortalidad = SeccionMortalidad()
