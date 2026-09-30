# metodo-biseccion
Implementación del método de bisección para encontrar raíces de funciones continuas

import math
import numpy as np
import matplotlib.pyplot as plt

def f(x):
    return x**3 - 7*x + 6

# ------------------------------------------------------------------
# 1) Datos del problema
# ------------------------------------------------------------------
a = 0.0
b = 1.5
eps = 1e-5

print("Función: f(x) = x^3 - 7x + 6")
print(f"Intervalo elegido: [{a}, {b}]")
print()

# Justificación del intervalo por cambio de signo
fa = f(a)
fb = f(b)

print("Justificación del intervalo:")
print(f"f({a}) = {fa}")
print(f"f({b}) = {fb}")

if fa == 0:
    print(f"La raíz es exactamente x = {a}")
    raise SystemExit
if fb == 0:
    print(f"La raíz es exactamente x = {b}")
    raise SystemExit

if fa * fb > 0:
    raise ValueError(
        "No hay cambio de signo en el intervalo dado. "
        "La hipótesis del teorema de Bolzano no se cumple."
    )

print("Como f(a) y f(b) tienen signos opuestos, por el teorema de Bolzano existe al menos una raíz en [a, b].")
print()
print("Además, la función se factoriza como:")
print("f(x) = x^3 - 7x + 6 = (x - 1)(x - 2)(x + 3)")
print("Por eso, la raíz en este intervalo es x = 1.")
print()

# Número de iteraciones estimado por la cota teórica
n_teorico = math.ceil(math.log2((b - a) / eps)) + 1
print(f"Máximo de iteraciones estimado por la cota teórica: {n_teorico}")
print()

# ------------------------------------------------------------------
# 2) Método de bisección
# ------------------------------------------------------------------
max_iter = 10000
iteraciones = []
contador = 0

while True:
    if contador >= max_iter:
        raise RuntimeError("Se excedió el número máximo de iteraciones permitidas.")

    m = (a + b) / 2.0
    fm = f(m)
    error = (b - a) / 2.0

    iteraciones.append({
        "iter": contador + 1,
        "a": a,
        "b": b,
        "m": m,
        "f(m)": fm,
        "error": error
    })

    # Criterio de paro:
    # si |f(m)| es muy pequeño o la amplitud del intervalo es menor que eps
    if abs(fm) < eps or error < eps:
        r = m
        break

    # Reducir intervalo según el signo
    if f(a) * fm <= 0:
        b = m
    else:
        a = m

    contador += 1

fr = f(r)

# ------------------------------------------------------------------
# 3) Impresión de resultados
# ------------------------------------------------------------------
print("Tabla de iteraciones:")
print(f"{'Iter':>5} | {'a':>12} | {'b':>12} | {'m':>12} | {'f(m)':>14} | {'error':>12}")
print("-" * 80)

for item in iteraciones:
    print(
        f"{item['iter']:>5} | "
        f"{item['a']:>12.8f} | "
        f"{item['b']:>12.8f} | "
        f"{item['m']:>12.8f} | "
        f"{item['f(m)']:>14.8f} | "
        f"{item['error']:>12.8e}"
    )

print()
print(f"Raíz aproximada r = {r:.10f}")
print(f"f(r) = {fr:.12e}")
print(f"Cantidad de iteraciones realizadas = {len(iteraciones)}")
print(f"Iteraciones requeridas por la cota teórica = {n_teorico}")

# ------------------------------------------------------------------
# 4) Gráfica de la función y la raíz
# ------------------------------------------------------------------
x = np.linspace(-4, 4, 1000)
y = f(x)

fig, ax = plt.subplots(figsize=(10, 6))

# Curva de la función
ax.plot(x, y, label=r"$f(x)=x^3-7x+6$", color="royalblue", linewidth=2.5)

# Eje x y eje y
ax.axhline(0, color="black", linewidth=1.0, alpha=0.8)
ax.axvline(0, color="black", linewidth=1.0, alpha=0.8)

# Sombreado del intervalo [a, b]
x_interval = np.linspace(a, b, 500)
y_interval = np.zeros_like(x_interval)
ax.fill_between(x_interval, y_interval, color="gray", alpha=0.15, label=f"Intervalo [{a}, {b}]")

# Raíz encontrada
ax.scatter(r, 0, color="red", s=80, zorder=5, label=f"Raíz ≈ {r:.8f}")
ax.axvline(r, color="red", linestyle="--", linewidth=1.2, alpha=0.8)

# Estética
ax.set_title("Gráfica de f(x) = x^3 - 7x + 6 y raíz encontrada", fontsize=14)
ax.set_xlabel("x", fontsize=12)
ax.set_ylabel("f(x)", fontsize=12)
ax.grid(True, linestyle="--", alpha=0.5)
ax.legend(loc="best")
plt.tight_layout()
plt.show()
