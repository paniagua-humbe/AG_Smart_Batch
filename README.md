# Smart Batch - Planificación Urbana con Algoritmos Genéticos

Smart Batch es un sistema de planificación urbana que utiliza algoritmos genéticos para optimizar la distribución de elementos urbanos como calles, áreas verdes, tanques de agua y sistemas de drenaje, considerando la topografía del terreno.

## Características

- **Algoritmo Genético Adaptativo**: Optimiza la distribución de elementos urbanos para maximizar la eficiencia y habitabilidad.
- **Optimización Topográfica**: Utiliza datos de elevación para colocar estratégicamente tanques de agua en zonas altas y drenajes en zonas bajas.
- **Distribución Inteligente de Áreas Verdes**: Coloca áreas verdes para maximizar la accesibilidad desde lotes residenciales.
- **Conectividad Urbana**: Garantiza que todos los lotes residenciales tengan acceso a calles.
- **Visualización Gráfica**: Representa visualmente la distribución urbana resultante.

## Requisitos

- Python 3.x
- NumPy
- Matplotlib (para visualización)

## Instalación

```bash
# Clonar el repositorio
git clone https://github.com/paniagua-humbe/AG_Smart_Batch.git
cd

# Instalar dependencias
pip install numpy matplotlib
```

## Uso

```bash
# Ejecutar el programa principal
python main.py
```

El programa solicitará los siguientes parámetros:
- Tamaño de la cuadrícula
- Número de áreas verdes
- Número de drenajes
- Número de tanques de agua
- Archivo de elevación (opcional)

## Estructura del Proyecto

- `main.py`: Interfaz principal y visualización
- `ag_core.py`: Implementación del algoritmo genético
- `Datos_entrada/`: Directorio con archivos de ejemplo para datos de elevación

## Cómo Funciona

El sistema utiliza un algoritmo genético para optimizar la distribución urbana:

1. **Representación**: Cada individuo representa una configuración de calles verticales y horizontales.
2. **Evaluación**: La función de fitness evalúa la calidad de cada solución basándose en:
   - Número de lotes residenciales
   - Distribución de áreas verdes
   - Accesibilidad a calles
   - Optimización topográfica (si hay datos de elevación)
3. **Evolución**: A través de operadores genéticos (selección, cruce, mutación), el algoritmo mejora iterativamente las soluciones.

## Licencia

Este proyecto está licenciado bajo la Licencia MIT - ver el archivo LICENSE para más detalles.
