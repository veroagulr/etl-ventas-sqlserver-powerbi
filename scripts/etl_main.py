"""
Orquestador del pipeline ETL.
Ejecuta en orden: extracción -> limpieza -> carga a staging en SQL Server.
"""

from sqlalchemy import text
from conexion import obtener_engine
from extraccion import extraer_clientes, extraer_productos, extraer_ventas
from limpieza import limpiar_clientes, limpiar_productos, limpiar_ventas


def cargar_a_staging(engine, nombre_tabla, df):
    """Vacía la tabla de staging y carga el DataFrame, preservando el esquema SQL."""
    with engine.begin() as conexion:
        conexion.execute(text(f"TRUNCATE TABLE staging.{nombre_tabla}"))

    df.to_sql(
        nombre_tabla,
        con=engine,
        schema="staging",
        if_exists="append",
        index=False,
    )
    print(f"[staging.{nombre_tabla}] {len(df)} filas cargadas")


def main():
    print("=== Iniciando pipeline ETL ===")
    engine = obtener_engine()

    df_clientes = extraer_clientes()
    df_productos = extraer_productos()
    df_ventas = extraer_ventas()

    df_clientes = limpiar_clientes(df_clientes)
    df_productos = limpiar_productos(df_productos)
    ids_clientes_validos = set(df_clientes["cliente_id"])
    df_ventas = limpiar_ventas(df_ventas, ids_clientes_validos)

    cargar_a_staging(engine, "clientes", df_clientes)
    cargar_a_staging(engine, "productos", df_productos)
    cargar_a_staging(engine, "ventas", df_ventas)

    print("=== Pipeline completado ===")


if __name__ == "__main__":
    main()