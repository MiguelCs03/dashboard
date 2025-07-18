# ========================================
# UTILIDADES DE EXPORTACIÓN - BOLIVIA DASHBOARD
# ========================================

import streamlit as st
import pandas as pd
import io
from datetime import datetime
from config import APP_CONFIG, FUENTES_DATOS

class ExportadorDatos:
    """Maneja la exportación de datos del dashboard"""
    
    def __init__(self):
        self.fecha_actual = datetime.now().strftime("%Y-%m-%d")
    
    def crear_excel_completo(self, datos_dict):
        """Crea un archivo Excel con múltiples hojas"""
        output = io.BytesIO()
        
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            # Hoja de resumen
            resumen = self._crear_hoja_resumen(datos_dict)
            resumen.to_excel(writer, sheet_name='Resumen', index=False)
            
            # Hojas de datos por sección
            for nombre, df in datos_dict.items():
                if isinstance(df, pd.DataFrame) and not df.empty:
                    df.to_excel(writer, sheet_name=nombre, index=False)
        
        return output.getvalue()
    
    def _crear_hoja_resumen(self, datos_dict):
        """Crea hoja de resumen con información general"""
        resumen_data = {
            'Sección': [],
            'Descripción': [],
            'Registros': [],
            'Fecha_Actualización': []
        }
        
        for nombre, df in datos_dict.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                resumen_data['Sección'].append(nombre)
                resumen_data['Descripción'].append(f"Datos de {nombre}")
                resumen_data['Registros'].append(len(df))
                resumen_data['Fecha_Actualización'].append(self.fecha_actual)
        
        return pd.DataFrame(resumen_data)
    
    def crear_reporte_texto(self, datos_dict):
        """Crea reporte en formato texto"""
        reporte = f"""
REPORTE BOLIVIA DASHBOARD
========================
Fecha: {self.fecha_actual}
Fuente: {FUENTES_DATOS['censo']}

RESUMEN EJECUTIVO:
==================
"""
        
        for nombre, df in datos_dict.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                reporte += f"\n{nombre.upper()}:\n"
                reporte += f"- Registros: {len(df)}\n"
                if 'Departamento' in df.columns:
                    reporte += f"- Departamentos: {df['Departamento'].nunique()}\n"
        
        reporte += f"""

INFORMACIÓN TÉCNICA:
====================
- Dashboard: {APP_CONFIG['titulo']}
- Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- Versión: 1.0
"""
        
        return reporte
    
    def crear_csv_combinado(self, datos_dict):
        """Crea un CSV con datos combinados"""
        dfs_combinados = []
        
        for nombre, df in datos_dict.items():
            if isinstance(df, pd.DataFrame) and not df.empty:
                df_copy = df.copy()
                df_copy['Sección'] = nombre
                dfs_combinados.append(df_copy)
        
        if dfs_combinados:
            df_final = pd.concat(dfs_combinados, ignore_index=True)
            return df_final.to_csv(index=False)
        return ""
    
    def render_botones_exportacion(self, datos_dict, prefijo="bolivia"):
        """Renderiza botones de exportación"""
        st.markdown("### 📊 Exportar Datos")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            # Exportar Excel
            excel_data = self.crear_excel_completo(datos_dict)
            st.download_button(
                label="📊 Descargar Excel",
                data=excel_data,
                file_name=f"{prefijo}_dashboard_{self.fecha_actual}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )
        
        with col2:
            # Exportar CSV
            csv_data = self.crear_csv_combinado(datos_dict)
            if csv_data:
                st.download_button(
                    label="📥 Descargar CSV",
                    data=csv_data,
                    file_name=f"{prefijo}_datos_{self.fecha_actual}.csv",
                    mime="text/csv",
                    use_container_width=True
                )
        
        with col3:
            # Exportar reporte
            reporte = self.crear_reporte_texto(datos_dict)
            st.download_button(
                label="📄 Descargar Reporte",
                data=reporte,
                file_name=f"{prefijo}_reporte_{self.fecha_actual}.txt",
                mime="text/plain",
                use_container_width=True
            )
        
        with col4:
            # Información sobre link online
            if st.button("🔗 Info Online", use_container_width=True):
                st.info("""
                🌐 **Para publicar online:**
                1. Sube el código a GitHub
                2. Conecta en streamlit.io
                3. ¡Comparte el link!
                
                💡 **Gratis y automático**
                """)

# Instancia global
exportador = ExportadorDatos()
