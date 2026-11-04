"""
Nombre completo: Diego Vázquez Hernández
Descripción: Clases POO (Nodo, Grafo) y algoritmo de Dijkstra.
Objetivo: Encontrar la ruta más corta (distancia mínima y secuencia de
    nodos) entre un nodo origen y un nodo destino en un grafo ponderado.
"""

import math


class Nodo:
    """Representa un nodo del grafo (universidad, estación, router, etc.)."""

    def __init__(self, nombre: str) -> None:
        """Crea un nodo sin vecinos con el nombre indicado."""
        self.nombre: str = nombre
        self.vecinos: dict[str, float] = {}  # {nombre_vecino: peso}

    def agregar_vecino(self, vecino: str, peso: float) -> None:
        """Registra (o actualiza) la conexión hacia un nodo vecino."""
        self.vecinos[vecino] = peso

    def __repr__(self) -> str:
        """Devuelve una representación legible del nodo."""
        return f"Nodo({self.nombre}, vecinos={self.vecinos})"


class Grafo:
    """Grafo ponderado representado con objetos Nodo."""

    def __init__(self) -> None:
        """Crea un grafo vacío."""
        self.nodos: dict[str, Nodo] = {}  # {nombre: Nodo}

    def agregar_nodo(self, nombre: str) -> None:
        """Agrega un nodo al grafo si todavía no existe."""
        if nombre not in self.nodos:
            self.nodos[nombre] = Nodo(nombre)

    def agregar_arista(
        self,
        origen: str,
        destino: str,
        peso: float,
        dirigido: bool = False,
    ) -> None:
        """Conecta dos nodos. Por defecto la conexión es en ambos sentidos.

        Lanza ValueError si el peso es negativo o no es un número finito.
        """
        if not math.isfinite(peso) or peso < 0:
            raise ValueError(
                "El peso debe ser un número finito mayor o igual a cero "
                "(Dijkstra no admite pesos negativos)."
            )

        self.agregar_nodo(origen)
        self.agregar_nodo(destino)

        self.nodos[origen].agregar_vecino(destino, peso)
        if not dirigido:
            self.nodos[destino].agregar_vecino(origen, peso)

    def dijkstra(self, inicio: str, destino: str) -> tuple[float, list[str]]:
        """Devuelve (distancia_total, camino) de inicio a destino.

        Si no existe ruta, devuelve (inf, []).
        Lanza ValueError si el nodo de inicio o destino no existe.
        """
        if inicio not in self.nodos or destino not in self.nodos:
            raise ValueError(
                "El nodo de inicio o destino no existe en el grafo."
            )

        distancias: dict[str, float] = {}
        anteriores: dict[str, str | None] = {}
        visitados: set[str] = set()

        for nombre in self.nodos:
            distancias[nombre] = float("inf")
            anteriores[nombre] = None

        distancias[inicio] = 0

        while len(visitados) < len(self.nodos):
            # Buscar el nodo no visitado más cercano
            nodo_actual: str | None = None
            menor_distancia = float("inf")

            for nombre in self.nodos:
                if nombre not in visitados:
                    if distancias[nombre] < menor_distancia:
                        menor_distancia = distancias[nombre]
                        nodo_actual = nombre

            if nodo_actual is None:
                break

            # Si llegamos al destino, terminamos
            if nodo_actual == destino:
                break

            visitados.add(nodo_actual)

            # Revisar vecinos
            nodo = self.nodos[nodo_actual]

            for vecino, peso in nodo.vecinos.items():
                nueva_distancia = distancias[nodo_actual] + peso

                if nueva_distancia < distancias[vecino]:
                    distancias[vecino] = nueva_distancia
                    anteriores[vecino] = nodo_actual

        # Si el destino sigue en infinito, no hay ruta posible
        if distancias[destino] == float("inf"):
            return float("inf"), []

        # Construir el camino
        camino: list[str] = []
        actual: str | None = destino

        while actual is not None:
            camino.append(actual)
            actual = anteriores[actual]

        camino.reverse()
        return distancias[destino], camino
