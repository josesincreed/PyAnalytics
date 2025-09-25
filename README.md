# 🛍️ E-commerce Arte de Vivir – Data Analytics

Aplicación en **Python** para **limpiar, preparar y analizar** datos de ventas de el e-commerce El Arte de Vivir. El proyecto sigue una estructura de **Git Flow** y demuestra buenas prácticas de análisis de datos. Este proyecto permite cargar datos desde archivos CSV y JSON, preprocesarlos (manejo de valores nulos, estandarización de texto y limpieza de precios), unir y analizar la información para responder preguntas clave como: ¿Cuál es el producto con más unidades vendidas?, ¿Cuál es el ingreso total por categoría de producto?, y ¿Cuántos pedidos contienen más de 2 unidades?

## Estructura del Proyecto

ecommerce-analytics/  
├─ data/ (Archivos de datos de ejemplo: products.csv y orders.json)  
├─ src/ (preprocess.py: módulo de funciones de limpieza y carga, analisis.py: script principal de análisis)  
├─ .gitignore  
└─ README.md

## Requisitos

- Python 3.11 o superior  
- pandas

## Instalación y Uso

1. Clonar el repositorio:  
   `git clone https://github.com/<usuario>/ecommerce-analytics.git`  
   `cd ecommerce-analytics`

2. Crear y activar un entorno virtual (recomendado):  
   `python -m venv venv`  
   `# Windows: venv\Scripts\activate`  
   `# macOS / Linux: source venv/bin/activate`

3. Instalar dependencias:  
   `pip install pandas`

4. Ejecutar el análisis:  
   `cd src`  
   `python analisis.py`

Ejemplo de salida en consola:  
Producto con más ventas (por unidades): pulsera azul  
Ingresos totales por categoría:  
category  
accesorios    434.0  
decoración    255.0  
hogar          98.0  
Name: revenue, dtype: float64  
Número de pedidos con más de 2 unidades: 6

## Datos de Ejemplo

- products.csv: Catálogo de productos (ID, nombre, categoría, precio con símbolo `$` y valores nulos simulados).  
- orders.json: Pedidos de clientes (ID de pedido, ID de producto, cliente, cantidad).  
Estos archivos incluyen inconsistencias de texto y algunos valores faltantes para mostrar la utilidad del módulo de preprocesamiento.

## Flujo de Trabajo con Git Flow

- master: Rama protegida para versiones estables.  
- develop: Rama base para integrar nuevas características.  
- feature/*: Ramas de desarrollo para cada nueva función o mejora.  
- Pull Requests: Para fusionar feature/* en develop y luego en main.

## Preguntas de Análisis Respondidas

- Análisis de Frecuencia: Producto con más registros/ventas.  
- Análisis de Agregación: Ingresos totales agrupados por categoría.  
- Análisis con Filtrado y Conteo: Número de pedidos que superan un umbral (más de 2 unidades).

## Autor

Proyecto desarrollado por [Tu Nombre] como parte del Momento 2 – Data Analytics.

## Licencia

Este proyecto se distribuye bajo la licencia MIT. Consulta el archivo LICENSE si deseas más información.
