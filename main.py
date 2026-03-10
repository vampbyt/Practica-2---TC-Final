import sys
from PyQt6.QtWidgets import QApplication
from vista import VistaLenguaje
from controlador import ControlLenguaje

def main():
    app = QApplication(sys.argv)

    modelo_lenguajes = []
    visi = VistaLenguaje() 
    control = ControlLenguaje(modelo_lenguajes, visi)
    
    visi.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()