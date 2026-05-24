"""
Lógica del juego de batalla.
"""

import random
import time
from modelos import Tripulante, Barco

# Constantes de puntuación
PUNTOS_VICTORIA: int = 50
PUNTOS_DERROTA: int = -30
PUNTOS_POR_ENEMIGO: int = 15
PUNTOS_POR_MUERTE_ALIADO: int = -10



def pedir_numero(mensaje: str, minimo: int, maximo: int) -> int:
    """
    Solicita un número al usuario dentro de un rango específico.
    Valida la entrada y reintenta si es necesario.
    """
    numero_valido: bool = False
    valor: int = 0
    while not numero_valido:
        try:
            entrada: str = input(mensaje)
            valor = int(entrada)
            if valor >= minimo and valor <= maximo:
                numero_valido = True
            else:
                print("  ❌ Elige un número entre " + str(minimo) + " y " + str(maximo) + ".")
        except ValueError:
            print("  ❌ Ingresa un número válido.")
    return valor
