"""
Nombre completo: Diego Vázquez Hernández
Descripción: Funciones de validación y de lectura/escritura del archivo CSV.
Objetivo: Persistir las conexiones de la red en nodos.csv y reconstruir el
    grafo en memoria a partir de dicho archivo.
"""

import csv
import math
from pathlib import Path
from typing import Optional, Sequence

from grafo import Grafo

RUTA_CSV: Path = Path(__file__).resolve().parent / "nodos.csv"
ENCABEZADOS: list[str] = ["Origen", "Destino", "Peso"]


def normalizar_nodo(texto: str) -> str:
    """Limpia el nombre de un nodo (sin espacios, en mayúsculas).

    Lanza ValueError si el nombre queda vacío.
    """
    nombre = texto.strip().upper()
    if not nombre:
        raise ValueError("El nombre del nodo no puede estar vacío.")
    return nombre


def validar_peso(texto: str) -> float:
    """Convierte un texto en un peso válido (número finito y no negativo).

    Lanza ValueError con un mensaje descriptivo si el texto está vacío,
    no es numérico o es negativo.
    """
    texto = texto.strip()
    if not texto:
        raise ValueError("El peso no puede estar vacío.")

    try:
        peso = float(texto)
    except ValueError:
        raise ValueError(
            f"'{texto}' no es un número válido "
            "(use punto decimal, por ejemplo 4.5)."
        ) from None

    if not math.isfinite(peso):
        raise ValueError("El peso debe ser un número finito.")
    if peso < 0:
        raise ValueError("El peso no puede ser negativo.")
    return peso


def formatear_peso(peso: float) -> str:
    """Devuelve el peso como texto (sin '.0' si el valor es entero)."""
    peso = round(peso, 6)
    if peso.is_integer():
        return str(int(peso))
    return str(peso)


def _archivo_termina_en_salto(ruta: Path) -> bool:
    """Indica si el último carácter del archivo es un salto de línea."""
    with open(ruta, "rb") as archivo:
        archivo.seek(-1, 2)
        return archivo.read(1) == b"\n"


def guardar_arista(
    origen: str,
    destino: str,
    peso: float,
    ruta: Path = RUTA_CSV,
) -> None:
    """Agrega una conexión al CSV en modo append ('a').

    Si el archivo no existe o está vacío, escribe primero los encabezados.
    Puede lanzar OSError si el archivo no se puede escribir.
    """
    necesita_encabezado = not ruta.exists() or ruta.stat().st_size == 0
    falta_salto = not necesita_encabezado and not _archivo_termina_en_salto(
        ruta
    )

    with open(ruta, "a", newline="", encoding="utf-8") as archivo:
        if falta_salto:
            archivo.write("\n")
        escritor = csv.writer(archivo, lineterminator="\n")
        if necesita_encabezado:
            escritor.writerow(ENCABEZADOS)
        escritor.writerow([origen, destino, formatear_peso(peso)])


def _validar_encabezados(campos: Optional[Sequence[str]]) -> None:
    """Verifica que el CSV tenga los encabezados Origen, Destino y Peso.

    Lanza KeyError si falta alguno (o si el archivo no tiene encabezados).
    """
    presentes = [campo.strip() for campo in campos or []]
    faltantes = [campo for campo in ENCABEZADOS if campo not in presentes]
    if faltantes:
        raise KeyError(", ".join(faltantes))


def _leer_fila(fila: dict[str, Optional[str]]) -> tuple[str, str, float]:
    """Extrae y valida (origen, destino, peso) de una fila del CSV.

    Lanza KeyError si falta una columna y ValueError si algún dato es
    inválido (vacío, peso no numérico, peso negativo, etc.).
    """
    valores: list[str] = []
    for clave in ENCABEZADOS:
        valor = fila[clave]
        if valor is None:
            raise ValueError(f"falta el valor de '{clave}'")
        valores.append(valor)

    origen = normalizar_nodo(valores[0])
    destino = normalizar_nodo(valores[1])
    peso = validar_peso(valores[2])
    return origen, destino, peso


def cargar_grafo(ruta: Path = RUTA_CSV) -> Grafo:
    """Lee el CSV fila por fila y construye el grafo en memoria.

    Las filas corruptas se omiten con un aviso, sin detener el sistema.
    Si el archivo no existe o no tiene los encabezados correctos, se
    devuelve un grafo vacío.
    """
    grafo = Grafo()
    omitidas = 0

    try:
        with open(ruta, newline="", encoding="utf-8-sig") as archivo:
            lector = csv.DictReader(archivo, skipinitialspace=True)
            _validar_encabezados(lector.fieldnames)

            for numero, fila in enumerate(lector, start=2):
                try:
                    origen, destino, peso = _leer_fila(fila)
                    grafo.agregar_arista(origen, destino, peso)
                except (KeyError, ValueError) as error:
                    omitidas += 1
                    print(f"  [Aviso] Fila {numero} omitida: {error}")
    except FileNotFoundError:
        print(f"  [Aviso] No se encontró el archivo '{ruta.name}'.")
    except KeyError as error:
        print(
            f"  [Error] Faltan encabezados en '{ruta.name}': "
            f"{error.args[0]}. "
            f"Se esperaba: {', '.join(ENCABEZADOS)}."
        )
    except (OSError, csv.Error, UnicodeDecodeError) as error:
        print(f"  [Error] No se pudo leer '{ruta.name}': {error}")

    if omitidas:
        print(f"  [Aviso] Total de filas omitidas: {omitidas}")
    return grafo
