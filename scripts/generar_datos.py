import pandas as pd
import random
from datetime import datetime, timedelta
from faker import Faker

fake = Faker("es_MX")
random.seed(42)

N_Clientes = 200
segmentos = ["Retail", "Mayorista", "Corporativo"]

clientes = []
for cliente_id in range(1, N_Clientes+1):
    clientes.append({
        "cliente_id": cliente_id,
        "nombre": fake.name(),
        "ciudad": fake.city(),
        "segmento": random.choice(segmentos),
        "fecha_registro": fake.date_between(start_date="-3y", end_date="today")

    })

df_clientes = pd.DataFrame(clientes)

df_clientes.loc[df_clientes.sample(5, random_state=1).index,"nombre"] = None

categorias = ["Electronica", "Hogar", "Deportes", "Alimentos"]
N_Productos = 50

productos = []
for producto_id in range(1, N_Productos + 1):
    productos.append({
        "producto_id": producto_id,
        "nombre_producto": fake.word().capitalize() + " " + fake.word().capitalize(),
        "categoria": random.choice(categorias),
        "precio_unitario": round(random.uniform(10, 500), 2),
    })

df_productos = pd.DataFrame(productos)
 
# Problema intencional: un precio negativo (error de captura típico)
df_productos.loc[df_productos.sample(1, random_state=2).index, "precio_unitario"] = -25.00
 
# ------------------------------
# 3. VENTAS
# ------------------------------
N_VENTAS = 2000
ventas = []
 
for venta_id in range(1, N_VENTAS + 1):
    producto = df_productos.sample(1).iloc[0]
    cantidad = random.randint(1, 10)
    fecha = fake.date_between(start_date="-1y", end_date="today")
 
    ventas.append({
        "venta_id": venta_id,
        "cliente_id": random.randint(1, N_Clientes),
        "producto_id": producto["producto_id"],
        "fecha_venta": fecha,
        "cantidad": cantidad,
        "precio_unitario": producto["precio_unitario"],
        "monto_total": round(cantidad * producto["precio_unitario"], 2),
    })
 
df_ventas = pd.DataFrame(ventas)

indices_invalidos = df_ventas.sample(8, random_state=3).index
df_ventas.loc[indices_invalidos, "cliente_id"] = 9999
 
indices_cantidad = df_ventas.sample(4, random_state=4).index
df_ventas.loc[indices_cantidad, "cantidad"] = -1
 
df_ventas = pd.concat([df_ventas, df_ventas.sample(6, random_state=5)], ignore_index=True)
 
df_clientes.to_csv("data/raw/clientes.csv", index=False)
df_productos.to_csv("data/raw/productos.csv", index=False)
df_ventas.to_csv("data/raw/ventas.csv", index=False)
 
print("✅ Archivos generados en data/raw/")
print(f"   clientes.csv: {len(df_clientes)} filas")
print(f"   productos.csv: {len(df_productos)} filas")
print(f"   ventas.csv: {len(df_ventas)} filas")