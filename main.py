"""
Nombre completo: Diego Vázquez Hernández
Descripción: Programa interactivo para administrar una red de transporte.
Objetivo: Ingresar conexiones de forma segura, guardarlas en nodos.csv,
    cargar el grafo en memoria y calcular la ruta más corta con Dijkstra.
"""

from grafo import Grafo
from io_handler import (
    cargar_grafo,
    formatear_peso,
    guardar_arista,
    normalizar_nodo,
    validar_peso,
)


def solicitar_nodo(mensaje: str) -> str:
    """Pide el nombre de un nodo hasta que el usuario ingrese uno válido."""
    while True:
        try:
            return normalizar_nodo(input(mensaje))
        except ValueError as error:
            print(f"  [Error] {error} Intente de nuevo.")


def solicitar_peso(mensaje: str) -> float:
    """Pide un peso hasta que sea un número válido (no vacío, no negativo)."""
    while True:
        try:
            return validar_peso(input(mensaje))
        except ValueError as error:
            print(f"  [Error] {error} Intente de nuevo.")


def ingresar_conexion() -> None:
    """Solicita una nueva conexión, la valida y la guarda en el CSV."""
    print("\n--- Nueva conexión ---")
    origen = solicitar_nodo("Nodo origen: ")

    while True:
        destino = solicitar_nodo("Nodo destino: ")
        if destino != origen:
            break
        print("  [Error] El destino debe ser distinto al origen.")

    peso = solicitar_peso("Peso de la arista: ")

    try:
        guardar_arista(origen, destino, peso)
    except OSError as error:
        print(f"  [Error] No se pudo guardar en el archivo: {error}\n")
        return

    print(
        f"  Conexión guardada: {origen} <-> {destino} "
        f"(peso {formatear_peso(peso)})\n"
    )


def mostrar_ruta(grafo: Grafo, inicio: str, destino: str) -> None:
    """Ejecuta Dijkstra y muestra la ruta más corta y su peso total."""
    try:
        distancia, camino = grafo.dijkstra(inicio, destino)
    except ValueError as error:
        print(f"  [Error] {error}\n")
        return

    print(f"\nRuta de {inicio} a {destino}")
    if not camino:
        print("  No existe una ruta entre estos nodos.\n")
        return
    print(f"  Peso total: {formatear_peso(distancia)}")
    print(f"  Recorrido: {' -> '.join(camino)}\n")


def calcular_ruta() -> None:
    """Carga el grafo desde el CSV y calcula una ruta entre dos nodos."""
    print("\n--- Calcular ruta más corta ---")
    grafo = cargar_grafo()

    if not grafo.nodos:
        print("  No hay conexiones cargadas. Agregue alguna primero.\n")
        return

    print(f"  Nodos disponibles: {', '.join(sorted(grafo.nodos))}")
    inicio = solicitar_nodo("Nodo de inicio: ")
    destino = solicitar_nodo("Nodo de destino: ")
    mostrar_ruta(grafo, inicio, destino)


def mostrar_menu() -> None:
    """Imprime el menú principal."""
    print("=== Red de transporte - Dijkstra ===")
    print("1. Agregar una conexión")
    print("2. Calcular la ruta más corta")
    print("3. Salir")


def main() -> None:
    """Ciclo principal del programa."""
    try:
        while True:
            mostrar_menu()
            opcion = input("Elija una opción: ").strip()

            if opcion == "1":
                ingresar_conexion()
            elif opcion == "2":
                calcular_ruta()
            elif opcion == "3":
                break
            else:
                print("  [Error] Opción no válida. Elija 1, 2 o 3.\n")
    except (KeyboardInterrupt, EOFError):
        print()

    print("Hasta pronto.")


if __name__ == "__main__":
    main()
