import os

from dotenv import load_dotenv


load_dotenv()


CATEGORIA_FAQ = "faq"
CATEGORIA_BUG = "bug"
CATEGORIA_TECNICO = "tecnico"
CATEGORIA_ESCALAR = "escalar"

CATEGORIAS_VALIDAS = {
    CATEGORIA_FAQ,
    CATEGORIA_BUG,
    CATEGORIA_TECNICO,
    CATEGORIA_ESCALAR,
}


OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")


if not OPENAI_API_KEY:
    raise RuntimeError(
        "No se ha encontrado OPENAI_API_KEY. "
        "Comprueba que existe un archivo .env en la raíz "
        "del proyecto y que contiene OPENAI_API_KEY."
    )