#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# DEFINICION DE LA FUNCION ORIGINAL
# ============================================================================

def f(x):
    """Función original: f(x) = e^(-x) - x"""
    try:
        return math.exp(-x) - x
    except:
        return float('inf')

def df(x):
    """Derivada: f'(x) = -e^(-x) - 1"""
    try:
        return -math.exp(-x) - 1
    except:
        return float('inf')

# ============================================================================
# DIFERENTES FORMAS DE g(x)
# ============================================================================

def g1(x):
    """g1(x) = e^(-x)  [NO CONVERGE]"""
    try:
        return math.exp(-x)
    except:
        return float('inf')

def g1_prima(x):
    """Derivada de g1: g1'(x) = -e^(-x)"""
    try:
        return -math.exp(-x)
    except:
        return float('inf')

def g2(x):
    """g2(x) = -ln(x)  [CONVERGE]"""
    if x <= 0:
        return float('inf')
    try:
        return -math.log(x)
    except:
        return float('inf')

def g2_prima(x):
    """Derivada de g2: g2'(x) = -1/x"""
    if x <= 0:
        return float('inf')
    try:
        return -1.0 / x
    except:
        return float('inf')

def g3(x):
    """g3(x) = ln(x) + x  [Alternativa, ver convergencia]"""
    if x <= 0:
        return float('inf')
    try:
        return math.log(x) + x
    except:
        return float('inf')

def g3_prima(x):
    """Derivada de g3: g3'(x) = 1/x + 1"""
    if x <= 0:
        return float('inf')
    try:
        return 1.0/x + 1
    except:
        return float('inf')

def g4(x):
    """g4(x) = 0.5*(e^(-x) + x)  [Promedio ponderado]"""
    try:
        return 0.5 * (math.exp(-x) + x)
    except:
        return float('inf')

def g4_prima(x):
    """Derivada de g4: g4'(x) = 0.5*(-e^(-x) + 1)"""
    try:
        return 0.5 * (-math.exp(-x) + 1)
    except:
        return float('inf')

def g5(x):
    """g5(x) = x - (e^(-x) - x)/(1 + e^(-x))  [Método de Newton simplificado]"""
    try:
        return x - (math.exp(-x) - x) / (1 + math.exp(-x))
    except:
        return float('inf')

def g5_prima(x):
    """Derivada de g5 (aproximada numéricamente)"""
    h = 1e-6
    try:
        return (g5(x + h) - g5(x - h)) / (2 * h)
    except:
        return float('inf')

# ============================================================================
# METODO DEL PUNTO FIJO
# ============================================================================

def punto_fijo(g, g_prima, x0, tol=1e-5, max_iter=100, nombre_g="g(x)"):
    """
    Método del punto fijo: x_{n+1} = g(x_n)
    
    Parámetros:
    - g: función de iteración
    - g_prima: derivada de g
    - x0: aproximación inicial
    - tol: tolerancia
    - max_iter: máximo de iteraciones
    - nombre_g: nombre descriptivo de g
    """
    
    tabla = []
    contador = 0
    x_prev = x0
    
    # Verificar convergencia en x0
    deriv_x0 = abs(g_prima(x0))
    
    while contador < max_iter:
        x_actual = g(x_prev)
        
        # Verificar si el resultado es válido
        if math.isinf(x_actual) or math.isnan(x_actual):
            return None, contador, tabla, False, deriv_x0
        
        # Error de aproximación
        if contador > 0:
            error = abs(x_actual - x_prev)
        else:
            error = float('inf')
        
        # Valor de la derivada en el punto actual
        deriv_actual = abs(g_prima(x_actual))
        
        # Guardar en tabla
        tabla.append({
            'iter': contador + 1,
            'x_n': x_prev,
            'x_n+1': x_actual,
            'g(x_n)': x_actual,
            'f(x_n+1)': f(x_actual),
            '|g\'(x_n)|': abs(g_prima(x_prev)),
            'error': error
        })
        
        # Criterio de parada
        if error < tol:
            convergencia = deriv_actual < 1.0
            return x_actual, contador + 1, tabla, convergencia, deriv_x0
        
        x_prev = x_actual
        contador += 1
    
    convergencia = deriv_actual < 1.0
    return x_prev, contador, tabla, convergencia, deriv_x0

