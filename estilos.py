# ========================================
# ESTILOS CSS PARA BOLIVIA DASHBOARD
# ========================================

def get_css_styles():
    """Retorna los estilos CSS personalizados"""
    return """
    <style>
        /* Importar fuente moderna */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;600;700&display=swap');
        
        /* Estilos generales */
        .main {
            font-family: 'Inter', sans-serif;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            padding: 0;
        }
        
        /* Container principal */
        .main .block-container {
            padding-top: 2rem;
            padding-bottom: 2rem;
            background: rgba(255, 255, 255, 0.95);
            border-radius: 15px;
            margin: 1rem;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
        }
        
        /* Cards de métricas */
        .metric-card {
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
            padding: 1.5rem;
            border-radius: 15px;
            text-align: center;
            box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
            transition: transform 0.3s ease;
            margin: 0.5rem 0;
        }
        
        .metric-card:hover {
            transform: translateY(-5px);
        }
        
        .metric-number {
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0.5rem 0;
        }
        
        .metric-label {
            font-size: 0.9rem;
            opacity: 0.9;
            text-transform: uppercase;
            letter-spacing: 1px;
        }
        
        /* Títulos */
        h1, h2, h3 {
            color: #2c3e50;
            font-weight: 600;
        }
        
        /* Sidebar */
        .css-1d391kg {
            background: linear-gradient(180deg, #2c3e50 0%, #34495e 100%);
        }
        
        .css-1d391kg .css-1vq4p4l {
            color: white;
        }
        
        /* Secciones */
        .seccion-container {
            margin: 2rem 0;
            padding: 1rem;
            border-radius: 10px;
            background: white;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        
        .seccion-titulo {
            color: #2c3e50;
            font-size: 1.5rem;
            font-weight: 600;
            margin-bottom: 1rem;
            border-bottom: 2px solid #667eea;
            padding-bottom: 0.5rem;
        }
    </style>
    """

def render_metric_card(label, value, subtitle=""):
    """Renderiza una tarjeta de métrica"""
    return f"""
    <div class="metric-card">
        <div class="metric-label">{label}</div>
        <div class="metric-number">{value}</div>
        <div style="font-size: 0.8rem;">{subtitle}</div>
    </div>
    """

def render_section_title(titulo, icono=""):
    """Renderiza el título de una sección"""
    return f"""
    <div class="seccion-titulo">
        {icono} {titulo}
    </div>
    """
