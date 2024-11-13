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
        pass

    def encontrar_no_ascii_mensaje(self, mensaje: str):
        pass

class ReglaCifradoTraslacion(ReglaCifrado):
    def mensaje_valido(self, mensaje: str) -> bool:
        pass

class ReglaCifradoNumerico(ReglaCifrado):
    def mensaje_valido(self, mensaje: str) -> bool:
        pass