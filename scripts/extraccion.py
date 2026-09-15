import pandas as pd

def extraer_clientes(ruta = "data/raw/clientes.csv"):
    return pd.read_csv(ruta)

def extraer_productos(ruta = "data/raw/productos.csv"):
    return pd.read_csv(ruta)

def extraer_ventas(ruta = "data/raw/ventas.csv"):
    return pd.read_csv(ruta) 