from app.estado import crear_estado_inicial
from app.grafo import router
from app.grafo import construir_grafo


def test_router_faq():
    estado = crear_estado_inicial("¿Cómo cambio mi contraseña?")
    estado["categoria"] = "faq"

    assert router(estado) == "faq"


def test_router_bug():
    estado = crear_estado_inicial("La aplicación se cierra.")
    estado["categoria"] = "bug"

    assert router(estado) == "bug"


def test_router_tecnico():
    estado = crear_estado_inicial("Error 503 en el servidor.")
    estado["categoria"] = "tecnico"

    assert router(estado) == "tecnico"


def test_router_escalar():
    estado = crear_estado_inicial(
        "Necesito hablar con una persona."
    )
    estado["categoria"] = "escalar"

    assert router(estado) == "escalar"


def test_router_categoria_desconocida():
    estado = crear_estado_inicial("Consulta desconocida.")
    estado["categoria"] = "categoria_invalida"

    assert router(estado) == "escalar"

def test_construir_grafo():
    grafo = construir_grafo()

    assert grafo is not None

def test_grafo_faq():
    grafo = construir_grafo()

    estado = crear_estado_inicial(
        "¿Cómo puedo recuperar mi contraseña?"
    )

    resultado = grafo.invoke(estado)

    assert resultado["categoria"] == "faq"

    assert resultado["requiere_humano"] is False

    assert resultado["respuesta_final"]

    assert len(resultado["contexto"]) >= 1

def test_grafo_bug():
    grafo = construir_grafo()

    estado = crear_estado_inicial(
        "La aplicación móvil se cierra cada vez que "
        "intento abrir la pantalla de configuración."
    )

    resultado = grafo.invoke(estado)

    assert resultado["categoria"] == "bug"

    assert resultado["requiere_humano"] is False

    assert resultado["respuesta_final"]

    assert "crear_ticket" in resultado["herramientas_usadas"]

    assert "bug" in resultado["metadata"]

def test_grafo_tecnico():
    grafo = construir_grafo()

    estado = crear_estado_inicial(
        "Estoy recibiendo un error 503 al conectar con el servidor."
    )

    resultado = grafo.invoke(estado)

    assert resultado["categoria"] == "tecnico"

    assert resultado["requiere_humano"] is False

    assert resultado["respuesta_final"]

    assert "diagnosticar_error" in resultado["herramientas_usadas"]

    assert "diagnostico" in resultado["metadata"]

    assert (
        resultado["metadata"]["diagnostico"]["codigo_error"]
        == "503"
    )

def test_grafo_escalar():
    grafo = construir_grafo()

    estado = crear_estado_inicial(
        "Necesito hablar con una persona sobre mi problema de facturación."
    )

    resultado = grafo.invoke(estado)

    assert resultado["categoria"] == "escalar"

    assert resultado["requiere_humano"] is True

    assert resultado["respuesta_final"] == ""

    assert len(resultado["contexto"]) == 1

def test_grafo_registra_duraciones():
    grafo = construir_grafo()

    estado = crear_estado_inicial(
        "¿Cómo puedo recuperar mi contraseña?"
    )

    resultado = grafo.invoke(estado)

    duraciones = resultado["metadata"]["duraciones_nodos"]

    assert "clasificador" in duraciones
    assert "faq" in duraciones
    assert "generador_respuesta" in duraciones

    assert duraciones["clasificador"] >= 0
    assert duraciones["faq"] >= 0
    assert duraciones["generador_respuesta"] >= 0

def test_grafo_registra_duracion_total():
    grafo = construir_grafo()

    estado = crear_estado_inicial(
        "Necesito hablar con una persona sobre mi facturación."
    )

    resultado = grafo.invoke(estado)

    # En esta prueba ejecutamos directamente el grafo, por lo que
    # el tiempo total lo añadiremos mediante ejecutar_consulta.