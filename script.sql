PRAGMA foreign_keys = OFF;
BEGIN TRANSACTION;

DROP TABLE IF EXISTS signos_vitales;
DROP TABLE IF EXISTS presion_social;
DROP TABLE IF EXISTS medicion;
DROP TABLE IF EXISTS alumno;
DROP TABLE IF EXISTS grupo;

PRAGMA foreign_keys = ON;

CREATE TABLE grupo (
  id_grupo TEXT PRIMARY KEY,
  nombre_grupo TEXT NOT NULL UNIQUE
);

CREATE TABLE alumno (
  id_alumno INTEGER PRIMARY KEY AUTOINCREMENT,
  id_grupo TEXT NOT NULL,
  numero_control TEXT NOT NULL UNIQUE,
  nombre TEXT NOT NULL,
  apellido_paterno TEXT NOT NULL,
  apellido_materno TEXT NOT NULL,
  curp TEXT NOT NULL UNIQUE,
  genero TEXT NOT NULL CHECK(genero IN ('Masculino','Femenino','Otro')),
  fecha_nacimiento DATE NOT NULL,
  FOREIGN KEY(id_grupo) REFERENCES grupo(id_grupo)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE medicion (
  id_medicion INTEGER PRIMARY KEY AUTOINCREMENT,
  id_alumno INTEGER NOT NULL,
  fecha_hora DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  edad_actual INTEGER NOT NULL,
  peso NUMERIC(5,2) NOT NULL,
  estatura NUMERIC(4,2) NOT NULL,
  imc NUMERIC(5,2),
  categoria_imc TEXT,
  FOREIGN KEY(id_alumno) REFERENCES alumno(id_alumno)
    ON DELETE CASCADE ON UPDATE CASCADE
);

CREATE TABLE presion_social (
  id_presion_sistolica INTEGER PRIMARY KEY AUTOINCREMENT,
  presion_sistolica INTEGER NOT NULL,
  presion_diastolica INTEGER NOT NULL
);

CREATE TABLE signos_vitales (
  id_signo INTEGER PRIMARY KEY AUTOINCREMENT,
  id_medicion INTEGER NOT NULL,
  frecuencia_cardiaca INTEGER NOT NULL,
  frecuencia_respiratoria INTEGER NOT NULL,
  temperatura NUMERIC(4,1) NOT NULL,
  saturacion_oxigeno INTEGER NOT NULL,
  id_presion_sistolica INTEGER NOT NULL,
  glucemia NUMERIC(5,2),
  FOREIGN KEY(id_medicion) REFERENCES medicion(id_medicion)
    ON DELETE CASCADE ON UPDATE CASCADE,
  FOREIGN KEY(id_presion_sistolica) REFERENCES presion_social(id_presion_sistolica)
    ON DELETE RESTRICT ON UPDATE CASCADE
);

INSERT INTO grupo (id_grupo, nombre_grupo) VALUES
  ('A','A'),
  ('B','B'),
  ('C','C'),
  ('D','D'),
  ('F','F');

COMMIT;