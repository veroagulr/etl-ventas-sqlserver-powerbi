"""
Módulo de limpieza y validación.
Reglas DURAS: el dato se elimina si no se cumple (rompe integridad).
Reglas SUAVES: el dato se conserva pero se marca con un flag para revisión.

Convención de logging:
  - INFO    -> progreso normal del proceso
  - WARNING -> filas eliminadas o marcadas como inválidas (requieren revisión)
"""

import logging
import pandas as pd

logger = logging.getLogger("etl_ventas")


def limpiar_clientes(df: pd.DataFrame) -> pd.DataFrame:
    filas_originales = len(df)

    df = df.dropna(subset=["nombre"])
    df = df.drop_duplicates(subset=["cliente_id"], keep="first")

    eliminadas = filas_originales - len(df)
    logger.info(f"[clientes] {filas_originales} -> {len(df)} filas procesadas")
    if eliminadas > 0:
        logger.warning(f"[clientes] {eliminadas} filas eliminadas (nombre nulo o duplicado)")

    return df


def limpiar_productos(df: pd.DataFrame) -> pd.DataFrame:
    df["precio_valido"] = df["precio_unitario"] >= 0
    invalidos = int((~df["precio_valido"]).sum())

    logger.info(f"[productos] {len(df)} filas procesadas")
    if invalidos > 0:
        logger.warning(f"[productos] {invalidos} filas con precio_valido=False (conservadas)")

    return df


def limpiar_ventas(df: pd.DataFrame, ids_clientes_validos: set) -> pd.DataFrame:
    filas_originales = len(df)

    df = df.drop_duplicates()
    df = df[df["cliente_id"].isin(ids_clientes_validos)]

    eliminadas = filas_originales - len(df)
    porcentaje_eliminado = (eliminadas / filas_originales) * 100 if filas_originales else 0

    df["cantidad_valida"] = df["cantidad"] > 0
    invalidas = int((~df["cantidad_valida"]).sum())

    logger.info(f"[ventas] {filas_originales} -> {len(df)} filas procesadas")

    if eliminadas > 0:
        logger.warning(f"[ventas] {eliminadas} filas eliminadas por duplicado/huérfana "
                       f"({porcentaje_eliminado:.1f}% del total)")
    if porcentaje_eliminado > 3:
        logger.warning("[ventas] El porcentaje de filas eliminadas supera el 3% esperado. "
                       "Revisar posible problema en el sistema origen.")
    if invalidas > 0:
        logger.warning(f"[ventas] {invalidas} filas con cantidad_valida=False (conservadas)")

    return df