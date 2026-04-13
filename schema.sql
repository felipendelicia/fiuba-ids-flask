CREATE DATABASE IF NOT EXISTS prode;

USE prode;

-- 1. Tabla de Equipos
CREATE TABLE IF NOT EXISTS equipos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Tabla de Usuarios
CREATE TABLE IF NOT EXISTS usuarios (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- 3. Tabla de Partidos
CREATE TABLE IF NOT EXISTS partidos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    local_id INT NOT NULL,
    visitante_id INT NOT NULL,
    fecha TIMESTAMP NOT NULL,
    goles_local INT DEFAULT NULL,
    goles_visitante INT DEFAULT NULL,
    fase VARCHAR(50) NOT NULL, -- 'Fase de grupos', 'Octavos', etc.
    estadio VARCHAR(100),

    FOREIGN KEY (local_id) REFERENCES equipos(id) ON DELETE CASCADE,
    FOREIGN KEY (visitante_id) REFERENCES equipos(id) ON DELETE CASCADE
);

-- 4. Tabla de Predicciones
CREATE TABLE IF NOT EXISTS predicciones (
    id INT AUTO_INCREMENT PRIMARY KEY,
    usuario_id INT NOT NULL,
    partido_id INT NOT NULL,
    goles_local INT NOT NULL,
    goles_visitante INT NOT NULL,
    
    FOREIGN KEY (usuario_id) REFERENCES usuarios(id) ON DELETE CASCADE,
    FOREIGN KEY (partido_id) REFERENCES partidos(id) ON DELETE CASCADE,
    -- RESTRICCIÓN: Un usuario solo puede tener una predicción por cada partido
    UNIQUE(usuario_id, partido_id)
);
