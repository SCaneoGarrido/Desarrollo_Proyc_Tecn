-- Crear tabla muni_colab
CREATE TABLE muni_colab (
    id SERIAL PRIMARY KEY,
    correo VARCHAR(255) NOT NULL UNIQUE,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    hash VARCHAR(255) NOT NULL,
    salt VARCHAR(255) NOT NULL
);

-- Crear tabla Asistentes
CREATE TABLE asistentes (
    asistenteid SERIAL PRIMARY KEY,
    rut INT NOT NULL UNIQUE,
    digito_v CHAR(1) NOT NULL CHECK (digito_v ~ '^[0-9Kk]$'),
    nombre VARCHAR(255),
    telefono VARCHAR(14),
    correo VARCHAR(255) UNIQUE,
    genero VARCHAR(10) CHECK (genero IN ('Masculino', 'Femenino', 'Otro')),
    edad INT CHECK (edad >= 0),
    nacionalidad VARCHAR(100),
    comuna VARCHAR(100),
    barrio VARCHAR(100),
    cursoID INT,
    FOREIGN KEY (cursoID) REFERENCES Cursos(CursoID)
);


-- Crear tabla Cursos
CREATE TABLE Cursos (
    CursoID SERIAL PRIMARY KEY,
    Nombre_curso VARCHAR(255) NOT NULL,
    Fecha_Inicio DATE NOT NULL,
    Fecha_Fin DATE NOT NULL,
    Colab_id INT,
    escuela VARCHAR(255) NOT NULL,
    actividad_servicio VARCHAR(255) NOT NULL,
    insititucion VARCHAR(255) NOT NULL,
    mes VARCHAR(255) NOT NULL,
    FOREIGN KEY (Colab_id) REFERENCES muni_colab(id)
);


-- Crear tabla Asistencia
CREATE TABLE AsistenciaDF (
    AsistenciaID SERIAL PRIMARY KEY,
    CursoID INT,
    Fecha DATE NOT NULL,
    ArchivoAsistencia BYTEA,
    colab_id INT,
    FOREIGN KEY (colab_id) REFERENCES muni_colab(id),
    FOREIGN KEY (CursoID) REFERENCES Cursos(CursoID),
    FOREIGN KEY (AsistenteID) REFERENCES Asistentes(AsistenteID)
);


-- Crear tabla Certificados
CREATE TABLE Certificados (
    CertificadoID SERIAL PRIMARY KEY,
    CursoID INT,
    AsistenteID INT,
    ArchivoCertificado BYTEA,
    FOREIGN KEY (CursoID) REFERENCES Cursos(CursoID),
    FOREIGN KEY (AsistenteID) REFERENCES asistentes(asistenteid)
);
