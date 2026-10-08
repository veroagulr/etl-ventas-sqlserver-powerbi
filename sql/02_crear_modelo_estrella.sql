USE VentasDW;
GO

CREATE TABLE DimCliente (
    cliente_key INT IDENTITY(1,1) PRIMARY KEY,
    cliente_id  INT NOT NULL,
    nombre      NVARCHAR(200) NOT NULL,
    ciudad      NVARCHAR(150) NULL,
    segmento    NVARCHAR(50) NULL
);
GO

CREATE TABLE DimProducto (
    producto_key    INT IDENTITY(1,1) PRIMARY KEY,
    producto_id     INT NOT NULL,
    nombre_producto NVARCHAR(200) NOT NULL,
    categoria       NVARCHAR(100) NULL,
    precio_valido   BIT NOT NULL DEFAULT 1
);
GO

CREATE TABLE DimFecha (
    fecha_key   INT PRIMARY KEY,      
    fecha       DATE NOT NULL, 
    anio        INT NOT NULL,
    mes         INT NOT NULL,
    nombre_mes  NVARCHAR(20) NOT NULL,
    trimestre   INT NOT NULL,
    dia_semana  NVARCHAR(20) NOT NULL
);
GO

CREATE TABLE FactVenta (
    venta_id         INT NOT NULL,
    cliente_key      INT NOT NULL REFERENCES DimCliente(cliente_key),
    producto_key     INT NOT NULL REFERENCES DimProducto(producto_key),
    fecha_key        INT NOT NULL REFERENCES DimFecha(fecha_key),
    cantidad         INT NOT NULL,
    precio_unitario  DECIMAL(10,2) NOT NULL,
    monto_total      DECIMAL(10,2) NOT NULL,
    cantidad_valida  BIT NOT NULL
);
GO