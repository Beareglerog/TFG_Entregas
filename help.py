import pandas as pd

tables = {}
DATA_DIR = "data/Lookup_Tables"

def load_all_tables():
    """Carga todas las tablas al inicio"""
    tables['zonas'] = pd.read_excel(f'{DATA_DIR}/zonas.xlsx')
    tables['C1_bloque'] = pd.read_excel(f'{DATA_DIR}/C1_bloque.xlsx')
    tables['C1_unifamiliar'] = pd.read_excel(f'{DATA_DIR}/C1_unifamiliar.xlsx')
    tables['C1_bloque_verano'] = pd.read_excel(f'{DATA_DIR}/C1_bloque_verano.xlsx')
    tables['C1_unifamiliar_verano'] = pd.read_excel(f'{DATA_DIR}/C1_unifamiliar_verano.xlsx')
    tables['Dispersion R'] = pd.read_excel(f'{DATA_DIR}/Dispersion R.xlsx')
    tables['Dispersion R verano'] = pd.read_excel(f'{DATA_DIR}/Dispersion R verano.xlsx')
    tables['sci_referencia'] = pd.read_excel(f'{DATA_DIR}/sci_referencia.xlsx')
    tables['scv_referencia'] = pd.read_excel(f'{DATA_DIR}/scv_referencia.xlsx')
    tables['SEER'] = pd.read_excel(f'{DATA_DIR}/SEER.xlsx')
    tables['HSPF_nuevo'] = pd.read_excel(f'{DATA_DIR}/HSPF_nuevo.xlsx')
    tables['HSPF_existente'] = pd.read_excel(f'{DATA_DIR}/HSPF_existente.xlsx')
    tables['Temp red ACS'] = pd.read_excel(f'{DATA_DIR}/Temp red ACS.xlsx')
    tables['ACS_SPFnuevo'] = pd.read_excel(f'{DATA_DIR}/ACS_SPFnuevo.xlsx')
    tables['ACS_SPFexistente'] = pd.read_excel(f'{DATA_DIR}/ACS_SPFexistente.xlsx')
    tables['CMECon'] = pd.read_excel(f'{DATA_DIR}/CMECon.xlsx')
    tables['CMESin'] = pd.read_excel(f'{DATA_DIR}/CMESin.xlsx')
    tables['Penetracion'] = pd.read_excel(f'{DATA_DIR}/Penetracion.xlsx')
    tables['Factores'] = pd.read_excel(f'{DATA_DIR}/Factores.xlsx')
    tables['impuestos'] = pd.read_excel(f'{DATA_DIR}/impuestos.xlsx')
    tables['tarifas'] = pd.read_excel(f'{DATA_DIR}/tarifas.xlsx')
    tables['pvpc'] = pd.read_excel(f'{DATA_DIR}/pvpc.xlsx')
    tables['pesos tarifa electrica'] = pd.read_excel(f'{DATA_DIR}/pesos tarifa electrica.xlsx')
    tables['pesos tarifa electrica verano'] = pd.read_excel(f'{DATA_DIR}/pesos tarifa electrica verano.xlsx')
    tables['alquiler equipos'] = pd.read_excel(f'{DATA_DIR}/alquiler equipos.xlsx')
    tables['Sur'] = pd.read_excel(f'{DATA_DIR}/Sur.xlsx')

    for name in tables:
        #tables[name] = tables[name].dropna(how='all') #quito lineas vacias
        tables[name] = tables[name].dropna(how='all').reset_index(drop=True)

    
    # Limpiar columnas de todas las tablas
    #for name, df in tables.items():
     #    df.columns = [c.strip() for c in df.columns]

#def read_table (name):
   # if name not in tables:
       # df = pd.read_excel(f"{DATA_DIR}/{name}.XLSX")
        # Formateo todas las columnas igual y quito espacios
      #  df.columns = [c.strip() for c in df.columns]
    #    tables[name] = df
   # return tables[name]

#def load_tables():
    #names = [
      #  "zonas",
      #  "C1_bloque",
      #  "C1_unifamiliar",
     #   "C1_bloque_verano",
    #    "C1_unifamiliar_verano",
     #   "Dispersion R",
     #   "Dispersion R verano",
    #    "sci_referencia",
   #     "scv_referencia",
   #     "SEER",
   #     "HSPF_nuevo",
   ##     "HSPF_existente",
   #     "Temp red ACS",
   #     "ACS_SPFnuevo",
   #     "ACS_SPFexistente",
   #     "CMECon",
   #     "CMESin",
    #    "Penetracion",
   #     "Factores",
   #     "impuestos",
   #     "tarifas",
   #     "pvpc",
    #    "pesos tarifa electrica",
   #     "pesos tarifa electrica verano",
   #     "alquiler equipos",
  #  ]
  #  for name in names:
   #     read_table(name)

def lookup_row(table_name, columna, value):

    if table_name not in tables:
        raise ValueError(f"Tabla '{table_name}' no está cargada.")

    df = tables[table_name]

    if isinstance(columna, int):
        serie = df.iloc[:, columna]
    else:
        serie = df[columna]

    rows = df[serie.astype(str).str.strip().str.replace('.0', '', regex=False) == str(value).strip()]

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