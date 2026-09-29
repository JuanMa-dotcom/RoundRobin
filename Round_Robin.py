"""
Round Robin - Planificación de procesos
---------------------------------------
Simula el algoritmo de planificación Round Robin:
cada proceso usa la CPU como máximo un "quantum" de tiempo.
Si no termina en ese tiempo, regresa al final de la cola de listos
y espera su siguiente turno.

Al final muestra:
  - El diagrama de Gantt (qué proceso usó la CPU y en qué intervalo).
  - Tiempo de finalización, retorno y espera de cada proceso.
  - Los promedios de retorno y espera.
"""

from collections import deque  # Cola eficiente para la cola de listos


def round_robin(procesos, quantum):
    """
    Ejecuta la simulación de Round Robin.

    Parámetros:
        procesos (list): lista de tuplas (nombre, llegada, rafaga).
        quantum (int): tiempo máximo que un proceso puede usar la CPU por turno.

    Regresa:
        ps (list): lista de procesos (diccionarios) con su tiempo de fin calculado.
        gantt (list): lista de tuplas (nombre, inicio, fin) con cada uso de la CPU.
                      El nombre "-" indica que la CPU estuvo ociosa.
    """
    # Convertimos cada proceso en un diccionario y los ordenamos por llegada.
    # "resta" guarda cuánto tiempo de ráfaga le falta a cada proceso.
    ps = sorted(
        [{"nombre": n, "llegada": l, "rafaga": r, "resta": r} for n, l, r in procesos],
        key=lambda p: p["llegada"],
    )

    cola = deque()   # Cola de listos
    gantt = []       # Registro de la ejecución
    t = 0            # Reloj del sistema
    i = 0            # Índice del siguiente proceso que aún no ha llegado
    terminados = 0   # Contador de procesos terminados

    def admitir():
        """Mete a la cola todos los procesos que ya llegaron (llegada <= t)."""
        nonlocal i
        while i < len(ps) and ps[i]["llegada"] <= t:
            cola.append(ps[i])
            i += 1

    admitir()  # Procesos que llegan en t = 0

    # El ciclo sigue hasta que todos los procesos hayan terminado
    while terminados < len(ps):

        # Si no hay procesos listos, la CPU queda ociosa
        # hasta que llegue el siguiente proceso.
        if not cola:
            gantt.append(("-", t, ps[i]["llegada"]))
            t = ps[i]["llegada"]
            admitir()
            continue

        # Se toma el primer proceso de la cola
        p = cola.popleft()

        # Se ejecuta el quantum completo o solo lo que le falte si es menos
        corre = min(quantum, p["resta"])
        gantt.append((p["nombre"], t, t + corre))
        t += corre
        p["resta"] -= corre

        # Los procesos que llegaron mientras este se ejecutaba
        # entran a la cola ANTES de que el proceso actual regrese a ella.
        admitir()

        if p["resta"] > 0:
            # No terminó: vuelve al final de la cola
            cola.append(p)
        else:
            # Terminó: se guarda su tiempo de finalización
            p["fin"] = t
            terminados += 1

    return ps, gantt


def main():
    """Pide los datos al usuario, ejecuta la simulación y muestra los resultados."""

    # ----- Captura de datos -----
    n = int(input("Número de procesos: "))
    procesos = []
    for k in range(n):
        llegada = int(input(f"P{k+1} - tiempo de llegada: "))
        rafaga = int(input(f"P{k+1} - ráfaga de CPU: "))
        procesos.append((f"P{k+1}", llegada, rafaga))
    quantum = int(input("Quantum: "))

    # ----- Simulación -----
    ps, gantt = round_robin(procesos, quantum)

    # ----- Diagrama de Gantt -----
    print("\nDiagrama de Gantt:")
    print(" | ".join(f"{nom} [{a}-{b}]" for nom, a, b in gantt))

    # ----- Tabla de resultados -----
    # Retorno = fin - llegada   (tiempo total en el sistema)
    # Espera  = retorno - ráfaga (tiempo que pasó en la cola sin usar la CPU)
    print(f"\n{'Proceso':<8}{'Llegada':>8}{'Ráfaga':>8}{'Fin':>6}{'Retorno':>9}{'Espera':>8}")
    suma_ret = suma_esp = 0
    for p in sorted(ps, key=lambda x: x["nombre"]):
        ret = p["fin"] - p["llegada"]
        esp = ret - p["rafaga"]
        suma_ret += ret
        suma_esp += esp
        print(f"{p['nombre']:<8}{p['llegada']:>8}{p['rafaga']:>8}{p['fin']:>6}{ret:>9}{esp:>8}")

    # ----- Promedios -----
    print(f"\nRetorno promedio: {suma_ret / n:.2f}")
    print(f"Espera promedio:  {suma_esp / n:.2f}")


# Punto de entrada del programa
if __name__ == "__main__":
    main()