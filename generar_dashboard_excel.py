# ========================================
# DASHBOARD EXCEL BOLIVIA - VERSIÓN SIMPLE Y FUNCIONAL
# ========================================

import pandas as pd
import xlsxwriter
import os

# Datos de Bolivia
departamentos_data = {
    'Departamento': ['Santa Cruz', 'La Paz', 'Cochabamba', 'Potosí', 'Chuquisaca', 'Tarija', 'Oruro', 'Beni', 'Pando'],
    'Población_2024': [4000143, 2706359, 2005373, 823517, 576153, 482196, 494178, 421196, 110436],
    'Superficie_km2': [370621, 133985, 55631, 118218, 51524, 37623, 53588, 213564, 63827],
    'Densidad_hab_km2': [10.8, 20.2, 36.0, 7.0, 11.2, 12.8, 9.2, 2.0, 1.7]
}

df_bolivia = pd.DataFrame(departamentos_data)

# Datos de alfabetización
años_alfabetizacion = {
    'Año': [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024],
    'Alfabetización_%': [95.37, 95.45, 95.52, 95.60, 95.68, 95.75, 95.83, 95.90, 95.98, 96.06]
}

df_alfabetizacion = pd.DataFrame(años_alfabetizacion)

def crear_dashboard_excel_simple():
    """
    Crea un dashboard Excel funcional y bonito
    """
    
    # Crear archivo Excel
    filename = 'Bolivia_Dashboard_Funcional.xlsx'
    workbook = xlsxwriter.Workbook(filename)
    
    # ========================================
    # FORMATOS
    # ========================================
    
    # Formato título principal
    titulo_format = workbook.add_format({
        'bold': True,
        'font_size': 20,
        'align': 'center',
        'valign': 'vcenter',
        'bg_color': '#667EEA',
        'font_color': 'white',
        'border': 2
    })
    
    # Formato métricas
    metrica_titulo = workbook.add_format({
        'bold': True,
        'font_size': 12,
        'align': 'center',
        'bg_color': '#E8F4F8',
        'border': 1
    })
    
    metrica_valor = workbook.add_format({
        'bold': True,
        'font_size': 16,
        'align': 'center',
        'bg_color': '#F8FBFF',
        'font_color': '#2C3E50',
        'border': 1
    })
    
    # Formato encabezados tabla
    header_format = workbook.add_format({
        'bold': True,
        'font_size': 11,
        'align': 'center',
        'bg_color': '#4472C4',
        'font_color': 'white',
        'border': 1
    })
    
    # Formato datos tabla
    data_format = workbook.add_format({
        'align': 'center',
        'border': 1,
        'num_format': '#,##0'
    })
    
    # ========================================
    # HOJA 1: DASHBOARD PRINCIPAL
    # ========================================
    
    worksheet_main = workbook.add_worksheet('🇧🇴 Dashboard Bolivia')
    
    # TÍTULO PRINCIPAL
    worksheet_main.merge_range('A1:J1', '🇧🇴 BOLIVIA - DASHBOARD ESTADÍSTICO 2024', titulo_format)
    
    # MÉTRICAS PRINCIPALES (Fila 3-4)
    metricas = [
        ('POBLACIÓN TOTAL', f"{df_bolivia['Población_2024'].sum():,}"),
        ('DEPARTAMENTOS', '9'),
        ('SUPERFICIE TOTAL', f"{df_bolivia['Superficie_km2'].sum():,} km²"),
        ('ALFABETIZACIÓN', '96.1%')
    ]
    
    col_positions = ['A', 'C', 'E', 'G']
    for i, (titulo, valor) in enumerate(metricas):
        col = col_positions[i]
        worksheet_main.write(f'{col}3', titulo, metrica_titulo)
        worksheet_main.write(f'{col}4', valor, metrica_valor)
    
    # ========================================
    # TABLA DE DATOS (Fila 6 en adelante)
    # ========================================
    
    # Encabezados
    headers = ['Departamento', 'Población 2024', 'Superficie (km²)', 'Densidad (hab/km²)']
    for col, header in enumerate(headers):
        worksheet_main.write(5, col, header, header_format)
    
    # Datos
    for row, (index, data) in enumerate(df_bolivia.iterrows()):
        worksheet_main.write(6 + row, 0, data['Departamento'], data_format)
        worksheet_main.write(6 + row, 1, data['Población_2024'], data_format)
        worksheet_main.write(6 + row, 2, data['Superficie_km2'], data_format)
        worksheet_main.write(6 + row, 3, data['Densidad_hab_km2'], data_format)
    
    # ========================================
    # GRÁFICO DE BARRAS - POBLACIÓN
    # ========================================
    
    chart_barras = workbook.add_chart({'type': 'column'})
    
    chart_barras.add_series({
        'name': 'Población 2024',
        'categories': [worksheet_main.name, 6, 0, 14, 0],  # Departamentos
        'values': [worksheet_main.name, 6, 1, 14, 1],       # Población
        'fill': {'color': '#5B9BD5'},
        'data_labels': {'value': True, 'font': {'size': 9}}
    })
    
    chart_barras.set_title({
        'name': 'Población por Departamento 2024',
        'font': {'size': 14, 'bold': True}
    })
    
    chart_barras.set_x_axis({
        'name': 'Departamentos',
        'name_font': {'size': 11, 'bold': True}
    })
    
    chart_barras.set_y_axis({
        'name': 'Población',
        'name_font': {'size': 11, 'bold': True},
        'num_format': '#,##0'
    })
    
    chart_barras.set_size({'width': 480, 'height': 300})
    worksheet_main.insert_chart('F6', chart_barras)
    
    # ========================================
    # GRÁFICO CIRCULAR - DISTRIBUCIÓN
    # ========================================
    
    chart_pie = workbook.add_chart({'type': 'pie'})
    
    chart_pie.add_series({
        'name': 'Distribución Poblacional',
        'categories': [worksheet_main.name, 6, 0, 14, 0],  # Departamentos
        'values': [worksheet_main.name, 6, 1, 14, 1],       # Población
        'data_labels': {'percentage': True, 'font': {'size': 9}}
    })
    
    chart_pie.set_title({
        'name': 'Distribución Poblacional por Departamento',
        'font': {'size': 14, 'bold': True}
    })
    
    chart_pie.set_size({'width': 400, 'height': 300})
    worksheet_main.insert_chart('F22', chart_pie)
    
    # ========================================
    # HOJA 2: EVOLUCIÓN ALFABETIZACIÓN
    # ========================================
    
    worksheet_alfab = workbook.add_worksheet('📈 Alfabetización')
    
    # Título
    worksheet_alfab.merge_range('A1:D1', 'EVOLUCIÓN DE LA ALFABETIZACIÓN 2015-2024', titulo_format)
    
    # Encabezados
    worksheet_alfab.write('A3', 'Año', header_format)
    worksheet_alfab.write('B3', 'Alfabetización (%)', header_format)
    
    # Datos
    for row, (index, data) in enumerate(df_alfabetizacion.iterrows()):
        worksheet_alfab.write(3 + row, 0, data['Año'], data_format)
        worksheet_alfab.write(3 + row, 1, data['Alfabetización_%'], data_format)
    
    # Gráfico de líneas
    chart_lineas = workbook.add_chart({'type': 'line'})
    
    chart_lineas.add_series({
        'name': 'Alfabetización %',
        'categories': [worksheet_alfab.name, 4, 0, 13, 0],  # Años
        'values': [worksheet_alfab.name, 4, 1, 13, 1],       # Porcentajes
        'line': {'color': '#70AD47', 'width': 3},
        'marker': {'type': 'circle', 'size': 6, 'fill': {'color': '#70AD47'}}
    })
    
    chart_lineas.set_title({
        'name': 'Evolución de la Alfabetización en Bolivia',
        'font': {'size': 14, 'bold': True}
    })
    
    chart_lineas.set_x_axis({
        'name': 'Año',
        'name_font': {'size': 11, 'bold': True}
    })
    
    chart_lineas.set_y_axis({
        'name': 'Porcentaje (%)',
        'name_font': {'size': 11, 'bold': True},
        'min': 95,
        'max': 97
    })
    
    chart_lineas.set_size({'width': 480, 'height': 300})
    worksheet_alfab.insert_chart('D4', chart_lineas)
    
    # ========================================
    # AJUSTAR COLUMNAS
    # ========================================
    
    # Dashboard principal
    worksheet_main.set_column('A:A', 15)  # Departamento
    worksheet_main.set_column('B:B', 15)  # Población
    worksheet_main.set_column('C:C', 15)  # Superficie
    worksheet_main.set_column('D:D', 18)  # Densidad
    
    # Alfabetización
    worksheet_alfab.set_column('A:A', 12)  # Año
    worksheet_alfab.set_column('B:B', 18)  # Alfabetización
    
    # Cerrar y guardar
    workbook.close()
    
    return filename

# ========================================
# EJECUTAR
# ========================================
if __name__ == "__main__":
    print("🚀 Creando dashboard Excel de Bolivia...")
    
    try:
        archivo = crear_dashboard_excel_simple()
        print(f"✅ ¡Dashboard creado exitosamente!")
        print(f"📊 Archivo: {archivo}")
        print(f"📁 Ubicación: {os.path.abspath(archivo)}")
        print("\n🎯 El archivo contiene:")
        print("   • 📊 Dashboard principal con gráficos")
        print("   • 📈 Evolución de alfabetización")
        print("   • 🎨 Formato profesional")
        print("   • 📱 Listo para presentar")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        print("💡 Asegúrate de tener instalado: pip install xlsxwriter pandas")