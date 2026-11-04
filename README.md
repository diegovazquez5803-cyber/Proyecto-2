# Proyecto 2 – Red de transporte con Dijkstra

Programa modular en Python que permite capturar conexiones de una red de
transporte, guardarlas en un archivo CSV, cargarlas como un grafo en memoria
y calcular la ruta más corta con el algoritmo de Dijkstra.

## Estructura

| Archivo           | Descripción                                              |
|-------------------|----------------------------------------------------------|
| `main.py`         | Script principal interactivo (menú y captura por consola)|
| `grafo.py`        | Clases POO `Nodo` y `Grafo` (incluye Dijkstra)           |
| `io_handler.py`   | Validación y lectura/escritura del CSV                   |
| `nodos.csv`       | Conexiones de la red (`Origen,Destino,Peso`)             |
| `requirements.txt`| Dependencias de desarrollo (`flake8`)                    |

## Requisitos

- Python 3.10 o superior (se usan anotaciones como `str | None`).

## Cómo ejecutarlo

```bash
cd proyecto2
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

Menú:

1. **Agregar una conexión**: pide origen, destino y peso. Si el peso está
   vacío, es texto (`cinco`), no es finito (`nan`, `inf`) o es negativo, se
   muestra el motivo y se vuelve a pedir. Al validarse, se guarda en
   `nodos.csv` (modo *append*).
2. **Calcular la ruta más corta**: vuelve a leer `nodos.csv`, construye el
   grafo, pide nodo de inicio y de destino, y muestra el recorrido y el peso
   total.
3. **Salir**.

## Formato de `nodos.csv`

```csv
Origen,Destino,Peso
UAG,UP,4.9
UAG,TEC,6.3
```

- Las conexiones son **bidireccionales**.
- Los nombres de nodo se normalizan a mayúsculas y sin espacios sobrantes.
- Si una misma conexión aparece varias veces, **gana la última fila**
  (así se puede actualizar un peso agregando la conexión de nuevo).
- Las filas corruptas (peso no numérico, negativo, campos vacíos, columnas
  faltantes) se **omiten con un aviso** sin detener el programa. Si falta el
  archivo o los encabezados, se avisa y el grafo queda vacío.

### Nodos de ejemplo

El `nodos.csv` original (catálogo de universidades) se convirtió al formato
de aristas. Los pesos son **distancias aproximadas en km en línea recta**,
calculadas con coordenadas estimadas; sirven como datos de demostración y
pueden reemplazarse por distancias reales.

| Nodo | Institución                                  |
|------|----------------------------------------------|
| UAG  | Universidad Autónoma de Guadalajara          |
| UP   | Universidad Panamericana, Campus Guadalajara |
| UDG  | Universidad de Guadalajara                   |
| TEC  | Tecnológico de Monterrey, Campus Guadalajara |
| UTEG | Centro Universitario UTEG                    |

## Calidad de código

```bash
flake8
```

Debe terminar sin mostrar errores. El código incluye *type hints* en todas
las funciones y métodos, *docstrings*, excepciones específicas
(`ValueError`, `KeyError`, `FileNotFoundError`, `OSError`, `csv.Error`) y
`with open(...)` en toda operación de disco.
