"""
Interfaz gráfica con Tkinter para el juego pirata.

"""

import tkinter as tk
from tkinter import messagebox
from modelos import Capitan, Marinero, PirataRaso, Barco, Tripulante
from persistencia import cargar_top, actualizar_top
from juego import PUNTOS_VICTORIA, PUNTOS_DERROTA
import random


class VentanaPrincipal:
    """Ventana principal del juego."""
    
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("⚔️ Juego de Aventura Pirata")
        self.ventana.geometry("700x500")
        self.ventana.resizable(False, False)
        
        self.barco = None
        self.enemigos = None
        self.batalla_activa = False
        
        self.mostrar_menu_principal()
    
    def limpiar(self):
        """Limpia todos los widgets de la ventana."""
        for widget in self.ventana.winfo_children():
            widget.destroy()
    
    def mostrar_menu_principal(self):
        """Menú principal."""
        self.limpiar()
        
        tk.Label(self.ventana, text="🏴‍☠️ AVENTURA PIRATA", 
                font=("Arial", 28, "bold")).pack(pady=30)
        
        tk.Label(self.ventana, text="Controla tu barco y derrota enemigos", 
                font=("Arial", 12)).pack(pady=10)
        
        tk.Button(self.ventana, text="Jugar", command=self.ventana_crear_barco,
                 width=25, font=("Arial", 12), bg="#2ecc71", fg="white").pack(pady=15)
        
        tk.Button(self.ventana, text="Ver Ranking", command=self.mostrar_ranking,
                 width=25, font=("Arial", 12), bg="#3498db", fg="white").pack(pady=10)
        
        tk.Button(self.ventana, text="Salir", command=self.ventana.quit,
                 width=25, font=("Arial", 12), bg="#e74c3c", fg="white").pack(pady=10)
    
    def ventana_crear_barco(self):
        """Ventana para crear el barco."""
        self.limpiar()
        
        tk.Label(self.ventana, text="Crea tu Barco", 
                font=("Arial", 22, "bold")).pack(pady=20)
        
        frame = tk.Frame(self.ventana)
        frame.pack(pady=10)
        
        # Nombre barco
        tk.Label(frame, text="Nombre del barco:", font=("Arial", 11)).pack(anchor="w", pady=5)
        entrada_barco = tk.Entry(frame, width=35, font=("Arial", 10))
        entrada_barco.pack(pady=5)
        entrada_barco.insert(0, "El Temido")
        
        # Nombre capitán
        tk.Label(frame, text="Nombre del Capitán:", font=("Arial", 11)).pack(anchor="w", pady=5)
        entrada_capitan = tk.Entry(frame, width=35, font=("Arial", 10))
        entrada_capitan.pack(pady=5)
        entrada_capitan.insert(0, "Drake")
        
        # Nombre marinero
        tk.Label(frame, text="Nombre del Marinero:", font=("Arial", 11)).pack(anchor="w", pady=5)
        entrada_marinero = tk.Entry(frame, width=35, font=("Arial", 10))
        entrada_marinero.pack(pady=5)
        entrada_marinero.insert(0, "Paco")
        
        # Nombre pirata
        tk.Label(frame, text="Nombre del Pirata Raso:", font=("Arial", 11)).pack(anchor="w", pady=5)
        entrada_pirata = tk.Entry(frame, width=35, font=("Arial", 10))
        entrada_pirata.pack(pady=5)
        entrada_pirata.insert(0, "Rata")
        
        def confirmar():
            cap = Capitan(entrada_capitan.get(), entrada_barco.get())
            mar = Marinero(entrada_marinero.get())
            pir = PirataRaso(entrada_pirata.get())
            
            tripulacion = [cap, mar, pir]
            self.barco = Barco(entrada_barco.get(), tripulacion)
            
            self.mostrar_pantalla_principal()
        
        tk.Button(self.ventana, text="Comenzar", command=confirmar,
                 width=25, font=("Arial", 12), bg="#2ecc71", fg="white").pack(pady=20)
        
        tk.Button(self.ventana, text="Volver", command=self.mostrar_menu_principal,
                 width=25, font=("Arial", 10), bg="#95a5a6", fg="white").pack(pady=5)
    
    def mostrar_pantalla_principal(self):
        """Pantalla principal del juego."""
        self.limpiar()
        
        tk.Label(self.ventana, text=f"⛵ {self.barco.nombre}", 
                font=("Arial", 20, "bold")).pack(pady=10)
        
        tk.Label(self.ventana, text=f"Puntos: {self.barco.puntos}", 
                font=("Arial", 14, "bold"), fg="#f39c12").pack(pady=5)
        
        # Frame para tripulación
        frame_trip = tk.LabelFrame(self.ventana, text="Tripulación", 
                                   font=("Arial", 11, "bold"), padx=10, pady=10)
        frame_trip.pack(pady=15, padx=20, fill=tk.BOTH, expand=True)
        
        for tripulante in self.barco.tripulacion:
            if tripulante.esta_vivo:
                color = "#2ecc71"
                estado = f"✓ Vida: {tripulante.vida}"
            else:
                color = "#e74c3c"
                estado = "✗ CAÍDO"
            
            tk.Label(frame_trip, text=f"{tripulante.nombre} [{tripulante.rango}] {estado}",
                    font=("Arial", 10), fg=color).pack(anchor="w", pady=3)
        
        # Botones de acción
        frame_botones = tk.Frame(self.ventana)
        frame_botones.pack(pady=15)
        
        tk.Button(frame_botones, text="⚔️  Zarpar (Buscar combate)", 
                 command=self.iniciar_combate,
                 width=30, font=("Arial", 11), bg="#e74c3c", fg="white").pack(pady=5)
        
        tk.Button(frame_botones, text="Volver al menú", 
                 command=self.mostrar_menu_principal,
                 width=30, font=("Arial", 11), bg="#95a5a6", fg="white").pack(pady=5)
    
    def iniciar_combate(self):
        """Inicia el combate."""
        if len(self.barco.tripulantes_vivos()) == 0:
            messagebox.showerror("Error", "No tienes tripulantes vivos.")
            return
        
        # Crear enemigos
        nombres_enemigos = ["Barbanegra", "Cojo Bill"]
        self.enemigos = []
        for nombre in nombres_enemigos:
            enemigo = Tripulante.crear_enemigo_aleatorio(nombre)
            self.enemigos.append(enemigo)
        
        self.batalla_activa = True
        self.mostrar_pantalla_batalla()
    
    def mostrar_pantalla_batalla(self):
        """Muestra la pantalla de batalla."""
        self.limpiar()
        
        # Verificar si la batalla terminó
        vivos_propios = self.barco.tripulantes_vivos()
        vivos_enemigos = [e for e in self.enemigos if e.esta_vivo]
        
        if len(vivos_enemigos) == 0:
            # Victoria
            self.barco.agregar_puntos(PUNTOS_VICTORIA)
            actualizar_top(self.barco)
            messagebox.showinfo("Victoria", f"¡Ganaste! +{PUNTOS_VICTORIA} puntos\nTotal: {self.barco.puntos} puntos")
            
            if len(vivos_propios) == 0:
                messagebox.showinfo("Fin del juego", "Toda tu tripulación ha caído.")
                self.mostrar_menu_principal()
            else:
                self.mostrar_pantalla_principal()
            return
        
        if len(vivos_propios) == 0:
            # Derrota
            self.barco.agregar_puntos(PUNTOS_DERROTA)
            actualizar_top(self.barco)
            messagebox.showinfo("Derrota", f"¡Perdiste! {PUNTOS_DERROTA} puntos\nTotal: {self.barco.puntos} puntos")
            messagebox.showinfo("Fin del juego", "Toda tu tripulación ha caído.")
            self.mostrar_menu_principal()
            return
        
        tk.Label(self.ventana, text="⚔️ ¡COMBATE!", 
                font=("Arial", 20, "bold"), fg="#e74c3c").pack(pady=15)
        
        # Tu tripulación
        tk.Label(self.ventana, text="TU TRIPULACIÓN:", 
                font=("Arial", 12, "bold"), fg="#2ecc71").pack(anchor="w", padx=20, pady=5)
        
        for tripulante in vivos_propios:
            barra_vida = "█" * (tripulante.vida // 5) + "░" * (4 - tripulante.vida // 5)
            tk.Label(self.ventana, text=f"  {tripulante.nombre}: [{barra_vida}] {tripulante.vida}",
                    font=("Arial", 10)).pack(anchor="w", padx=40)
        
        # Enemigos
        tk.Label(self.ventana, text="ENEMIGOS:", 
                font=("Arial", 12, "bold"), fg="#e74c3c").pack(anchor="w", padx=20, pady=(10, 5))
        
        for enemigo in vivos_enemigos:
            barra_vida = "█" * (enemigo.vida // 5) + "░" * (4 - enemigo.vida // 5)
            tk.Label(self.ventana, text=f"  {enemigo.nombre}: [{barra_vida}] {enemigo.vida}",
                    font=("Arial", 10)).pack(anchor="w", padx=40)
        
        # Botones de combate
        frame_combate = tk.Frame(self.ventana)
        frame_combate.pack(pady=20)
        
        def ronda_combate():
            todos = vivos_propios + vivos_enemigos
            random.shuffle(todos)
            
            for atacante in todos:
                if not atacante.esta_vivo:
                    continue
                
                vivos_p = self.barco.tripulantes_vivos()
                vivos_e = [e for e in self.enemigos if e.esta_vivo]
                
                if len(vivos_p) == 0 or len(vivos_e) == 0:
                    break
                
                if atacante in self.barco.tripulacion:
                    objetivo = random.choice(vivos_e)
                    murio = atacante.atacar(objetivo)
                    if murio:
                        self.barco.agregar_puntos(15)
                else:
                    objetivo = random.choice(vivos_p)
                    murio = atacante.atacar(objetivo)
                    if murio:
                        self.barco.agregar_puntos(-10)
            
            self.mostrar_pantalla_batalla()
        
        tk.Button(frame_combate, text="Atacar", command=ronda_combate,
                 width=15, font=("Arial", 11), bg="#2ecc71", fg="white").pack(side=tk.LEFT, padx=10)
        
        tk.Button(frame_combate, text="Huir", command=self.huir_batalla,
                 width=15, font=("Arial", 11), bg="#e74c3c", fg="white").pack(side=tk.LEFT, padx=10)
    
    def huir_batalla(self):
        """Huir del combate."""
        messagebox.showinfo("Huida", "Escapaste del combate sin gloria.")
        self.mostrar_pantalla_principal()
    
    def mostrar_ranking(self):
        """Muestra el ranking."""
        self.limpiar()
        
        tk.Label(self.ventana, text="🏆 RANKING TOP 5", 
                font=("Arial", 22, "bold")).pack(pady=20)
        
        top = cargar_top()
        
        frame_top = tk.Frame(self.ventana)
        frame_top.pack(pady=10, fill=tk.BOTH, expand=True, padx=20)
        
        if not top:
            tk.Label(frame_top, text="Aún no hay registros.", 
                    font=("Arial", 12)).pack(pady=30)
        else:
            for i, registro in enumerate(top, 1):
                texto = f"{i}. {registro['barco']} - {registro['puntos']} pts"
                tripulacion = ", ".join(registro['tripulacion'])
                
                tk.Label(frame_top, text=texto, font=("Arial", 12, "bold")).pack(anchor="w", pady=5)
                tk.Label(frame_top, text=f"   {tripulacion}", font=("Arial", 10)).pack(anchor="w", pady=2)
        
        tk.Button(self.ventana, text="Volver", command=self.mostrar_menu_principal,
                 width=25, font=("Arial", 11), bg="#95a5a6", fg="white").pack(pady=20)
