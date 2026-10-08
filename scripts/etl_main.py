"""
Orquestador del pipeline ETL.
Ejecuta en orden: extracción -> limpieza -> carga a staging en SQL Server.
Registra todo en logs/ y termina de forma controlada si algo falla.
"""

import sys
from sqlalchemy import text
from conexion import obtener_engine
from extraccion import extraer_clientes, extraer_productos, extraer_ventas
from limpieza import limpiar_clientes, limpiar_productos, limpiar_ventas
from logger_config import configurar_logger

logger = configurar_logger()


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
    logger.info(f"[staging.{nombre_tabla}] {len(df)} filas cargadas")

def cargar_dw(engine):
    with engine.begin() as conexion:
        antes = conexion.execute(text("SELECT COUNT(*) FROM FactVenta")).scalar()
        conexion.execute(text("EXEC dbo.usp_cargar_dw"))
        despues = conexion.execute(text("SELECT COUNT(*) FROM FactVenta")).scalar()

    logger.info(f"[DW] FactVenta: {antes} -> {despues} filas ({despues - antes} nuevas)")

def main():
    logger.info("=== Iniciando pipeline ETL ===")

    try:
        engine = obtener_engine()

        logger.info("Extrayendo archivos CSV...")
        df_clientes = extraer_clientes()
        df_productos = extraer_productos()
        df_ventas = extraer_ventas()

        logger.info("Aplicando reglas de limpieza y validación...")
        df_clientes = limpiar_clientes(df_clientes)
        df_productos = limpiar_productos(df_productos)
        ids_clientes_validos = set(df_clientes["cliente_id"])
        df_ventas = limpiar_ventas(df_ventas, ids_clientes_validos)

        logger.info("Cargando datos limpios a staging...")
        cargar_a_staging(engine, "clientes", df_clientes)
        cargar_a_staging(engine, "productos", df_productos)
        cargar_a_staging(engine, "ventas", df_ventas)

        logger.info("Cargando del staging al Data Warehouse...")
        cargar_dw(engine)

        logger.info("=== Pipeline completado exitosamente ===")

    except FileNotFoundError as e:
        logger.critical(f"Archivo fuente no encontrado: {e}")
        sys.exit(1)

    except Exception as e:
        logger.critical(f"Pipeline detenido por un error inesperado: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()