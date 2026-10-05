import time

from app.estado import crear_estado_inicial
from app.grafo import construir_grafo


def ejecutar_consulta(mensaje: str):
    """
    Ejecuta una consulta completa utilizando el grafo de soporte.
    """

    grafo = construir_grafo()

    estado = crear_estado_inicial(mensaje)

    tiempo_inicio = time.perf_counter()

    resultado = grafo.invoke(
        estado,
        config={
            "run_name": "soporte_usuario",
            "tags": [
                "langgraph-support-agent",
                "produccion",
            ],
            "metadata": {
                "version_grafo": "1.0.0",
            },
        },
    )

    tiempo_total = time.perf_counter() - tiempo_inicio

    resultado["metadata"]["tiempo_total"] = tiempo_total

    return resultado


if __name__ == "__main__":
    mensaje = input("Consulta: ")

    resultado = ejecutar_consulta(mensaje)

    print("\nCategoría:", resultado["categoria"])

    print(
        "\nHerramientas utilizadas:",
        resultado["herramientas_usadas"],
    )

    print(
        "\nRequiere humano:",
        resultado["requiere_humano"],
    )

    print(
        "\nRespuesta:",
        resultado["respuesta_final"],
    )

    print("\nDuración de los nodos:")

    for nodo, duracion in resultado["metadata"].get(
        "duraciones_nodos",
        {},
    ).items():
        print(
            f"  - {nodo}: {duracion:.4f} segundos"
        )

    print(
        "\nTiempo total:",
        f"{resultado['metadata']['tiempo_total']:.4f} segundos",
    )