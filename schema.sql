-- 1. Tabla de Equipos
CREATE TABLE equipos (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL UNIQUE
);

-- 2. Tabla de Usuarios
CREATE TABLE usuarios (
    id SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL
);

-- 3. Tabla de Partidos
CREATE TABLE partidos (
    id SERIAL PRIMARY KEY,
    local_id INTEGER NOT NULL REFERENCES equipos(id) ON DELETE CASCADE,
    visitante_id INTEGER NOT NULL REFERENCES equipos(id) ON DELETE CASCADE,
    fecha TIMESTAMP NOT NULL,
    goles_local INTEGER DEFAULT NULL,
    goles_visitante INTEGER DEFAULT NULL,
    fase VARCHAR(50), -- 'Fase de grupos', 'Octavos', etc.
    estadio VARCHAR(100)
);

-- 4. Tabla de Predicciones
CREATE TABLE predicciones (
    id SERIAL PRIMARY KEY,
    usuario_id INTEGER NOT NULL REFERENCES usuarios(id) ON DELETE CASCADE,
    partido_id INTEGER NOT NULL REFERENCES partidos(id) ON DELETE CASCADE,
    goles_local INTEGER NOT NULL,
    goles_visitante INTEGER NOT NULL,
    
    -- RESTRICCIÓN: Un usuario solo puede tener una predicción por cada partido
    UNIQUE(usuario_id, partido_id)
);
