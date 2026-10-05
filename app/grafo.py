from typing import Literal

from langgraph.graph import END, START, StateGraph

from app.estado import EstadoSoporte
from app.nodos import (
    generar_respuesta_final,
    nodo_bug,
    nodo_escalar,
    nodo_faq,
    nodo_tecnico,
    nodo_clasificador,
)

def router(
    state: EstadoSoporte,
) -> Literal["faq", "bug", "tecnico", "escalar"]:
    """
    Determina el siguiente nodo del grafo según la categoría
    obtenida por el clasificador.
    """

    categoria = state["categoria"]

    if categoria == "faq":
        return "faq"

    if categoria == "bug":
        return "bug"

    if categoria == "tecnico":
        return "tecnico"

    return "escalar"

def construir_grafo():
    """
    Construye y compila el grafo de soporte.
    """

    builder = StateGraph(EstadoSoporte)

    builder.add_node(
        "clasificador",
        nodo_clasificador,
    )

    builder.add_node(
        "faq",
        nodo_faq,
    )

    builder.add_node(
        "bug",
        nodo_bug,
    )

    builder.add_node(
        "tecnico",
        nodo_tecnico,
    )

    builder.add_node(
        "escalar",
        nodo_escalar,
    )

    builder.add_node(
        "generador_respuesta",
        generar_respuesta_final,
    )

    builder.add_edge(
        START,
        "clasificador",
    )

    builder.add_conditional_edges(
        "clasificador",
        router,
        {
            "faq": "faq",
            "bug": "bug",
            "tecnico": "tecnico",
            "escalar": "escalar",
        },
    )

    builder.add_edge(
        "faq",
        "generador_respuesta",
    )

    builder.add_edge(
        "bug",
        "generador_respuesta",
    )

    builder.add_edge(
        "tecnico",
        "generador_respuesta",
    )

    builder.add_edge(
        "escalar",
        END,
    )

    builder.add_edge(
        "generador_respuesta",
        END,
    )

    return builder.compile()