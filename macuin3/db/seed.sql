-- MACUIN Platform - Datos Semilla
-- Password para todos: password123

INSERT INTO roles (nombre, descripcion) VALUES
('admin', 'Administrador del sistema'),
('personal_interno', 'Empleado interno de MACUIN'),
('cliente_externo', 'Cliente externo');

INSERT INTO usuarios (email, password_hash, nombre, apellido, telefono, rol_id, activo) VALUES
('admin@macuin.com', '$2b$12$8kTpnuEQ3/uffxLHl9bmouwtorkc13mlgmrjYy7KHitxM9Ylaz.Iq', 'Carlos', 'Mendoza', '4421001000', 1, TRUE),
('ventas@macuin.com', '$2b$12$8kTpnuEQ3/uffxLHl9bmouwtorkc13mlgmrjYy7KHitxM9Ylaz.Iq', 'Ana', 'García', '4421002000', 2, TRUE),
('almacen@macuin.com', '$2b$12$8kTpnuEQ3/uffxLHl9bmouwtorkc13mlgmrjYy7KHitxM9Ylaz.Iq', 'Luis', 'Hernández', '4421003000', 2, TRUE),
('logistica@macuin.com', '$2b$12$8kTpnuEQ3/uffxLHl9bmouwtorkc13mlgmrjYy7KHitxM9Ylaz.Iq', 'Pedro', 'Ramírez', '4421004000', 2, TRUE),
('taller.roma@mail.com', '$2b$12$8kTpnuEQ3/uffxLHl9bmouwtorkc13mlgmrjYy7KHitxM9Ylaz.Iq', 'Roberto', 'López', '5551001000', 3, TRUE),
('refac.central@mail.com', '$2b$12$8kTpnuEQ3/uffxLHl9bmouwtorkc13mlgmrjYy7KHitxM9Ylaz.Iq', 'María', 'Sánchez', '5551002000', 3, TRUE);

INSERT INTO empleados (usuario_id, numero_empleado, departamento, puesto) VALUES
(1, 'EMP001', 'Dirección', 'Director General'),
(2, 'EMP002', 'Ventas', 'Ejecutivo de Ventas'),
(3, 'EMP003', 'Almacén', 'Jefe de Almacén'),
(4, 'EMP004', 'Logística', 'Coordinador de Envíos');

INSERT INTO clientes (usuario_id, razon_social, rfc, direccion, ciudad, estado, codigo_postal, tipo_cliente) VALUES
(5, 'Taller Mecánico Roma SA de CV', 'TMR200101ABC', 'Av. Insurgentes 450', 'CDMX', 'CDMX', '06700', 'taller'),
(6, 'Refaccionaria Central del Bajío', 'RCB190501XYZ', 'Blvd. Bernardo Quintana 200', 'Querétaro', 'Querétaro', '76090', 'refaccionaria');

INSERT INTO categorias (nombre, descripcion) VALUES
('Frenos', 'Pastillas, discos, balatas y componentes de frenado'),
('Motor', 'Filtros, bujías, bandas y componentes de motor'),
('Suspensión', 'Amortiguadores, resortes, bujes'),
('Eléctrico', 'Baterías, alternadores, marchas'),
('Transmisión', 'Clutch, volantes, crucetas'),
('Lubricantes', 'Aceites, grasas y líquidos'),
('Carrocería', 'Espejos, faros, defensas');

