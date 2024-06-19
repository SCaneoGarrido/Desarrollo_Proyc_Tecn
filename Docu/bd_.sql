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
CREATE TABLE Asistentes (
    AsistenteID SERIAL PRIMARY KEY,
    Nombre VARCHAR(255) NOT NULL,
    Edad INT NOT NULL,
    apellido VARCHAR(255),
    direccion VARCHAR(255),
    estadoCivil VARCHAR(255),
    genero VARCHAR(50),
    rut VARCHAR(255) NOT NULL UNIQUE
    FOREIGN KEY curso_id REFERENCES Cursos(CursoID);
);

-- Crear tabla Cursos
CREATE TABLE Cursos (
    CursoID SERIAL PRIMARY KEY,
    Nombre_curso VARCHAR(255) NOT NULL,
    Fecha_Inicio DATE NOT NULL,
    Fecha_Fin DATE NOT NULL,
    Colab_id INT,
    FOREIGN KEY (Colab_id) REFERENCES muni_colab(id)
);

-- Crear tabla Asistencia
CREATE TABLE Asistencia (
    AsistenciaID SERIAL PRIMARY KEY,
    CursoID INT,
    AsistenteID INT,
    Fecha DATE NOT NULL,
    Estado VARCHAR(50) NOT NULL,
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
    FOREIGN KEY (AsistenteID) REFERENCES Asistentes(AsistenteID)
);