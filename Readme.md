# ☠️ Juego de Aventura Pirata

Un juego de combate por turnos basado en **Programación Orientada a Objetos (POO)** donde diriges un barco pirata y su tripulación en batallas estratégicas contra enemigos.

**Desarrollado por:** Karen Juliana Jaramillo Gutierrez | Samuel Alejandro Larios Ramos

---

## 🎮 ¿De qué se trata?

Es un juego de estrategia y simulación donde:
- **Creas tu barco** con un Capitán, Marinero y Pirata
- **Diriges combates** contra enemigos aleatorios
- **Ganas puntos** por victorias y derrotas
- **Compites en el TOP 5** de mejores barcos (ranking persistente)

---

## ⚙️ Funcionalidades principales

### 🚢 Sistema de Tripulación
Tres tipos de personajes con habilidades diferentes:

| Rol | Vida | Fuerza | Defensa | Arma |
|-----|------|--------|---------|------|
| **Capitán** | 20 | 12 | 3 | Espada |
| **Marinero** | 15 | 8 | 4 | Cañón |
| **Pirata Raso** | 18 | 9 | 5 | Pistola |

### ⚔️ Sistema de Combate
- Batallas por **turnos aleatorios**
- Cada combate enfrenta **2 enemigos aleatorios**
- Los enemigos pueden ser cualquiera de los 3 tipos
- El jugador elige atacar o huir en cada ronda

### 📊 Sistema de Puntos
```
Victoria            +50 pts
Derrota            -30 pts
Enemigo derrotado  +15 pts por cada uno
Aliado muerto      -10 pts
```

### 🏆 Ranking Persistente
- Guarda automáticamente los **TOP 5 barcos** en archivo JSON
- Las puntuaciones se actualizan tras cada partida
- Se mantiene entre sesiones

---

## 🎯 Cómo se juega

### Inicio del juego
1. Se muestra el TOP 5 actual
2. Ingresas los nombres de tu barco y tripulación
3. Tu barco aparece listo para zarpar

### En el menú principal
```
1. Ver tripulación    → Muestra estado actual de tus personajes
2. Zarpar             → Busca combate (inicia batalla)
3. Salir del juego    → Termina la sesión
```

### Durante la batalla
- Ves el estado de ambas tripulaciones
- Eliges: **continuar peleando** o **huir**
- Los combates son automáticos (el código resuelve los ataques)
- Ganas si eliminas todos los enemigos
- Pierdes si tu tripulación es derrotada

### Fin de partida
- Se actualiza automáticamente el ranking
- Si pierdes toda la tripulación, termina el juego
- Puedes ver el TOP 5 final

---

## 📋 Requisitos

- **Python 3.7+**
- Librerías estándar (no necesita instalación):
  - `abc` (clases abstractas)
  - `json` (persistencia)
  - `random` (eventos aleatorios)
  - `time` (animaciones)
  - `os` (gestión de archivos)

---

## 🚀 Cómo ejecutar

### Opción 1: Terminal/CMD
```bash
python juego_pirata.py
```

### Opción 2: IDE (Visual Studio Code, PyCharm, etc.)
1. Abre el archivo `juego_pirata.py`
2. Presiona el botón "Run" o `F5`

---

## 🏗️ Estructura del Código (POO Avanzada)

### Clases principales

**`Tripulante` (Clase Abstracta)**
- Define el contrato para todos los personajes
- Métodos abstractos: `atacar()`, `realizar_accion_especial()`
- Maneja vida, ataque, defensa y daño

```
Tripulante (abstracta)
├── Capitán
├── Marinero
└── PirataRaso
```

**`Barco` (Composición)**
- Contiene una lista de Tripulantes
- Gestiona puntos y estado general

### Conceptos OOP aplicados
- ✅ **Herencia:** Subclases de Tripulante
- ✅ **Polimorfismo:** Cada clase implementa `atacar()` diferente
- ✅ **Clases abstractas:** `ABC` y `@abstractmethod`
- ✅ **Composición:** Barco contiene Tripulantes
- ✅ **Métodos estáticos/de clase:** `crear_enemigo_aleatorio()`, `total_tripulantes()`
- ✅ **Propiedades:** `@property` para proteger datos

---

## 📁 Archivos generados

- **`top_jugadores.json`** - Ranking persistente (se crea automáticamente)

Contenido de ejemplo:
```json
[
  {
    "barco": "El Temido",
    "tripulacion": ["Drake", "Paco", "Rata"],
    "puntos": 85
  }
]
```

---

## 💡 Ejemplos de juego

### Ejemplo de batalla
```
¡¡BARCO PIRATA ENEMIGO A LA VISTA!!
Enemigos que se acercan:
  • Barbanegra [Capitán de Barco Corsario] — Vida: 18

⚔️ ¡COMIENZA EL COMBATE!

TU TRIPULACIÓN:
  Drake [Capitán] — Vida: 25
  Paco [Marinero] — Vida: 14
  Rata [Pirata] — Vida: 19

ENEMIGOS:
  Barbanegra [Capitán de Barco Corsario] — Vida: 18

⚔️ RONDA DE COMBATE ⚡

⚔️ El Capitán Drake ataca ferozmente con su ESPADA.
  Barbanegra bloquea parcialmente. Mitigación: 4
  Barbanegra resiste. Vida: 10

💣 El Marinero Paco dispara un CAÑONAZO.
  Barbanegra bloquea parcialmente. Mitigación: 3
  💀 Barbanegra ha caído en combate.

🎉 ¡VICTORIA! Derrotaste a toda la tripulación enemiga.
✅ ¡Victoria! +50 puntos de botín.
```

---

## 🎓 Conceptos educativos

Este proyecto enseña:
- **POO Avanzada:** Herencia, polimorfismo, composición
- **Clases abstractas:** Diseño de contratos
- **Persistencia de datos:** Lectura/escritura JSON
- **Control de flujo:** Bucles, condicionales, validación de entrada
- **Aleatoriedad:** Generación de eventos impredecibles
- **Estructuras de datos:** Listas y diccionarios

---

## 🐛 Notas técnicas

- La vida de cada tripulante varía ±10 unidades 
- Los enemigos se generan aleatoriamente
- El orden de ataque en combate es aleatorio
- El ranking solo guarda los 5 mejores barcos
- Si el archivo JSON se daña, el juego continúa sin ranking

---

## 📝 Licencia

Proyecto educativo para el curso de POO - Universidad Pascual Bravo

---

## 👥 Autores

- **Karen Juliana Jaramillo Gutierrez**
- **Samuel Alejandro Larios Ramos**

---

**¡Que tengas suerte en alta mar, marinero! 🏴‍☠️**