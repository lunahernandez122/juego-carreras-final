# Juego de Carreras 

# Equipo
- Kevin Hernández Henao
- Luna Hernández Montoya

Programación Orientada a Objetos — Institución Universitaria Pascual Bravo

# Descripción del juego
Juego de carreras por turnos desarrollado en Python, 
donde el jugador compite contra rivales aleatorios 
controlados por la máquina para llegar primero a la meta.

# Lo que había en la Fase 1
En la primera versión el jugador podía:
- Elegir la distancia de la carrera (100, 500, 1000 o 2000 metros)
- Registrar su vehículo con nombre y tipo (carro, moto o camión)
- Definir la cantidad de rivales manualmente o de forma aleatoria
- Elegir la dificultad del juego
- Jugar en modo manual o automático

Cada vehículo avanzaba según su tipo, podía activar turbos y encontraba obstáculos aleatorios. La carrera terminaba cuando un vehículo alcanzaba la meta.

# Lo nuevo en la Fase 2 
La Fase 2 se agregaron varias cosas como la clase campeonato que es la que permite que se juguen tres carreras para hacerlo mas completo:

- Sistema de campeonato de 3 carreras consecutivas con acumulación de puntos al estilo Fórmula 1
- Dificultad aleatoria en cada carrera (Fácil, Normal, Difícil) que afecta turbos, obstáculos y rivales
- Habilidades especiales únicas para cada tipo de vehículo (esta al final no se utilizo en el juego es para mostrar la abstracción)
- Sistema de inventario con ítems consumibles por vehículo
- Clasificación final acumulada de todos los participantes al terminar el campeonato
- Exportación de resultados en 4 formatos: CSV, JSON, TXT y XLSX
- Nuevas clases: "Campeonato", "Inventario", "Item" y "Exportador"

# Lo nuevo en la Fase 3 — Interfaz gráfica con Pygame
En la Fase 3 se reemplazó completamente la consola por una interfaz 
gráfica visual construida con la librería Pygame. El juego ahora se 
juega con clics del mouse, sin escribir nada en la terminal.

Pantallas implementadas:
- Pantalla de inicio: el jugador escribe su nombre, el nombre de su 
  vehículo y elige el tipo (Carro, Moto o Camión) con botones visuales
- Pantalla de preparación: antes de cada carrera muestra la distancia, 
  la dificultad asignada y los rivales que van a competir
- Pantalla de carrera: muestra en tiempo real las barras de progreso de 
  todos los vehículos, el turno actual y dos botones: Acelerar y Usar Turbo
- Pantalla de resultado por carrera: al terminar cada carrera muestra el 
  podio (1°, 2°, 3°) y los puntos obtenidos por el jugador
- Pantalla final del campeonato: muestra la clasificación acumulada de 
  las 3 carreras y permite exportar los resultados en CSV, JSON, TXT o XLSX 
  con un botón por formato

# ¿Cómo se juega?
1. Ingresa tu nombre de piloto y el nombre de tu vehículo
2. Elige el tipo de vehículo:  Carro (+10m/turno), Moto (+15m/turno) o Camión (+5m/turno)
3. En cada turno puedes acelerar normalmente o usar un turbo para avanzar más
4. Aparecen obstáculos aleatorios que pueden hacerte retroceder o ganar ventaja
5. Al terminar las 3 carreras se muestra la clasificación final con puntos acumulados
6. Puedes exportar los resultados en el formato que prefieras

# ¿Qué es el entorno virtual y por qué lo usamos?
Un entorno virtual (venv) es una carpeta aislada donde se instalan 
las librerías del proyecto sin afectar el resto del computador. 
Lo usamos para que cualquiera pueda instalar exactamente las mismas 
dependencias que usamos nosotros durante el desarrollo.

1. Descargar el repositorio:
git clone URL_DEL_REPOSITORIO

2. Entrar a la carpeta del proyecto:
cd juego_carreras

3. Crear y activar el entorno virtual:
python -m venv venv
venv\Scripts\activate

4. Instalar las dependencias necesarias:
pip install -r requirements.txt

5. Ejecutar el juego:
python main.py

> "openpyxl" es una librería opcional utilizada para exportar archivos en formato XLSX.

# Archivos del proyecto
juego_carreras/
├── main.py          # interfaz gráfica con pygame y control de pantallas
├── logica.py        # todas las clases del juego
├── requirements.txt
└── README.md


# Tecnologías
- Python 3.10+
- pygame (interfaz gráfica)
- openpyxl (exportación a Excel, opcional)
- Módulos estándar: `random`, `json`, `csv`, `abc`

# Conceptos de POO que aplicamos
| Concepto | Dónde lo usamos |
|---|---|
| Abstracción | `Vehiculo` es una clase abstracta con métodos `acelerar` y `habilidad_especial` que cada subclase debe implementar |
| Herencia | `Carro`, `Moto` y `Camion` heredan de `Vehiculo` |
| Polimorfismo | Cada vehículo implementa `acelerar()` distinto (10m, 15m, 5m) |
| Encapsulamiento | `__nombre` en `Vehiculo` y `__items` en `Inventario` son privados |
| Composición | `Vehiculo` tiene un `Inventario`; `Carrera` tiene una lista de vehículos |
| Métodos de clase | `Carrera.crear_aleatoria()`, `Campeonato.nuevo()`, `Vehiculo.total_vehiculos()` |
| Métodos estáticos | `calcular_avance_turbo()`, `clasificar_posicion()`, `puntos_por_posicion()` |
| Dunder methods | `__str__`, `__repr__`, `__eq__`, `__lt__`, `__len__`, `__iter__`, `__contains__` |
