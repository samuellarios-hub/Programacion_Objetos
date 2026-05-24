# Juego de Aventura Pirata

Un juego interactivo de aventuras piratas donde controlas tu barco, entrenas tu tripulación y luchas contra enemigos. Desarrollado como proyecto final del curso de Programación Orientada a Objetos.

## Cómo instalar

1. Clona el repositorio:
```bash
git clone https://github.com/samuellarios-hub/Programacion_Objetos.git
```

2. Entra a la carpeta:
```bash
cd Programacion_Objetos
```

3. (Opcional) Crea un entorno virtual:
```bash
python -m venv venv
```

En Windows activa con:
```bash
venv\Scripts\activate
```


4. Instala las dependencias:
```bash
pip install -r requirements.txt
```

## Cómo jugar

Ejecuta el juego con:
```bash
python main.py
```

Se abre una ventana. Ahí creas tu barco con nombres que quieras, y empiezas a luchar contra enemigos.

## Qué tiene el juego

- Creas un barco con 3 tripulantes
- Luchas contra enemigos por turnos
- Ganas puntos si ganas las batallas
- Hay un ranking de los mejores barcos
- Los puntos se guardan automáticamente

## Cómo está organizado

- `main.py` → archivo principal, ejecuta el juego
- `gui.py` → pantallas y botones del juego
- `modelos.py` → las clases del juego (tripulantes, barco)
- `juego.py` → la lógica de las batallas
- `persistencia.py` → guarda el ranking en JSON

## Tecnologías

- Python
- Tkinter (para las ventanas)

## Autores

Samuel Alejandro Larios Ramos

Karen Juliana Jaramillo Gutierrez
