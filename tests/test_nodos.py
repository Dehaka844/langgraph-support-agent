from app.estado import crear_estado_inicial
from app.nodos import (
    buscar_en_conocimiento,
    extraer_codigo_error,
    extraer_datos_bug,
    generar_respuesta_final,
    nodo_bug,
    nodo_escalar,
    nodo_faq,
    nodo_tecnico,
)


def test_busqueda_conocimiento_encontrada():
    resultado = buscar_en_conocimiento(
        "¿Cómo puedo recuperar mi contraseña?"
    )

    assert resultado is not None
    assert "contraseña" in resultado.lower()


def test_busqueda_conocimiento_no_encontrada():
    resultado = buscar_en_conocimiento(
        "¿Cómo puedo cambiar el color de la aplicación?"
    )

    assert resultado is None


def test_nodo_faq_con_respuesta():
    estado = crear_estado_inicial(
        "¿Cómo puedo recuperar mi contraseña?"
    )

    estado["categoria"] = "faq"

    resultado = nodo_faq(estado)

    assert resultado["requiere_humano"] is False
    assert len(resultado["contexto"]) == 1
    assert "contraseña" in resultado["contexto"][0].lower()


def test_nodo_faq_sin_respuesta():
    estado = crear_estado_inicial(
        "¿Cómo puedo cambiar el color de la aplicación?"
    )

    estado["categoria"] = "faq"

    resultado = nodo_faq(estado)

    assert resultado["requiere_humano"] is True
    assert len(resultado["contexto"]) == 1

def test_extraer_datos_bug():
    resultado = extraer_datos_bug(
        "La aplicación móvil se cierra cada vez que "
        "intento abrir la pantalla de configuración."
    )

    assert resultado.producto
    assert resultado.descripcion
    assert resultado.severidad in {"baja", "media", "alta"}

def test_nodo_bug():
    estado = crear_estado_inicial(
        "La aplicación móvil se cierra cada vez que "
        "intento abrir la pantalla de configuración."
    )

    estado["categoria"] = "bug"

    resultado = nodo_bug(estado)

    assert resultado["requiere_humano"] is False
    assert "crear_ticket" in resultado["herramientas_usadas"]

    assert len(resultado["contexto"]) == 4

    assert "bug" in resultado["metadata"]
    assert resultado["metadata"]["bug"]["producto"]
    assert resultado["metadata"]["bug"]["descripcion"]
    assert resultado["metadata"]["bug"]["severidad"]

def test_extraer_codigo_error():
    resultado = extraer_codigo_error(
        "Estoy recibiendo un error 503 al conectar con el servidor."
    )

    assert resultado == "503"


def test_extraer_codigo_error_no_encontrado():
    resultado = extraer_codigo_error(
        "¿Dónde encuentro la documentación de la API?"
    )

    assert resultado is None


def test_nodo_tecnico_diagnostico():
    estado = crear_estado_inicial(
        "Estoy recibiendo un error 503 al conectar con el servidor."
    )

    estado["categoria"] = "tecnico"

    resultado = nodo_tecnico(estado)

    assert "diagnosticar_error" in resultado["herramientas_usadas"]

    assert len(resultado["contexto"]) == 1

    assert "503" in resultado["contexto"][0]

    assert "diagnostico" in resultado["metadata"]

    assert (
        resultado["metadata"]["diagnostico"]["codigo_error"]
        == "503"
    )


def test_nodo_tecnico_documentacion():
    estado = crear_estado_inicial(
        "¿Dónde encuentro la documentación de la API?"
    )

    estado["categoria"] = "tecnico"

    resultado = nodo_tecnico(estado)

    assert "buscar_documentacion" in resultado["herramientas_usadas"]

    assert len(resultado["contexto"]) == 1

    assert "API" in resultado["contexto"][0]

    assert "documentacion" in resultado["metadata"]

def test_nodo_escalar():
    estado = crear_estado_inicial(
        "Necesito hablar con una persona sobre mi facturación."
    )

    estado["categoria"] = "escalar"

    resultado = nodo_escalar(estado)

    assert resultado["requiere_humano"] is True

    assert len(resultado["contexto"]) == 1

    assert "humano" in resultado["contexto"][0].lower()

def test_generar_respuesta_final():
    estado = crear_estado_inicial(
        "¿Cómo puedo recuperar mi contraseña?"
    )

    estado["categoria"] = "faq"

    estado["contexto"].append(
        "Para restablecer la contraseña, accede a la pantalla "
        "de inicio de sesión y selecciona '¿Has olvidado tu contraseña?'."
    )

    resultado = generar_respuesta_final(estado)

    assert resultado["respuesta_final"]

    assert isinstance(
        resultado["respuesta_final"],
        str,
    )