from app.metricas import (
    calcular_distribucion_categorias,
    calcular_tasa_escalado,
    calcular_tiempo_medio_por_nodo,
    obtener_nodo_mas_lento,
    generar_resumen_metricas,
)


def obtener_ejecuciones_prueba():
    return [
        {
            "categoria": "faq",
            "requiere_humano": False,
            "metadata": {
                "duraciones_nodos": {
                    "clasificador": 0.5,
                    "faq": 0.2,
                    "generador_respuesta": 0.8,
                }
            },
        },
        {
            "categoria": "bug",
            "requiere_humano": False,
            "metadata": {
                "duraciones_nodos": {
                    "clasificador": 0.7,
                    "bug": 0.8,
                    "generador_respuesta": 0.9,
                }
            },
        },
        {
            "categoria": "tecnico",
            "requiere_humano": False,
            "metadata": {
                "duraciones_nodos": {
                    "clasificador": 0.6,
                    "tecnico": 0.3,
                    "generador_respuesta": 1.0,
                }
            },
        },
        {
            "categoria": "escalar",
            "requiere_humano": True,
            "metadata": {
                "duraciones_nodos": {
                    "clasificador": 1.2,
                    "escalar": 0.1,
                }
            },
        },
    ]


def test_calcular_tiempo_medio_por_nodo():
    ejecuciones = obtener_ejecuciones_prueba()

    resultado = calcular_tiempo_medio_por_nodo(
        ejecuciones
    )

    assert resultado["clasificador"] == 0.75

    assert resultado["generador_respuesta"] == 0.9


def test_calcular_distribucion_categorias():
    ejecuciones = obtener_ejecuciones_prueba()

    resultado = calcular_distribucion_categorias(
        ejecuciones
    )

    assert resultado == {
        "faq": 1,
        "bug": 1,
        "tecnico": 1,
        "escalar": 1,
    }


def test_calcular_tasa_escalado():
    ejecuciones = obtener_ejecuciones_prueba()

    resultado = calcular_tasa_escalado(
        ejecuciones
    )

    assert resultado == 0.25


def test_calcular_tasa_escalado_sin_ejecuciones():
    resultado = calcular_tasa_escalado([])

    assert resultado == 0.0


def test_obtener_nodo_mas_lento():
    ejecuciones = obtener_ejecuciones_prueba()

    tiempos = calcular_tiempo_medio_por_nodo(
        ejecuciones
    )

    resultado = obtener_nodo_mas_lento(tiempos)

    assert resultado == "generador_respuesta"


def test_obtener_nodo_mas_lento_sin_datos():
    resultado = obtener_nodo_mas_lento({})

    assert resultado is None

def test_generar_resumen_metricas():
    ejecuciones = obtener_ejecuciones_prueba()

    resultado = generar_resumen_metricas(
        ejecuciones
    )

    assert "tiempo_medio_por_nodo" in resultado

    assert "distribucion_categorias" in resultado

    assert "tasa_escalado" in resultado

    assert "nodo_mas_lento" in resultado

    assert resultado["nodo_mas_lento"] == "generador_respuesta"

def test_calcular_tiempo_medio_por_nodo_lee_duraciones_desde_metadata():
    ejecuciones = [
        {
            "metadata": {
                "duraciones_nodos": {
                    "clasificador": 1.0,
                    "tecnico": 0.5,
                }
            }
        },
        {
            "metadata": {
                "duraciones_nodos": {
                    "clasificador": 3.0,
                    "tecnico": 1.5,
                }
            }
        },
    ]

    resultado = calcular_tiempo_medio_por_nodo(ejecuciones)

    assert resultado["clasificador"] == 2.0
    assert resultado["tecnico"] == 1.0