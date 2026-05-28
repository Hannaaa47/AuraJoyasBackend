CREATE DATABASE IF NOT EXISTS mcc_2026;
USE mcc_2026;

CREATE TABLE IF NOT EXISTS registros (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    categoria VARCHAR(80) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) DEFAULT 0,
    activo BOOLEAN DEFAULT TRUE,
    destacado BOOLEAN DEFAULT FALSE
);

CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(120) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS catalogo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT NOT NULL,
    precio DECIMAL(10,2) NOT NULL DEFAULT 0,
    existencia INT NOT NULL DEFAULT 0,
    imagen VARCHAR(255) DEFAULT NULL,
    activo BOOLEAN DEFAULT TRUE
);


INSERT INTO catalogo (nombre, descripcion, precio, existencia, imagen, activo)
VALUES
('Collar de plata 925', 'Collar artesanal elaborado en plata 925 con diseño de cadena veneciana. Longitud 45 cm, ideal para uso diario.', 349.00, 15, 'collar-plata-925.jpg', TRUE),
('Aretes de ópalo', 'Aretes con piedra de ópalo natural engarzada en plata fina. Diseño minimalista perfecto para cualquier ocasión.', 289.00, 8, 'aretes-opalo.jpg', TRUE),
('Pulsera de oro laminado', 'Pulsera tejida a mano con oro laminado de 18k. Cierre de mosquetón ajustable, resistente al agua.', 520.00, 5, 'pulsera-oro-laminado.jpg', TRUE),
('Anillo de turquesa', 'Anillo de plata con piedra turquesa natural. Talla ajustable, acabado pulido a mano.', 195.00, 12, 'anillo-turquesa.jpg', TRUE),
('Set de aretes perla', 'Juego de tres pares de aretes con perla cultivada en diferentes tamaños. Presentación en caja de regalo.', 410.00, 6, 'set-aretes-perla.jpg', TRUE),
('Dije de corazón', 'Dije de corazón en plata esterlina con baño de rodio. Compatible con cadenas de hasta 3 mm.', 120.00, 20, 'dije-corazon.jpg', TRUE),
('Tobillera de chapa de oro', 'Tobillera delicada con chapa de oro 14k y dije de estrella. Largo 22 cm con extensión de 3 cm.', 275.00, 9, 'tobillera-chapa-oro.jpg', TRUE),
('Collar de cuarzo rosa', 'Collar con colgante de cuarzo rosa natural pulido. Cadena de acero inoxidable dorado de 50 cm.', 180.00, 14, 'collar-cuarzo-rosa.jpg', TRUE);


INSERT INTO registros (nombre, categoria, descripcion, precio, activo, destacado)
VALUES
('Servicio de mantenimiento', 'Servicios', 'Revisión general del equipo o servicio.', 500.00, TRUE, FALSE),
('Producto básico', 'Productos', 'Producto de ejemplo para el negocio.', 150.00, TRUE, FALSE),
('Cita de diagnóstico', 'Citas', 'Agenda inicial para revisar una solicitud.', 0.00, TRUE, FALSE);
