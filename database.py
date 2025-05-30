import os
import sqlite3
import csv

class Database:
    def __init__(self, db_path="somatomatria.db", sql_schema_path=None):
        if sql_schema_path is None:
            base = os.path.dirname(__file__)
            sql_schema_path = os.path.join(base, "script.sql")

        db_exists = os.path.exists(db_path)
        self.conn = sqlite3.connect(db_path)
        self.conn.execute("PRAGMA foreign_keys = ON;")

        if not db_exists:
            self.load_schema(sql_schema_path)

    def load_schema(self, sql_schema_path):
        with open(sql_schema_path, "r", encoding="utf-8") as f:
            self.conn.executescript(f.read())

    def import_csv(self, table_name, csv_path):
        with open(csv_path, newline='', encoding="utf-8") as csvfile:
            reader = csv.DictReader(csvfile)
            cols = reader.fieldnames
            placeholders = ",".join("?" for _ in cols)
            stmt = f"INSERT INTO {table_name} ({','.join(cols)}) VALUES ({placeholders})"
            with self.conn:
                for row in reader:
                    self.conn.execute(stmt, [row[c] for c in cols])

    def add_alumno(self, alumno_data):
        cols = ",".join(alumno_data.keys())
        placeholders = ",".join("?" for _ in alumno_data)
        sql = f"INSERT INTO alumno ({cols}) VALUES ({placeholders})"
        cur = self.conn.cursor()
        cur.execute(sql, list(alumno_data.values()))
        self.conn.commit()
        return cur.lastrowid

    def add_medicion(self, medicion_data):
        cols = ",".join(medicion_data.keys())
        placeholders = ",".join("?" for _ in medicion_data)
        sql = f"INSERT INTO medicion ({cols}) VALUES ({placeholders})"
        cur = self.conn.cursor()
        cur.execute(sql, list(medicion_data.values()))
        self.conn.commit()
        return cur.lastrowid

    def add_signos_vitales(self, signos_data):
        cols = ",".join(signos_data.keys())
        placeholders = ",".join("?" for _ in signos_data)
        sql = f"INSERT INTO signos_vitales ({cols}) VALUES ({placeholders})"
        cur = self.conn.cursor()
        cur.execute(sql, list(signos_data.values()))
        self.conn.commit()
        return cur.lastrowid

    def calcular_rango_imc(self, imc):
        if imc < 18.5:
            return "Bajo peso"
        elif 18.5 <= imc < 25:
            return "Normal"
        elif 25 <= imc < 30:
            return "Sobrepeso"
        else:
            return "Obesidad"