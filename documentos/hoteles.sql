-- Crear la base de datos
CREATE DATABASE IF NOT EXISTS hoteles;
USE hoteles;

-- Tabla: categorías de hotel
CREATE TABLE categorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL
);

-- Tabla: hoteles
CREATE TABLE hoteles (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    direccion VARCHAR(150),
    telefono VARCHAR(20),
    anio_apertura INT,
    categoria_id INT,
    FOREIGN KEY (categoria_id) REFERENCES categorias(id)
);

-- Tabla: tipos de habitación
CREATE TABLE tipos_habitacion (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion TEXT
);

-- Tabla: habitaciones
CREATE TABLE habitaciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    codigo VARCHAR(10) NOT NULL,
    numero INT,
    piso INT,
    estado ENUM('disponible', 'ocupada') DEFAULT 'disponible',
    hotel_id INT,
    tipo_id INT,
    FOREIGN KEY (hotel_id) REFERENCES hoteles(id),
    FOREIGN KEY (tipo_id) REFERENCES tipos_habitacion(id)
);

-- Tabla: tipos de cliente
CREATE TABLE tipos_cliente (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL -- nacional, extranjero, agencia, etc.
);

-- Tabla: clientes
CREATE TABLE clientes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    tipo_cliente_id INT,
    es_juridico BOOLEAN DEFAULT 0, -- true si es agencia
    identificacion VARCHAR(50),
    FOREIGN KEY (tipo_cliente_id) REFERENCES tipos_cliente(id)
);

-- Tabla: motivos de viaje
CREATE TABLE motivos_viaje (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL -- turismo, negocios, salud, etc.
);

-- Tabla: temporadas
CREATE TABLE temporadas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    fecha_inicio DATE,
    fecha_fin DATE
);

-- Tabla: reservas
CREATE TABLE reservas (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cliente_id INT,
    habitacion_id INT,
    motivo_viaje_id INT,
    fecha_inicio DATE,
    fecha_fin DATE,
    temporada_id INT,
    precio DECIMAL(10,2),
    aplica_iva BOOLEAN,
    FOREIGN KEY (cliente_id) REFERENCES clientes(id),
    FOREIGN KEY (habitacion_id) REFERENCES habitaciones(id),
    FOREIGN KEY (motivo_viaje_id) REFERENCES motivos_viaje(id),
    FOREIGN KEY (temporada_id) REFERENCES temporadas(id)
);

-- Tabla: usuarios del sistema
CREATE TABLE usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100),
    correo VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    rol ENUM('admin', 'recepcionista') DEFAULT 'recepcionista'
);
