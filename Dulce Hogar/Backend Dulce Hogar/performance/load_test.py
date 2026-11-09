
import argparse
import statistics
import time
from concurrent.futures import ThreadPoolExecutor, as_completed

import httpx
import psutil


URL = "http://127.0.0.1:8001/graphql"

CONSULTA = {
    "query": """
        query {
            producto(productId: 1) {
                id
                nombre
                precio
                disponible
            }
        }
    """
}


def enviar_solicitud():
    inicio = time.perf_counter()

    try:
        respuesta = httpx.post(
            URL,
            json=CONSULTA,
            timeout=10.0
        )

        datos = respuesta.json()

        correcta = (
            respuesta.status_code == 200
            and not datos.get("errors")
            and datos.get("data", {}).get("producto") is not None
        )

    except (httpx.RequestError, ValueError):
        correcta = False

    duracion = (time.perf_counter() - inicio) * 1000

    return duracion, correcta


def ejecutar_prueba(solicitudes, concurrencia):
    proceso = psutil.Process()
    cpu_inicial = proceso.cpu_times()
    memoria_inicial = proceso.memory_info().rss

    latencias = []
    errores = 0

    inicio = time.perf_counter()

    with ThreadPoolExecutor(max_workers=concurrencia) as executor:
        tareas = [
            executor.submit(enviar_solicitud)
            for _ in range(solicitudes)
        ]

        for tarea in as_completed(tareas):
            latencia, correcta = tarea.result()
            latencias.append(latencia)

            if not correcta:
                errores += 1

    tiempo_total = time.perf_counter() - inicio

    cpu_final = proceso.cpu_times()
    memoria_final = proceso.memory_info().rss

    latencias.sort()
    indice_p95 = max(
        0,
        int(len(latencias) * 0.95 + 0.999999) - 1
    )

    print("\n=== RESULTADOS DE RENDIMIENTO ===")
    print(f"Solicitudes: {solicitudes}")
    print(f"Concurrencia: {concurrencia}")
    print(f"Tiempo total: {tiempo_total:.3f} s")
    print(f"Latencia promedio: {statistics.mean(latencias):.2f} ms")
    print(f"Latencia p95: {latencias[indice_p95]:.2f} ms")
    print(f"Rendimiento: {solicitudes / tiempo_total:.2f} solicitudes/s")
    print(f"Errores: {errores}")
    print(f"Tasa de errores: {errores / solicitudes * 100:.2f}%")
    print(
        "CPU del proceso de prueba: "
        f"{(cpu_final.user + cpu_final.system - cpu_inicial.user - cpu_inicial.system):.3f} s"
    )
    print(
        "Memoria del proceso de prueba: "
        f"{memoria_inicial / 1024**2:.2f} MB -> "
        f"{memoria_final / 1024**2:.2f} MB"
    )


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--requests",
        type=int,
        default=50
    )
    parser.add_argument(
        "--concurrency",
        type=int,
        default=5
    )

    args = parser.parse_args()

    if args.requests < 1 or args.concurrency < 1:
        parser.error("Los valores deben ser mayores que cero")

    ejecutar_prueba(args.requests, args.concurrency)
