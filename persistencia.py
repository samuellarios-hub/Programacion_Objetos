"""
Manejo de persistencia del ranking en JSON.
"""

import json
import os

ARCHIVO_TOP: str = "top_jugadores.json"
MAX_TOP: int = 5


def cargar_top() -> list[dict]:
    """Carga el ranking desde el archivo JSON."""
    if os.path.exists(ARCHIVO_TOP):
        try:
            with open(ARCHIVO_TOP, "r", encoding="utf-8") as archivo:
                return json.load(archivo)
        except (json.JSONDecodeError, IOError):
            return []
    return []


def guardar_top(top: list[dict]) -> None:
    """Guarda el ranking en el archivo JSON."""
    try:
        with open(ARCHIVO_TOP, "w", encoding="utf-8") as archivo:
            json.dump(top, archivo, ensure_ascii=False, indent=2)
    except IOError as e:
        print("❌ Error al guardar el TOP: " + str(e))


def actualizar_top(barco) -> None:
    """Actualiza el ranking con el barco actual."""
    top: list[dict] = cargar_top()

    nueva_entrada: dict = {
        "barco": barco.nombre,
        "tripulacion": barco.obtener_nombres_tripulacion(),
        "puntos": barco.puntos
    }

    encontrado: bool = False
    for i in range(len(top)):
        registro = top[i]
        if registro["barco"] == barco.nombre:
            if barco.puntos > registro["puntos"]:
                top[i] = nueva_entrada
            encontrado = True
            break

    if not encontrado:
        top.append(nueva_entrada)

    # Ordena por puntos descendente
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

    # Mantiene top 5
    while len(top) > MAX_TOP:
        top.pop()

    guardar_top(top)