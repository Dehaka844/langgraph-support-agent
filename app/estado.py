from typing import TypedDict


class EstadoSoporte(TypedDict):
    """
    Estado compartido por todos los nodos del grafo de soporte.
    """

    mensaje_usuario: str
    categoria: str
    contexto: list[str]
    herramientas_usadas: list[str]
    respuesta_final: str
    requiere_humano: bool
    metadata: dict

def crear_estado_inicial(mensaje_usuario: str) -> EstadoSoporte:
    """
    Crea el estado inicial del grafo a partir del mensaje del usuario.
    """

    return {
        "mensaje_usuario": mensaje_usuario,
        "categoria": "",
        "contexto": [],
        "herramientas_usadas": [],
        "respuesta_final": "",
        "requiere_humano": False,
        "metadata": {},
    }