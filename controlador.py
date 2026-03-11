#Importaciones IMPORTANTES
import sys
from PyQt6.QtWidgets import QInputDialog, QMessageBox
from modelo import OperacionesLenguajes


class ControlLenguaje:
    #Constructor que recibe las referencias del modelo de datos y la ventana principal
    def __init__(self, modelo, vista):
        self.modelo = modelo 
        self.vista = vista

        #CONEXIONES 
        #Vincula el evento 'clicked' de cada botón en la UI con su método correspondiente en esta clase
        self.vista.botonSubir.clicked.connect(self.manejarArchivos)
        self.vista.botonOriginales.clicked.connect(self.mostrarOriginales) 
        self.vista.botonUnion.clicked.connect(self.opUnion)
        self.vista.botonConcatenacion.clicked.connect(self.opConcatenacion)
        self.vista.botonPotencia.clicked.connect(self.opPotencia)
        self.vista.botonCerraduraP.clicked.connect(self.opCerraduraP) 
        self.vista.botonCerraduraK.clicked.connect(self.opCerraduraK)
        self.vista.botonReflex.clicked.connect(self.opReflexion)
        self.vista.botonGuardar.clicked.connect(self.opGuardar)  
         

    #Lee los archivos de texto, limpia los caracteres innecesarios y guarda los lenguajes en el modelo
    def manejarArchivos(self):
        #Llama a la vista para abrir el explorador y obtener una lista de rutas de archivos
        rutas = self.vista.obtenerRutasArchivos() 
        #Si el usuario seleccionó al menos un archivo
        if rutas: 
            #Vacia la lista actual del modelo para no mezclar datos viejos
            self.modelo.clear()
            #Bloque try-except para evitar cierres inesperados por archivos corruptos o ilegibles
            try:
                #Itera sobre cada ruta obtenida
                for ruta in rutas:
                    #Abre el archivo en modo lectura ('r') con codificación UTF-8
                    with open(ruta, 'r', encoding='utf-8') as f:
                        #Lee todo el contenido del txt como un solo string
                        contenido = f.read()
                        #Recorre una cadena con caracteres especiales que ensucian los datos
                        for char in "[]',\"":
                            #replace sustituye cada caracter especial encontrado por un espacio en blanco
                            contenido = contenido.replace(char, " ")
                        
                        #split separa todo el texto en una lista de palabras usando los espacios
                        partes = contenido.split()
                        #Se usa un set (conjunto) para que las palabras se guarden sin duplicados
                        lenguaje_limpio = set()
                        
                        #Recorre cada palabra extraída
                        for p in partes:
                            #Filtra: ignora etiquetas (con ':'), números (isdigit) o la palabra 'res'
                            if ":" not in p and not p.isdigit() and p.lower() != "res":
                                #add mete la palabra válida al conjunto
                                lenguaje_limpio.add(p)
                                
                        #Agrega este nuevo conjunto (lenguaje) a la lista principal del modelo
                        self.modelo.append(lenguaje_limpio)
                
                #Notifica al usuario mediante un pop-up de éxito
                self.vista.mostrarMensajeExito("Archivos cargados correctamente.")
                #Actualiza la pantalla para ver los datos recién cargados
                self.mostrarListaInicial()
            except Exception as e:
                #Si falla la lectura, muestra el error exacto convirtiendo la excepción a string
                self.vista.mostrarMensajeError(f"Error al cargar: {str(e)}")


    #Vuelve a mostrar los lenguajes originales cargados sin operaciones aplicadas
    def mostrarOriginales(self):
        #Solo ejecuta si verificarCarga() devuelve True
        if self.verificarCarga():
            self.mostrarListaInicial()


    #Ejecuta la operación de unión entre dos lenguajes
    def opUnion(self):
        if not self.verificarCarga(): return
        #Pide a la vista que el usuario elija dos lenguajes (binaria=True)
        indices = self.vista.seleccionarIndices(binaria=True)
        #Si el usuario completó la selección
        if indices:
            #Llama al método estático unir pasándole los dos conjuntos seleccionados del modelo
            res = OperacionesLenguajes.unir(self.modelo[indices[0]], self.modelo[indices[1]])
            #Manda a imprimir el resultado a la UI con formato matemático
            self.mostrarResultado("UNIÓN", res, f"L{indices[0]+1} ∪ L{indices[1]+1}")


    #Ejecuta la operación de concatenación entre dos lenguajes
    def opConcatenacion(self):
        if not self.verificarCarga(): return
        indices = self.vista.seleccionarIndices(binaria=True)
        if indices:
            res = OperacionesLenguajes.concatenar(self.modelo[indices[0]], self.modelo[indices[1]])
            self.mostrarResultado("CONCATENACIÓN", res, f"L{indices[0]+1}L{indices[1]+1}")


    #Ejecuta la operación de potencia sobre un solo lenguaje
    def opPotencia(self):
        if not self.verificarCarga(): return
        #binaria=False indica que solo se seleccionará un índice (un lenguaje)
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            #Abre un cuadro de diálogo nativo de PyQt (QInputDialog) para pedir un número entero (n)
            #Parámetros: widget padre, título, mensaje, valor inicial (0), mínimo (-10), máximo (10), paso (1)
            n, ok = QInputDialog.getInt(self.vista, "Potencia", "Introduce n (-10 a 10):", 0, -10, 10, 1)
            #Si el usuario presionó Aceptar ('ok' es True)
            if ok:
                # Al darle OK, el programa se quedará "pensando" unos segundos/minutos sin crashear.
                res = OperacionesLenguajes.potencia(self.modelo[idx], n)
                self.mostrarResultado(f"POTENCIA (n={n})", res, f"L{idx+1}^{n}")


    #Ejecuta la cerradura positiva (L+)
    def opCerraduraP(self): 
        if not self.verificarCarga(): return
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            res = OperacionesLenguajes.cerraduraPositiva(self.modelo[idx])
            self.mostrarResultado("CERRADURA POSITIVA", res, f"L{idx+1}+")


    #Ejecuta la cerradura de Kleene (L*)
    def opCerraduraK(self):
        if not self.verificarCarga(): return
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            res = OperacionesLenguajes.cerraduraKleene(self.modelo[idx])
            self.mostrarResultado("CERRADURA DE KLEENE", res, f"L{idx+1}*")

    #Ejecuta la reflexión (equivalente a potencia -1)
    def opReflexion(self):
        if not self.verificarCarga(): return
        idx = self.vista.seleccionarIndices(binaria=False)
        if idx is not None:
            res = OperacionesLenguajes.potencia(self.modelo[idx], -1)
            self.mostrarResultado("REFLEXIÓN", res, f"L{idx+1}^R")


    # FUNCIONES AUXILIARES
    
    #Valida que existan al menos 3 lenguajes en memoria antes de permitir operaciones
    def verificarCarga(self):
        #len cuenta cuántos elementos tiene la lista del modelo
        if len(self.modelo) < 3:
            self.vista.mostrarMensajeError("Primero carga los 3 archivos.")
            return False
        return True


    #Limpia el cuadro de lista en la UI y escribe los lenguajes base
    def mostrarListaInicial(self):
        #clear borra todos los items previos en el widget de lista (QListWidget)
        self.vista.resultadoListaWidget.clear()
        #addItem añade una nueva fila de texto a la lista visual
        self.vista.resultadoListaWidget.addItem("--- LENGUAJES CARGADOS ---")
        self.vista.resultadoListaWidget.addItem("")
        #enumerate devuelve tanto el índice (i) como el valor (lang) en cada iteración
        for i, lang in enumerate(self.modelo):
            #Convierte el set a lista y lo ordena alfabéticamente para mejor lectura
            lista_ordenada = sorted(list(lang))
            #Formatea el string sumando 1 al índice para que se vea L1, L2, etc. en lugar de L0
            formato_linea = f"L{i+1}: {lista_ordenada}"
            self.vista.resultadoListaWidget.addItem(formato_linea)


    #Imprime un resultado procesado en la lista visual de la interfaz
    def mostrarResultado(self, nombre, conjunto, operacion):
        self.vista.resultadoListaWidget.clear()
        self.vista.resultadoListaWidget.addItem(f"--- RESULTADO {nombre} ({operacion}) ---")
        self.vista.resultadoListaWidget.addItem(f"Cardinalidad: {len(conjunto)}")
        self.vista.resultadoListaWidget.addItem("")
        
        #Comprensión de lista con operador ternario: si la cadena está vacía "", imprime "λ" (épsilon/lambda), si no, deja la palabra normal
        palabras = [w if w != "" else "λ" for w in sorted(list(conjunto))] 
        
        # TRUNCADO INTELIGENTE
        #Límite máximo de palabras a mostrar en pantalla para evitar trabar la UI gráfica
        LIMITE = 1000  
        
        #Si el resultado supera el límite
        if len(palabras) > LIMITE:
            #Abre un QMessageBox (cuadro de diálogo de PyQt) con botones Yes/No preguntando si se quiere exportar
            respuesta = QMessageBox.question(
                self.vista,
                "Demasiado texto",
                f"El resultado tiene {len(palabras)} combinaciones.\n\n¿Deseas guardar el resultado completo en un archivo .txt y ver solo una muestra aquí?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
            )
            
            #Si el usuario hizo clic en 'Yes'
            if respuesta == QMessageBox.StandardButton.Yes:
                #Pide ruta de guardado
                ruta = self.vista.obtenerRutaGuardar()
                if ruta:
                    OperacionesLenguajes.guardarArchivo(ruta, palabras)
                    self.vista.mostrarMensajeExito("Archivo guardado con todas las combinaciones.")
            
            #Informa que la vista estará recortada
            self.vista.resultadoListaWidget.addItem(f"AVISO: Mostrando solo una muestra de {LIMITE} palabras...")
            #Usa slicing ([:LIMITE]) para cortar la lista y agarrar solo los primeros 1000 elementos
            palabras_para_mostrar = palabras[:LIMITE]
        else:
            #Si no supera el límite, se muestra completo
            palabras_para_mostrar = palabras

        #join une la lista de palabras en un solo string, separadas por coma y espacio
        texto_para_mostrar = ", ".join(palabras_para_mostrar) 
        self.vista.resultadoListaWidget.addItem(texto_para_mostrar) 


    #Extrae el contenido actual de la lista visual en la interfaz y lo guarda en un TXT
    def opGuardar(self):
        #count devuelve la cantidad de renglones; si es menor a 3, asume que no hay datos reales (solo cabeceras o vacío)
        if self.vista.resultadoListaWidget.count() < 3:
            self.vista.mostrarMensajeError("No hay resultado para guardar.")
            return

        #Lista temporal para guardar solo las líneas que nos importan
        lineas_resultado = []
        #Recorre cada renglón del ListWidget
        for i in range(self.vista.resultadoListaWidget.count()):
            #Obtiene el string de esa fila exacta
            texto = self.vista.resultadoListaWidget.item(i).text()
            #Ignora líneas decorativas (---), la de cardinalidad, los avisos, o renglones vacíos (strip remueve espacios en blanco)
            if "---" not in texto and "Cardinalidad" not in texto and "AVISO:" not in texto and texto.strip() != "":
                lineas_resultado.append(texto)

        #Si tras filtrar no quedó nada, lanza error
        if not lineas_resultado:
            self.vista.mostrarMensajeError("El resultado está vacío.")
            return
            
        #Une todas las líneas rescatadas en un solo bloque de texto
        texto_sucio = " ".join(lineas_resultado)
        #Recorre y elimina caracteres de lista y el símbolo lambda antes de exportar
        for char in "[],λ":
            texto_sucio = texto_sucio.replace(char, "")
    
        #1. Cambia comas por espacios, 2. Hace split por espacios, 3. strip limpia cada palabra, 4. Ignora elementos vacíos
        palabras = [p.strip() for p in texto_sucio.replace(",", " ").split() if p.strip()]

        #Abre diálogo de guardado
        ruta = self.vista.obtenerRutaGuardar()
        if ruta:
            try:
                #Llama al método del modelo para generar el archivo físico
                exito = OperacionesLenguajes.guardarArchivo(ruta, palabras)
                if exito:
                    self.vista.mostrarMensajeExito("Archivo guardado correctamente.")
                else:
                    #Lanza error forzado para caer en el except si exito fue False
                    raise Exception("Error al escribir el archivo.")
            except Exception as e:
                self.vista.mostrarMensajeError(f"Error al guardar: {e}")