from pathlib import Path
import pandas as pd
from preprocess import (
    load_data,
    handle_missing_values,
    standardize_text,
    clean_price_column,
)

# Función para imprimir títulos con estilo
def print_title(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title) + "\n")

# Función para imprimir resultados destacados
def print_result(label, value, emoji=""):
    print(f"{emoji} {label}: {value}")

# Cargar datos 
productos = load_data(Path("../data/products.csv"))
pedidos   = load_data(Path("../data/orders.json"))

# Manejo de valores nulos
productos = handle_missing_values(productos, strategy="drop")
pedidos   = handle_missing_values(pedidos,   strategy="fill0")

# Estandarizar texto en columnas de texto
productos = standardize_text(productos, ["nombre", "categoría"])

# Limpiar columna de precios (eliminar $ y convertir a float)
productos = clean_price_column(productos, "precio")

# Validar columnas clave para el merge 
required_cols_productos = {"id", "nombre", "categoría", "precio"}
required_cols_pedidos   = {"product_id", "quantity"}

missing_prod = required_cols_productos - set(productos.columns)
missing_ord  = required_cols_pedidos   - set(pedidos.columns)

if missing_prod:
    raise KeyError(f"Faltan columnas en products.csv: {missing_prod}")
if missing_ord:
    raise KeyError(f"Faltan columnas en orders.json: {missing_ord}")

# Unir pedidos con productos por ID 
merged = pedidos.merge(productos, left_on="product_id", right_on="id", how="inner")

# Análisis de Frecuencia 
ventas_por_producto = merged.groupby("nombre")["quantity"].sum()
producto_top = ventas_por_producto.idxmax()
print_title("📊 Producto con más ventas")
print_result("Producto más vendido (unidades)", producto_top, "🔥")

# Análisis de Agregación
merged["ingresos"] = merged["precio"] * merged["quantity"]
ingresos_por_categoria = merged.groupby("categoría")["ingresos"].sum()

print_title("💰 Ingresos totales por categoría")
for categoria, ingreso in ingresos_por_categoria.items():
    print_result(f"Categoría '{categoria}'", f"${ingreso:,.2f}", "💵")

# Análisis con Filtrado y Conteo 
pedidos_grandes = merged[merged["quantity"] > 2].shape[0]
print_title("📦 Pedidos grandes")
print_result("Número de pedidos con más de 2 unidades", pedidos_grandes, "📬")

# 10. Fin del análisis
print("\n✅ Análisis completado con éxito!")
