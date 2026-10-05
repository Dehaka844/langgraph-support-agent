from pydantic import BaseModel, Field
from langsmith import traceable
import re
import time
import unicodedata

from langchain_openai import ChatOpenAI

from app.configuracion import CATEGORIAS_VALIDAS
from app.estado import EstadoSoporte
from app.prompts import (
    PROMPT_CLASIFICADOR,
    PROMPT_EXTRACCION_BUG,
    PROMPT_RESPUESTA_FINAL,
)
from data.conocimiento import BASE_CONOCIMIENTO
from app.herramientas import (
    buscar_documentacion,
    crear_ticket,
    diagnosticar_error,
)



class ResultadoClasificacion(BaseModel):
    categoria: str = Field(
        description=(
            "Categoría de la consulta. Debe ser exactamente una de: "
            "faq, bug, tecnico, escalar."
        )
    )

    confianza: float = Field(
        description=(
            "Nivel de confianza de la clasificación entre 0.0 y 1.0."
        ),
        ge=0.0,
        le=1.0,
    )

class DatosBug(BaseModel):
    producto: str = Field(
        description="Producto o aplicación afectada por el bug."
    )

    descripcion: str = Field(
        description="Descripción del problema reportado."
    )

    severidad: str = Field(
        description=(
            "Severidad del problema: baja, media o alta."
        )
    )

class RespuestaFinal(BaseModel):
    respuesta: str = Field(
        description="Respuesta final que se enviará al usuario."
    )

def _registrar_duracion(
    state: EstadoSoporte,
    nombre_nodo: str,
    tiempo_inicio: float,
) -> None:
    """
    Registra la duración de un nodo en el estado.
    """

    duracion = time.perf_counter() - tiempo_inicio

    duraciones = state["metadata"].setdefault(
        "duraciones_nodos",
        {},
    )

    duraciones[nombre_nodo] = duracion

def crear_modelo_clasificador() -> ChatOpenAI:
    return ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0,
    )

def clasificar_consulta(mensaje_usuario: str) -> ResultadoClasificacion:
    """
    Clasifica una consulta utilizando el LLM.
    """

    modelo = crear_modelo_clasificador()

    modelo_estructurado = modelo.with_structured_output(
        ResultadoClasificacion
    )

    prompt = PROMPT_CLASIFICADOR.format(
        mensaje_usuario=mensaje_usuario
    )

    resultado = modelo_estructurado.invoke(prompt)

    if resultado.categoria not in CATEGORIAS_VALIDAS:
        raise ValueError(
            f"Categoría inválida recibida del LLM: {resultado.categoria}"
        )

    return resultado

@traceable(
    name="nodo_clasificador",
    tags=["nodo", "clasificacion"],
    metadata={
        "version_grafo": "1.0.0",
    },
)
def nodo_clasificador(state: EstadoSoporte) -> EstadoSoporte:
    """
    Nodo de LangGraph encargado de clasificar la consulta.
    """

    tiempo_inicio = time.perf_counter()

    resultado = clasificar_consulta(
        state["mensaje_usuario"]
    )

    state["categoria"] = resultado.categoria

    state["metadata"]["confianza_clasificacion"] = (
        resultado.confianza
    )

    _registrar_duracion(
        state,
        "clasificador",
        tiempo_inicio,
    )

    return state

def normalizar_texto(texto: str) -> str:
    texto = texto.lower()
    texto = unicodedata.normalize("NFD", texto)
    return "".join(
        caracter
        for caracter in texto
        if unicodedata.category(caracter) != "Mn"
    )


def buscar_en_conocimiento(mensaje: str) -> str | None:
    mensaje_normalizado = normalizar_texto(mensaje)

    for palabra_clave, respuesta in BASE_CONOCIMIENTO.items():
        palabra_clave_normalizada = normalizar_texto(palabra_clave)

        if palabra_clave_normalizada in mensaje_normalizado:
            return respuesta

    return None

@traceable(
    name="nodo_faq",
    tags=["nodo", "faq"],
    metadata={
        "version_grafo": "1.0.0",
    },
)
def nodo_faq(state: EstadoSoporte) -> EstadoSoporte:
    """
    Busca una respuesta en la base de conocimiento para una consulta FAQ.
    """

    tiempo_inicio = time.perf_counter()

    respuesta = buscar_en_conocimiento(
        state["mensaje_usuario"]
    )

    if respuesta is not None:
        state["contexto"].append(respuesta)
    else:
        state["requiere_humano"] = True
        state["contexto"].append(
            "No se encontró información relevante en la base de conocimiento."
        )
    
    _registrar_duracion(
        state,
        "faq",
        tiempo_inicio,
    )

    return state