INSERT INTO autopartes (sku, nombre, descripcion, marca, categoria_id, precio, compatibilidad_vehicular, activo) VALUES
('FRE-001', 'Pastillas de freno delanteras cerámicas', 'Pastillas de alto rendimiento para frenado suave', 'Brembo', 1, 850.00, 'Nissan Sentra 2018-2024, Versa 2020-2024', TRUE),
('FRE-002', 'Disco de freno ventilado 280mm', 'Disco ventilado de alta resistencia', 'Wagner', 1, 1200.00, 'VW Jetta 2015-2024, Golf 2015-2024', TRUE),
('FRE-003', 'Balatas traseras semimetálicas', 'Balatas de larga duración', 'TRW', 1, 620.00, 'Chevrolet Aveo 2018-2023', TRUE),
('MOT-001', 'Filtro de aceite premium', 'Filtro sintético de alta eficiencia', 'MANN', 2, 180.00, 'Universal motores 1.4L-2.5L', TRUE),
('MOT-002', 'Bujía de iridio', 'Bujía larga vida 100,000 km', 'NGK', 2, 250.00, 'Toyota Corolla 2015-2024', TRUE),
('MOT-003', 'Kit banda de distribución', 'Banda con tensores, kit completo', 'Gates', 2, 2800.00, 'VW Jetta 2.0 2015-2020', TRUE),
('SUS-001', 'Amortiguador delantero gas', 'Amortiguador gas presurizado', 'Monroe', 3, 1500.00, 'Nissan March 2015-2024', TRUE),
('SUS-002', 'Resorte suspensión progresivo', 'Resorte progresivo mayor confort', 'Sachs', 3, 900.00, 'Chevrolet Spark 2017-2023', TRUE),
('ELE-001', 'Batería 600 CCA', 'Batería libre mantenimiento 12V', 'LTH', 4, 2200.00, 'Universal compactos y medianos', TRUE),
('ELE-002', 'Alternador remanufacturado 90A', 'Alternador garantía 2 años', 'Bosch', 4, 3500.00, 'Ford Focus 2012-2018', TRUE),
('TRA-001', 'Kit de clutch completo', 'Disco, plato y collarín', 'LUK', 5, 4200.00, 'Nissan Tsuru 2005-2017', TRUE),
('LUB-001', 'Aceite sintético 5W-30 4L', 'Aceite 100% sintético', 'Mobil', 6, 650.00, 'Universal', TRUE),
('LUB-002', 'Líquido de frenos DOT 4 500ml', 'Líquido alta temperatura', 'Prestone', 6, 120.00, 'Universal', TRUE),
('CAR-001', 'Faro delantero izquierdo LED', 'Faro con tecnología LED', 'Hella', 7, 5800.00, 'Mazda 3 2019-2024', TRUE),
('CAR-002', 'Espejo lateral derecho eléctrico', 'Espejo con desempañador', 'Depo', 7, 1800.00, 'Honda Civic 2016-2021', TRUE);

INSERT INTO inventario (autoparte_id, stock_actual, stock_minimo, ubicacion_almacen) VALUES
(1, 45, 10, 'A1-01'), (2, 30, 8, 'A1-02'), (3, 55, 10, 'A1-03'),
(4, 120, 20, 'B1-01'), (5, 80, 15, 'B1-02'), (6, 12, 5, 'B2-01'),
(7, 18, 5, 'C1-01'), (8, 22, 5, 'C1-02'), (9, 15, 5, 'D1-01'),
(10, 8, 3, 'D1-02'), (11, 10, 3, 'E1-01'), (12, 60, 15, 'F1-01'),
(13, 90, 20, 'F1-02'), (14, 6, 2, 'G1-01'), (15, 10, 3, 'G1-02');

INSERT INTO pedidos (folio, cliente_id, estatus, subtotal, impuesto, total, notas) VALUES
('PED-2024-0001', 1, 'enviado', 2550.00, 408.00, 2958.00, 'Entregar en horario matutino'),
('PED-2024-0002', 2, 'en_proceso', 5450.00, 872.00, 6322.00, NULL),
('PED-2024-0003', 1, 'recibido', 1300.00, 208.00, 1508.00, 'Pedido urgente');

INSERT INTO detalle_pedido (pedido_id, autoparte_id, cantidad, precio_unitario, subtotal) VALUES
(1, 1, 2, 850.00, 1700.00), (1, 4, 3, 180.00, 540.00), (1, 13, 1, 120.00, 120.00), (1, 5, 1, 250.00, 250.00),
(2, 6, 1, 2800.00, 2800.00), (2, 12, 2, 650.00, 1300.00), (2, 7, 1, 1500.00, 1500.00),
(3, 2, 1, 1200.00, 1200.00), (3, 13, 1, 120.00, 120.00);

INSERT INTO historial_estatus_pedido (pedido_id, estatus_anterior, estatus_nuevo, comentario, usuario_id) VALUES
(1, NULL, 'recibido', 'Pedido creado por cliente', 5),
(1, 'recibido', 'en_proceso', 'Producto preparado en almacén', 3),
(1, 'en_proceso', 'enviado', 'Enviado por paquetería DHL', 3),
(2, NULL, 'recibido', 'Pedido creado por cliente', 6),
(2, 'recibido', 'en_proceso', 'Listo para envío', 3),
(3, NULL, 'recibido', 'Pedido urgente creado', 5);
