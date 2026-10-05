from app.nodos import clasificar_consulta


def test_clasificador_faq():
    resultado = clasificar_consulta(
        "¿Cómo puedo cambiar mi contraseña?"
    )

    assert resultado.categoria == "faq"
    assert 0.0 <= resultado.confianza <= 1.0


def test_clasificador_bug():
    resultado = clasificar_consulta(
        "La aplicación se cierra cuando abro el menú de configuración."
    )

    assert resultado.categoria == "bug"
    assert 0.0 <= resultado.confianza <= 1.0


def test_clasificador_tecnico():
    resultado = clasificar_consulta(
        "Estoy recibiendo un error 503 al conectarme al servidor."
    )

    assert resultado.categoria == "tecnico"
    assert 0.0 <= resultado.confianza <= 1.0


def test_clasificador_escalar():
    resultado = clasificar_consulta(
        "Necesito hablar con una persona sobre mi problema de facturación."
    )

    assert resultado.categoria == "escalar"
    assert 0.0 <= resultado.confianza <= 1.0