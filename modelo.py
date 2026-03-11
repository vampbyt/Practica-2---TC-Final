
class OperacionesLenguajes:
    @staticmethod
    def unir(L_a, L_b):
        return L_a | L_b

    @staticmethod
    def concatenar(L_a, L_b):
        return {w1 + w2 for w1 in L_a for w2 in L_b}

    @staticmethod
    def reflexionar(L):
        return {w[::-1] for w in L}

    @staticmethod
    def potencia(L, n):
        if n == 0: return {""}
        base = L if n > 0 else {w[::-1] for w in L} # Reflexión si n es negativo
        exp = abs(n)
        res = {""}
        for _ in range(exp):
            res = {w1 + w2 for w1 in res for w2 in base}
        return res
    
    @staticmethod
    def cerraduraPositiva(L):
        # L+ = L^1 U L^2 U L^3 U L^4
        res = set()
        for i in range(1, 5):
            res |= OperacionesLenguajes.potencia(L, i)
        return res

    @staticmethod
    def cerraduraKleene(L):
        # L* = L^0 U L^1 U L^2 U L^3 U L^4
        res = {""}
        for i in range(1, 5):
            res |= OperacionesLenguajes.potencia(L, i)
        return res
    
    @staticmethod
    def guardarArchivo(ruta, palabras):
        try:
            with open(ruta, 'w', encoding='utf-8') as f:
                f.write(" ".join(palabras))
            return True
        except Exception:
            return False
