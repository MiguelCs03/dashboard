# ========================================
# SECCIÓN FECUNDIDAD - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
# from datos import datos_bolivia
# from estilos import render_metric_card, render_section_title

class SeccionFecundidad:
    """Maneja toda la funcionalidad de la sección fecundidad Bolivia"""
    
    def __init__(self):
        # Datos de ejemplo mientras configuras los imports
        self.df_departamental = self._get_datos_ejemplo()
        
    def _get_datos_ejemplo(self):
        """Datos reales de fecundidad basados en UDAPE 2015-2022"""
        
        # Datos por departamento (2022 - más recientes del PDF)
        df_departamental = pd.DataFrame({
            'Departamento': ['Santa Cruz', 'La Paz', 'Cochabamba', 'Potosí', 'Beni', 'Chuquisaca', 'Tarija', 'Oruro', 'Pando'],
            'Nacimientos_2022': [72183, 54492, 42407, 20594, 13628, 13720, 11139, 9519, 4156],
            'Tasa_Natalidad_x1000': [21.1, 17.9, 20.0, 22.5, 26.4, 20.8, 18.5, 17.2, 25.4],
            'Tasa_Fecundidad_Global': [2.5, 2.3, 2.4, 3.0, 3.3, 2.6, 2.4, 2.3, 3.2]
        })
        
        # Datos históricos nacionales
        self.df_historico = pd.DataFrame({
            'Año': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022],
            'Nacimientos_Bolivia': [247639, 246989, 246276, 245508, 244676, 243784, 249365, 241838],
            'Tasa_Natalidad_Bolivia': [22.8, 22.4, 22.0, 21.6, 21.3, 20.9, 24.1, 20.1],
            'Tasa_Fecundidad_Bolivia': [2.9, 2.8, 2.7, 2.7, 2.6, 2.6, 3.0, 2.5]
        })
        
        return df_departamental
    
    def render_metric_card(self, titulo, valor, descripcion):
        """Función auxiliar para renderizar cards de métricas"""
        return f"""
        <div style="
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            margin: 0.5rem 0;
        ">
            <div style="font-size: 0.9rem; opacity: 0.9; text-transform: uppercase; letter-spacing: 1px;">{titulo}</div>
            <div style="font-size: 2.5rem; font-weight: 700; margin: 0.5rem 0;">{valor}</div>
            <div style="font-size: 0.8rem;">{descripcion}</div>
        </div>
        """
    
    def render_section_title(self, titulo, icono):
        """Función auxiliar para renderizar títulos de sección"""
        return f"""
        <div style="text-align: center; padding: 1rem 0;">
            <h2 style="color: #2c3e50; font-size: 2rem; margin-bottom: 0;">{icono} {titulo}</h2>
        </div>
        """
    
    def render_metricas(self):
        """Renderiza las métricas principales de fecundidad basadas en datos UDAPE 2022"""
        tasa_fecundidad_nacional = 2.5  # TFG Nacional 2022
        nacimientos_total = 241838  # Total nacional 2022
        tasa_natalidad_nacional = 20.1  # Por mil habitantes 2022
        
        # Departamentos con mayor y menor fecundidad
        dept_mayor_fecundidad = self.df_departamental.loc[self.df_departamental['Tasa_Fecundidad_Global'].idxmax(), 'Departamento']
        dept_menor_fecundidad = self.df_departamental.loc[self.df_departamental['Tasa_Fecundidad_Global'].idxmin(), 'Departamento']
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown(self.render_metric_card(
                "Tasa Fecundidad Global", 
                f"{tasa_fecundidad_nacional}",
                "hijos por mujer (2022)"
            ), unsafe_allow_html=True)
        
        with col2:
            st.markdown(self.render_metric_card(
                "Nacimientos 2022", 
                f"{nacimientos_total:,.0f}",
                "total nacional"
            ), unsafe_allow_html=True)
        
        with col3:
            st.markdown(self.render_metric_card(
                "Mayor Fecundidad", 
                f"{dept_mayor_fecundidad}",
                f"{self.df_departamental['Tasa_Fecundidad_Global'].max():.1f} hijos/mujer"
            ), unsafe_allow_html=True)
        
        with col4:
            st.markdown(self.render_metric_card(
                "Menor Fecundidad", 
                f"{dept_menor_fecundidad}",
                f"{self.df_departamental['Tasa_Fecundidad_Global'].min():.1f} hijos/mujer"
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
            st.subheader("📈 Tasa de Natalidad por Departamento")
            
            fig_natalidad = px.bar(
                df_filtrado.sort_values('Tasa_Natalidad_x1000'),
                x='Tasa_Natalidad_x1000',
                y='Departamento',
                orientation='h',
                color='Tasa_Natalidad_x1000',
                color_continuous_scale='blues',
                text='Tasa_Natalidad_x1000',
                title="Por mil habitantes (2022)"
            )
            
            fig_natalidad.update_traces(texttemplate='%{text:.1f}‰', textposition='outside')
            fig_natalidad.update_layout(
                height=400,
                showlegend=False,
                xaxis_title="Tasa de Natalidad (‰)",
                yaxis_title="",
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)'
            )
            
            st.plotly_chart(fig_natalidad, use_container_width=True)
    
    def render_nacimientos_distribucion(self, departamentos_seleccionados=None):
        """Renderiza gráfico de distribución de nacimientos"""
        if departamentos_seleccionados:
            df_filtrado = self.df_departamental[self.df_departamental['Departamento'].isin(departamentos_seleccionados)]
        else:
            df_filtrado = self.df_departamental
            
        st.subheader("🍼 Distribución de Nacimientos 2024")
        
        fig_nacimientos = px.pie(
            df_filtrado,
            values='Nacimientos_2022',
            names='Departamento',
            title="Distribución de Nacimientos por Departamento (2022)",
            color_discrete_sequence=px.colors.qualitative.Pastel
        )
        
        fig_nacimientos.update_traces(textposition='inside', textinfo='percent+label')
        fig_nacimientos.update_layout(
            height=400,
            showlegend=False,
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig_nacimientos, use_container_width=True)
    
    def render_tabla_datos(self):
        """Renderiza tabla con datos detallados"""
        st.subheader("📋 Datos Detallados de Fecundidad")
        st.dataframe(
            self.df_departamental[['Departamento', 'Tasa_Fecundidad_Global', 'Nacimientos_2022', 'Tasa_Natalidad_x1000']],
            use_container_width=True
        )
    
    def render(self, departamentos_seleccionados=None, mostrar_correlacion=True, mostrar_tabla=True):
        """Renderiza toda la sección de fecundidad"""
        st.markdown(self.render_section_title("Fecundidad y Natalidad", "👶"), unsafe_allow_html=True)
        
        # Métricas
        self.render_metricas()
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Gráficos principales
        self.render_graficos(departamentos_seleccionados)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Distribución de nacimientos
        self.render_nacimientos_distribucion(departamentos_seleccionados)
        
        if mostrar_tabla:
            st.markdown("<br>", unsafe_allow_html=True)
            self.render_tabla_datos()

# Instancia global
seccion_fecundidad = SeccionFecundidad()

# ========================================
# EJEMPLO DE USO
# ========================================
if __name__ == "__main__":
    import streamlit as st
    
    st.set_page_config(page_title="Fecundidad Bolivia", layout="wide")
    
    # Ejemplo de uso
    seccion_fecundidad.render(
        departamentos_seleccionados=['Santa Cruz', 'La Paz', 'Cochabamba'],
        mostrar_correlacion=True,
        mostrar_tabla=True
    )