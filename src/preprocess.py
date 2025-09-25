import pandas as pd
from pathlib import Path
import json

def load_data(file_path) -> pd.DataFrame:
    """
    Carga CSV o JSON (lista de objetos) en un DataFrame.
    - Para CSV usa pandas.read_csv
    - Para JSON usa json.load para leer un array de objetos.
    Acepta rutas tipo str o pathlib.Path.
    """
    file_path = Path(file_path)

    if file_path.suffix.lower() == ".csv":
        return pd.read_csv(file_path)

    elif file_path.suffix.lower() == ".json":
        # Lee el archivo completo como lista de diccionarios
        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            # Valida que realmente sea una lista de objetos
            if not isinstance(data, list):
                raise ValueError(
                    f"El archivo {file_path} no contiene una lista JSON válida."
                )
        return pd.DataFrame(data)

    else:
        raise ValueError("Formato no soportado: solo .csv o .json")

def handle_missing_values(df: pd.DataFrame, strategy: str = "drop") -> pd.DataFrame:
    """Maneja valores nulos: 'drop' para eliminar filas o 'fill0' para rellenar con 0."""
    if strategy == "drop":
        return df.dropna()
    elif strategy == "fill0":
        return df.fillna(0)
    else:
        raise ValueError("Estrategia no soportada: usa 'drop' o 'fill0'")

def standardize_text(df: pd.DataFrame, columns: list[str]) -> pd.DataFrame:
    """Convierte a minúsculas y quita espacios extra en las columnas de texto indicadas."""
    for col in columns:
        if col in df.columns:
            df[col] = df[col].astype(str).str.lower().str.strip()
    return df

def clean_price_column(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Elimina el símbolo '$' y convierte la columna a tipo float."""
    if column in df.columns:
        df[column] = df[column].replace(r"[\$,]", "", regex=True).astype(float)
    return df
