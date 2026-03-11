import sys
from PyQt6.QtWidgets import QInputDialog
from modelo import OperacionesLenguajes

class ControlLenguaje:
    def __init__(self, modelo, vista):
        self.modelo = modelo 
        self.vista = vista

        # CONEXIONES 
        self.vista.botonSubir.clicked.connect(self.manejarArchivos)
        self.vista.botonUnion.clicked.connect(self.opUnion)
        self.vista.botonConcatenacion.clicked.connect(self.opConcatenacion)
        self.vista.botonPotencia.clicked.connect(self.opPotencia)
        self.vista.botonCerraduraP.clicked.connect(self.opCerraduraP) 
        self.vista.botonCerraduraK.clicked.connect(self.opCerraduraK)
        self.vista.botonReflex.clicked.connect(self.opReflexion)
        self.vista.botonGuardar.clicked.connect(self.opGuardar)  
         
    def manejarArchivos(self):
        rutas = self.vista.obtenerRutasArchivos() 
        if rutas: 
            self.modelo.clear()
            try:
                for ruta in rutas:
                    with open(ruta, 'r', encoding='utf-8') as f:
                        contenido = f.read()
                        for char in "[]',\"":
                            contenido = contenido.replace(char, " ")
                        
                        partes = contenido.split()
                        lenguaje_limpio = set()
                        
                        for p in partes:
                            if ":" not in p and not p.isdigit() and p.lower() != "res":
                                lenguaje_limpio.add(p)
                                
                        self.modelo.append(lenguaje_limpio)
                
                self.vista.mostrarMensajeExito("Archivos cargados correctamente.")
                self.mostrarListaInicial()
            except Exception as e:
                self.vista.mostrarMensajeError(f"Error al cargar: {str(e)}")

    def opUnion(self):
        if not self.verificarCarga(): return
        indices = self.vista.seleccionarIndices(binaria=True)
        if indices:
            res = OperacionesLenguajes.unir(self.modelo[indices[0]], self.modelo[indices[1]])
            self.mostrarResultado("UNIÓN", res, f"L{indices[0]+1} ∪ L{indices[1]+1}")

    def opConcatenacion(self):
        if not self.verificarCarga(): return
        indices = self.vista.seleccionarIndices(binaria=True)
        if indices:
            res = OperacionesLenguajes.concatenar(self.modelo[indices[0]], self.modelo[indices[1]])
            self.mostrarResultado("CONCATENACIÓN", res, f"L{indices[0]+1}L{indices[1]+1}")

    def opPotencia(self):
        if not self.verificarCarga(): return
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            n, ok = QInputDialog.getInt(self.vista, "Potencia", "Introduce n (-5 a 8):", 0, -5, 8, 1)
            if ok:
                res = OperacionesLenguajes.potencia(self.modelo[idx], n)
                self.mostrarResultado(f"POTENCIA (n={n})", res, f"L{idx+1}^{n}")

    def opCerraduraP(self): 
        if not self.verificarCarga(): return
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            res = OperacionesLenguajes.cerraduraPositiva(self.modelo[idx])
            self.mostrarResultado("CERRADURA POSITIVA", res, f"L{idx+1}+")

    def opCerraduraK(self):
        if not self.verificarCarga(): return
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            res = OperacionesLenguajes.cerraduraKleene(self.modelo[idx])
            self.mostrarResultado("CERRADURA DE KLEENE", res, f"L{idx+1}*")

    def opReflexion(self):
        if not self.verificarCarga(): return
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            res = OperacionesLenguajes.potencia(self.modelo[idx], -1)
            self.mostrarResultado("REFLEXIÓN", res, f"L{idx+1}^R")

    # FUNCIONES AUXILIARES
    def verificarCarga(self):
        if len(self.modelo) < 3:
            self.vista.mostrarMensajeError("Primero carga los 3 archivos.")
            return False
        return True

    def mostrarListaInicial(self):
        self.vista.resultadoListaWidget.clear()
        self.vista.resultadoListaWidget.addItem("--- LENGUAJES CARGADOS ---")
        self.vista.resultadoListaWidget.addItem("")
        for i, lang in enumerate(self.modelo):
            lista_ordenada = sorted(list(lang))
            formato_linea = f"L{i+1}: {lista_ordenada}"
            self.vista.resultadoListaWidget.addItem(formato_linea)


    def mostrarResultado(self, nombre, conjunto, operacion):
        self.vista.resultadoListaWidget.clear()
        self.vista.resultadoListaWidget.addItem(f"--- RESULTADO {nombre} ({operacion}) ---")
        self.vista.resultadoListaWidget.addItem(f"Cardinalidad: {len(conjunto)}")
        self.vista.resultadoListaWidget.addItem("")
        palabras = [w if w != "" else "λ" for w in sorted(list(conjunto))] 
        texto_para_mostrar = ", ".join(palabras) 
        self.vista.resultadoListaWidget.addItem(texto_para_mostrar) 

    def opGuardar(self):
        if self.vista.resultadoListaWidget.count() < 3:
            self.vista.mostrarMensajeError("No hay resultado para guardar.")
            return

        lineas_resultado = []
        for i in range(self.vista.resultadoListaWidget.count()):
            texto = self.vista.resultadoListaWidget.item(i).text()
            if "---" not in texto and "Cardinalidad" not in texto and texto.strip() != "":
                lineas_resultado.append(texto)

        if not lineas_resultado:
            self.vista.mostrarMensajeError("El resultado está vacío.")
            return
        texto_sucio = " ".join(lineas_resultado)
    
        for char in "[],λ":
            texto_sucio = texto_sucio.replace(char, "")
    
        palabras = [p.strip() for p in texto_sucio.replace(",", " ").split() if p.strip()]

        ruta = self.vista.obtenerRutaGuardar()
        if ruta:
            try:
                exito = OperacionesLenguajes.guardarArchivo(ruta, palabras)
                if exito:
                    self.vista.mostrarMensajeExito("Archivo guardado correctamente.")
                else:
                    raise Exception("Error al escribir el archivo.")
            except Exception as e:
                self.vista.mostrarMensajeError(f"Error al guardar: {e}")