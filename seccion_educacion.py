# ========================================
# SECCIÓN EDUCACIÓN - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from datos import datos_bolivia
from estilos import render_metric_card, render_section_title

class SeccionEducacion:
    """Maneja toda la funcionalidad de la sección educación"""
    
    def __init__(self):
        self.df_temporal, self.df_departamental = datos_bolivia.get_datos_educacion()
    
    def render_metricas(self):
        """Renderiza las métricas principales de educación"""
        alfabetizacion_actual = self.df_temporal['Alfabetización_%'].iloc[-1]
        analfabetismo_actual = self.df_temporal['Analfabetismo_%'].iloc[-1]
        
        # Métricas departamentales
        secundaria_promedio = self.df_departamental['Secundaria_Completa_%'].mean()
        universitaria_promedio = self.df_departamental['Universitaria_%'].mean()
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(render_metric_card(
                "Alfabetización", 
                f"{alfabetizacion_actual:.1f}%",
                "Nacional 2024"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(render_metric_card(
                "Analfabetismo", 
                f"{analfabetismo_actual:.1f}%",
                "Nacional 2024"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(render_metric_card(
                "Secundaria Completa", 
                f"{secundaria_promedio:.1f}%",
                "Promedio nacional"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(render_metric_card(
                "Educación Universitaria", 
                f"{universitaria_promedio:.1f}%",
                "Promedio nacional"
            ), unsafe_allow_html=True)
    
    def render_evolucion_alfabetizacion(self):
        """Renderiza la evolución de la alfabetización"""
        st.subheader("📈 Evolución de la Alfabetización 2015-2024")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_alfabetizacion = px.line(
                self.df_temporal,
                x='Año',
                y='Alfabetización_%',
                markers=True,
                title="Tasa de Alfabetización (%)",
                color_discrete_sequence=['#2ecc71']
            )
            
            fig_alfabetizacion.update_layout(
                height=350,
                yaxis=dict(range=[94, 97]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_alfabetizacion, use_container_width=True)
        
        with col2:
            fig_analfabetismo = px.line(
                self.df_temporal,
                x='Año',
                y='Analfabetismo_%',
                markers=True,
                title="Tasa de Analfabetismo (%)",
                color_discrete_sequence=['#e74c3c']
            )
            
            fig_analfabetismo.update_layout(
                height=350,
                yaxis=dict(range=[3, 5]),
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_analfabetismo, use_container_width=True)
    
    def render_educacion_departamental(self, departamentos_seleccionados=None):
        """Renderiza educación por departamento"""
        if departamentos_seleccionados:
            df_filtrado = self.df_departamental[self.df_departamental['Departamento'].isin(departamentos_seleccionados)]
        else:
            df_filtrado = self.df_departamental
        
        st.subheader("🎓 Educación por Departamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_alfabetizacion_dept = px.bar(
                df_filtrado.sort_values('Alfabetización_%'),
                x='Alfabetización_%',
                y='Departamento',
                orientation='h',
                color='Alfabetización_%',
                color_continuous_scale='greens',
                title="Alfabetización por Departamento (%)",
                text='Alfabetización_%'
            )
            
            fig_alfabetizacion_dept.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_alfabetizacion_dept.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_alfabetizacion_dept, use_container_width=True)
        
        with col2:
            fig_secundaria = px.bar(
                df_filtrado.sort_values('Secundaria_Completa_%'),
                x='Secundaria_Completa_%',
                y='Departamento',
                orientation='h',
                color='Secundaria_Completa_%',
                color_continuous_scale='blues',
                title="Secundaria Completa por Departamento (%)",
                text='Secundaria_Completa_%'
            )
            
            fig_secundaria.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_secundaria.update_layout(
                height=400,
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_secundaria, use_container_width=True)
    
    def render_niveles_educativos(self):
        """Renderiza comparación de niveles educativos"""
        st.subheader("📚 Comparación de Niveles Educativos")
        
        # Preparar datos para gráfico de barras agrupadas
        df_niveles = self.df_departamental.melt(
            id_vars=['Departamento'],
            value_vars=['Primaria_Completa_%', 'Secundaria_Completa_%', 'Universitaria_%'],
            var_name='Nivel_Educativo',
            value_name='Porcentaje'
        )
        
        # Limpiar nombres
        df_niveles['Nivel_Educativo'] = df_niveles['Nivel_Educativo'].str.replace('_Completa_%', '').str.replace('_%', '').str.replace('_', ' ')
        
        fig_niveles = px.bar(
            df_niveles,
            x='Departamento',
            y='Porcentaje',
            color='Nivel_Educativo',
            barmode='group',
            title="Niveles Educativos Completados por Departamento",
            color_discrete_sequence=['#3498db', '#e74c3c', '#f39c12']
        )
        
        fig_niveles.update_layout(
            height=500,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            xaxis_tickangle=-45
        )
        
        st.plotly_chart(fig_niveles, use_container_width=True)
    
    def render_educacion_universitaria(self):
        """Renderiza análisis específico de educación universitaria"""
        st.subheader("🎓 Educación Universitaria por Departamento")
        
        col1, col2 = st.columns(2)
        
        with col1:
            fig_universitaria = px.bar(
                self.df_departamental.sort_values('Universitaria_%', ascending=False),
                x='Departamento',
                y='Universitaria_%',
                color='Universitaria_%',
                color_continuous_scale='viridis',
                title="Porcentaje con Educación Universitaria",
                text='Universitaria_%'
            )
            
            fig_universitaria.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
            fig_universitaria.update_layout(
                height=350,
                showlegend=False,
                xaxis_tickangle=-45,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_universitaria, use_container_width=True)
        
        with col2:
            fig_pie_universitaria = px.pie(
                self.df_departamental,
                values='Universitaria_%',
                names='Departamento',
                title="Distribución de Educación Universitaria",
                color_discrete_sequence=px.colors.qualitative.Set3
            )
            
            fig_pie_universitaria.update_traces(textposition='inside', textinfo='percent+label')
            fig_pie_universitaria.update_layout(
                height=350,
                showlegend=False,
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_pie_universitaria, use_container_width=True)
    
    def render_brechas_educativas(self):
        """Renderiza análisis de brechas educativas"""
        st.subheader("📊 Brechas Educativas entre Departamentos")
        
        # Calcular brechas
        df_brechas = self.df_departamental.copy()
        
        max_alfabetizacion = df_brechas['Alfabetización_%'].max()
        min_alfabetizacion = df_brechas['Alfabetización_%'].min()
        
        max_universitaria = df_brechas['Universitaria_%'].max()
        min_universitaria = df_brechas['Universitaria_%'].min()
        
        # Crear gráfico de dispersión
        fig_brechas = px.scatter(
            df_brechas,
            x='Alfabetización_%',
            y='Universitaria_%',
            size='Secundaria_Completa_%',
            color='Secundaria_Completa_%',
            hover_name='Departamento',
            title="Relación entre Alfabetización y Educación Universitaria",
            color_continuous_scale='viridis'
        )
        
        fig_brechas.update_layout(
            height=400,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_brechas, use_container_width=True)
        
        # Mostrar información de brechas
        col1, col2 = st.columns(2)
        
        with col1:
            st.info(f"""
            **Brecha en Alfabetización:**
            - Máximo: {max_alfabetizacion:.1f}%
            - Mínimo: {min_alfabetizacion:.1f}%
            - Diferencia: {max_alfabetizacion - min_alfabetizacion:.1f} puntos
            """)
        
        with col2:
            st.info(f"""
            **Brecha en Educación Universitaria:**
            - Máximo: {max_universitaria:.1f}%
            - Mínimo: {min_universitaria:.1f}%
            - Diferencia: {max_universitaria - min_universitaria:.1f} puntos
            """)
    
    def render_tabla_datos(self):
        """Renderiza tabla con datos detallados"""
        st.subheader("📋 Datos Detallados de Educación")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("**Evolución Temporal**")
            st.dataframe(
                self.df_temporal,
                use_container_width=True
            )
        
        with col2:
            st.markdown("**Datos por Departamento**")
            st.dataframe(
                self.df_departamental,
                use_container_width=True
            )
    
    def render(self, departamentos_seleccionados=None, mostrar_niveles=True, 
               mostrar_universitaria=True, mostrar_brechas=True, mostrar_tabla=True):
        """Renderiza toda la sección de educación"""
        st.markdown(render_section_title("Educación", "📚"), unsafe_allow_html=True)
        
        # Métricas
        self.render_metricas()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Evolución temporal
        self.render_evolucion_alfabetizacion()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Educación departamental
        self.render_educacion_departamental(departamentos_seleccionados)
        
        if mostrar_niveles:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_niveles_educativos()
        
        if mostrar_universitaria:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_educacion_universitaria()
        
        if mostrar_brechas:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_brechas_educativas()
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_educacion = SeccionEducacion()
