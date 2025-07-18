# ========================================
# SECCIÓN DATOS ELECTORALES - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datos import datos_bolivia
from estilos import render_metric_card, render_section_title

class SeccionDatosElectorales:
    """Maneja toda la funcionalidad de la sección datos electorales"""
    
    def __init__(self):
        self.df = datos_bolivia.get_datos_electorales()
    
    def render_metricas(self):
        """Renderiza las métricas principales de datos electorales"""
        habilitados_total = self.df['Habilitados_2025'].sum()
        inhabilitados_total = self.df['Inhabilitados'].sum()
        depurados_total = self.df['Depurados'].sum()
        nuevos_total = self.df['Nuevos_Registros'].sum()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card(
                "Habilitados 2025", 
                f"{habilitados_total:,.0f}",
                "Votantes activos"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_metric_card(
                "Inhabilitados", 
                f"{inhabilitados_total:,.0f}",
                "Registros"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_metric_card(
                "Depurados", 
                f"{depurados_total:,.0f}",
                "Limpieza padrón"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_metric_card(
                "Nuevos Registros", 
                f"{nuevos_total:,.0f}",
                "Jóvenes 2025"
            ), unsafe_allow_html=True)
    
    def render_graficos_principales(self, departamentos_seleccionados=None):
        """Renderiza los gráficos principales de datos electorales"""
        if departamentos_seleccionados:
            df_filtrado = self.df[self.df['Departamento'].isin(departamentos_seleccionados)]
        else:
            df_filtrado = self.df
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("🗳️ Votantes Habilitados por Departamento")
            
            fig_habilitados = px.bar(
                df_filtrado.sort_values('Habilitados_2025'),
                x='Habilitados_2025',
                y='Departamento',
                orientation='h',
                color='Habilitados_2025',
                color_continuous_scale='greens',
                text='Habilitados_2025'
            )
            
            fig_habilitados.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_habilitados.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Votantes Habilitados",
                yaxis_title="",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_habilitados, use_container_width=True)
        
        with col2:
            st.subheader("📊 Porcentaje de Habilitación")
            
            fig_porcentaje = px.bar(
                df_filtrado.sort_values('Porcentaje_Habilitados'),
                x='Porcentaje_Habilitados',
                y='Departamento',
                orientation='h',
                color='Porcentaje_Habilitados',
                color_continuous_scale='blues',
                text='Porcentaje_Habilitados'
            )
            
            fig_porcentaje.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_porcentaje.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="% Habilitados",
                yaxis_title="",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_porcentaje, use_container_width=True)
    
    def render_analisis_depuracion(self):
        """Renderiza análisis de depuración del padrón"""
        st.subheader("🔍 Análisis de Depuración del Padrón")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_depurados = px.pie(
                self.df,
                values='Depurados',
                names='Departamento',
                title="Distribución de Registros Depurados",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_depurados.update_traces(textposition='inside', textinfo='percent+label')
            fig_depurados.update_layout(
                height=400,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_depurados, use_container_width=True)
        
        with col2:
            fig_inhabilitados = px.bar(
                self.df.sort_values('Inhabilitados'),
                x='Inhabilitados',
                y='Departamento',
                orientation='h',
                color='Inhabilitados',
                color_continuous_scale='reds',
                title="Registros Inhabilitados por Departamento",
                text='Inhabilitados'
            )
            
            fig_inhabilitados.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig_inhabilitados.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_inhabilitados, use_container_width=True)
    
    def render_nuevos_votantes(self):
        """Renderiza análisis de nuevos votantes"""
        st.subheader("🆕 Nuevos Votantes 2025")
        
        fig_nuevos = px.bar(
            self.df.sort_values('Nuevos_Registros', ascending=False),
            x='Departamento',
            y='Nuevos_Registros',
            color='Nuevos_Registros',
            color_continuous_scale='viridis',
            title="Jóvenes que Alcanzan Mayoría de Edad para Votar",
            text='Nuevos_Registros'
        )
        
        fig_nuevos.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig_nuevos.update_layout(
            height=400,
            showlegend=False,
            xaxis_tickangle=-45,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_nuevos, use_container_width=True)
    
    def render_comparativo_padron(self):
        """Renderiza comparativo del padrón electoral"""
        st.subheader("⚖️ Comparativo del Padrón Electoral")
        
        # Preparar datos para el gráfico stacked
        df_stack = self.df.copy()
        
        fig_stack = go.Figure()
        
        fig_stack.add_trace(go.Bar(
            name='Habilitados',
            x=df_stack['Departamento'],
            y=df_stack['Habilitados_2025'],
            marker_color='green'
        ))
        
        fig_stack.add_trace(go.Bar(
            name='Inhabilitados',
            x=df_stack['Departamento'],
            y=df_stack['Inhabilitados'],
            marker_color='red'
        ))
        
        fig_stack.update_layout(
            barmode='stack',
            title="Composición del Padrón Electoral por Departamento",
            xaxis_title="Departamento",
            yaxis_title="Número de Registros",
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_stack, use_container_width=True)
    
    def render_metricas_participacion(self):
        """Renderiza métricas de participación electoral"""
        st.subheader("📈 Métricas de Participación")
        
        # Calcular métricas adicionales
        df_metricas = self.df.copy()
        df_metricas['Tasa_Depuración_%'] = (df_metricas['Depurados'] / df_metricas['Total_Padrón']) * 100
        df_metricas['Tasa_Inhabilitación_%'] = (df_metricas['Inhabilitados'] / df_metricas['Total_Padrón']) * 100
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_depuracion = px.bar(
                df_metricas.sort_values('Tasa_Depuración_%'),
                x='Tasa_Depuración_%',
                y='Departamento',
                orientation='h',
                title="Tasa de Depuración (%)",
                color='Tasa_Depuración_%',
                color_continuous_scale='oranges'
            )
            
            fig_depuracion.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_depuracion, use_container_width=True)
        
        with col2:
            fig_inhabilitacion = px.bar(
                df_metricas.sort_values('Tasa_Inhabilitación_%'),
                x='Tasa_Inhabilitación_%',
                y='Departamento',
                orientation='h',
                title="Tasa de Inhabilitación (%)",
                color='Tasa_Inhabilitación_%',
                color_continuous_scale='reds'
            )
            
            fig_inhabilitacion.update_layout(
                height=350,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_inhabilitacion, use_container_width=True)
    
    def render_tabla_datos(self):
        """Renderiza tabla con datos detallados"""
        st.subheader("📋 Datos Detallados Electorales")
        st.dataframe(
            self.df[['Departamento', 'Habilitados_2025', 'Inhabilitados', 'Depurados', 
                    'Nuevos_Registros', 'Porcentaje_Habilitados']],
            use_container_width=True
        )
    
    def render(self, departamentos_seleccionados=None, mostrar_depuracion=True, 
               mostrar_nuevos=True, mostrar_comparativo=True, mostrar_tabla=True):
        """Renderiza toda la sección de datos electorales"""
        st.markdown(render_section_title("Datos Electorales 2025", "🗳️"), unsafe_allow_html=True)
        
        # Métricas
        self.render_metricas()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos principales
        self.render_graficos_principales(departamentos_seleccionados)
        
        if mostrar_depuracion:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_analisis_depuracion()
        
        if mostrar_nuevos:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_nuevos_votantes()
        
        if mostrar_comparativo:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_comparativo_padron()
        
        st.markdown("<br>", unsafe_allow_html=True)
        self.render_metricas_participacion()
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_datos_electorales = SeccionDatosElectorales()
