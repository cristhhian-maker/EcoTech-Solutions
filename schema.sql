-- schema.sql
-- Base de datos para el sistema de gestión según Diagrama de Clases UML

CREATE DATABASE IF NOT EXISTS EcoTech;
USE EcoTech;

-- 1. Tabla: Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL UNIQUE,
    contrasena_hash VARCHAR(255) NOT NULL,
    activo BOOLEAN NOT NULL DEFAULT TRUE,
    rol VARCHAR(50) DEFAULT 'Empleado'
);

-- 2. Tabla: Departamentos
CREATE TABLE IF NOT EXISTS departamentos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    gerente_id INT NULL
);

-- 3. Tabla: Empleados
CREATE TABLE IF NOT EXISTS empleados (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    direccion VARCHAR(200) NOT NULL DEFAULT 'Sin dirección',
    telefono VARCHAR(30) NOT NULL DEFAULT '000-0000',
    fecha_inicio_contrato DATE NOT NULL,
    salario DECIMAL(10, 2) NOT NULL,
    departamento_id INT NULL,
    puesto VARCHAR(50) NOT NULL DEFAULT 'Empleado',
    codigo_interno VARCHAR(20) NOT NULL,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (departamento_id) REFERENCES departamentos(id) ON DELETE SET NULL
);

-- 4. Tabla: Proyectos
CREATE TABLE IF NOT EXISTS proyectos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    descripcion TEXT,
    fecha_inicio DATE NOT NULL
);

-- 5. Tabla Intermedia: Asignación de Empleados a Proyectos (0..* a 0..*)
CREATE TABLE IF NOT EXISTS empleado_proyecto (
    empleado_id INT NOT NULL,
    proyecto_id INT NOT NULL,
    PRIMARY KEY (empleado_id, proyecto_id),
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
);

-- 6. Tabla: Registros de Tiempo
CREATE TABLE IF NOT EXISTS registros_tiempo (
    id INT AUTO_INCREMENT PRIMARY KEY,
    fecha DATE NOT NULL,
    horas DECIMAL(5, 2) NOT NULL,
    descripcion TEXT,
    empleado_id INT NOT NULL,
    proyecto_id INT NOT NULL,
    FOREIGN KEY (empleado_id) REFERENCES empleados(id) ON DELETE CASCADE,
    FOREIGN KEY (proyecto_id) REFERENCES proyectos(id) ON DELETE CASCADE
);

-- 7. Tabla: Auditoría
CREATE TABLE IF NOT EXISTS auditorias (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    accion VARCHAR(100) NOT NULL,
    fecha DATETIME NOT NULL,
    detalle TEXT,
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE
);

-- 8. Tabla: Reportes
CREATE TABLE IF NOT EXISTS reportes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    tipo VARCHAR(50) NOT NULL,
    formato VARCHAR(20) NOT NULL,
    fecha_creacion DATETIME NOT NULL,
    contenido TEXT
);

-- 9. Tabla: Clientes (Compatibilidad con módulos preexistentes)
CREATE TABLE IF NOT EXISTS clientes (
    id_cliente INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    correo VARCHAR(100) NOT NULL,
    telefono VARCHAR(30) NOT NULL,
    codigo_interno VARCHAR(20) NOT NULL
);
