import pandas as pd

tables = {}
DATA_DIR = "data/Lookup_Tables"

def read_table (name):
    if name not in tables:
        df = pd.read_excel(f"{DATA_DIR}/{name}.XLSX")
        # Formateo todas las columnas igual y quito espacios
        df.columns = [c.strip() for c in df.columns]
        tables[name] = df
    return tables[name]

def load_tables():
    names = [
        "zonas",
        "C1_bloque",
        "C1_unifamiliar",
        "C1_bloque_verano",
        "C1_unifamiliar_verano",
        "Dispersion R",
        "Dispersion R verano",
        "sci_referencia",
        "scv_referencia",
        "SEER",
        "HSPF_nuevo",
        "HSPF_existente",
        "Temp red ACS",
        "ACS_SPFnuevo",
        "ACS_SPFexistente",
        "CMECon",
        "CMESin",
        "Penetracion",
        "Factores",
        "impuestos",
        "tarifas",
        "pvpc",
        "pesos tarifa electrica",
        "pesos tarifa electrica verano",
        "alquiler equipos",
    ]
    for name in names:
        read_table(name)

def lookup_row(df, columna, value):
   # Devuelve la PRIMERA fila (como df) donde df[columna] == valor.
    # Si no existe, lanza error.

    rows = df[df[columna] == value]
    if len(rows) == 0:
        raise ValueError(f"No encontrado: {columna}={value}")
    return rows.iloc[0]  # primera coincidencia

def lookup_value(df, fila, columna):

    try:
        if isinstance(columna, int):
            return df.iloc[fila - 1, columna - 1]
        elif isinstance(columna, str):
            return df.iloc[fila - 1][columna]
        else:
            raise TypeError("columna debe ser el índice de la columna entero o el nombre de columna")
    except (IndexError, KeyError):
        raise ValueError(f"Lookup fuera de rango: fila={fila}, columna={columna}")
