# Round Robin – Simulador de planificación de procesos

Programa en Python que simula el algoritmo de planificación de CPU **Round Robin** y muestra los resultados en la terminal.

## ¿Qué es Round Robin?

Round Robin es un algoritmo de planificación **apropiativo** que usan los sistemas operativos para repartir la CPU entre varios procesos de forma equitativa.

Cada proceso puede usar la CPU durante un tiempo máximo llamado **quantum**. Cuando se le acaba el quantum:

- Si el proceso **ya terminó**, sale del sistema.
- Si **no ha terminado**, regresa al **final de la cola de listos** y espera su siguiente turno.

Así ningún proceso acapara la CPU y todos avanzan poco a poco.

## Requisitos

- Python 3.8 o superior.
- No necesita librerías externas (solo usa `collections`, que viene con Python).

## Cómo ejecutarlo

```
python Round_Robin.py
```

El programa pide:

1. El número de procesos.
2. El tiempo de llegada y la ráfaga de CPU de cada proceso.
3. El quantum.

## Ejemplo

Entrada:

| Proceso | Llegada | Ráfaga |
|---------|---------|--------|
| P1      | 0       | 5      |
| P2      | 1       | 3      |
| P3      | 2       | 1      |
| P4      | 3       | 4      |

Quantum = 2

Salida:

```
Diagrama de Gantt:
P1 [0-2] | P2 [2-4] | P3 [4-5] | P1 [5-7] | P4 [7-9] | P2 [9-10] | P1 [10-11] | P4 [11-13]

Proceso  Llegada  Ráfaga   Fin  Retorno  Espera
P1             0       5    11       11       6
P2             1       3    10        9       6
P3             2       1     5        3       2
P4             3       4    13       10       6

Retorno promedio: 8.25
Espera promedio:  5.00
```

## Funcionamiento del algoritmo

1. Los procesos se ordenan por tiempo de llegada.
2. Los procesos que ya llegaron entran a la **cola de listos** (una `deque`).
3. Mientras queden procesos sin terminar:
   - Si la cola está vacía, la CPU queda **ociosa** hasta que llegue el siguiente proceso (se marca con `-` en el Gantt).
   - Se saca el primer proceso de la cola y se ejecuta durante `min(quantum, tiempo restante)`.
   - Se avanza el reloj y se descuenta ese tiempo de la ráfaga restante.
   - Los procesos que **llegaron durante la ejecución** entran a la cola **antes** de que el proceso actual regrese.
   - Si al proceso le falta tiempo, vuelve al final de la cola; si no, se registra su tiempo de fin.
4. Se calculan las métricas y se imprimen los resultados.

## Métricas calculadas

| Métrica | Fórmula | Significado |
|---------|---------|-------------|
| Fin | — | Instante en que el proceso termina. |
| Retorno | Fin − Llegada | Tiempo total que el proceso estuvo en el sistema. |
| Espera | Retorno − Ráfaga | Tiempo que pasó en la cola sin usar la CPU. |

También se muestran los promedios de retorno y espera.

## Estructura del código

- `round_robin(procesos, quantum)`: hace la simulación y regresa los procesos con su tiempo de fin y la lista del diagrama de Gantt.
- `admitir()`: función interna que mete a la cola los procesos cuya llegada ya ocurrió.
- `main()`: pide los datos, llama a la simulación e imprime el Gantt, la tabla y los promedios.

## Notas sobre el quantum

- **Quantum muy pequeño**: el reparto es más justo, pero hay muchos cambios de contexto.
- **Quantum muy grande**: Round Robin se comporta casi como FCFS (primero en llegar, primero en ser atendido).
