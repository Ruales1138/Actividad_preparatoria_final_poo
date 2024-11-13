from abc import ABC, abstractmethod


class ReglaCifrado(ABC):
    def __init__(self, token: int):
        self.token: int = token

    @abstractmethod
    def encriptar(self, mensaje: str) -> str:
        ...

    @abstractmethod
    def desencriptar(self, mensaje: str) -> str:
        ...

    @abstractmethod
    def mensaje_valido(self, mensaje: str) -> bool:
        ...

    def encontrar_numeros_mensaje(self, mensaje: str):
        # numeros = []
        # for i in mensaje:
        #    numeros.append(i)
        return [0,1,2]


    def encontrar_no_ascii_mensaje(self, mensaje: str):
        return [3,2,1]


class ReglaCifradoTraslacion(ReglaCifrado):
    def mensaje_valido(self, mensaje: str) -> bool:
        return True

    def encriptar(self, mensaje: str) -> str:
        mensaje_min = mensaje.lower()
        alfabeto = "abcdefghijklmnopqrstuvwxyz"
        resultado = ''

        for letra in mensaje_min:
            if letra in alfabeto:
                nuevo_indice = (alfabeto.index(letra) + self.token) % len(alfabeto)
                resultado += alfabeto[nuevo_indice]
            else:
                resultado += letra

        return resultado


    def desencriptar(self, mensaje: str) -> str:
        return 'des1'


class ReglaCifradoNumerico(ReglaCifrado):
    def mensaje_valido(self, mensaje: str) -> bool:
        return False

    def encriptar(self, mensaje: str) -> str:
        return 'enc2'

    def desencriptar(self, mensaje: str) -> str:
        return 'des2'


class Cifrador:
    def __init__(self, agente: ReglaCifrado):
        self.agente: ReglaCifrado = agente

    def encriptar(self, mensaje: str) -> str:
        return self.agente.encriptar(mensaje)

    def desencriptar(self, mensaje: str) -> str:
        return self.agente.desencriptar(mensaje)

