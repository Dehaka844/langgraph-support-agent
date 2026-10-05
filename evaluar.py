from ejecutar import ejecutar_consulta
from app.metricas import generar_resumen_metricas


CONSULTAS_PRUEBA = [
    "Como reseteo mi contrasena?",
    "La app crashea cuando abro el menu de configuracion",
    "Error 503 al conectar con el servidor",
    "Necesito hablar con alguien sobre mi facturacion",
    "Donde encuentro la documentacion de la API?",
]


def ejecutar_evaluacion():
    ejecuciones = []

    for numero, consulta in enumerate(CONSULTAS_PRUEBA, start=1):
        print("=" * 70)
        print(f"CONSULTA {numero}")
        print("=" * 70)
        print(consulta)

        resultado = ejecutar_consulta(consulta)

        ejecuciones.append(resultado)

        print(f"\nCategoría: {resultado['categoria']}")
        print(f"Herramientas: {resultado['herramientas_usadas']}")
        print(f"Requiere humano: {resultado['requiere_humano']}")
        print(f"Respuesta: {resultado['respuesta_final']}")

        print("\nDuración de los nodos:")
        for nodo, duracion in resultado["metadata"].get(
            "duraciones_nodos", {}
        ).items():
            print(f"  - {nodo}: {duracion:.4f} segundos")

        print(
            "\nTiempo total:",
            f"{resultado['metadata']['tiempo_total']:.4f} segundos",
        )

        print()

    resumen = generar_resumen_metricas(ejecuciones)

    print("=" * 70)
    print("RESUMEN DE MÉTRICAS")
    print("=" * 70)

    print("\nTiempo medio por nodo:")
    for nodo, tiempo in resumen["tiempo_medio_por_nodo"].items():
        print(f"  - {nodo}: {tiempo:.4f} segundos")

    print("\nDistribución de categorías:")
    for categoria, cantidad in resumen["distribucion_categorias"].items():
        print(f"  - {categoria}: {cantidad}")

    print(
        "\nTasa de escalado:",
        f"{resumen['tasa_escalado'] * 100:.2f}%",
    )

    print(
        "\nNodo más lento:",
        resumen["nodo_mas_lento"],
    )


if __name__ == "__main__":
    ejecutar_evaluacion()