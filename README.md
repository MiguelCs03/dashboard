# Dashboard Bolivia - Estructura Modular

## 📋 Descripción
Dashboard interactivo de estadísticas de Bolivia con arquitectura modular que permite fácil mantenimiento y modificación de secciones.

## 🏗️ Estructura del Proyecto

```
dashboard/
├── bolivia_dashboard.py      # Archivo principal
├── config.py                # Configuración y control de secciones
├── datos.py                 # Gestión centralizada de datos
├── estilos.py               # Estilos CSS personalizados
├── utilidades.py            # Utilidades de exportación
├── seccion_poblacion.py     # Módulo de población
├── seccion_desempleo.py     # Módulo de desempleo
├── seccion_fecundidad.py    # Módulo de fecundidad
├── seccion_mortalidad.py    # Módulo de mortalidad
├── seccion_datos_electorales.py  # Módulo electoral
├── seccion_educacion.py     # Módulo de educación
├── requirements.txt         # Dependencias
└── README.md               # Esta documentación
```

## 🎛️ Control de Secciones

### Para Habilitar/Deshabilitar Secciones
Edita el archivo `config.py`:

```python
SECCIONES_VISIBLES = {
    'poblacion': True,          # Mostrar sección población
    'desempleo': False,         # Ocultar sección desempleo  
    'fecundidad': True,         # Mostrar sección fecundidad
    'mortalidad': True,         # Mostrar sección mortalidad
    'datos_electorales': True,  # Mostrar datos electorales
    'educacion': True           # Mostrar sección educación
}
```

## 📊 Secciones Disponibles

### 1. 👥 Población
- Datos poblacionales por departamento
- Densidad poblacional
- Crecimiento demográfico
- Análisis territorial

### 2. 💼 Desempleo
- Tasas de desempleo departamental
- Empleo formal vs informal
- Comparativos temporales
- Métricas laborales

### 3. 👶 Fecundidad
- Tasas de fecundidad
- Natalidad por departamento
- Mortalidad infantil
- Correlaciones demográficas

### 4. ⚰️ Mortalidad
- Mortalidad general
- Esperanza de vida
- Impacto COVID-19
- Evolución temporal

### 5. 🗳️ Datos Electorales
- Padrón electoral 2025
- Votantes habilitados/inhabilitados
- Depuración de registros
- Nuevos votantes

### 6. 📚 Educación
- Alfabetización nacional
- Niveles educativos
- Brechas departamentales
- Educación universitaria

## 🔧 Cómo Modificar una Sección

### Ejemplo: Modificar la sección de población

1. **Editar datos**: Modifica `datos.py` → método `get_datos_poblacion()`
2. **Cambiar visualización**: Edita `seccion_poblacion.py`
3. **Los cambios se reflejan automáticamente**

### Ejemplo: Agregar nueva métrica
```python
# En seccion_poblacion.py
def render_metricas(self):
    # ...código existente...
    
    # Nueva métrica
    with col5:
        st.markdown(render_metric_card(
            "Nueva Métrica", 
            f"{nuevo_valor}",
            "descripción"
        ), unsafe_allow_html=True)
```

## 🎨 Personalización de Estilos

Edita `estilos.py` para cambiar:
- Colores del tema
- Fuentes
- Animaciones
- Layout de tarjetas

## 📥 Exportación de Datos

El sistema incluye exportación automática en:
- **Excel**: Múltiples hojas por sección
- **CSV**: Datos combinados
- **TXT**: Reportes ejecutivos
- **HTML**: Gráficos interactivos

## 🚀 Ejecución

```bash
# Instalar dependencias
pip install -r requirements.txt

# Ejecutar dashboard
streamlit run bolivia_dashboard.py
```

## 📱 Principios de Diseño

### KISS (Keep It Simple, Stupid)
- Cada sección es independiente
- Código claro y directo
- Funciones con un propósito específico

### YAGNI (You Aren't Gonna Need It)
- Solo incluye funcionalidades necesarias
- Evita sobre-ingeniería
- Fácil extensión cuando se requiera

## 🔄 Mantenimiento

### Para agregar nueva sección:
1. Crear `seccion_nueva.py` siguiendo el patrón
2. Agregar datos en `datos.py`
3. Incluir en `config.py`
4. Importar en `bolivia_dashboard.py`

### Para modificar datos:
- Solo editar `datos.py`
- Los cambios se propagan automáticamente

### Para cambiar diseño:
- Editar `estilos.py` para cambios globales
- Editar sección específica para cambios locales

## 🎯 Beneficios de esta Estructura

✅ **Modular**: Cada sección es independiente  
✅ **Mantenible**: Fácil localizar y modificar código  
✅ **Escalable**: Agregar nuevas secciones sin afectar existentes  
✅ **Configurable**: Control granular de visibilidad  
✅ **Reutilizable**: Componentes pueden usarse en otros proyectos  

## 🔍 Solución de Problemas

### Error de importación:
- Verificar que todos los archivos estén en la misma carpeta
- Instalar dependencias: `pip install -r requirements.txt`

### Sección no aparece:
- Verificar `config.py` → `SECCIONES_VISIBLES`
- Verificar checkbox en sidebar

### Error de datos:
- Verificar `datos.py` → método correspondiente
- Verificar nombres de columnas en DataFrames

## 📞 Soporte

Para modificaciones específicas o dudas:
- Documentar el cambio deseado
- Identificar la sección afectada
- Seguir la estructura modular existente
