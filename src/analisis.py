from pathlib import Path
import pandas as pd
from preprocess import (
    load_data,
    handle_missing_values,
    standardize_text,
    clean_price_column,
)

# === 1. Cargar datos ===
products = load_data(Path("../data/products.csv"))
orders   = load_data(Path("../data/orders.json"))

# === 2. Renombrar columnas del CSV para unificarlas ===
# Aseguramos que los nombres esperados existan antes de renombrar
rename_map = {}
if "nombre" in products.columns:
    rename_map["nombre"] = "name"
if "categoría" in products.columns:
    rename_map["categoría"] = "category"
if "precio" in products.columns:
    rename_map["precio"] = "price"
products = products.rename(columns=rename_map)

# === 3. Manejo de valores nulos ===
products = handle_missing_values(products, strategy="drop")
orders   = handle_missing_values(orders,   strategy="fill0")

# === 4. Estandarizar texto en columnas de texto ===
products = standardize_text(products, ["name", "category"])

# === 5. Limpiar columna de precios (eliminar $ y convertir a float) ===
products = clean_price_column(products, "price")

# === 6. Validar columnas clave para el merge ===
required_cols_products = {"id", "name", "category", "price"}
required_cols_orders   = {"product_id", "quantity"}

missing_prod = required_cols_products - set(products.columns)
missing_ord  = required_cols_orders   - set(orders.columns)

if missing_prod:
    raise KeyError(f"Faltan columnas en products.csv: {missing_prod}")
if missing_ord:
    raise KeyError(f"Faltan columnas en orders.json: {missing_ord}")

# === 7. Unir pedidos con productos por ID ===
merged = orders.merge(products, left_on="product_id", right_on="id", how="inner")

# === 8. Análisis de Frecuencia ===
# Producto con mayor cantidad de unidades vendidas
sales_by_product = merged.groupby("name")["quantity"].sum()
top_product = sales_by_product.idxmax()
print(f"Producto con más ventas (por unidades): {top_product}")

# === 9. Análisis de Agregación ===
# Ingresos totales por categoría (evita el FutureWarning de groupby.apply)
merged["revenue"] = merged["price"] * merged["quantity"]
revenue_by_category = merged.groupby("category", as_index=True)["revenue"].sum()
print("\nIngresos totales por categoría:")
print(revenue_by_category)

# === 10. Análisis con Filtrado y Conteo ===
# Número de pedidos con más de 2 unidades
big_orders_count = merged[merged["quantity"] > 2].shape[0]
print(f"\nNúmero de pedidos con más de 2 unidades: {big_orders_count}")
