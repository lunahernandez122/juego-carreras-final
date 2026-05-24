# Juego de Carreras 🏎️

**Kevin Hernández Henao & Luna Hernandez Montoya**  
Programación Orientada a Objetos — Pascual Bravo

---

## ¿De qué va el juego?

Es un juego de carreras por turnos. Tú eliges tu vehículo (carro, moto o camión), le pones nombre, y te metes a un campeonato de 3 carreras contra rivales generados aleatoriamente.

En cada turno decides si acelerar normal o gastar un turbo para ir más rápido. Los rivales se mueven solos y también tienen sus turbos. Por el camino pueden aparecer obstáculos (baches, derrames de aceite) o cosas buenas (viento a favor, turbos extra). Al final de cada carrera se reparten puntos al estilo F1 y se arma una clasificación acumulada.

Cuando termina el campeonato podés exportar los resultados en CSV, JSON, TXT o XLSX.

## ¿Cómo correrlo?

Primero clonás el repo y entrás a la carpeta:

```bash
git clone <url-del-repo>
cd juego_carreras
```

Se recomienda usar un entorno virtual:

```bash
python -m venv venv

# Windows:
venv\Scripts\activate

# macOS / Linux:
source venv/bin/activate
```

Instalás las dependencias:

```bash
pip install -r requirements.txt
```

Y lo ejecutás:

```bash
python main.py
```

> `openpyxl` es opcional, solo lo necesitás si querés exportar a XLSX.

## Archivos del proyecto

```
juego_carreras/
├── main.py          # interfaz gráfica con pygame y control de pantallas
├── logica.py        # todas las clases del juego
├── requirements.txt
└── README.md
```

## Tecnologías

- Python 3.10+
- pygame (interfaz gráfica)
- openpyxl (exportación a Excel, opcional)
- Módulos estándar: `random`, `json`, `csv`, `abc`

## Conceptos de POO que aplicamos

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
