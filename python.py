# Juego de Aventura Pirata - Poo
# KAREN JULIANA JARAMILLO GUTIERREZ
# SAMUEL ALEJANDRO LARIOS RAMOS

import random
import time

class MascotaLoro:
    def __init__(self, color_plumaje="Verde"):
        self.__entrenado = True
        self.nombre = "Kiwi"
        self.frases = ["¡A navegar!", "Ron para el Capitán", "Tierra a la vista"]
        self.color = color_plumaje

    @property
    def entrenado(self):
        return self.__entrenado

    def morder_apoyo(self, objetivo):
        if self.__entrenado:
            print("\n Kiwi vuela y muerde a", objetivo.nombre, "(Daño extra: 5)")
            return objetivo.recibir_danio(5)
        return False

    def hablar(self):
        if self.__entrenado:
            frase_elegida = random.choice(self.frases)
            print("\n Kiwi chilla:", frase_elegida)
        else:
            print("\n Kiwi solo dice: ¡Croac! ¡Croac!")

    def realizar_truco(self):
        print("\n Kiwi da 3 vueltas en el aire y mueve sus alas", self.color)

class Tripulante:
    def __init__(self, nombre_persona, puntos_vida, fuerza, defensa, rango_social):
        self.nombre = nombre_persona
        self.vida = puntos_vida
        self.fuerza = fuerza
        self.defensa = defensa
        self.__rango = rango_social
        self.esta_vivo = True

    @property
    def rango(self):
        return self.__rango

    def atacar(self, objetivo):
        dano_base = random.randint(self.fuerza - 5, self.fuerza)
        bloqueo_enemigo = objetivo.defenderse()
        dano_final = dano_base - bloqueo_enemigo
        if dano_final < 2:
            dano_final = 2
        return objetivo.recibir_danio(dano_final)

    def defenderse(self):
        mitigacion = random.randint(self.defensa // 4, self.defensa // 2)
        print(self.nombre, "intenta bloquear. Mitigación:", mitigacion)
        return mitigacion

    def recibir_danio(self, cantidad):
        self.vida = self.vida - cantidad
        if self.vida <= 0:
            self.vida = 0
            self.esta_vivo = False
            print(self.nombre, "se ha muerto en combate .... se acaba la aventura para él.")
            return True
        else:
            print(self.nombre, "aguanta el golpe, le quedan " , self.vida, "puntos de vida.")
            return False

    def curar(self):
        self.vida = self.vida + 20
        print("\n", self.nombre, "recupera 20 de vida por su valor en combate.")

    def presentarse(self):
        print("Nombre:", self.nombre, "| Rango:", self.__rango, "| Vida:", self.vida)

    def realizar_accion_especial(self):
        print(self.nombre, "no hace nada especial.")

class Capitan(Tripulante):
    def __init__(self, nombre_persona, nombre_del_barco):
        super().__init__(nombre_persona, 150, 45, 10, "Capitán")
        self.barco_que_manda = nombre_del_barco
        # El capitán tiene un loro que lo acompaña
        self.mi_loro = MascotaLoro()

    def atacar(self, objetivo):
        print("\nEl Capitán", self.nombre, "ataca ferozmente con su ESPADA.")
        murio_en_combate = super().atacar(objetivo)
        if murio_en_combate == False:
            murio_en_combate = self.mi_loro.morder_apoyo(objetivo)
        return murio_en_combate

    def realizar_accion_especial(self):
        print(self.nombre, "grita: ¡Nadie descansa hasta que el tesoro sea nuestro!")
        print(self.nombre, "está revisando el mapa del tesoro de su barco", self.barco_que_manda)

class Marinero(Tripulante):
    def __init__(self, nombre_persona):
        super().__init__(nombre_persona, 100, 30, 15, "Marinero")

    def atacar(self, objetivo):
        print("\nEl Marinero", self.nombre, "dispara un gran CAÑONAZO.")
        return super().atacar(objetivo)
    
    def realizar_accion_especial(self):
        print(self.nombre, "está trapeando la cubierta con agua salada.")
        print(self.nombre, "canta: ¡La vida pirata es la vida mejor!")

class PirataRaso(Tripulante):
    def __init__(self, nombre_persona):
        super().__init__(nombre_persona, 120, 25, 20, "Pirata")

    def atacar(self, objetivo):
        print("\nEl Pirata", self.nombre, "apunta y dispara su PISTOLA.")
        return super().atacar(objetivo)

    def realizar_accion_especial(self):
        print(self.nombre, "está sacando filo a su vieja daga de hierro.")
        print(self.nombre, "mira con atención el suelo buscando monedas perdidas.")

def iniciar_batalla(lista_jugadores, lista_enemigos):
    print("\n¡COMIENZA EL COMBATE!")
    while True:
        vivos_mios = [aliado for aliado in lista_jugadores if aliado.esta_vivo]
        vivos_enemigos = [enemigo for enemigo in lista_enemigos if enemigo.esta_vivo]

        if not vivos_enemigos:
            print("\n¡VICTORIA! Has derrotado a toda la tripulación enemiga.")
            break
        if not vivos_mios:
            print("\nNos hundieron.... la tripulación fue capturada.")
            break

        print("\n--- TU TURNO ---")
        for i in range(len(vivos_mios)):
            print(i + 1, ".", vivos_mios[i].nombre, "(Vida:", vivos_mios[i].vida, ")")

        try:
            seleccion = int(input("\nSelecciona quién ataca (número): ")) - 1
            atacante = vivos_mios[seleccion]
        except (ValueError, IndexError):
            print("Número inválido. Elige un número de la lista.")
            continue

        objetivo_enemigo = random.choice(vivos_enemigos)
        if atacante.atacar(objetivo_enemigo):
            atacante.curar()

        if not any(e.esta_vivo for e in lista_enemigos):
            print("\n¡Ganaste la batalla!")
            break

        print("\nTurno del enemigo")
        vivos_enemigos_post = [e for e in lista_enemigos if e.esta_vivo]
        enemigo_que_ataca = random.choice(vivos_enemigos_post)
        if enemigo_que_ataca.atacar(atacante):
            enemigo_que_ataca.curar()

if __name__ == "__main__":
    nombre_barco = input("Nombre de tu barco: ")
    capitan_jugador = Capitan(input("Nombre del Capitán: "), nombre_barco)
    marinero_jugador = Marinero(input("Nombre del Marinero: "))
    pirata_jugador = PirataRaso(input("Nombre del Pirata: "))

    lista_tripulacion = [capitan_jugador, marinero_jugador, pirata_jugador]

    jugando = True
    while jugando:
        print("\nMenú: [presentar, revista, loro, zarpar, salir]")
        comando = input("> ").lower()

        if comando == "presentar":
            print("\n-- Tu Tripulación --")
            for alguien in lista_tripulacion:
                alguien.presentarse()

        elif comando == "revista":
            print("\n-- Revisando tripulación --")
            # Aquí usamos polimorfismo porque cada personaje
            # tiene una acción diferente
            for alguien in lista_tripulacion:
                alguien.realizar_accion_especial()
                print("")

        
        elif comando == "loro":
            while True:

                opcion_loro = input("\n¿Qué hace Kiwi? (hablar / volar / truco): ").lower()
                if opcion_loro == "hablar":
                    capitan_jugador.mi_loro.hablar()
                    break
                elif opcion_loro == "volar":
                    print("\nKiwi vuela alrededor del barco y vigila.")
                    break
                elif opcion_loro == "truco":
                    capitan_jugador.mi_loro.realizar_truco()
                    break
                else:
                    print("Opción no válida. Elige: hablar, volar , truco. ")

        elif comando == "zarpar":
            print("\nNavegando...")
            time.sleep(1)
            print("¡¡BARCO PIRATA A LA VISTA!!")
            while True:
                opcion_batalla = input("\n¿Deseas (pelear) o (huir)? ").lower() 
                if opcion_batalla == "pelear":
                    enemigos = [PirataRaso("Barbanegra"), Marinero("Cojo")]
                    iniciar_batalla(lista_tripulacion, enemigos)
                    break
                elif opcion_batalla == "huir" :
                    print("\nEscapaste con éxito.")
                    break
                else:
                    print("Opción no válida elige: (pelear o huir)")
    

        elif comando == "salir":
            print("\n¡Hasta la próxima travesía!")   
            jugando = False
        
        else:
            print("Comando no reconocido, Intenta de nuevo.")
