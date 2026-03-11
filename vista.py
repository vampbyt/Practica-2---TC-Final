import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QPushButton, QListWidget, QFileDialog, QMessageBox, QInputDialog
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

class VistaLenguaje(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Práctica 2 - Operaciones entre lenguajes")
        self.setGeometry(100, 100, 500, 600)

        self.setStyleSheet("QPushButton { background-color: #6495ED; color: white; border-radius: 5px; min-height: 30px; }")
        self.layout = QVBoxLayout()

        self.label = QLabel("OPERACIONES ENTRE LENGUAJES")
        self.label.setFont(QFont("Arial", 16, QFont.Weight.Bold))
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.layout.addWidget(self.label)

        self.resultadoListaWidget = QListWidget()
        self.resultadoListaWidget.setWordWrap(True)
        self.resultadoListaWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        
        self.resultadoListaWidget.setStyleSheet("background-color: #DCDCDC; color: black; border-radius: 10px; padding: 5px;")
        self.resultadoListaWidget.setFont(QFont("Courier New", 10))
        self.resultadoListaWidget.setMinimumHeight(150)
        self.layout.addWidget(self.resultadoListaWidget)

        self.botonSubir = QPushButton("Subir archivo")
        self.botonOriginales = QPushButton("Ver lenguajes originales") 
        self.botonUnion = QPushButton("Unión")
        self.botonConcatenacion = QPushButton("Concatenación")
        self.botonPotencia = QPushButton("Potencia")
        self.botonCerraduraP = QPushButton("Cerradura positiva")
        self.botonCerraduraK = QPushButton("Cerradura de Kleene")
        self.botonReflex = QPushButton("Reflexión")
        self.botonGuardar = QPushButton("Guardar resultado actual")

        botones = [self.botonSubir, self.botonOriginales, self.botonUnion, self.botonConcatenacion, 
                   self.botonPotencia, self.botonCerraduraP, self.botonCerraduraK, self.botonReflex, self.botonGuardar]
        for b in botones:
            self.layout.addWidget(b)
        self.setLayout(self.layout)

    def obtenerRutasArchivos(self):
        archivos, _ = QFileDialog.getOpenFileNames(self, "Selecciona 3 archivos", "", "Archivos de texto (*.txt)")
        if len(archivos) != 3:
            QMessageBox.warning(self, "Error", "Por favor, seleccione 3 archivos.")
            return None
        return archivos

    def mostrarMensajeExito(self, mensaje):
        QMessageBox.information(self, "Éxito", mensaje)

    def mostrarMensajeError(self, mensaje):
        QMessageBox.critical(self, "Error", mensaje)

    def seleccionarIndices(self, binaria=True):
        items = ["1", "2", "3"]
        l1, ok1 = QInputDialog.getItem(self, "Seleccionar", "Lenguaje A:", items, 0, False)
    
        if ok1:
            if binaria:
                l2, ok2 = QInputDialog.getItem(self, "Seleccionar", "Lenguaje B:", items, 0, False)
                if ok2:
                    return int(l1) - 1, int(l2) - 1
            else:
                return int(l1) - 1
        return None

    def obtenerRutaGuardar(self):
        ruta, _ = QFileDialog.getSaveFileName(self, "Guardar lenguaje resultante", "", "Archivos de texto (*.txt)")
        return ruta