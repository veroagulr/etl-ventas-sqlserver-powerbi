"""
Módulo de limpieza y validación.
Aplica dos tipos de reglas:
  - Reglas DURAS: el dato se elimina si no se cumple (rompe integridad).
  - Reglas SUAVES: el dato se conserva pero se marca con un flag para revisión.
"""

import pandas as pd


def limpiar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    filas_originales = len(df)

    df = df.dropna(subset=["nombre"])

    df = df.drop_duplicates(subset=["cliente_id"], keep="first")

    print(f"[clientes] {filas_originales} -> {len(df)} filas "
          f"({filas_originales - len(df)} eliminadas)")
    return df


def limpiar_productos(df: pd.DataFrame) -> pd.DataFrame:

    df["precio_valido"] = df["precio_unitario"] >= 0
    invalidos = (~df["precio_valido"]).sum()

    print(f"[productos] {len(df)} filas, {invalidos} con precio_valido=False (conservadas)")
    return df


def limpiar_ventas(df: pd.DataFrame, ids_clientes_validos: set) -> pd.DataFrame:
    filas_originales = len(df)

    df = df.drop_duplicates()

    df = df[df["cliente_id"].isin(ids_clientes_validos)]

    df["cantidad_valida"] = df["cantidad"] > 0
    invalidas = (~df["cantidad_valida"]).sum()

    print(f"[ventas] {filas_originales} -> {len(df)} filas "
          f"({filas_originales - len(df)} eliminadas por duplicado/huérfana, "
          f"{invalidas} con cantidad_valida=False conservadas)")
    return df