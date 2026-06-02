-- Mi Árbol, Mi Historia — Setup DB
-- Ejecutar en Supabase SQL Editor

CREATE TABLE IF NOT EXISTS arbol_procesos (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    nombre              TEXT NOT NULL,
    correo              TEXT NOT NULL,
    estado              TEXT DEFAULT 'en_curso',  -- en_curso | completado
    patron_dominante    TEXT,
    patron_secundario   TEXT,
    patron_terciario    TEXT,
    intensidad_dominante TEXT,
    puntajes            JSONB,
    carta_generada      TEXT,
    acto_generado       TEXT,
    mensaje_liberacion  TEXT,
    practicas_generadas TEXT,
    fecha_creacion      TIMESTAMPTZ DEFAULT NOW(),
    fecha_completado    TIMESTAMPTZ
);

CREATE TABLE IF NOT EXISTS arbol_respuestas (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    proceso_id      UUID REFERENCES arbol_procesos(id) ON DELETE CASCADE,
    pregunta_id     INT NOT NULL,
    valor_escala    INT,        -- NULL si tipo = abierta
    texto_respuesta TEXT,       -- NULL si tipo = escala
    UNIQUE(proceso_id, pregunta_id)
);

CREATE TABLE IF NOT EXISTS arbol_familia (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    proceso_id          UUID REFERENCES arbol_procesos(id) ON DELETE CASCADE,
    generacion          TEXT,   -- bisabuelos | abuelos | padres
    nombre_referencia   TEXT,
    pais_origen         TEXT,
    notas_libres        TEXT,
    UNIQUE(proceso_id, generacion)
);

-- Deshabilitar RLS para acceso sin auth
ALTER TABLE arbol_procesos  DISABLE ROW LEVEL SECURITY;
ALTER TABLE arbol_respuestas DISABLE ROW LEVEL SECURITY;
ALTER TABLE arbol_familia    DISABLE ROW LEVEL SECURITY;