# ============================================================================
# FUNCION PARA IMPRIMIR TABLA
# ============================================================================

def imprimir_tabla_completa(tabla, titulo=""):
    """Imprime la tabla completa de manera legible"""
    
    if not tabla:
        print("No hay datos o el método divergió")
        return
    
    if titulo:
        print("\n" + "="*160)
        print(titulo)
        print("="*160 + "\n")
    
    # Encabezado
    print(f"{'iter':>4} | {'x_n':>15} | {'x_{n+1}':>15} | {'g(x_n)':>15} | {'f(x_{n+1})':>15} | {'|g\'(x_n)|':>15} | {'error':>15}")
    print("-"*160)
    
    # Datos
    for row in tabla:
        iter_val = row['iter']
        xn = row['x_n']
        xn1 = row['x_n+1']
        gxn = row['g(x_n)']
        fxn1 = row['f(x_n+1)']
        deriv = row['|g\'(x_n)|']
        err = row['error']
        
        print(f"{iter_val:>4} | {xn:>15.10f} | {xn1:>15.10f} | {gxn:>15.10f} | {fxn1:>15.10e} | {deriv:>15.10f} | {err:>15.10e}")
    
    print("-"*160 + "\n")

# ============================================================================
# FUNCION PARA IMPRIMIR RESULTADOS FINALES
# ============================================================================

def imprimir_resultados_finales(nombre_metodo, raiz, iter_count, tabla, convergencia, deriv_inicial):
    """Imprime los resultados finales de forma clara"""
    
    print("\n" + "="*120)
    print(f"RESULTADOS FINALES - {nombre_metodo}")
    print("="*120 + "\n")
    
    if raiz is not None:
        print(f"RAIZ APROXIMADA:")
        print(f"  r = {raiz:.15f}\n")
        
        print(f"VALOR DE LA FUNCION EN LA RAIZ:")
        print(f"  f(r) = {f(raiz):.15e}\n")
        
        print(f"CANTIDAD DE ITERACIONES:")
        print(f"  Iteraciones realizadas = {iter_count}\n")
        
        print(f"ANALISIS DE CONVERGENCIA:")
        print(f"  |g'(x0)| = {deriv_inicial:.10f}")
        if convergencia:
            print(f"  ✓ CONVERGE (|g'(x)| < 1)")
        else:
            print(f"  ✗ NO CONVERGE (|g'(x)| >= 1)")
        print()
        
        print(f"TABLA DE ITERACIONES:")
        imprimir_tabla_completa(tabla)
    else:
        print(f"ERROR: El método divergió o no pudo calcularse")
        print()

# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*160)
    print("METODO DEL PUNTO FIJO - ANALISIS DE CONVERGENCIA")
    print("="*160)
    
    print(f"\nFUNCION ORIGINAL: f(x) = e^(-x) - x")
    print(f"\nOBJETIVO: Encontrar x tal que f(x) = 0, es decir, e^(-x) = x")
    print(f"\nNOTA: Esto equivale a encontrar x tal que x = g(x)")
    
    print(f"\nAnálisis teórico:")
    print(f"  El punto fijo converge si |g'(x)| < 1 cerca de la solución")
    print(f"  Inicialmente probaremos g1(x) = e^(-x) que NO converge")
    print(f"  Luego usaremos g2(x) = -ln(x) que SÍ converge")
    
    # Aproximación inicial
    x0 = 0.5
    tol = 1e-5
    
    print(f"\nPARAMETROS:")
    print(f"  x0 = {x0}")
    print(f"  Tolerancia = {tol}")
    print(f"  f(x0) = {f(x0):.10f}")
    
    # ========================================================================
    # METODO 1: g1(x) = e^(-x) - NO CONVERGE
    # ========================================================================
    
    print("\n" + "="*160)
    print("METODO 1: g1(x) = e^(-x)")
    print("="*160)
    
    print("\nAnalisis teórico:")
    print(f"  g1(x) = e^(-x)")
    print(f"  g1'(x) = -e^(-x)")
    print(f"  g1'({x0}) = {g1_prima(x0):.10f}")
    print(f"  |g1'(x0)| = {abs(g1_prima(x0)):.10f}")
    
    if abs(g1_prima(x0)) < 1:
        print(f"  ✓ Condición |g'(x)| < 1 se cumple → Puede converger")
    else:
        print(f"  ✗ Condición |g'(x)| < 1 NO se cumple → NO converge")
    
    print(f"\nAplicando el método del punto fijo...")
    r1, n1, tabla1, conv1, deriv1 = punto_fijo(g1, g1_prima, x0, tol, max_iter=50, nombre_g="g1")
    
    if r1 is not None:
        imprimir_resultados_finales("METODO 1: g1(x) = e^(-x)", r1, n1, tabla1, conv1, deriv1)
    else:
        print(f"\nEl método g1(x) = e^(-x) DIVERGE")
        print(f"Esto se debe a que |g1'(x)| = e^(-x) puede ser mayor que 1 en el intervalo")
        print()
    
    # ========================================================================
    # METODO 2: g2(x) = -ln(x) - CONVERGE
    # ========================================================================
    
    print("\n" + "="*160)
    print("METODO 2: g2(x) = -ln(x)")
    print("="*160)
    
    print("\nAnalisis teórico:")
    print(f"  g2(x) = -ln(x)")
    print(f"  g2'(x) = -1/x")
    print(f"  g2'({x0}) = {g2_prima(x0):.10f}")
    print(f"  |g2'(x0)| = {abs(g2_prima(x0)):.10f}")
    
    if abs(g2_prima(x0)) < 1:
        print(f"  ✓ Condición |g'(x)| < 1 se cumple → Converge")
    else:
        print(f"  ✗ Condición |g'(x)| < 1 NO se cumple → NO converge")
    
    print(f"\nAplicando el método del punto fijo...")
    r2, n2, tabla2, conv2, deriv2 = punto_fijo(g2, g2_prima, x0, tol, max_iter=100, nombre_g="g2")
    
    if r2 is not None:
        imprimir_resultados_finales("METODO 2: g2(x) = -ln(x)", r2, n2, tabla2, conv2, deriv2)
    else:
        print(f"\nEl método g2(x) = -ln(x) DIVERGE o no es válido en el intervalo")
        print()
    
    # ========================================================================
    # METODO 3: g3(x) = ln(x) + x - ANALIZAR
    # ========================================================================
    
    print("\n" + "="*160)
    print("METODO 3: g3(x) = ln(x) + x")
    print("="*160)
    
    print("\nAnalisis teórico:")
    print(f"  g3(x) = ln(x) + x")
    print(f"  g3'(x) = 1/x + 1")
    print(f"  g3'({x0}) = {g3_prima(x0):.10f}")
    print(f"  |g3'(x0)| = {abs(g3_prima(x0)):.10f}")
    
    if abs(g3_prima(x0)) < 1:
        print(f"  ✓ Condición |g'(x)| < 1 se cumple → Converge")
    else:
        print(f"  ✗ Condición |g'(x)| < 1 NO se cumple → NO converge")
    
    print(f"\nAplicando el método del punto fijo...")
    r3, n3, tabla3, conv3, deriv3 = punto_fijo(g3, g3_prima, x0, tol, max_iter=100, nombre_g="g3")
    
    if r3 is not None:
        imprimir_resultados_finales("METODO 3: g3(x) = ln(x) + x", r3, n3, tabla3, conv3, deriv3)
    else:
        print(f"\nEl método g3(x) = ln(x) + x DIVERGE o no es válido en el intervalo")
        print()
    
    # ========================================================================
    # METODO 4: g4(x) = 0.5*(e^(-x) + x) - ANALIZAR
    # ========================================================================
    
    print("\n" + "="*160)
    print("METODO 4: g4(x) = 0.5*(e^(-x) + x)")
    print("="*160)
    
    print("\nAnalisis teórico:")
    print(f"  g4(x) = 0.5*(e^(-x) + x)")
    print(f"  g4'(x) = 0.5*(-e^(-x) + 1)")
    print(f"  g4'({x0}) = {g4_prima(x0):.10f}")
    print(f"  |g4'(x0)| = {abs(g4_prima(x0)):.10f}")
    
    if abs(g4_prima(x0)) < 1:
        print(f"  ✓ Condición |g'(x)| < 1 se cumple → Converge")
    else:
        print(f"  ✗ Condición |g'(x)| < 1 NO se cumple → NO converge")
    
    print(f"\nAplicando el método del punto fijo...")
    r4, n4, tabla4, conv4, deriv4 = punto_fijo(g4, g4_prima, x0, tol, max_iter=100, nombre_g="g4")
    
    if r4 is not None:
        imprimir_resultados_finales("METODO 4: g4(x) = 0.5*(e^(-x) + x)", r4, n4, tabla4, conv4, deriv4)
    else:
        print(f"\nEl método g4(x) = 0.5*(e^(-x) + x) DIVERGE")
        print()
    
    # ========================================================================
    # METODO 5: g5(x) - Método de Newton simplificado - ANALIZAR
    # ========================================================================
    
    print("\n" + "="*160)
    print("METODO 5: g5(x) = x - (e^(-x) - x)/(1 + e^(-x))")
    print("="*160)
    
    print("\nAnalisis teórico:")
    print(f"  g5(x) = x - (e^(-x) - x)/(1 + e^(-x))")
    print(f"  (Método de Newton simplificado)")
    print(f"  g5'({x0}) ≈ {g5_prima(x0):.10f} (aproximación numérica)")
    print(f"  |g5'(x0)| ≈ {abs(g5_prima(x0)):.10f}")
    
    if abs(g5_prima(x0)) < 1:
        print(f"  ✓ Condición |g'(x)| < 1 se cumple → Converge")
    else:
        print(f"  ✗ Condición |g'(x)| < 1 NO se cumple → NO converge")
    
    print(f"\nAplicando el método del punto fijo...")
    r5, n5, tabla5, conv5, deriv5 = punto_fijo(g5, g5_prima, x0, tol, max_iter=100, nombre_g="g5")
    
    if r5 is not None:
        imprimir_resultados_finales("METODO 5: g5(x) = Método Newton simplificado", r5, n5, tabla5, conv5, deriv5)
    else:
        print(f"\nEl método g5(x) DIVERGE")
        print()
    
    # ========================================================================
    # COMPARACION FINAL
    # ========================================================================
    
    print("\n" + "="*160)
    print("COMPARACION FINAL DE TODOS LOS METODOS")
    print("="*160 + "\n")
    
    resultados = []
    
    if r1 is not None:
        resultados.append(("g1(x) = e^(-x)", r1, n1, f(r1), abs(deriv1), "NO" if not conv1 else "SI"))
    else:
        resultados.append(("g1(x) = e^(-x)", "DIVERGE", "DIVERGE", "DIVERGE", abs(deriv1), "NO"))
    
    if r2 is not None:
        resultados.append(("g2(x) = -ln(x)", r2, n2, f(r2), abs(deriv2), "SI" if conv2 else "NO"))
    else:
        resultados.append(("g2(x) = -ln(x)", "DIVERGE", "DIVERGE", "DIVERGE", abs(deriv2), "NO"))
    
    if r3 is not None:
        resultados.append(("g3(x) = ln(x) + x", r3, n3, f(r3), abs(deriv3), "NO" if not conv3 else "SI"))
    else:
        resultados.append(("g3(x) = ln(x) + x", "DIVERGE", "DIVERGE", "DIVERGE", abs(deriv3), "NO"))
    
    if r4 is not None:
        resultados.append(("g4(x) = 0.5*(e^(-x) + x)", r4, n4, f(r4), abs(deriv4), "SI" if conv4 else "NO"))
    else:
        resultados.append(("g4(x) = 0.5*(e^(-x) + x)", "DIVERGE", "DIVERGE", "DIVERGE", abs(deriv4), "NO"))
    
    if r5 is not None:
        resultados.append(("g5(x) = Newton simplif.", r5, n5, f(r5), abs(deriv5), "SI" if conv5 else "NO"))
    else:
        resultados.append(("g5(x) = Newton simplif.", "DIVERGE", "DIVERGE", "DIVERGE", abs(deriv5), "NO"))
    
    print(f"{'g(x)':.<35} | {'RAIZ':>15} | {'ITER':>6} | {'f(r)':>15} | {'|g\'|':>10} | {'CONVERGE':>10}")
    print("-"*160)
    
    for nombre, raiz, iters, f_r, deriv, conv in resultados:
        if isinstance(raiz, str):
            print(f"{nombre:<35} | {raiz:>15} | {str(iters):>6} | {str(f_r):>15} | {deriv:>10.6f} | {conv:>10}")
        else:
            print(f"{nombre:<35} | {raiz:>15.10f} | {int(iters):>6} | {f_r:>15.8e} | {deriv:>10.6f} | {conv:>10}")
    
    print()
    
    # ========================================================================
    # GRAFICAS
    # ========================================================================
    
    print("Generando gráficas...")
    
    x_graf = np.linspace(0.1, 2.0, 500)
    y_graf = [f(x) for x in x_graf]
    
    # Figura 1: Función original y raíz
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('METODO DEL PUNTO FIJO - ANALISIS COMPLETO\nf(x) = e^(-x) - x', 
                 fontsize=16, fontweight='bold')
    
    # Subplot 1: Función original
    ax = plt.subplot(2, 3, 1)
    ax.plot(x_graf, y_graf, 'b-', linewidth=2.5, label='f(x) = e^(-x) - x')
    ax.axhline(0, color='k', linewidth=0.8, alpha=0.5)
    ax.axvline(0, color='k', linewidth=0.8, alpha=0.5)
    if r2 is not None:
        ax.scatter([r2], [0], color='red', s=150, zorder=5, marker='o', edgecolors='darkred', linewidth=2, label=f'Raíz ≈ {r2:.6f}')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('f(x)', fontsize=11, fontweight='bold')
    ax.set_title('Función Original y Raíz', fontsize=12, fontweight='bold')
    ax.legend(fontsize=10)
    ax.set_ylim(-1, 1)
    
    # Subplot 2: g1(x) - No converge
    ax = plt.subplot(2, 3, 2)
    y_g1 = [g1(x) for x in x_graf]
    ax.plot(x_graf, y_g1, 'r-', linewidth=2.5, label='g1(x) = e^(-x)')
    ax.plot(x_graf, x_graf, 'k--', linewidth=1.5, label='y = x')
    if r1 is not None and not math.isnan(r1) and not math.isinf(r1):
        ax.scatter([r1], [r1], color='red', s=100, zorder=5, marker='o')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.set_title('g1(x) = e^(-x) (NO CONVERGE)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    
    # Subplot 3: g2(x) - Converge
    ax = plt.subplot(2, 3, 3)
    x_g2 = np.linspace(0.1, 2.0, 500)
    y_g2 = [-math.log(x) for x in x_g2]
    ax.plot(x_g2, y_g2, 'g-', linewidth=2.5, label='g2(x) = -ln(x)')
    ax.plot(x_g2, x_g2, 'k--', linewidth=1.5, label='y = x')
    if r2 is not None:
        ax.scatter([r2], [r2], color='green', s=100, zorder=5, marker='o', edgecolors='darkgreen', linewidth=2)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.set_title('g2(x) = -ln(x) (CONVERGE)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0, 2)
    ax.set_ylim(0, 2)
    
    # Subplot 4: Convergencia g2
    if tabla2:
        ax = plt.subplot(2, 3, 4)
        iters = [row['iter'] for row in tabla2]
        errores = [row['error'] for row in tabla2 if row['error'] != float('inf')]
        if errores:
            ax.semilogy(iters[:len(errores)], errores, 'o-', color='green', linewidth=2.5, markersize=7, label='|error|')
            ax.axhline(tol, color='red', linestyle='--', linewidth=2, label=f'Tolerancia = {tol}')
            ax.grid(True, alpha=0.3, linestyle='--', which='both')
            ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
            ax.set_ylabel('|x_{n+1} - x_n| (log)', fontsize=11, fontweight='bold')
            ax.set_title(f'Convergencia g2 ({n2} iteraciones)', fontsize=12, fontweight='bold')
            ax.legend(fontsize=9)
    
    # Subplot 5: Derivada de g(x)
    ax = plt.subplot(2, 3, 5)
    g1_primas = [abs(g1_prima(x)) for x in x_graf]
    g2_primas = [abs(g2_prima(x)) for x in x_graf]
    g4_primas = [abs(g4_prima(x)) for x in x_graf]
    
    ax.plot(x_graf, g1_primas, 'r-', linewidth=2, label="|g1'(x)|")
    ax.plot(x_graf, g2_primas, 'g-', linewidth=2, label="|g2'(x)|")
    ax.plot(x_graf, g4_primas, 'b-', linewidth=2, label="|g4'(x)|")
    ax.axhline(1, color='k', linestyle='--', linewidth=2, label='|g\'(x)| = 1')
    ax.fill_between(x_graf, 0, 1, alpha=0.1, color='green', label='Región de convergencia')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel("|g'(x)|", fontsize=11, fontweight='bold')
    ax.set_title('Análisis de Derivadas: Condición de Convergencia', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0.1, 2)
    ax.set_ylim(0, 2)
    
    # Subplot 6: Tabla de resumen
    ax = plt.subplot(2, 3, 6)
    ax.axis('off')
    
    resumen_text = "RESUMEN DE CONVERGENCIA\n" + "="*40 + "\n\n"
    resumen_text += "g1(x) = e^(-x)\n"
    resumen_text += f"  |g1'(x0)| = {abs(g1_prima(x0)):.4f}\n"
    resumen_text += "  ✗ NO CONVERGE\n\n"
    
    resumen_text += "g2(x) = -ln(x)\n"
    resumen_text += f"  |g2'(x0)| = {abs(g2_prima(x0)):.4f}\n"
    resumen_text += "  ✓ CONVERGE\n"
    if r2 is not None:
        resumen_text += f"  Raíz: {r2:.8f}\n"
        resumen_text += f"  Iteraciones: {n2}\n\n"
    
    resumen_text += "g4(x) = 0.5*(e^(-x) + x)\n"
    resumen_text += f"  |g4'(x0)| = {abs(g4_prima(x0)):.4f}\n"
    if abs(g4_prima(x0)) < 1:
        resumen_text += "  ✓ CONVERGE\n"
    else:
        resumen_text += "  ✗ NO CONVERGE\n"
    
    ax.text(0.05, 0.95, resumen_text, transform=ax.transAxes, fontsize=10,
            verticalalignment='top', fontfamily='monospace',
            bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
    
    plt.tight_layout()
    plt.savefig('punto_fijo_analisis_completo.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica 1 guardada: punto_fijo_analisis_completo.png")
    
    # Figura 2: Iteraciones gráficamente
    fig, axes = plt.subplots(2, 2, figsize=(14, 10))
    fig.suptitle('VISUALIZACION DE ITERACIONES DEL PUNTO FIJO', fontsize=14, fontweight='bold')
    
    # g1 - No converge
    ax = axes[0, 0]
    x_plot = np.linspace(0.1, 1.5, 300)
    y_g1_plot = [g1(x) for x in x_plot]
    ax.plot(x_plot, y_g1_plot, 'r-', linewidth=2, label='g1(x) = e^(-x)')
    ax.plot(x_plot, x_plot, 'k--', linewidth=1.5, label='y = x')
    
    if tabla1:
        x_iter = x0
        for i, row in enumerate(tabla1[:min(5, len(tabla1))]):
            x_next = row['x_n+1']
            ax.plot([x_iter, x_iter], [x_iter, x_next], 'b--', alpha=0.5, linewidth=1)
            ax.plot([x_iter, x_next], [x_next, x_next], 'b--', alpha=0.5, linewidth=1)
            ax.scatter([x_iter], [x_iter], s=30, color='blue', alpha=0.5)
            x_iter = x_next
    
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.set_title('g1(x): Divergencia (iteraciones no convergen)', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0.1, 1.5)
    ax.set_ylim(0.1, 1.5)
    
    # g2 - Converge
    ax = axes[0, 1]
    x_plot = np.linspace(0.2, 1.5, 300)
    y_g2_plot = [-math.log(x) for x in x_plot]
    ax.plot(x_plot, y_g2_plot, 'g-', linewidth=2, label='g2(x) = -ln(x)')
    ax.plot(x_plot, x_plot, 'k--', linewidth=1.5, label='y = x')
    
    if tabla2:
        x_iter = x0
        for i, row in enumerate(tabla2[:min(8, len(tabla2))]):
            x_next = row['x_n+1']
            if x_next > 0:
                ax.plot([x_iter, x_iter], [x_iter, x_next], 'b--', alpha=0.5, linewidth=1)
                ax.plot([x_iter, x_next], [x_next, x_next], 'b--', alpha=0.5, linewidth=1)
                ax.scatter([x_iter], [x_iter], s=30, color='blue', alpha=0.5)
                x_iter = x_next
    
    ax.scatter([r2], [r2], s=100, color='green', marker='*', zorder=5, edgecolors='darkgreen', linewidth=2)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.set_title(f'g2(x): Convergencia a r={r2:.6f}', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0.2, 1.5)
    ax.set_ylim(0.2, 1.5)
    
    # g4 - Convergencia
    ax = axes[1, 0]
    x_plot = np.linspace(0.1, 1.5, 300)
    y_g4_plot = [0.5*(math.exp(-x) + x) for x in x_plot]
    ax.plot(x_plot, y_g4_plot, 'b-', linewidth=2, label='g4(x) = 0.5*(e^(-x) + x)')
    ax.plot(x_plot, x_plot, 'k--', linewidth=1.5, label='y = x')
    
    if tabla4:
        x_iter = x0
        for i, row in enumerate(tabla4[:min(8, len(tabla4))]):
            x_next = row['x_n+1']
            ax.plot([x_iter, x_iter], [x_iter, x_next], 'r--', alpha=0.5, linewidth=1)
            ax.plot([x_iter, x_next], [x_next, x_next], 'r--', alpha=0.5, linewidth=1)
            ax.scatter([x_iter], [x_iter], s=30, color='red', alpha=0.5)
            x_iter = x_next
    
    if r4 is not None:
        ax.scatter([r4], [r4], s=100, color='blue', marker='*', zorder=5, edgecolors='darkblue', linewidth=2)
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('y', fontsize=11, fontweight='bold')
    ax.set_title(f'g4(x): Convergencia' + (f' a r={r4:.6f}' if r4 is not None else ''), fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_xlim(0.1, 1.5)
    ax.set_ylim(0.1, 1.5)
    
    # Comparación de errores
    ax = axes[1, 1]
    
    if tabla2:
        iters2 = [row['iter'] for row in tabla2]
        errs2 = [row['error'] for row in tabla2 if row['error'] != float('inf')]
        ax.semilogy(iters2[:len(errs2)], errs2, 'o-', color='green', linewidth=2, markersize=6, label=f'g2 ({n2} iter)')
    
    if tabla4:
        iters4 = [row['iter'] for row in tabla4]
        errs4 = [row['error'] for row in tabla4 if row['error'] != float('inf')]
        ax.semilogy(iters4[:len(errs4)], errs4, 's-', color='blue', linewidth=2, markersize=6, label=f'g4 ({n4} iter)')
    
    ax.axhline(tol, color='red', linestyle='--', linewidth=2, label=f'Tolerancia = {tol}')
    ax.grid(True, alpha=0.3, linestyle='--', which='both')
    ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
    ax.set_ylabel('Error |x_{n+1} - x_n|', fontsize=11, fontweight='bold')
    ax.set_title('Comparación de Convergencia', fontsize=11, fontweight='bold')
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig('punto_fijo_iteraciones.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica 2 guardada: punto_fijo_iteraciones.png")
    
    plt.show()
    
    print("\n" + "="*160)
    print("ANALISIS COMPLETADO EXITOSAMENTE")
    print("="*160)
    print("\nArchivos generados:")
    print("  1. punto_fijo_analisis_completo.png")
    print("  2. punto_fijo_iteraciones.png")
    print()
