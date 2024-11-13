# cifradorMensajes/modelo/errores.py

class ContieneNoAscii(Exception):
    pass

class ContieneNumero(Exception):
    pass

class SinLetras(Exception):
    pass

class NoTrim(Exception):
    pass

class DobleEspacio(Exception):
    pass
