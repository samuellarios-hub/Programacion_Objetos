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


def iniciar_batalla(barco: Barco) -> bool:
    """
    Inicia una batalla entre el barco del jugador y dos enemigos aleatorios.
    Retorna True si gana, False si pierde.
    """
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

    batalla_activa: bool = True
    while batalla_activa:
        vivos_propios: list[Tripulante] = barco.tripulantes_vivos()
        vivos_enemigos: list[Tripulante] = []
        
        for enemigo in lista_enemigos:
            if enemigo.esta_vivo:
                vivos_enemigos.append(enemigo)

        if len(vivos_enemigos) == 0:
            print("\n  🎉 ¡VICTORIA! Derrotaste a toda la tripulación enemiga.")
            return True
        
        if len(vivos_propios) == 0:
            print("\n  💀 ¡DERROTA! Tu tripulación fue hundida.")
            return False

        print("\n" + "-" * 45)
        print("  TU TRIPULACIÓN:")
        for t in vivos_propios:
            print("    " + str(t))
        print("  ENEMIGOS:")
        for e in vivos_enemigos:
            print("    " + str(e))
        print("-" * 45)

        print("\n  ¿Qué ordenas?")
        print("  1. Continuar peleando")
        print("  2. Huir del combate")

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

        if opcion == 2:
            print("  Escapaste del combate... sin gloria ni puntos.")
            return False

        print("\n  ⚡ RONDA DE COMBATE ⚡")
        todos: list[Tripulante] = vivos_propios + vivos_enemigos
        random.shuffle(todos)

        for atacante in todos:
            if not atacante.esta_vivo:
                continue

            vivos_p: list[Tripulante] = barco.tripulantes_vivos()
            vivos_e: list[Tripulante] = []
            for e in lista_enemigos:
                if e.esta_vivo:
                    vivos_e.append(e)

            if len(vivos_p) == 0 or len(vivos_e) == 0:
                break

            if atacante in barco.tripulacion:
                objetivo: Tripulante = random.choice(vivos_e)
                murio_enemigo: bool = atacante.atacar(objetivo)
                if murio_enemigo:
                    barco.agregar_puntos(PUNTOS_POR_ENEMIGO)
            else:
                objetivo = random.choice(vivos_p)
                murio_aliado: bool = atacante.atacar(objetivo)
                if murio_aliado:
                    barco.agregar_puntos(PUNTOS_POR_MUERTE_ALIADO)

        time.sleep(0.5)

    return False


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