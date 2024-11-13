from abc import ABC, abstractmethod

from cifradorMensajes.modelo.errores import ContieneNumero, ContieneNoAscii, ErrorContenido, SinLetras, NoTrim


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

    def encontrar_numeros_mensaje(self, mensaje: str) -> list[int]:
        numeros = []
        for i, caracter in enumerate(mensaje):
            if caracter.isdigit():
                numeros.append(i)
        return numeros

    def encontrar_no_ascii_mensaje(self, mensaje: str):
        no_ascii = []
        for i, caracter in enumerate(mensaje):
            if ord(caracter) > 127:
                no_ascii.append(i)
        return no_ascii


class ReglaCifradoTraslacion(ReglaCifrado):
    def mensaje_valido(self, mensaje: str) -> bool:
        if self.encontrar_numeros_mensaje(mensaje):
            raise ContieneNumero('ContieneNumero')
        if self.encontrar_no_ascii_mensaje(mensaje):
            raise ContieneNoAscii('ContieneNoAscii')
        if not any(caracter.isalpha() for caracter in mensaje):
            raise SinLetras('SinLetras')
        return True

    def encriptar(self, mensaje: str) -> str:
        if not self.mensaje_valido(mensaje):
            raise ValueError

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
        alfabeto = "abcdefghijklmnopqrstuvwxyz"
        resultado = ''

        for letra in mensaje:
            if letra in alfabeto:
                nuevo_indice = (alfabeto.index(letra) - self.token) % len(alfabeto)
                resultado += alfabeto[nuevo_indice]
            else:
                resultado += letra

        return resultado


class ReglaCifradoNumerico(ReglaCifrado):
    def mensaje_valido(self, mensaje: str) -> bool:
        if self.encontrar_numeros_mensaje(mensaje):
            raise ContieneNumero('ContieneNumero')
        if self.encontrar_no_ascii_mensaje(mensaje):
            raise ContieneNoAscii('ContieneNoAscii')
        if any(caracter.isalpha for caracter in mensaje):
            raise NoTrim('NoTrim')
        return True

    def encriptar(self, mensaje: str) -> str:
        if not self.mensaje_valido(mensaje):
            raise ValueError
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
