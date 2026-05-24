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
        print("  " + self.nombre + " bloquea parcialmente. Mitigación: " + str(mitigacion))
        return mitigacion

    def recibir_danio(self, cantidad: int) -> bool:
        # Reduce vida. Si llega a 0, el tripulante muere
        self.vida -= cantidad
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False
            print("  💀 " + self.nombre + " ha caído en combate.")
            return True
        else:
            print("  " + self.nombre + " resiste. Vida: " + str(self.vida))
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


# Funciones para persistencia en JSON

def cargar_top() -> list[dict]:
    # Intenta leer el archivo JSON. Si no existe o está dañado, retorna lista vacía
    if os.path.exists(ARCHIVO_TOP):
        try:
            with open(ARCHIVO_TOP, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            # Si hay error de lectura o formato JSON inválido, retorna lista vacía
            return []
    return []


def guardar_top(top: list[dict]) -> None:
    # Escribe el top en el archivo JSON de forma persistente
    try:
        with open(ARCHIVO_TOP, "w", encoding="utf-8") as archivo:
            json.dump(top, archivo, ensure_ascii=False, indent=2)
    except IOError as e:
        # Captura errores de escritura en el archivo
        print("  ❌ Error al guardar el TOP: " + str(e))


def actualizar_top(barco: Barco) -> None:
    # Carga el ranking actual desde el archivo
    top: list[dict] = cargar_top()

    # Crea una nueva entrada con los datos del barco actual
    nueva_entrada: dict = {
        "barco": barco.nombre,
        "tripulacion": barco.obtener_nombres_tripulacion(),
        "puntos": barco.puntos
    }

    # Busca si el barco ya existe en el ranking
    encontrado: bool = False
    for i in range(len(top)):
        registro = top[i]
        if registro["barco"] == barco.nombre:
            # Si existe y tiene más puntos, actualiza la entrada
            if barco.puntos > registro["puntos"]:
                top[i] = nueva_entrada
            encontrado = True
            break

    # Si el barco no existe, lo agrega a la lista
    if not encontrado:
        top.append(nueva_entrada)

    # Ordena la lista por puntos en orden descendente
    nueva_lista: list[dict] = []
    while len(top) > 0:
        mayor: dict = top[0]
        indice_mayor: int = 0
        for j in range(1, len(top)):
            if top[j]["puntos"] > mayor["puntos"]:
                mayor = top[j]
                indice_mayor = j
        nueva_lista.append(mayor)
        top.pop(indice_mayor)
    top = nueva_lista

    # Mantiene solo los TOP 5 mejores
    while len(top) > MAX_TOP:
        top.pop()

    guardar_top(top)


def mostrar_top() -> None:
    # Carga y muestra el ranking de los mejores barcos
    top: list[dict] = cargar_top()
    print("\n" + "=" * 50)
    print("       🏆  TOP " + str(MAX_TOP) + " — MEJORES BARCOS  🏆")
    print("=" * 50)
    if not top:
        print("  Aún no hay registros. ¡Sé el primero en el ranking!")
    else:
        posicion: int = 1
        for registro in top:
            tripulacion_str: str = ", ".join(registro["tripulacion"])
            print("  " + str(posicion) + ". " + registro["barco"] + " — " + str(registro["puntos"]) + " pts")
            print("      Tripulación: " + tripulacion_str)
            posicion = posicion + 1
    print("=" * 50)


# Función de batalla por turnos

def iniciar_batalla(barco: Barco) -> bool:
    # Crea dos enemigos aleatorios para enfrentar al jugador
    nombres_enemigos: list[str] = ["Barbanegra", "Cojo Bill"]
    lista_enemigos: list[Tripulante] = []
    for nombre in nombres_enemigos:
        enemigo: Tripulante = Tripulante.crear_enemigo_aleatorio(nombre)
        lista_enemigos.append(enemigo)

    print("\n  ¡¡BARCO PIRATA ENEMIGO A LA VISTA!!")
    print("  Enemigos que se acercan:")
    for enemigo in lista_enemigos:
        print("    • " + str(enemigo))

    print("\n  ⚔️  ¡COMIENZA EL COMBATE!")
    time.sleep(0.8)

    # Bucle principal del combate que continúa hasta que un bando sea derrotado
    batalla_activa: bool = True
    while batalla_activa:
        # Obtiene los tripulantes vivos de ambos lados
        vivos_propios: list[Tripulante] = barco.tripulantes_vivos()
        vivos_enemigos: list[Tripulante] = []
        for enemigo in lista_enemigos:
            if enemigo.esta_vivo:
                vivos_enemigos.append(enemigo)

        # Verifica condiciones de fin de batalla
        if len(vivos_enemigos) == 0:
            print("\n  🎉 ¡VICTORIA! Derrotaste a toda la tripulación enemiga.")
            return True
        if len(vivos_propios) == 0:
            print("\n  💀 ¡DERROTA! Tu tripulación fue hundida.")
            return False

        # Muestra el estado actual de ambos bandos
        print("\n" + "-" * 45)
        print("  TU TRIPULACIÓN:")
        for t in vivos_propios:
            print("    " + str(t))
        print("  ENEMIGOS:")
        for e in vivos_enemigos:
            print("    " + str(e))
        print("-" * 45)

        # Menú interactivo del jugador
        print("\n  ¿Qué ordenas?")
        print("  1. Continuar peleando")
        print("  2. Huir del combate")

        # Control de entrada con validación
        opcion_valida: bool = False
        opcion: int = 0
        while not opcion_valida:
            try:
                entrada: str = input("  Tu elección: ")
                opcion = int(entrada)
                if opcion == 1 or opcion == 2:
                    opcion_valida = True
                else:
                    print("  ❌ Elige 1 o 2.")
            except ValueError:
                print("  ❌ Ingresa un número válido.")

        # Si el jugador elige huir, termina la batalla
        if opcion == 2:
            print("  Escapaste del combate... sin gloria ni puntos.")
            return False

        # Inicia una ronda de combate con turnos aleatorios
        print("\n  ⚡ RONDA DE COMBATE ⚡")
        todos: list[Tripulante] = vivos_propios + vivos_enemigos
        random.shuffle(todos)

        # Cada participante ataca en orden aleatorio
        for atacante in todos:
            if not atacante.esta_vivo:
                continue

            # Recalcula los vivos actuales por si alguien murió en el turno anterior
            vivos_p: list[Tripulante] = barco.tripulantes_vivos()
            vivos_e: list[Tripulante] = []
            for e in lista_enemigos:
                if e.esta_vivo:
                    vivos_e.append(e)

            # Verifica si la batalla terminó durante la ronda
            if len(vivos_p) == 0 or len(vivos_e) == 0:
                break

            # Determina quién ataca a quién según el bando
            if atacante in barco.tripulacion:
                # El atacante es del barco del jugador
                objetivo: Tripulante = random.choice(vivos_e)
                murio_enemigo: bool = atacante.atacar(objetivo)
                if murio_enemigo:
                    barco.agregar_puntos(PUNTOS_POR_ENEMIGO)
            else:
                # El atacante es un enemigo
                objetivo = random.choice(vivos_p)
                murio_aliado: bool = atacante.atacar(objetivo)
                if murio_aliado:
                    barco.agregar_puntos(PUNTOS_POR_MUERTE_ALIADO)

        time.sleep(0.5)

    return False


# Función auxiliar para validar entrada de números

def pedir_numero(mensaje: str, minimo: int, maximo: int) -> int:
    # Solicita al usuario un número dentro de un rango específico
    # Valida la entrada y reintenta si es necesario
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


# Función principal del juego

def main() -> None:
    # Pantalla de bienvenida
    print("\n" + "=" * 50)
    print("    ☠️   JUEGO DE AVENTURA PIRATA   ☠️")
    print("    Samuel A. Larios")
    print("=" * 50)

    # Muestra el ranking actual
    mostrar_top()

    # Solicita al jugador los nombres del barco y tripulación
    print("\n⚓ Crea tu barco y tripulación:\n")

    nombre_barco: str = input("  Nombre de tu barco: ").strip()
    if nombre_barco == "":
        nombre_barco = "El Temido"

    nombre_capitan: str = input("  Nombre del Capitán: ").strip()
    if nombre_capitan == "":
        nombre_capitan = "Drake"

    nombre_marinero: str = input("  Nombre del Marinero: ").strip()
    if nombre_marinero == "":
        nombre_marinero = "Paco"

    nombre_pirata: str = input("  Nombre del Pirata Raso: ").strip()
    if nombre_pirata == "":
        nombre_pirata = "Rata"

    # Crea las instancias de los tripulantes
    capitan: Capitan = Capitan(nombre_capitan, nombre_barco)
    marinero: Marinero = Marinero(nombre_marinero)
    pirata: PirataRaso = PirataRaso(nombre_pirata)

    # Crea el barco con la tripulación (composición)
    tripulacion_inicial: list[Tripulante] = [capitan, marinero, pirata]
    barco: Barco = Barco(nombre_barco, tripulacion_inicial)

    print("\n  ¡Bienvenido, Capitán " + nombre_capitan + "!")
    print("  El barco '" + nombre_barco + "' está listo para zarpar.")
    barco.mostrar_tripulacion()

    # Bucle principal del juego
    jugando: bool = True
    while jugando:
        print("\n" + "=" * 45)
        print("  ⛵ " + str(barco))
        print("  ¿Qué deseas hacer?")
        print("  1. Ver tripulación")
        print("  2. Zarpar (buscar combate)")
        print("  3. Salir del juego")
        print("=" * 45)

        opcion: int = pedir_numero("  Tu elección: ", 1, 3)

        if opcion == 1:
            barco.mostrar_tripulacion()

        elif opcion == 2:
            # Verifica que haya tripulantes vivos para poder zarpar
            if len(barco.tripulantes_vivos()) == 0:
                print("\n  ❌ No tienes tripulantes vivos. No puedes zarpar.")
                continue

            print("\n  ⛵ Navegando hacia alta mar...")
            time.sleep(1)

            # Ejecuta la batalla
            resultado: bool = iniciar_batalla(barco)

            # Procesa el resultado de la batalla
            if resultado:
                barco.agregar_puntos(PUNTOS_VICTORIA)
                print("\n  ✅ ¡Victoria! +" + str(PUNTOS_VICTORIA) + " puntos de botín.")
            else:
                barco.agregar_puntos(PUNTOS_DERROTA)
                print("\n  ❌ Derrota. " + str(PUNTOS_DERROTA) + " puntos.")

            print("  Puntos acumulados: " + str(barco.puntos))
            actualizar_top(barco)

            # Si toda la tripulación muere, termina el juego
            if len(barco.tripulantes_vivos()) == 0:
                print("\n  ☠️  Toda tu tripulación ha caído.")
                print("  El juego termina aquí.")
                jugando = False

        elif opcion == 3:
            print("\n  ¡Hasta la próxima travesía, marinero!")
            jugando = False

    # Pantalla de fin del juego
    print("\n" + "=" * 50)
    actualizar_top(barco)
    print("  Resultado final del barco '" + barco.nombre + "': " + str(barco.puntos) + " puntos")
    print("  Tripulantes totales creados en sesión: " + str(Tripulante.total_tripulantes()))
    print("=" * 50)

    # Muestra el ranking final
    mostrar_top()

    print("\n  ¡Gracias por jugar! 🏴‍☠️\n")

if __name__ == "__main__":
    main()