from abc import ABC, abstractmethod

from cifradorMensajes.modelo.errores import ContieneNumero, ContieneNoAscii, ErrorContenido, SinLetras, NoTrim, \
    DobleEspacio


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
        def encontrar_espacios(mens: str):
            if mens.startswith(' ') or mens.endswith(' '):
                return False
            return True

        def encontrar_doble_espacio(mens: str):
            palabras = mens.split(' ')
            for palabra in palabras:
                if palabra == '':
                    return False
            return True

        if self.encontrar_numeros_mensaje(mensaje):
            raise ContieneNumero('ContieneNumero')
        if self.encontrar_no_ascii_mensaje(mensaje):
            raise ContieneNoAscii('ContieneNoAscii')
        if not encontrar_espacios(mens=mensaje):
            raise NoTrim('NoTrim')
        if not encontrar_doble_espacio(mens=mensaje):
            raise DobleEspacio('DobleEspacio')
        return True

    def encriptar(self, mensaje: str) -> str:
        if not self.mensaje_valido(mensaje):
            raise ValueError

        mensaje_min = mensaje.lower()
        resultado = ''
        for caracter in mensaje:
            num = ord(caracter) * self.token
            resultado += f'{num} '

        return resultado.strip()

    def desencriptar(self, mensaje: str) -> str:
        numeros = mensaje.split(' ')
        resultado = ''
        for numero in numeros:
            numero_original = int(numero) / self.token
            resultado +=  chr(int(numero_original))
        return resultado




class Cifrador:
    def __init__(self, agente: ReglaCifrado):
        self.agente: ReglaCifrado = agente

    def encriptar(self, mensaje: str) -> str:
        return self.agente.encriptar(mensaje)

    def desencriptar(self, mensaje: str) -> str:
        return self.agente.desencriptar(mensaje)
