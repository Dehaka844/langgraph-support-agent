from app.herramientas import (
    buscar_documentacion,
    crear_ticket,
    diagnosticar_error,
)


def test_crear_ticket():
    resultado = crear_ticket.invoke(
        {
            "producto": "Aplicación móvil",
            "descripcion": "La aplicación se cierra al abrir configuración.",
            "severidad": "alta",
        }
    )

    assert resultado.startswith("Ticket TCK-")
    assert "creado correctamente" in resultado
    assert "Aplicación móvil" in resultado
    assert "alta" in resultado


def test_buscar_documentacion():
    resultado = buscar_documentacion.invoke(
        "¿Dónde encuentro la documentación de la API?"
    )

    assert resultado
    assert "API" in resultado


def test_diagnosticar_error():
    resultado = diagnosticar_error.invoke("503")

    assert resultado
    assert "503" in resultado
    assert "disponible" in resultado.lower()