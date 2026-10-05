import uuid

from langchain_core.tools import tool


@tool
def crear_ticket(
    producto: str,
    descripcion: str,
    severidad: str,
) -> str:
    """
    Simula la creación de un ticket de soporte.

    Devuelve un identificador ficticio del ticket.
    """

    ticket_id = f"TCK-{uuid.uuid4().hex[:8].upper()}"

    return (
        f"Ticket {ticket_id} creado correctamente. "
        f"Producto: {producto}. "
        f"Severidad: {severidad}."
    )


@tool
def buscar_documentacion(consulta: str) -> str:
    """
    Busca información en una documentación técnica simulada.
    """

    consulta_normalizada = consulta.lower()

    if "api" in consulta_normalizada:
        return (
            "La API está disponible en el portal de desarrolladores. "
            "La documentación incluye autenticación, endpoints, "
            "parámetros y ejemplos de uso."
        )

    if "autenticación" in consulta_normalizada or "login" in consulta_normalizada:
        return (
            "La autenticación de la API utiliza tokens de acceso. "
            "El token debe enviarse en la cabecera Authorization "
            "de las peticiones."
        )

    if "configuración" in consulta_normalizada:
        return (
            "La configuración del servicio se encuentra en el archivo "
            "config.json. Los cambios requieren reiniciar el servicio "
            "para aplicarse."
        )

    return (
        "No se ha encontrado documentación específica para la consulta."
    )


@tool
def diagnosticar_error(codigo_error: str) -> str:
    """
    Diagnostica un código de error conocido.
    """

    codigo_normalizado = codigo_error.upper().strip()

    diagnosticos = {
        "400": (
            "Error 400: la petición enviada no es válida. "
            "Comprueba los parámetros y el formato de la solicitud."
        ),
        "401": (
            "Error 401: falta autenticación o las credenciales "
            "proporcionadas no son válidas."
        ),
        "403": (
            "Error 403: el usuario no tiene permisos suficientes "
            "para realizar esta operación."
        ),
        "404": (
            "Error 404: el recurso solicitado no existe o no está "
            "disponible en la ruta indicada."
        ),
        "500": (
            "Error 500: se ha producido un error interno del servidor. "
            "Revisa los registros del servicio."
        ),
        "503": (
            "Error 503: el servicio no está disponible temporalmente. "
            "Comprueba el estado del servidor y vuelve a intentarlo."
        ),
    }

    return diagnosticos.get(
        codigo_normalizado,
        (
            f"No existe un diagnóstico específico para el código "
            f"{codigo_error}."
        ),
    )