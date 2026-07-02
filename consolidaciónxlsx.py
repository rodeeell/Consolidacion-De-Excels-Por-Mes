import pandas as pd
import json
import unicodedata
from pathlib import Path

carpeta_origen = Path("./archivosbase") #
archivos_salida = Path("./ejemplo_tabla.xlsx") #aquí cambiar el nombre de las salidas o carpeta de origen a conveniencia :)
procesados = Path("./procesados.json") 

meses = {
    "enero": "01",
    "febrero": "02",
    "marzo": "03",
    "abril": "04",
    "mayo": "05",
    "junio": "06",
    "julio": "07",
    "agosto": "08",
    "septiembre": "09",
    "octubre": "10",
    "noviembre": "11",
    "diciembre": "12",
}

def normalizar(txt: str) -> str:
    txt = txt.lower().strip()
    return "".join(c for c in unicodedata.normalize("NFD", txt) if unicodedata.category(c) != "Mn")

def extraer_periodo(texto: str) -> str:
    texto_norm = normalizar(texto)
    anio = next(
        (t for t in texto_norm.replace("&", " ").replace(".", " ").split() if t.isdigit() and len(t) == 4),
        None,
    )
    mes_num = next((num for mes, num in meses.items() if mes in texto_norm), None)
    if anio and mes_num:
        return f"{anio}{mes_num}"
    raise ValueError(f"No se pudo extraer periodo de: {texto}")

def procesar_archivo(filepath: Path) -> pd.DataFrame:
    df = pd.read_excel(filepath, sheet_name=0, header=2)

    col_concepto = next(
        (c for c in df.columns if isinstance(c, str) and c.strip().startswith("P&L")),
        None,
    )
    if col_concepto is None:
        raise ValueError("No se encontró la columna de conceptos P&L")

    periodo = extraer_periodo(str(col_concepto))

    df = df.rename(columns={col_concepto: "Concepto P&L"})
    columnas_compania = [
        c
        for c in df.columns
        if c != "Concepto P&L" and not (isinstance(c, str) and c.startswith("Unnamed"))
    ]
    df_largo = df.melt(
        id_vars=["Concepto P&L"],
        value_vars=columnas_compania,
        var_name="variable",
        value_name="value",
    )

    df_largo["variable"] = df_largo["variable"].astype(str).str.strip(" -_")
    df_largo["value"] = pd.to_numeric(df_largo["value"], errors="coerce")
    df_largo["value"] = df_largo["value"].fillna(0).round(2)

    return df_largo[["Concepto P&L", "variable", "value", "Periodo"]]

def cargar_log() -> set:
    if procesados.exists():
        with open(procesados, "r") as f:
            return set(json.load(f))
    return set()

def guardar_log(log: set):
    with open(procesados, "w") as f:
        json.dump(list(log), f)

def actualizar_tabla():
    log_procesados = cargar_log()

    archivos = sorted(carpeta_origen.glob("*.xlsx"))
    nuevos = [f for f in archivos if f.name not in log_procesados]

    if not nuevos:
        print("No hay nuevos archivos para procesar, Todo Ok!")
        return
    tablas_nuevas = []

    for f in nuevos:
        try:
            tablas_nuevas.append(procesar_archivo(f))
            log_procesados.add(f.name)
            print(f"Archivo {f.name} procesado correctamente")
        except Exception as e:
            print(f"Error al procesar el archivo {f.name}: {e}")
    if not tablas_nuevas:
        return

    df_nuevo = pd.concat(tablas_nuevas, ignore_index=True)

    if archivos_salida.exists():
        df_existente = pd.read_excel(archivos_salida)
        df_nuevo = pd.concat([df_existente, df_nuevo], ignore_index=True)

        df_nuevo = df_nuevo.drop_duplicates(
            subset=["Concepto P&L", "variable", "Periodo"], keep="last"
        )

    df_nuevo.to_excel(archivos_salida, index=False)
    guardar_log(log_procesados)
    print(f"Tabla actualizada y guardada en {archivos_salida}")

def main():
    actualizar_tabla()

if __name__ == "__main__":
    main()
