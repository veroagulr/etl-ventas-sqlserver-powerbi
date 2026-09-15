from sqlalchemy import create_engine

servidor = "localhost"
base_datos = "VentasDW"
driver = "ODBC Driver 17 for SQL Server"

def obtener_engine():
    cadena_conexion = (
        f"mssql+pyodbc://@{servidor}/{base_datos}"
        f"?driver={driver.replace(' ', '+')}"
        f"&trusted_connection=yes"
    )

    engine = create_engine(cadena_conexion)

    return engine


if __name__ == "__main__":

    engine = obtener_engine()
    with engine.connect() as conexion: 
        print("Conexion exitosa a", base_datos) 