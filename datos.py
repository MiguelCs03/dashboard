# ========================================
# DATOS BOLIVIA - MÓDULO CENTRALIZADO
# ========================================

import pandas as pd
import numpy as np

class DatosBolivia:
    """Clase para manejar todos los datos del dashboard de Bolivia"""
    
    def __init__(self):
        self.departamentos = ['Santa Cruz', 'La Paz', 'Cochabamba', 'Potosí', 
                             'Chuquisaca', 'Tarija', 'Oruro', 'Beni', 'Pando']
    
    def get_datos_poblacion(self):
        """Datos poblacionales por departamento - Censo 2024 (Datos reales INE)"""
        datos = {
            'Departamento': self.departamentos,
            'Población_2024': [3115386, 3022566, 2005373, 856419, 600132, 534348, 570194, 477441, 130761],
            'Población_2012': [2657762, 2719344, 1762761, 828093, 581347, 483518, 494587, 422008, 110436],
            'Superficie_km2': [370621, 133985, 55631, 118218, 51524, 37623, 53588, 213564, 63827],
        }
        df = pd.DataFrame(datos)
        
        # Calcular métricas derivadas
        df['Densidad'] = df['Población_2024'] / df['Superficie_km2']
        df['Crecimiento_%'] = ((df['Población_2024'] / df['Población_2012']) - 1) * 100
        df['Crecimiento_Absoluto'] = df['Población_2024'] - df['Población_2012']
        
        # Participación porcentual
        poblacion_total = df['Población_2024'].sum()
        df['Participación_%'] = (df['Población_2024'] / poblacion_total) * 100
        
        return df
    
    def get_datos_desempleo(self):
        """Datos de desempleo EPA Bolivia - II Trimestre 2024 (Datos reales INE)"""
        # Datos nacionales EPA II Trim 2024
        datos_nacionales = {
            'Categoría': ['Tasa de desempleo (EPA)', 'Paro menores de 25 años', 'Paro mayores de 24 años', 
                         'Paro entre 25 y 54 años', 'Paro mayores de 54 años'],
            'Total_%': [2.8, 4.3, 2.4, 2.9, 1.0],
            'Hombres_%': [2.3, 3.8, 1.9, 2.2, 1.3],
            'Mujeres_%': [3.3, 4.9, 3.0, 3.8, 0.6]
        }
        
        # Datos de parados (en miles)
        datos_parados = {
            'Categoría': ['Parados', 'Parados menores de 25 años', 'Parados mayores de 24 años', 
                         'Paro entre 25 y 54 años', 'Parados mayores de 55 años'],
            'Total_miles': [195, 56, 139, 125, 14],
            'Hombres_miles': [84, 27, 57, 47, 10],
            'Mujeres_miles': [111, 29, 82, 78, 4]
        }
        
        # Datos históricos de comparación
        datos_historicos = {
            'Año': [2022, 2023],
            'Tasa_desempleo_EPA_%': [3.3, 2.9],
            'Tasa_desempleo_hombres_%': [2.9, 2.6],
            'Tasa_desempleo_mujeres_%': [3.7, 3.2],
            'Paro_menores_25_%': [5.6, 4.6],
            'Paro_mayores_24_%': [2.7, 2.4]
        }
        
        return (pd.DataFrame(datos_nacionales), 
                pd.DataFrame(datos_parados), 
                pd.DataFrame(datos_historicos))
    
    def get_datos_fecundidad(self):
        """Datos de fecundidad y natalidad Bolivia 2024 (Datos reales INE)"""
        # Datos departamentales de fecundidad
        datos_departamentales = {
            'Departamento': self.departamentos,
            'Tasa_Fecundidad_Global': [2.9, 2.1, 2.6, 3.8, 3.4, 2.7, 3.2, 4.1, 4.5],  # Hijos por mujer
            'Nacimientos_2024': [62850, 48320, 35670, 18420, 15680, 12450, 14230, 12180, 3850],
            'Mortalidad_Infantil_x1000': [22.5, 18.7, 21.2, 28.9, 26.4, 19.8, 25.3, 31.2, 35.6],  # Por mil nacidos vivos
            'Tasa_Natalidad_x1000': [20.2, 16.0, 17.8, 21.5, 26.1, 23.3, 24.9, 25.5, 29.4]  # Por mil habitantes
        }
        
        # Datos históricos nacionales
        datos_historicos = {
            'Año': [2010, 2012, 2014, 2016, 2018, 2020, 2022, 2024],
            'Tasa_Fecundidad_Global': [3.5, 3.2, 3.0, 2.9, 2.8, 2.7, 2.6, 2.5],
            'Tasa_Natalidad_x1000': [25.8, 24.2, 22.9, 21.8, 20.9, 19.8, 18.9, 18.2],
            'Mortalidad_Infantil_x1000': [42.0, 38.5, 35.2, 32.1, 29.4, 27.0, 24.8, 22.9]
        }
        
        # Datos por grupos de edad de la madre
        datos_edad_madre = {
            'Grupo_Edad': ['15-19', '20-24', '25-29', '30-34', '35-39', '40-44', '45-49'],
            'Tasa_Fecundidad_2024': [68, 142, 135, 108, 75, 32, 4],  # Por mil mujeres del grupo
            'Tasa_Fecundidad_2020': [72, 148, 140, 112, 78, 35, 5],
            'Porcentaje_Nacimientos': [12.5, 28.8, 26.2, 19.8, 10.1, 2.4, 0.2]
        }
        
        return (pd.DataFrame(datos_departamentales), 
                pd.DataFrame(datos_historicos), 
                pd.DataFrame(datos_edad_madre))
    
    def get_datos_mortalidad(self):
        """Datos de mortalidad general - Bolivia (datos reales)"""
        datos = {
            'Año': [2012, 2013, 2014, 2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023],
            'Defunciones': [81092, 81778, 82468, 82947, 83678, 84640, 87015, 88177, 128041, 140753, 92765, 87815],
            'Tasa_Mortalidad': [7.84, 7.78, 7.73, 7.66, 7.61, 7.59, 7.56, 7.56, 10.84, 11.79, 7.68, 7.17],
            'Esperanza_Vida': [69.8, 69.9, 70.1, 70.3, 70.5, 70.7, 70.9, 71.1, 70.8, 70.6, 70.9, 71.2]
        }
        return pd.DataFrame(datos)
    
    def get_datos_electorales(self):
        """Datos de padrón electoral 2025"""
        datos = {
            'Departamento': self.departamentos,
            'Habilitados_2025': [2890450, 1950320, 1520680, 625840, 438590, 367280, 376420, 320150, 84270],
            'Inhabilitados': [45120, 32890, 28450, 18950, 15670, 12340, 14580, 11230, 3240],
            'Depurados': [12890, 8950, 7230, 5680, 4320, 3170, 4120, 3850, 1180],
            'Nuevos_Registros': [125680, 89450, 72340, 35670, 28950, 22180, 26340, 18950, 6890]
        }
        df = pd.DataFrame(datos)
        df['Total_Padrón'] = df['Habilitados_2025'] + df['Inhabilitados']
        df['Porcentaje_Habilitados'] = (df['Habilitados_2025'] / df['Total_Padrón']) * 100
        return df
    
    def get_evolucion_poblacion_historica(self):
        """Datos de evolución poblacional histórica 1950-2024"""
        datos = {
            'Año': [1950, 1976, 1992, 2001, 2012, 2024],
            'Población': [2704165, 4613419, 6420792, 8274325, 10059856, 11312620]
        }
        df = pd.DataFrame(datos)
        
        # Calcular crecimiento por período
        df['Crecimiento_Absoluto'] = df['Población'].diff()
        df['Crecimiento_%'] = (df['Población'].pct_change() * 100).round(2)
        
        return df
    
    def get_tasas_crecimiento_intercensal(self):
        """Tasas de crecimiento intercensal por período"""
        datos = {
            'Período': ['50-76', '76-92', '92-01', '01-12', '12-24'],
            'Tasa_Crecimiento': [2.050, 2.110, 2.740, 1.743, 1.035],
            'Años': [26, 16, 9, 11, 12]
        }
        df = pd.DataFrame(datos)
        
        # Calcular promedio anual
        df['Promedio_Anual_%'] = df['Tasa_Crecimiento']
        
        return df

# Instancia global de los datos
datos_bolivia = DatosBolivia()
