from pathlib import Path
import pandas as pd
from preprocess import load_data, handle_missing_values, standardize_text, clean_price_column

# Estilos de prints
def print_title(title):
    print("\n" + "="*len(title))
    print(title)
    print("="*len(title) + "\n")

def print_result(label, value, emoji=""):
    print(f"{emoji} {label}: {value}")

# Carga de datos
productos = load_data(Path("../data/products.csv"))
pedidos   = load_data(Path("../data/orders.json"))
clientes  = load_data(Path("../data/customers.csv"))

# Renombrar columna 'id' de clientes a 'customer_id' 
if "id" in clientes.columns:
    clientes.rename(columns={"id": "customer_id"}, inplace=True)

# Manejo de valores nulos 
productos = handle_missing_values(productos, "drop")
pedidos   = handle_missing_values(pedidos, "fill0")
clientes  = handle_missing_values(clientes, "drop")

# Estandarizar texto y limpiar precios 
productos = standardize_text(productos, ["nombre", "categoría"])
clientes  = standardize_text(clientes, ["nombre", "ciudad", "email"])
productos = clean_price_column(productos, "precio")

# Validar columnas clave 
required_cols_productos = {"id", "nombre", "categoría", "precio"}
required_cols_pedidos   = {"product_id", "customer_id", "quantity"}
required_cols_clientes  = {"customer_id", "nombre", "ciudad", "email"}

for cols, df_name, df in [
    (required_cols_productos, "products.csv", productos),
    (required_cols_pedidos, "orders.json", pedidos),
    (required_cols_clientes, "customers.csv", clientes)
]:
    missing = cols - set(df.columns)
    if missing:
        raise KeyError(f"Faltan columnas en {df_name}: {missing}")

# Merge de datos 
merged = pedidos.merge(productos, left_on="product_id", right_on="id") \
                .merge(clientes, left_on="customer_id", right_on="customer_id")

merged.rename(columns={
    "nombre_x": "producto",
    "categoría": "categoria",
    "precio": "precio",
    "nombre_y": "cliente"
}, inplace=True)

# Producto más vendido 
ventas_por_producto = merged.groupby("producto")["quantity"].sum()
top_producto = ventas_por_producto.idxmax()
top_cantidad = ventas_por_producto.max()
print_title("📊 Producto con más ventas")
print_result("Producto más vendido (unidades)", f"{top_producto} ({top_cantidad} unidades)", "🔥")

# Ingresos totales por categoría
merged["ingresos"] = merged["precio"] * merged["quantity"]
ingresos_por_categoria = merged.groupby("categoria")["ingresos"].sum()
print_title("💰 Ingresos totales por categoría")
for cat, ingreso in ingresos_por_categoria.items():
    print_result(f"Categoría '{cat}'", f"${ingreso:,.2f}", "💵")

# Producto más vendido por ciudad 
top_ciudad_producto = merged.groupby(["ciudad","producto"])["quantity"].sum() \
                            .reset_index().sort_values(["ciudad","quantity"], ascending=[True, False])
top_ciudad_producto = top_ciudad_producto.groupby("ciudad").first().reset_index()
print_title("🏙️ Producto más vendido por ciudad")
for _, row in top_ciudad_producto.iterrows():
    print_result(f"Ciudad '{row['ciudad']}'", f"{row['producto']} ({row['quantity']} unidades)", "📦")

# Categoría más rentable por ciudad
top_ciudad_categoria = merged.groupby(["ciudad","categoria"])["ingresos"].sum() \
                             .reset_index().sort_values(["ciudad","ingresos"], ascending=[True, False])
top_ciudad_categoria = top_ciudad_categoria.groupby("ciudad").first().reset_index()
print_title("💹 Categoría más rentable por ciudad")
for _, row in top_ciudad_categoria.iterrows():
    print_result(f"Ciudad '{row['ciudad']}'", f"{row['categoria']} (${row['ingresos']:,.2f})", "🏘️")

# Pedidos grandes 
pedidos_grandes = merged[merged["quantity"] > 2].shape[0]
print_title("📬 Pedidos grandes")
print_result("Número de pedidos con más de 2 unidades", pedidos_grandes, "📦")

# Fin del análisis 
print("\n✅ Análisis completado con éxito!")
