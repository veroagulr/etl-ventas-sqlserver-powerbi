"""
Configuración centralizada de logging para el pipeline ETL.
Escribe simultáneamente a un archivo (historial) y a la consola (en vivo).
"""

import logging
import os
from datetime import datetime


def configurar_logger():
    os.makedirs("logs", exist_ok=True)

    nombre_archivo = f"logs/etl_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        handlers=[
            logging.FileHandler(nombre_archivo, encoding="utf-8"),
            logging.StreamHandler()
        ]
    )

    return logging.getLogger("etl_ventas")