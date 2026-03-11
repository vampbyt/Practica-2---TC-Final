#OPERACIONES CON LENGUAJES
class OperacionesLenguajes:

    #Une dos lenguajes formales (conjuntos de cadenas)
    @staticmethod
    def unir(L_a, L_b):
        #El operador | realiza la unión de dos conjuntos (sets) en Python evitando duplicados
        return L_a | L_b


    #Concatena cada cadena del primer lenguaje con cada cadena del segundo lenguaje
    @staticmethod
    def concatenar(L_a, L_b):
        #Usa comprensión de conjuntos para generar todas las combinaciones posibles sin duplicados
        return {w1 + w2 for w1 in L_a for w2 in L_b}


    #Invierte (refleja) cada una de las cadenas dentro del lenguaje
    @staticmethod
    def reflexionar(L):
        #w[::-1] es la sintaxis de Python (slicing) para leer una cadena al revés
        return {w[::-1] for w in L}


    #Eleva un lenguaje a una potencia n
    #Si n es negativo, primero refleja el lenguaje y luego lo eleva a la potencia absoluta
    @staticmethod
    def potencia(L, n):
        #Cualquier lenguaje a la potencia 0 da como resultado la cadena vacía (épsilon)
        if n == 0: return {""}
        #Determina la base: si n es negativo, invierte las cadenas del lenguaje primero
        base = L if n > 0 else {w[::-1] for w in L} 
        #Obtiene el valor absoluto del exponente para saber cuántas veces concatenar
        exp = abs(n)
        #Inicializa el resultado con la cadena vacía para comenzar la concatenación
        res = {""}
        
        #Itera 'exp' veces para concatenar la base consigo misma
        for _ in range(exp):

            # Protección de memoria RAM (Evita colapsos extremos antes de la UI)
            #if len(res) * len(base) > 2000000: 
            #    raise MemoryError("La operación superaría los 2 millones de combinaciones y colapsaría la memoria de tu PC.")
            #res = {w1 + w2 for w1 in res for w2 in base}
            # Aquí quitamos el límite
            
            #Realiza la concatenación acumulativa entre el resultado actual y la base
            res = {w1 + w2 for w1 in res for w2 in base}
        return res
    

    #Genera la cerradura positiva (+) del lenguaje
    #Es la unión de las potencias del lenguaje desde 1 hasta el infinito (aquí limitado a 4 por practicidad)
    @staticmethod
    def cerraduraPositiva(L):
        #Inicializa un conjunto vacío
        res = set()
        #Calcula las potencias del 1 al 4 (simulando el infinito)
        for i in range(1, 5):
            #El operador |= actualiza el conjunto 'res' uniéndolo con el resultado de la nueva potencia
            res |= OperacionesLenguajes.potencia(L, i)
        return res


    #Genera la cerradura de Kleene (*) del lenguaje
    #Es igual a la cerradura positiva, pero incluye por defecto la potencia 0 (cadena vacía)
    @staticmethod
    def cerraduraKleene(L):
        #Inicializa el conjunto directamente con la cadena vacía (potencia 0)
        res = {""}
        #Itera para unir las potencias del 1 al 4
        for i in range(1, 5):
            #Acumula las uniones en el resultado
            res |= OperacionesLenguajes.potencia(L, i)
        return res
    
    
    #MANEJO DE ARCHIVOS
    #Guarda las palabras generadas del lenguaje en un archivo de texto
    @staticmethod
    def guardarArchivo(ruta, palabras):
        #Bloque try-except para capturar y manejar errores de permisos o escritura
        try:
            #Abre el archivo en modo escritura ('w') usando codificación UTF-8
            #with asegura que el archivo se cierre automáticamente al terminar o fallar
            with open(ruta, 'w', encoding='utf-8') as f:
                #Convierte el conjunto de palabras en una sola cadena separada por espacios y la escribe
                f.write(" ".join(palabras))
            #Si tiene éxito, devuelve True
            return True
        except Exception:
            #Si ocurre cualquier excepción, devuelve False indicando error
            return False