import pandas as pd
from pathlib import Path

tables = {}
DATA_DIR = Path(__file__).parent / "data" / "Lookup_Tables"

def load_all_tables():
    tables['zonas'] = pd.read_excel(DATA_DIR / 'zonas.xlsx')
    tables['C1_bloque'] = pd.read_excel(DATA_DIR / 'C1_bloque.xlsx', thousands='.', decimal=',')
    tables['C1_unifamiliar'] = pd.read_excel(DATA_DIR / 'C1_unifamiliar.xlsx', thousands='.', decimal=',')
    tables['C1_bloque_verano'] = pd.read_excel(DATA_DIR / 'C1_bloque_verano.xlsx', thousands='.', decimal=',')
    tables['C1_unifamiliar_verano'] = pd.read_excel(DATA_DIR / 'C1_unifamiliar_verano.xlsx', thousands='.', decimal=',')
    tables['Dispersion R'] = pd.read_excel(DATA_DIR / 'Dispersion R.xlsx', thousands='.', decimal=',')
    tables['Dispersion R verano'] = pd.read_excel(DATA_DIR / 'Dispersion R verano.xlsx', thousands='.', decimal=',')
    tables['sci_referencia'] = pd.read_excel(DATA_DIR / 'sci_referencia.xlsx', thousands='.', decimal=',')
    tables['scv_referencia'] = pd.read_excel(DATA_DIR / 'scv_referencia.xlsx', thousands='.', decimal=',')
    tables['SEER'] = pd.read_excel(DATA_DIR / 'SEER.xlsx', thousands='.', decimal=',')
    tables['HSPF_nuevo'] = pd.read_excel(DATA_DIR / 'HSPF_nuevo.xlsx', thousands='.', decimal=',')
    tables['HSPF_existente'] = pd.read_excel(DATA_DIR / 'HSPF_existente.xlsx', thousands='.', decimal=',')
    tables['Temp red ACS'] = pd.read_excel(DATA_DIR / 'Temp red ACS.xlsx', thousands='.', decimal=',')
    tables['ACS_SPFnuevo'] = pd.read_excel(DATA_DIR / 'ACS_SPFnuevo.xlsx', thousands='.', decimal=',')
    tables['ACS_SPFexistente'] = pd.read_excel(DATA_DIR / 'ACS_SPFexistente.xlsx', thousands='.', decimal=',')
    tables['CMECon'] = pd.read_excel(DATA_DIR / 'CMECon.xlsx', thousands='.', decimal=',')
    tables['CMESin'] = pd.read_excel(DATA_DIR / 'CMESin.xlsx', thousands='.', decimal=',')
    tables['Penetracion'] = pd.read_excel(DATA_DIR / 'Penetracion.xlsx', thousands='.', decimal=',')
    tables['Factores'] = pd.read_excel(DATA_DIR / 'Factores.xlsx', thousands='.', decimal=',')
    tables['impuestos'] = pd.read_excel(DATA_DIR / 'impuestos.xlsx', thousands='.', decimal=',')
    tables['tarifas'] = pd.read_excel(DATA_DIR / 'tarifas.xlsx', thousands='.', decimal=',')
    tables['pvpc'] = pd.read_excel(DATA_DIR / 'pvpc.xlsx', thousands='.', decimal=',')
    tables['pesos tarifa electrica'] = pd.read_excel(DATA_DIR / 'pesos tarifa electrica.xlsx', thousands='.', decimal=',')
    tables['pesos tarifa electrica verano'] = pd.read_excel(DATA_DIR / 'pesos tarifa electrica verano.xlsx', thousands='.', decimal=',')
    tables['alquiler equipos'] = pd.read_excel(DATA_DIR / 'alquiler equipos.xlsx', thousands='.', decimal=',')
    tables['Sur'] = pd.read_excel(DATA_DIR / 'Sur.xlsx', thousands='.', decimal=',')
    tables['Canarias'] = pd.read_excel(DATA_DIR / 'Canarias.xlsx', thousands='.', decimal=',')

    for name in tables:
        tables[name] = tables[name].dropna(how='all').reset_index(drop=True)

def lookup_row(table_name, columna, value):

    if table_name not in tables:
        raise ValueError(f"Tabla '{table_name}' no está cargada.")

    df = tables[table_name]

    if isinstance(columna, int):
        serie = df.iloc[:, columna]
    else:
        serie = df[columna]

    rows = df[serie.astype(str).str.strip().str.replace(r'\.0$', '', regex=True) == str(value).strip()]

    if len(rows) == 0:
        raise ValueError(f"No encontrado: {columna}={value} en '{table_name}'")

    return rows.index[0] + 1

def lookup_value(table_name, fila, columna):

    if table_name not in tables:
        raise ValueError(f"Tabla '{table_name}' no está cargada.")

    df = tables[table_name]

    try:
        if isinstance(columna, int):
            val = df.iloc[fila - 1, columna - 1]
        else:
            val = df.iloc[fila - 1][str(columna).strip()]
    except (IndexError, KeyError):
        raise ValueError(
            f"Lookup fuera de rango en '{table_name}': fila={fila}, columna={columna}"
        )

    # Auto-convert numeric strings (handles both "0,27" and "0.27")
    if isinstance(val, str):
        try:
            return float(val.replace(",", "."))
        except (ValueError, TypeError):
            return val  # keep as string if not numeric (e.g. "A3", "punta")
    
    return val