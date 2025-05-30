from PyQt6.QtWidgets import (
    QApplication, QWidget, QStackedWidget, QVBoxLayout, QLabel,
    QPushButton, QLineEdit, QComboBox, QFormLayout, QMessageBox
)
from PyQt6.QtGui import QPixmap, QFont
from PyQt6.QtCore import Qt
import os
from src.backend.database import Database

class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(850, 620)
        self.db = Database()
        self.alumno_id = None
        self.medicion_id = None
        self.imc = 0
        self.imc_rango = ""
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("CBTis 191 - Somatometría")
        self.stack = QStackedWidget()

        self.setStyleSheet("""
            QWidget {
                background-color: #87CEEB;  /* skyblue */
                color: #1b2838;
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            }
            QLineEdit, QComboBox {
                background: white;
                border: 1.5px solid #1b2838;
                border-radius: 6px;
                padding: 6px;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1b2838;
                color: white;
                font-size: 16px;
                border-radius: 8px;
                padding: 10px;
                font-weight: bold;
                min-height: 40px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #32475a;
            }
            QPushButton:pressed {
                background-color: #121d28;
            }
            QFormLayout {
                margin-top: 20px;
                margin-left: 30px;
                margin-right: 30px;
            }
        """)

        home = QWidget()
        h_layout = QVBoxLayout()
        h_layout.setContentsMargins(40, 30, 40, 30)
        h_layout.setSpacing(20)

        img_path = os.path.join(os.path.dirname(__file__), "usr.png")
        lbl = QLabel()
        pixmap = QPixmap(img_path)
        if not pixmap.isNull():
            lbl.setPixmap(pixmap.scaled(400, 200, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        lbl.setAlignment(Qt.AlignmentFlag.AlignCenter)
        h_layout.addWidget(lbl)

        intro_text = QLabel("Sistema de Registro Médico CBTis 191")
        intro_text.setFont(QFont("Arial", 30, QFont.Weight.Bold)) 
        intro_text.setAlignment(Qt.AlignmentFlag.AlignCenter)
        intro_text.setStyleSheet("color: #1b2838;")
        h_layout.addWidget(intro_text)

        btn = QPushButton("Agregar usuario")
        btn.setFixedHeight(50)
        btn.clicked.connect(lambda: self.stack.setCurrentIndex(1))
        h_layout.addWidget(btn, alignment=Qt.AlignmentFlag.AlignCenter)

        home.setLayout(h_layout)

        person = QWidget()
        pf = QFormLayout()
        pf.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        pf.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        pf.setHorizontalSpacing(30)
        pf.setVerticalSpacing(15)

        self.name_input = QLineEdit()
        self.age_input = QLineEdit()
        self.curp_input = QLineEdit()
        self.peso_input = QLineEdit()
        self.estatura_input = QLineEdit()
        self.perimetro_input = QLineEdit()
        self.control_input = QLineEdit()
        self.grupo_input = QComboBox()
        for grade in ["A","B","C","D","F"]:
            self.grupo_input.addItem(grade, grade)

        pf.addRow("Nombre completo:", self.name_input)
        pf.addRow("Edad:", self.age_input)
        pf.addRow("CURP:", self.curp_input)
        pf.addRow("Peso (kg):", self.peso_input)
        pf.addRow("Estatura (cm):", self.estatura_input)
        pf.addRow("Perímetro abdomen:", self.perimetro_input)
        pf.addRow("No. control:", self.control_input)
        pf.addRow("Grupo:", self.grupo_input)

        btn_next = QPushButton("Siguiente")
        btn_next.setFixedWidth(180)
        btn_next.clicked.connect(self.save_person)
        pf.addRow("", btn_next)

        person.setLayout(pf)

        med = QWidget()
        mf = QFormLayout()
        mf.setLabelAlignment(Qt.AlignmentFlag.AlignRight)
        mf.setFormAlignment(Qt.AlignmentFlag.AlignCenter)
        mf.setHorizontalSpacing(30)
        mf.setVerticalSpacing(15)

        self.tension_input = QLineEdit()
        self.freq_c_input = QLineEdit()
        self.freq_r_input = QLineEdit()
        self.temp_input = QLineEdit()
        self.sat_input = QLineEdit()
        self.gluc_input = QLineEdit()
        self.imc_result = QLabel("IMC: -")
        self.imc_result.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.imc_result.setStyleSheet("color: #1b2838; padding: 8px;")

        mf.addRow("Tensión Art. (sist/diast):", self.tension_input)
        mf.addRow("Frecuencia Cardiaca:", self.freq_c_input)
        mf.addRow("Frecuencia Respiratoria:", self.freq_r_input)
        mf.addRow("Temperatura:", self.temp_input)
        mf.addRow("Sat. Oxígeno:", self.sat_input)
        mf.addRow("Glucemia:", self.gluc_input)
        mf.addRow("IMC Calculado:", self.imc_result)

        btn_save = QPushButton("Guardar")
        btn_save.setFixedWidth(180)
        btn_save.setStyleSheet("background-color: #27ae60; color: white; font-weight: bold;")
        btn_save.clicked.connect(self.save_med)
        mf.addRow("", btn_save)

        med.setLayout(mf)

        self.stack.addWidget(home)
        self.stack.addWidget(person)
        self.stack.addWidget(med)

        self.setLayout(QVBoxLayout())
        self.layout().addWidget(self.stack)

    def save_person(self):
        try:
            peso = float(self.peso_input.text())
            estatura_cm = float(self.estatura_input.text())
            estatura = estatura_cm / 100 if estatura_cm >= 3 else estatura_cm
            self.imc = peso / (estatura ** 2)
        except Exception as e:
            QMessageBox.warning(self, "Error", f"Datos inválidos para peso/estatura: {e}")
            return

        self.imc_rango = self.db.calcular_rango_imc(self.imc)

        parts = self.name_input.text().split()
        data = {
            "id_grupo": self.grupo_input.currentData(),
            "numero_control": self.control_input.text(),
            "nombre": parts[0] if parts else "",
            "apellido_paterno": parts[1] if len(parts) > 1 else "",
            "apellido_materno": parts[2] if len(parts) > 2 else "",
            "curp": self.curp_input.text(),
            "genero": "Otro",
            "fecha_nacimiento": "2000-01-01"
        }
        self.alumno_id = self.db.add_alumno(data)
        med_data = {
            "id_alumno": self.alumno_id,
            "edad_actual": int(self.age_input.text()),
            "peso": peso,
            "estatura": estatura,
            "imc": round(self.imc, 2),
            "categoria_imc": self.imc_rango
        }
        self.medicion_id = self.db.add_medicion(med_data)
        self.stack.setCurrentIndex(2)
        self.imc_result.setText(f"IMC: {self.imc:.2f} ({self.imc_rango})")

    def save_med(self):
        try:
            sist, diast = map(int, self.tension_input.text().split("/"))
        except:
            QMessageBox.warning(self, "Error", "Formato de tensión inválido. Usa el formato: 120/80")
            return

        cur = self.db.conn.cursor()
        cur.execute(
            "INSERT INTO presion_social (presion_sistolica, presion_diastolica) VALUES (?, ?)",
            (sist, diast)
        )
        pres_id = cur.lastrowid

        signos = {
            "id_medicion": self.medicion_id,
            "frecuencia_cardiaca": int(self.freq_c_input.text()),
            "frecuencia_respiratoria": int(self.freq_r_input.text()),
            "temperatura": float(self.temp_input.text()),
            "saturacion_oxigeno": int(self.sat_input.text()),
            "id_presion_sistolica": pres_id,
            "glucemia": float(self.gluc_input.text()) if self.gluc_input.text() else None
        }

        self.db.add_signos_vitales(signos)
        QMessageBox.information(self, "Éxito", "Registro guardado correctamente.")
        self.close()
