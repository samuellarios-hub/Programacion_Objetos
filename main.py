"""
Juego de Aventura Pirata - Fase 3 POO
Punto de entrada de la aplicación.

Autores: Samuel Alejandro Larios Ramos
Karen Juliana Jaramillo Gutierrez
"""

import tkinter as tk
from gui import VentanaPrincipal


def main():
    """Inicia el juego."""
    ventana = tk.Tk()
    app = VentanaPrincipal(ventana)
    ventana.mainloop()


if __name__ == "__main__":
    main()
