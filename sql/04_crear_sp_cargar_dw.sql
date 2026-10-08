USE VentasDW;
GO

CREATE OR ALTER PROCEDURE dbo.usp_cargar_dw
AS
BEGIN
    SET NOCOUNT ON;

    BEGIN TRANSACTION;
    BEGIN TRY

        -- Solo clientes que aun no existen en la dimension
        INSERT INTO DimCliente (cliente_id, nombre, ciudad, segmento)
        SELECT s.cliente_id, s.nombre, s.ciudad, s.segmento
        FROM staging.clientes s
        WHERE NOT EXISTS (
            SELECT 1 FROM DimCliente d WHERE d.cliente_id = s.cliente_id
        );

        -- Solo productos nuevos
        INSERT INTO DimProducto (producto_id, nombre_producto, categoria, precio_valido)
        SELECT s.producto_id, s.nombre_producto, s.categoria, s.precio_valido
        FROM staging.productos s
        WHERE NOT EXISTS (
            SELECT 1 FROM DimProducto d WHERE d.producto_id = s.producto_id
        );

        -- Solo ventas nuevas (venta_id que aun no esta en la tabla de hechos)
        INSERT INTO FactVenta (
            venta_id, cliente_key, producto_key, fecha_key,
            cantidad, precio_unitario, monto_total, cantidad_valida
        )
        SELECT
            v.venta_id,
            dc.cliente_key,
            dp.producto_key,
            CONVERT(INT, FORMAT(v.fecha_venta, 'yyyyMMdd')),
            v.cantidad,
            v.precio_unitario,
            v.monto_total,
            v.cantidad_valida
        FROM staging.ventas v
        INNER JOIN DimCliente  dc ON dc.cliente_id  = v.cliente_id
        INNER JOIN DimProducto dp ON dp.producto_id = v.producto_id
        INNER JOIN DimFecha    df ON df.fecha_key   = CONVERT(INT, FORMAT(v.fecha_venta, 'yyyyMMdd'))
        WHERE NOT EXISTS (
            SELECT 1 FROM FactVenta f WHERE f.venta_id = v.venta_id
        );

        COMMIT TRANSACTION;
    END TRY
    BEGIN CATCH
        ROLLBACK TRANSACTION;
        THROW;  -- relanza el error para que Python lo capture y lo loguee
    END CATCH
END;
GO