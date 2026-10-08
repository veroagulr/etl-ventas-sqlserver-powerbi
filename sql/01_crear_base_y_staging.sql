IF DB_ID('VentasDW') IS NULL
    CREATE DATABASE VentasDW;
GO

USE VentasDW;
GO

IF SCHEMA_ID('staging') IS NULL
    EXEC('CREATE SCHEMA staging');
GO

CREATE TABLE staging.clientes (
    cliente_id      INT,
    nombre          NVARCHAR(200) NULL,
    ciudad          NVARCHAR(150) NULL,
    segmento        NVARCHAR(50)  NULL,
    fecha_registro  DATE          NULL
);

CREATE TABLE staging.productos (
    producto_id      INT,
    nombre_producto  NVARCHAR(200) NULL,
    categoria        NVARCHAR(100) NULL,
    precio_unitario  DECIMAL(10,2) NULL,
    precio_valido    BIT           NULL
);

CREATE TABLE staging.ventas (
    venta_id         INT,
    cliente_id       INT,
    producto_id      INT,
    fecha_venta      DATE          NULL,
    cantidad         INT           NULL,
    precio_unitario  DECIMAL(10,2) NULL,
    monto_total      DECIMAL(10,2) NULL,
    cantidad_valida  BIT           NULL
);
GO