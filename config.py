# ========================================
# CONFIGURACIÓN DEL DASHBOARD BOLIVIA
# ========================================

# Configuración de secciones visibles
# Cambia True/False para mostrar/ocultar secciones
SECCIONES_VISIBLES = {
    'poblacion': True,
    'desempleo': True,
    'fecundidad': True,
    'mortalidad': True,
    'datos_electorales': False  # Deshabilitado por request del usuario
}

# Configuración general
APP_CONFIG = {
    'titulo': '🇧🇴 Bolivia Dashboard',
    'subtitulo': 'Dashboard Estadístico Nacional',
    'icono': '🇧🇴',
    'layout': 'wide',
    'tema_color': {
        'primario': '#667eea',
        'secundario': '#764ba2',
        'fondo': '#2c3e50'
    }
}

# Fuentes de datos
FUENTES_DATOS = {
    'censo': 'INE Bolivia - Censo 2024',
    'educacion': 'Ministerio de Educación',
    'salud': 'Ministerio de Salud',
    'electoral': 'TSE Bolivia',
    'trabajo': 'INE Bolivia - Encuesta de Hogares'
}
