from collections import deque


def round_robin(procesos, quantum):
    ps = sorted(
        [{"nombre": n, "llegada": l, "rafaga": r, "resta": r} for n, l, r in procesos],
        key=lambda p: p["llegada"],
    )
    cola, gantt = deque(), []
    t, i, terminados = 0, 0, 0

    def admitir():
        nonlocal i
        while i < len(ps) and ps[i]["llegada"] <= t:
            cola.append(ps[i])
            i += 1

    admitir()
    while terminados < len(ps):
        if not cola:
            gantt.append(("-", t, ps[i]["llegada"]))
            t = ps[i]["llegada"]
            admitir()
            continue

        p = cola.popleft()
        corre = min(quantum, p["resta"])
        gantt.append((p["nombre"], t, t + corre))
        t += corre
        p["resta"] -= corre

        admitir()
        if p["resta"] > 0:
            cola.append(p)
        else:
            p["fin"] = t
            terminados += 1

    return ps, gantt


def main():
    n = int(input("Número de procesos: "))
    procesos = []
    for k in range(n):
        llegada = int(input(f"P{k+1} - tiempo de llegada: "))
        rafaga = int(input(f"P{k+1} - ráfaga de CPU: "))
        procesos.append((f"P{k+1}", llegada, rafaga))
    quantum = int(input("Quantum: "))

    ps, gantt = round_robin(procesos, quantum)

    print("\nDiagrama de Gantt:")
    print(" | ".join(f"{nom} [{a}-{b}]" for nom, a, b in gantt))

    print(f"\n{'Proceso':<8}{'Llegada':>8}{'Ráfaga':>8}{'Fin':>6}{'Retorno':>9}{'Espera':>8}")
    suma_ret = suma_esp = 0
    for p in sorted(ps, key=lambda x: x["nombre"]):
        ret = p["fin"] - p["llegada"]
        esp = ret - p["rafaga"]
        suma_ret += ret
        suma_esp += esp
        print(f"{p['nombre']:<8}{p['llegada']:>8}{p['rafaga']:>8}{p['fin']:>6}{ret:>9}{esp:>8}")

    print(f"\nRetorno promedio: {suma_ret / n:.2f}")
    print(f"Espera promedio:  {suma_esp / n:.2f}")


if __name__ == "__main__":
    main()