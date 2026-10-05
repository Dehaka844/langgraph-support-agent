from collections import Counter
from statistics import mean


def calcular_tiempo_medio_por_nodo(
    ejecuciones: list[dict],
) -> dict[str, float]:
    tiempos = {}

    for ejecucion in ejecuciones:
        duraciones = ejecucion.get("metadata", {}).get(
            "duraciones_nodos",
            {},
        )

        for nodo, duracion in duraciones.items():
            tiempos.setdefault(nodo, []).append(duracion)

    return {
        nodo: mean(duraciones)
        for nodo, duraciones in tiempos.items()
    }


def calcular_distribucion_categorias(
    ejecuciones: list[dict],
) -> dict[str, int]:
    """
    Calcula cuántas ejecuciones pertenecen a cada categoría.
    """

    categorias = [
        ejecucion.get("categoria", "desconocida")
        for ejecucion in ejecuciones
    ]

    return dict(Counter(categorias))


def calcular_tasa_escalado(
    ejecuciones: list[dict],
) -> float:
    """
    Calcula el porcentaje de ejecuciones que requieren intervención humana.
    """

    if not ejecuciones:
        return 0.0

    escaladas = sum(
        ejecucion.get("requiere_humano", False)
        for ejecucion in ejecuciones
    )

    return escaladas / len(ejecuciones)


def obtener_nodo_mas_lento(
    tiempos_medios: dict[str, float],
) -> str | None:
    """
    Devuelve el nodo con mayor tiempo medio de ejecución.
    """

    if not tiempos_medios:
        return None

    return max(
        tiempos_medios,
        key=tiempos_medios.get,
    )

def generar_resumen_metricas(
    ejecuciones: list[dict],
) -> dict:
    """
    Genera un resumen completo de las métricas del sistema.
    """

    tiempos_medios = calcular_tiempo_medio_por_nodo(
        ejecuciones
    )

    return {
        "tiempo_medio_por_nodo": tiempos_medios,
        "distribucion_categorias": (
            calcular_distribucion_categorias(ejecuciones)
        ),
        "tasa_escalado": calcular_tasa_escalado(
            ejecuciones
        ),
        "nodo_mas_lento": obtener_nodo_mas_lento(
            tiempos_medios
        ),
    }