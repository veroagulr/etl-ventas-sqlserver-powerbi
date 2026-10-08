USE VentasDW;
GO

INSERT INTO DimCliente (cliente_id, nombre, ciudad, segmento)
SELECT cliente_id, nombre, ciudad, segmento
FROM staging.clientes;
GO
 
INSERT INTO DimProducto (producto_id, nombre_producto, categoria, precio_valido)
SELECT producto_id, nombre_producto, categoria, precio_valido
FROM staging.productos;
GO

INSERT INTO FactVenta (
    venta_id, cliente_key, producto_key, fecha_key,
    cantidad, precio_unitario, monto_total, cantidad_valida
)
SELECT
    v.venta_id,
    dc.cliente_key,
    dp.producto_key,
    CONVERT(INT, FORMAT(v.fecha_venta, 'yyyyMMdd'))  AS fecha_key,
    v.cantidad,
    v.precio_unitario,
    v.monto_total,
    v.cantidad_valida
FROM staging.ventas v
INNER JOIN DimCliente dc ON dc.cliente_id = v.cliente_id
INNER JOIN DimProducto dp ON dp.producto_id = v.producto_id
INNER JOIN DimFecha df ON df.fecha_key = CONVERT(INT, FORMAT(v.fecha_venta, 'yyyyMMdd'));
GO

SELECT
    (SELECT COUNT(*) FROM DimCliente)  AS total_clientes,
    (SELECT COUNT(*) FROM DimProducto) AS total_productos,
    (SELECT COUNT(*) FROM DimFecha)    AS total_fechas,
    (SELECT COUNT(*) FROM staging.ventas) AS staging_ventas,
    (SELECT COUNT(*) FROM FactVenta)   AS total_factventa;
GO