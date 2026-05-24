"""
JUEGO DE AVENTURA PIRATA - FASE 3 POO AVANZADA
Samuel Alejandro Larios Ramos
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import random
import time
import json
import os

# Constantes globales del juego
ARCHIVO_TOP: str = "top_jugadores.json"
MAX_TOP: int = 5
PUNTOS_VICTORIA: int = 50
PUNTOS_DERROTA: int = -30
PUNTOS_POR_ENEMIGO: int = 15
PUNTOS_POR_MUERTE_ALIADO: int = -10


class Tripulante(ABC):
    """Clase abstracta que define el contrato para todos los tripulantes."""

    _contador: int = 0

    def __init__(self, nombre: str, vida_base: int, fuerza: int,
                 defensa: int, rango: str) -> None:
        Tripulante._contador += 1
        self.nombre: str = nombre
        # La vida tiene variación para hacer el juego más dinámico
        self.vida: int = random.randint(vida_base - 10, vida_base + 10)
        self.fuerza: int = fuerza
        self.defensa: int = defensa
        self.__rango: str = rango
        self.esta_vivo: bool = True

    @property
    def rango(self) -> str:
        return self.__rango

    @abstractmethod
    def atacar(self, objetivo: Tripulante) -> bool:
        pass

    @abstractmethod
    def realizar_accion_especial(self) -> None:
        pass

    def _calcular_ataque(self, objetivo: Tripulante) -> bool:
        # Calcula el daño: fuerza base menos la defensa del oponente
        dano_base: int = random.randint(self.fuerza - 5, self.fuerza)
        bloqueo: int = objetivo.defenderse()
        dano_final: int = max(2, dano_base - bloqueo)
        return objetivo.recibir_danio(dano_final)

    def defenderse(self) -> int:
        # La defensa reduce parte del daño entrante de forma aleatoria
        mitigacion: int = random.randint(self.defensa // 4, self.defensa // 2)
        return mitigacion

    def recibir_danio(self, cantidad: int) -> bool:
        # Reduce vida. Si llega a 0, el tripulante muere
        self.vida -= cantidad
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False
            return True
        else:
            return False

    def presentarse(self) -> None:
        estado: str = Tripulante.clasificar_vida(self.vida)
        print("  • " + self.nombre + " [" + self.rango + "] — Vida: " + str(self.vida) + " (" + estado + ")")

    @classmethod
    def total_tripulantes(cls) -> int:
        return cls._contador

    @classmethod
    def crear_enemigo_aleatorio(cls, nombre: str) -> Tripulante:
        # Constructor de fábrica: genera un enemigo aleatorio de los 3 tipos disponibles
        tipo: int = random.randint(1, 3)
        if tipo == 1:
            return Capitan(nombre, "Barco Corsario")
        elif tipo == 2:
            return Marinero(nombre)
        else:
            return PirataRaso(nombre)

    @staticmethod
    def clasificar_vida(vida: int) -> str:
        # Método estático para clasificar el nivel de vida de cualquier tripulante
        if vida > 20:
            return "Excelente"
        elif vida > 10:
            return "Moderado"
        else:
            return "Crítico"

    def __str__(self) -> str:
        return self.nombre + " [" + self.rango + "] — Vida: " + str(self.vida)

    def __repr__(self) -> str:
        return (type(self).__name__ + "(nombre=" + repr(self.nombre) +
                ", vida=" + str(self.vida) + ", rango=" + repr(self.rango) + ")")

# Subclases concretas de Tripulante

class Capitan(Tripulante):
    """Tripulante líder con mayor fuerza."""

    def __init__(self, nombre: str, nombre_del_barco: str) -> None:
        super().__init__(nombre, 20, 12, 3, "Capitán")
        self.barco_que_manda: str = nombre_del_barco

    def atacar(self, objetivo: Tripulante) -> bool:
        print("\n  ⚔️  El Capitán " + self.nombre + " ataca ferozmente con su ESPADA.")
        return self._calcular_ataque(objetivo)

    def realizar_accion_especial(self) -> None:
        print("  " + self.nombre + " grita: ¡Nadie descansa hasta que el tesoro sea nuestro!")
        print("  " + self.nombre + " revisa el mapa de " + self.barco_que_manda + ".")

    def __str__(self) -> str:
        return self.nombre + " [Capitán de " + self.barco_que_manda + "] — Vida: " + str(self.vida)

    def __repr__(self) -> str:
        return ("Capitan(nombre=" + repr(self.nombre) +
                ", barco=" + repr(self.barco_que_manda) + ", vida=" + str(self.vida) + ")")


class Marinero(Tripulante):
    """Tripulante equilibrado que usa cañones."""

    def __init__(self, nombre: str) -> None:
        super().__init__(nombre, 15, 8, 4, "Marinero")

    def atacar(self, objetivo: Tripulante) -> bool:
        print("\n  💣 El Marinero " + self.nombre + " dispara un CAÑONAZO.")
        return self._calcular_ataque(objetivo)

    def realizar_accion_especial(self) -> None:
        print("  " + self.nombre + " trapea la cubierta y canta: ¡La vida pirata es la mejor!")

    def __str__(self) -> str:
        return self.nombre + " [Marinero] — Vida: " + str(self.vida)

    def __repr__(self) -> str:
        return "Marinero(nombre=" + repr(self.nombre) + ", vida=" + str(self.vida) + ")"


class PirataRaso(Tripulante):
    """Tripulante con alta defensa que usa pistola."""

    def __init__(self, nombre: str) -> None:
        super().__init__(nombre, 18, 9, 5, "Pirata")

    def atacar(self, objetivo: Tripulante) -> bool:
        print("\n  🔫 El Pirata " + self.nombre + " apunta y dispara su PISTOLA.")
        return self._calcular_ataque(objetivo)

    def realizar_accion_especial(self) -> None:
        print("  " + self.nombre + " saca filo a su daga y busca monedas en el suelo.")

    def __str__(self) -> str:
        return self.nombre + " [Pirata] — Vida: " + str(self.vida)

    def __repr__(self) -> str:
        return "PirataRaso(nombre=" + repr(self.nombre) + ", vida=" + str(self.vida) + ")"

# Clase de Composición: Barco

class Barco:
    """Barco que contiene una tripulación de Tripulantes."""

    def __init__(self, nombre: str, tripulacion: list[Tripulante]) -> None:
        self.nombre: str = nombre
        self.tripulacion: list[Tripulante] = tripulacion
        self.puntos: int = 0

    def tripulantes_vivos(self) -> list[Tripulante]:
        # Filtra solo los tripulantes que siguen con vida
        vivos: list[Tripulante] = []
        for tripulante in self.tripulacion:
            if tripulante.esta_vivo:
                vivos.append(tripulante)
        return vivos

    def agregar_puntos(self, cantidad: int) -> None:
        self.puntos += cantidad

    def obtener_nombres_tripulacion(self) -> list[str]:
        # Extrae el nombre de cada tripulante para el ranking
        nombres: list[str] = []
        for tripulante in self.tripulacion:
            nombres.append(tripulante.nombre)
        return nombres

    def mostrar_tripulacion(self) -> None:
        print("\n  ⛵ " + str(self))
        print("  Tripulación:")
        for tripulante in self.tripulacion:
            if tripulante.esta_vivo:
                tripulante.presentarse()
            else:
                print("  • " + tripulante.nombre + " [" + tripulante.rango + "] — ☠️  Caído")

    def __str__(self) -> str:
        return "Barco '" + self.nombre + "' — Puntos: " + str(self.puntos)

    def __repr__(self) -> str:
        return "Barco(nombre=" + repr(self.nombre) + ", puntos=" + str(self.puntos) + ")"
