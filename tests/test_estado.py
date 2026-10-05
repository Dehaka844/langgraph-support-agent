from app.estado import EstadoSoporte, crear_estado_inicial


def test_crear_estado_inicial():
    mensaje = "¿Cómo puedo resetear mi contraseña?"

    estado = crear_estado_inicial(mensaje)

    assert estado["mensaje_usuario"] == mensaje
    assert estado["categoria"] == ""
    assert estado["contexto"] == []
    assert estado["herramientas_usadas"] == []
    assert estado["respuesta_final"] == ""
    assert estado["requiere_humano"] is False
    assert estado["metadata"] == {}


def test_estado_tiene_todas_las_claves():
    estado = crear_estado_inicial("Hola")

    claves_esperadas = {
        "mensaje_usuario",
        "categoria",
        "contexto",
        "herramientas_usadas",
        "respuesta_final",
        "requiere_humano",
        "metadata",
    }

    assert set(estado.keys()) == claves_esperadas