def extraer_datos_bug(mensaje_usuario: str) -> DatosBug:
    """
    Extrae información estructurada de un reporte de bug.
    """

    modelo = crear_modelo_clasificador()

    modelo_estructurado = modelo.with_structured_output(
        DatosBug
    )

    prompt = PROMPT_EXTRACCION_BUG.format(
        mensaje_usuario=mensaje_usuario
    )

    resultado = modelo_estructurado.invoke(prompt)

    return resultado

@traceable(
    name="nodo_bug",
    tags=["nodo", "bug"],
    metadata={
        "version_grafo": "1.0.0",
    },
)
def nodo_bug(state: EstadoSoporte) -> EstadoSoporte:
    """
    Procesa un reporte de bug, crea un ticket y actualiza el estado.
    """

    tiempo_inicio = time.perf_counter()

    datos_bug = extraer_datos_bug(
        state["mensaje_usuario"]
    )

    resultado_ticket = crear_ticket.invoke(
        {
            "producto": datos_bug.producto,
            "descripcion": datos_bug.descripcion,
            "severidad": datos_bug.severidad,
        }
    )

    state["contexto"].append(
        f"Producto afectado: {datos_bug.producto}"
    )

    state["contexto"].append(
        f"Descripción: {datos_bug.descripcion}"
    )

    state["contexto"].append(
        f"Severidad: {datos_bug.severidad}"
    )

    state["contexto"].append(
        resultado_ticket
    )

    state["herramientas_usadas"].append(
        "crear_ticket"
    )

    state["metadata"]["bug"] = {
        "producto": datos_bug.producto,
        "descripcion": datos_bug.descripcion,
        "severidad": datos_bug.severidad,
    }

    _registrar_duracion(
        state,
        "bug",
        tiempo_inicio,
    )

    return state

def extraer_codigo_error(mensaje: str) -> str | None:
    """
    Busca un código de error numérico dentro del mensaje.

    Devuelve:
        str: código de error encontrado.
        None: si no se encuentra ningún código.
    """

    coincidencia = re.search(r"\b([45]\d{2})\b", mensaje)

    if coincidencia:
        return coincidencia.group(1)

    return None

@traceable(
    name="nodo_tecnico",
    tags=["nodo", "tecnico"],
    metadata={
        "version_grafo": "1.0.0",
    },
)
def nodo_tecnico(state: EstadoSoporte) -> EstadoSoporte:
    """
    Procesa consultas técnicas utilizando las herramientas disponibles.

    Si la consulta contiene un código de error HTTP, utiliza la herramienta
    de diagnóstico. En caso contrario, busca información en documentación.
    """

    tiempo_inicio = time.perf_counter()

    mensaje = state["mensaje_usuario"]

    codigo_error = extraer_codigo_error(mensaje)

    if codigo_error is not None:
        resultado = diagnosticar_error.invoke(codigo_error)

        state["herramientas_usadas"].append(
            "diagnosticar_error"
        )

        state["metadata"]["diagnostico"] = {
            "codigo_error": codigo_error,
            "resultado": resultado,
        }

    else:
        resultado = buscar_documentacion.invoke(mensaje)

        state["herramientas_usadas"].append(
            "buscar_documentacion"
        )

        state["metadata"]["documentacion"] = {
            "consulta": mensaje,
            "resultado": resultado,
        }

    state["contexto"].append(resultado)

    _registrar_duracion(
        state,
        "tecnico",
        tiempo_inicio,
    )

    return state

@traceable(
    name="nodo_escalar",
    tags=["nodo", "escalado"],
    metadata={
        "version_grafo": "1.0.0",
    },
)
def nodo_escalar(state: EstadoSoporte) -> EstadoSoporte:
    """
    Marca la consulta como pendiente de intervención humana.
    """

    tiempo_inicio = time.perf_counter()

    state["requiere_humano"] = True

    state["contexto"].append(
        "Esta consulta requiere la intervención de un agente humano."
    )

    _registrar_duracion(
        state,
        "escalar",
        tiempo_inicio,
    )

    return state

@traceable(
    name="generador_respuesta",
    tags=["nodo", "respuesta"],
    metadata={
        "version_grafo": "1.0.0",
    },
)
def generar_respuesta_final(state: EstadoSoporte) -> EstadoSoporte:
    """
    Genera una respuesta final utilizando el contexto acumulado.
    """

    tiempo_inicio = time.perf_counter()

    modelo = crear_modelo_clasificador()

    modelo_estructurado = modelo.with_structured_output(
        RespuestaFinal
    )

    contexto = "\n".join(state["contexto"])

    prompt = PROMPT_RESPUESTA_FINAL.format(
        mensaje_usuario=state["mensaje_usuario"],
        contexto=contexto,
    )

    resultado = modelo_estructurado.invoke(prompt)

    state["respuesta_final"] = resultado.respuesta

    _registrar_duracion(
        state,
        "generador_respuesta",
        tiempo_inicio,
    )

    return state