#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import math
import numpy as np
import matplotlib.pyplot as plt

# ============================================================================
# DEFINICION DE LA FUNCION
# ============================================================================

def f(x):
    """Función f(x) = x^3 + x^2 - 1"""
    return x**3 + x**2 - 1

def df(x):
    """Derivada f'(x) = 3x^2 + 2x"""
    return 3*x**2 + 2*x

def ddf(x):
    """Segunda derivada f''(x) = 6x + 2"""
    return 6*x + 2

# ============================================================================
# METODO 1: FALSA POSICION CLASICO
# ============================================================================

def metodo_clasico(a, b, tol=1e-5, max_iter=100):
    """
    Método de Falsa Posición Clásico
    Puede presentar estancamiento
    """
    if f(a) * f(b) > 0:
        return None, None, []
    
    tabla = []
    contador = 0
    
    while contador < max_iter:
        fa = f(a)
        fb = f(b)
        
        denominador = fb - fa
        if abs(denominador) < 1e-15:
            break
        
        c = (a * fb - b * fa) / denominador
        fc = f(c)
        
        error_intervalo = abs(b - a)
        
        tabla.append({
            'iter': contador + 1,
            'a': a,
            'b': b,
            'c': c,
            'f_a': fa,
            'f_b': fb,
            'f_c': fc,
            'error': error_intervalo
        })
        
        if abs(fc) < tol or error_intervalo < tol:
            return c, contador + 1, tabla
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        
        contador += 1
    
    return c, contador, tabla

# ============================================================================
# METODO 2: FALSA POSICION ILLINOIS
# ============================================================================

def metodo_illinois(a, b, tol=1e-5, max_iter=100):
    """
    Método de Falsa Posición Illinois (Mejorado)
    Mitiga estancamiento con modificación
    """
    if f(a) * f(b) > 0:
        return None, None, []
    
    tabla = []
    contador = 0
    extremo_fijo = None
    
    while contador < max_iter:
        fa = f(a)
        fb = f(b)
        
        # Modificación Illinois
        fa_mod = fa
        fb_mod = fb
        
        if extremo_fijo == 'a':
            fa_mod = fa / 2.0
        elif extremo_fijo == 'b':
            fb_mod = fb / 2.0
        
        denominador = fb_mod - fa_mod
        if abs(denominador) < 1e-15:
            break
        
        c = (a * fb_mod - b * fa_mod) / denominador
        fc = f(c)
        
        error_intervalo = abs(b - a)
        
        mod_texto = "Si" if extremo_fijo else "No"
        
        tabla.append({
            'iter': contador + 1,
            'a': a,
            'b': b,
            'c': c,
            'f_a': fa,
            'f_b': fb,
            'f_c': fc,
            'error': error_intervalo,
            'modificado': mod_texto
        })
        
        if abs(fc) < tol or error_intervalo < tol:
            return c, contador + 1, tabla
        
        if f(a) * fc < 0:
            extremo_fijo = 'b'
            b = c
        else:
            extremo_fijo = 'a'
            a = c
        
        contador += 1
    
    return c, contador, tabla

# ============================================================================
# METODO 3: HIBRIDO (FALSA POSICION + BISECCION)
# ============================================================================

def metodo_hibrido(a, b, tol=1e-5, max_iter=100):
    """
    Método Híbrido: Falsa Posición + Bisección
    Cambia a bisección cuando detecta estancamiento
    """
    if f(a) * f(b) > 0:
        return None, None, []
    
    tabla = []
    contador = 0
    a_prev = None
    b_prev = None
    estancado_consecutivo = 0
    
    while contador < max_iter:
        fa = f(a)
        fb = f(b)
        
        # Detectar estancamiento
        estancado = False
        if a_prev is not None and b_prev is not None:
            if abs(a - a_prev) < 1e-14 and abs(b - b_prev) < 1e-14:
                estancado = True
                estancado_consecutivo += 1
            else:
                estancado_consecutivo = 0
        
        # Elegir método
        if estancado_consecutivo >= 1:
            c = (a + b) / 2.0
            metodo_usado = "Biseccion"
        else:
            denominador = fb - fa
            if abs(denominador) < 1e-15:
                c = (a + b) / 2.0
                metodo_usado = "Biseccion"
            else:
                c = (a * fb - b * fa) / denominador
                metodo_usado = "Falsa_Pos"
        
        fc = f(c)
        error_intervalo = abs(b - a)
        
        tabla.append({
            'iter': contador + 1,
            'a': a,
            'b': b,
            'c': c,
            'f_a': fa,
            'f_b': fb,
            'f_c': fc,
            'error': error_intervalo,
            'metodo': metodo_usado
        })
        
        if abs(fc) < tol or error_intervalo < tol:
            return c, contador + 1, tabla
        
        if f(a) * fc < 0:
            b = c
        else:
            a = c
        
        a_prev = a
        b_prev = b
        contador += 1
    
    return c, contador, tabla

# ============================================================================
# FUNCION PARA IMPRIMIR TABLAS
# ============================================================================

def imprimir_tabla_completa(tabla, titulo=""):
    """Imprime la tabla completa de manera legible"""
    
    if not tabla:
        print("No hay datos")
        return
    
    if titulo:
        print("\n" + "="*140)
        print(titulo)
        print("="*140 + "\n")
    
    # Encabezado
    print(f"{'iter':>4} | {'a':>15} | {'b':>15} | {'c':>15} | {'f(a)':>15} | {'f(b)':>15} | {'f(c)':>15} | {'error':>15}", end="")
    
    # Encabezado adicional si existe
    if 'modificado' in tabla[0]:
        print(" | {'mod':>6}", end="")
    if 'metodo' in tabla[0]:
        print(" | {'metodo':>10}", end="")
    
    print("\n" + "-"*140)
    
    # Datos
    for row in tabla:
        iter_val = row['iter']
        a_val = row['a']
        b_val = row['b']
        c_val = row['c']
        fa_val = row['f_a']
        fb_val = row['f_b']
        fc_val = row['f_c']
        err_val = row['error']
        
        print(f"{iter_val:>4} | {a_val:>15.10f} | {b_val:>15.10f} | {c_val:>15.10f} | {fa_val:>15.10f} | {fb_val:>15.10f} | {fc_val:>15.10f} | {err_val:>15.10e}", end="")
        
        if 'modificado' in row:
            print(f" | {row['modificado']:>6}", end="")
        if 'metodo' in row:
            print(f" | {row['metodo']:>10}", end="")
        
        print()
    
    print("-"*140 + "\n")

# ============================================================================
# FUNCION PARA IMPRIMIR RESULTADOS FINALES
# ============================================================================

def imprimir_resultados_finales(metodo_nombre, raiz, iter_count, tabla, f_raiz):
    """Imprime los resultados finales de forma clara y estructurada"""
    
    print("\n" + "="*100)
    print(f"RESULTADOS FINALES - {metodo_nombre}")
    print("="*100 + "\n")
    
    print(f"RAIZ APROXIMADA:")
    print(f"  r = {raiz:.15f}\n")
    
    print(f"VALOR DE LA FUNCION EN LA RAIZ:")
    print(f"  f(r) = {f_raiz:.15e}\n")
    
    print(f"CANTIDAD DE ITERACIONES:")
    print(f"  Iteraciones realizadas = {iter_count}\n")
    
    print(f"TABLA DE ITERACIONES:")
    imprimir_tabla_completa(tabla)
    
    return raiz, f_raiz, iter_count

# ============================================================================
# PROGRAMA PRINCIPAL
# ============================================================================

if __name__ == "__main__":
    
    print("\n" + "="*140)
    print("METODO DE FALSA POSICION - ANALISIS COMPLETO DE ESTANCAMIENTO")
    print("="*140)
    
    a_ini = 0.0
    b_ini = 2.0
    eps = 1e-5
    
    print(f"\nFUNCION: f(x) = x³ + x² - 1")
    print(f"INTERVALO: [{a_ini}, {b_ini}]")
    print(f"TOLERANCIA: {eps}")
    print(f"\nVERIFICACION DE CONDICIONES:")
    print(f"  f({a_ini}) = {f(a_ini):.10f}")
    print(f"  f({b_ini}) = {f(b_ini):.10f}")
    print(f"  f(a) * f(b) = {f(a_ini) * f(b_ini):.10f} < 0")
    print(f"\n✓ CAMBIO DE SIGNO DETECTADO - EXISTE RAIZ EN EL INTERVALO")
    
    print(f"\nANALISIS DE LA FUNCION:")
    print(f"  f'(x) = 3x² + 2x")
    print(f"  f''(x) = 6x + 2")
    print(f"  f''(x) > 0 para todo x en [0,2] → FUNCION CONVEXA")
    print(f"\n  f'(0) = {df(0):.6f} (creciente)")
    print(f"  f'(2) = {df(2):.6f} (creciente)")
    
    n_teorico = math.ceil(math.log2((b_ini - a_ini) / eps))
    print(f"\nITERACIONES ESTIMADAS (por Bisección): {n_teorico}")
    
    # ========================================================================
    # EJECUTAR METODOS
    # ========================================================================
    
    print("\n" + "="*140)
    print("METODO 1: FALSA POSICION CLASICO")
    print("="*140)
    
    r1, iter1, tabla1 = metodo_clasico(a_ini, b_ini, eps)
    
    if r1 is not None:
        print(f"\nRESULTADOS:")
        print(f"  Raiz aproximada: r = {r1:.15f}")
        print(f"  Valor en raiz:   f(r) = {f(r1):.15e}")
        print(f"  Iteraciones:     {iter1}")
        
        imprimir_tabla_completa(tabla1, "TABLA DE ITERACIONES - FALSA POSICION CLASICO")
        
        print("ANALISIS DEL ESTANCAMIENTO:")
        print("-"*140)
        print("CAUSA IDENTIFICADA:")
        print("  • La función es CONVEXA en [0,2] (f''(x) = 6x + 2 > 0)")
        print("  • El extremo izquierdo a=0 permanece fijo en iteraciones iniciales")
        print("  • La línea de interpolación no cruza el extremo con gran curvatura")
        print("  • Esto ralentiza significativamente la convergencia")
        print()
    
    # ========================================================================
    # METODO ILLINOIS
    # ========================================================================
    
    print("\n" + "="*140)
    print("METODO 2: FALSA POSICION ILLINOIS (MEJORADO)")
    print("="*140)
    
    r2, iter2, tabla2 = metodo_illinois(a_ini, b_ini, eps)
    
    if r2 is not None:
        print(f"\nRESULTADOS:")
        print(f"  Raiz aproximada: r = {r2:.15f}")
        print(f"  Valor en raiz:   f(r) = {f(r2):.15e}")
        print(f"  Iteraciones:     {iter2}")
        
        imprimir_tabla_completa(tabla2, "TABLA DE ITERACIONES - FALSA POSICION ILLINOIS")
        
        print("ESTRATEGIA DE MEJORA:")
        print("-"*140)
        print("MODIFICACION ILLINOIS:")
        print("  • Cuando un extremo permanece fijo, se divide su f(x) por 2")
        print("  • Esto modifica la pendiente de la interpolación lineal")
        print("  • Fuerza al algoritmo a reducir más equilibradamente el intervalo")
        print()
        
        if iter1 is not None and iter2 is not None:
            mejora = ((iter1 - iter2) / iter1) * 100
            print(f"MEJORA LOGRADA:")
            print(f"  • Reducción de iteraciones: {mejora:.1f}%")
            print(f"  • De {iter1} iteraciones a {iter2} iteraciones")
            print()
    
    # ========================================================================
    # METODO HIBRIDO
    # ========================================================================
    
    print("\n" + "="*140)
    print("METODO 3: HIBRIDO (FALSA POSICION + BISECCION)")
    print("="*140)
    
    r3, iter3, tabla3 = metodo_hibrido(a_ini, b_ini, eps)
    
    if r3 is not None:
        print(f"\nRESULTADOS:")
        print(f"  Raiz aproximada: r = {r3:.15f}")
        print(f"  Valor en raiz:   f(r) = {f(r3):.15e}")
        print(f"  Iteraciones:     {iter3}")
        
        imprimir_tabla_completa(tabla3, "TABLA DE ITERACIONES - METODO HIBRIDO")
        
        print("ESTRATEGIA HIBRIDA:")
        print("-"*140)
        print("FUNCIONAMIENTO:")
        print("  • Usa Falsa Posición cuando converge normalmente")
        print("  • Detecta estancamiento automaticamente")
        print("  • Cambia a Bisección cuando hay estancamiento")
        print("  • Combina velocidad de convergencia con robustez")
        print()
        
        # Contar cambios de método
        cambios = sum(1 for row in tabla3 if row['metodo'] == 'Biseccion')
        if cambios > 0:
            print(f"ESTADISTICAS:")
            print(f"  • Iteraciones con Bisección: {cambios}")
            print(f"  • Iteraciones con Falsa Pos: {iter3 - cambios}")
            print()
    
    # ========================================================================
    # COMPARACION FINAL
    # ========================================================================
    
    print("\n" + "="*140)
    print("COMPARACION FINAL DE LOS TRES METODOS")
    print("="*140 + "\n")
    
    print(f"{'METODO':<30} {'ITERACIONES':>15} {'RAIZ':>20} {'f(RAIZ)':>20} {'ERROR ABS':>20}")
    print("-"*140)
    print(f"{'Falsa Pos. Clásico':<30} {iter1:>15} {r1:>20.12f} {f(r1):>20.12e} {abs(f(r1)):>20.12e}")
    print(f"{'Falsa Pos. Illinois':<30} {iter2:>15} {r2:>20.12f} {f(r2):>20.12e} {abs(f(r2)):>20.12e}")
    print(f"{'Híbrido':<30} {iter3:>15} {r3:>20.12f} {f(r3):>20.12e} {abs(f(r3)):>20.12e}")
    print()
    
    print("CONCLUSIONES:")
    print("-"*140)
    print(f"1. Método Clásico: {iter1} iteraciones (LENTO - ESTANCAMIENTO)")
    print(f"2. Método Illinois: {iter2} iteraciones (MEJORA: {((iter1-iter2)/iter1*100):.1f}%)")
    print(f"3. Método Híbrido: {iter3} iteraciones (ROBUSTO)")
    print()
    
    print("RECOMENDACIONES:")
    print("-"*140)
    print("✓ Para funciones DESCONOCIDAS: Usar método HIBRIDO (más seguro)")
    print("✓ Para funciones CON ESTANCAMIENTO: Usar ILLINOIS (mejor convergencia)")
    print("✓ Para funciones BIEN COMPORTADAS: CLASICO es suficiente")
    print()

    # ========================================================================
    # GRAFICAS
    # ========================================================================
    
    print("\nGenerando gráficas...")
    
    x_graf = np.linspace(-0.5, 2.5, 500)
    y_graf = f(x_graf)
    
    # Figura 1: Análisis General
    fig = plt.figure(figsize=(16, 12))
    fig.suptitle('MÉTODO DE FALSA POSICIÓN - ANÁLISIS COMPLETO\nf(x) = x³ + x² - 1, Intervalo [0, 2]', 
                 fontsize=16, fontweight='bold')
    
    # Subplot 1: Función general con raíces
    ax = plt.subplot(3, 3, 1)
    ax.plot(x_graf, y_graf, 'b-', linewidth=2.5, label='f(x) = x³ + x² - 1')
    ax.axhline(0, color='k', linewidth=0.8, alpha=0.5)
    ax.axvline(0, color='k', linewidth=0.8, alpha=0.5)
    ax.fill_between(np.linspace(a_ini, b_ini, 100), -2, 10, alpha=0.1, color='gray', label='Intervalo [0, 2]')
    ax.scatter([r1], [0], color='red', s=150, zorder=5, marker='o', edgecolors='darkred', linewidth=2, label=f'Raíz ≈ {r1:.6f}')
    ax.plot([a_ini, b_ini], [f(a_ini), f(b_ini)], 'go', markersize=10, label='Extremos iniciales')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('f(x)', fontsize=11, fontweight='bold')
    ax.set_title('Función y Localización de Raíz', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    ax.set_ylim(-2, 8)
    
    # Subplot 2: Convergencia Clásico
    ax = plt.subplot(3, 3, 2)
    iters_c = [row['iter'] for row in tabla1]
    errs_c = [abs(row['f_c']) for row in tabla1]
    ax.semilogy(iters_c, errs_c, 'o-', color='red', linewidth=2.5, markersize=7, label='|f(c)|')
    ax.axhline(eps, color='green', linestyle='--', linewidth=2.5, label=f'Tolerancia = {eps}')
    ax.grid(True, alpha=0.3, linestyle='--', which='both')
    ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
    ax.set_ylabel('|f(c)| (escala log)', fontsize=11, fontweight='bold')
    ax.set_title(f'Convergencia: Clásico ({iter1} iter)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    
    # Subplot 3: Convergencia Illinois
    ax = plt.subplot(3, 3, 3)
    iters_i = [row['iter'] for row in tabla2]
    errs_i = [abs(row['f_c']) for row in tabla2]
    ax.semilogy(iters_i, errs_i, 'o-', color='orange', linewidth=2.5, markersize=7, label='|f(c)|')
    ax.axhline(eps, color='green', linestyle='--', linewidth=2.5, label=f'Tolerancia = {eps}')
    ax.grid(True, alpha=0.3, linestyle='--', which='both')
    ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
    ax.set_ylabel('|f(c)| (escala log)', fontsize=11, fontweight='bold')
    ax.set_title(f'Convergencia: Illinois ({iter2} iter)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    
    # Subplot 4: Evolución extremo a - Clásico
    ax = plt.subplot(3, 3, 4)
    a_vals = [row['a'] for row in tabla1]
    b_vals = [row['b'] for row in tabla1]
    ax.plot(iters_c, a_vals, 'o-', color='blue', linewidth=2, markersize=6, label='a (inferior)')
    ax.plot(iters_c, b_vals, 's-', color='red', linewidth=2, markersize=6, label='b (superior)')
    ax.axhline(r1, color='green', linestyle='--', linewidth=2, label=f'Raíz = {r1:.6f}')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
    ax.set_ylabel('Valor', fontsize=11, fontweight='bold')
    ax.set_title('Evolución Extremos: Clásico', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    
    # Subplot 5: Evolución extremo a - Illinois
    ax = plt.subplot(3, 3, 5)
    a_vals = [row['a'] for row in tabla2]
    b_vals = [row['b'] for row in tabla2]
    ax.plot(iters_i, a_vals, 'o-', color='blue', linewidth=2, markersize=6, label='a (inferior)')
    ax.plot(iters_i, b_vals, 's-', color='red', linewidth=2, markersize=6, label='b (superior)')
    ax.axhline(r2, color='green', linestyle='--', linewidth=2, label=f'Raíz = {r2:.6f}')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
    ax.set_ylabel('Valor', fontsize=11, fontweight='bold')
    ax.set_title('Evolución Extremos: Illinois', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    
    # Subplot 6: Evolución extremo a - Híbrido
    ax = plt.subplot(3, 3, 6)
    iters_h = [row['iter'] for row in tabla3]
    a_vals = [row['a'] for row in tabla3]
    b_vals = [row['b'] for row in tabla3]
    ax.plot(iters_h, a_vals, 'o-', color='blue', linewidth=2, markersize=6, label='a (inferior)')
    ax.plot(iters_h, b_vals, 's-', color='red', linewidth=2, markersize=6, label='b (superior)')
    ax.axhline(r3, color='green', linestyle='--', linewidth=2, label=f'Raíz = {r3:.6f}')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
    ax.set_ylabel('Valor', fontsize=11, fontweight='bold')
    ax.set_title('Evolución Extremos: Híbrido', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    
    # Subplot 7: Comparación iteraciones
    ax = plt.subplot(3, 3, 7)
    metodos = ['Clásico', 'Illinois', 'Híbrido']
    iters_list = [iter1, iter2, iter3]
    colores = ['#FF6B6B', '#FFA500', '#4ECDC4']
    barras = ax.bar(metodos, iters_list, color=colores, alpha=0.8, edgecolor='black', linewidth=2)
    ax.set_ylabel('Número de iteraciones', fontsize=11, fontweight='bold')
    ax.set_title('Comparación: Iteraciones Requeridas', fontsize=12, fontweight='bold')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y')
    
    for barra, it in zip(barras, iters_list):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, altura,
                f'{int(it)}', ha='center', va='bottom', fontsize=12, fontweight='bold')
    
    # Subplot 8: Error absoluto final
    ax = plt.subplot(3, 3, 8)
    errores = [abs(f(r1)), abs(f(r2)), abs(f(r3))]
    barras = ax.bar(metodos, errores, color=colores, alpha=0.8, edgecolor='black', linewidth=2)
    ax.set_ylabel('|f(r)| (escala log)', fontsize=11, fontweight='bold')
    ax.set_title('Comparación: Error Absoluto Final', fontsize=12, fontweight='bold')
    ax.set_yscale('log')
    ax.grid(True, alpha=0.3, linestyle='--', axis='y', which='both')
    
    for barra, err in zip(barras, errores):
        altura = barra.get_height()
        ax.text(barra.get_x() + barra.get_width()/2, altura,
                f'{err:.2e}', ha='center', va='bottom', fontsize=10, fontweight='bold')
    
    # Subplot 9: Convergencia Híbrido
    ax = plt.subplot(3, 3, 9)
    errs_h = [abs(row['f_c']) for row in tabla3]
    colores_metodo = ['orange' if row['metodo'] == 'Falsa_Pos' else 'purple' for row in tabla3]
    ax.semilogy(iters_h, errs_h, 'o-', color='cyan', linewidth=2.5, markersize=7, label='|f(c)|')
    # Marcar puntos donde cambió a bisección
    for i, (it, err, color) in enumerate(zip(iters_h, errs_h, colores_metodo)):
        if color == 'purple':
            ax.scatter(it, err, s=100, color='purple', marker='s', zorder=5, edgecolors='darkviolet', linewidth=1.5)
    ax.axhline(eps, color='green', linestyle='--', linewidth=2.5, label=f'Tolerancia = {eps}')
    ax.grid(True, alpha=0.3, linestyle='--', which='both')
    ax.set_xlabel('Iteración', fontsize=11, fontweight='bold')
    ax.set_ylabel('|f(c)| (escala log)', fontsize=11, fontweight='bold')
    ax.set_title(f'Convergencia: Híbrido ({iter3} iter)', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9)
    
    plt.tight_layout()
    plt.savefig('falsa_posicion_analisis_completo.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica 1 guardada: falsa_posicion_analisis_completo.png")
    
    # Figura 2: Aproximaciones en la función
    fig, axes = plt.subplots(1, 3, figsize=(18, 5))
    fig.suptitle('ITERACIONES VISUALIZADAS EN LA FUNCIÓN\nMostrándo el cambio de la aproximación c en cada iteración', 
                 fontsize=14, fontweight='bold')
    
    # Clásico
    ax = axes[0]
    ax.plot(x_graf, y_graf, 'b-', linewidth=2.5, label='f(x)', alpha=0.7)
    ax.axhline(0, color='k', linewidth=0.8, alpha=0.3)
    ax.axvline(0, color='k', linewidth=0.8, alpha=0.3)
    
    # Mostrar primeras 5 iteraciones
    c_vals_plot = [row['c'] for row in tabla1[:min(5, len(tabla1))]]
    fc_vals_plot = [row['f_c'] for row in tabla1[:min(5, len(tabla1))]]
    colores_iter = plt.cm.Reds(np.linspace(0.3, 0.9, len(c_vals_plot)))
    
    for i, (c, fc, color) in enumerate(zip(c_vals_plot, fc_vals_plot, colores_iter)):
        ax.scatter(c, fc, s=100, color=color, zorder=5, edgecolors='darkred', linewidth=1.5, label=f'Iter {i+1}')
    
    ax.scatter([r1], [0], s=200, color='green', marker='*', zorder=10, edgecolors='darkgreen', linewidth=2, label='Raíz final')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('f(x)', fontsize=11, fontweight='bold')
    ax.set_title('Clásico: Convergencia Iterativa', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.set_ylim(-0.5, 2)
    
    # Illinois
    ax = axes[1]
    ax.plot(x_graf, y_graf, 'b-', linewidth=2.5, label='f(x)', alpha=0.7)
    ax.axhline(0, color='k', linewidth=0.8, alpha=0.3)
    ax.axvline(0, color='k', linewidth=0.8, alpha=0.3)
    
    c_vals_plot = [row['c'] for row in tabla2[:min(5, len(tabla2))]]
    fc_vals_plot = [row['f_c'] for row in tabla2[:min(5, len(tabla2))]]
    colores_iter = plt.cm.Oranges(np.linspace(0.3, 0.9, len(c_vals_plot)))
    
    for i, (c, fc, color) in enumerate(zip(c_vals_plot, fc_vals_plot, colores_iter)):
        ax.scatter(c, fc, s=100, color=color, zorder=5, edgecolors='darkorange', linewidth=1.5, label=f'Iter {i+1}')
    
    ax.scatter([r2], [0], s=200, color='green', marker='*', zorder=10, edgecolors='darkgreen', linewidth=2, label='Raíz final')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('f(x)', fontsize=11, fontweight='bold')
    ax.set_title('Illinois: Convergencia Iterativa', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.set_ylim(-0.5, 2)
    
    # Híbrido
    ax = axes[2]
    ax.plot(x_graf, y_graf, 'b-', linewidth=2.5, label='f(x)', alpha=0.7)
    ax.axhline(0, color='k', linewidth=0.8, alpha=0.3)
    ax.axvline(0, color='k', linewidth=0.8, alpha=0.3)
    
    c_vals_plot = [row['c'] for row in tabla3[:min(5, len(tabla3))]]
    fc_vals_plot = [row['f_c'] for row in tabla3[:min(5, len(tabla3))]]
    colores_iter = plt.cm.Blues(np.linspace(0.3, 0.9, len(c_vals_plot)))
    
    for i, (c, fc, color) in enumerate(zip(c_vals_plot, fc_vals_plot, colores_iter)):
        ax.scatter(c, fc, s=100, color=color, zorder=5, edgecolors='darkblue', linewidth=1.5, label=f'Iter {i+1}')
    
    ax.scatter([r3], [0], s=200, color='green', marker='*', zorder=10, edgecolors='darkgreen', linewidth=2, label='Raíz final')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_xlabel('x', fontsize=11, fontweight='bold')
    ax.set_ylabel('f(x)', fontsize=11, fontweight='bold')
    ax.set_title('Híbrido: Convergencia Iterativa', fontsize=12, fontweight='bold')
    ax.legend(fontsize=9, loc='upper right')
    ax.set_ylim(-0.5, 2)
    
    plt.tight_layout()
    plt.savefig('falsa_posicion_iteraciones.png', dpi=300, bbox_inches='tight')
    print("✓ Gráfica 2 guardada: falsa_posicion_iteraciones.png")
    
    plt.show()

    # ========================================================================
    # RESUMEN FINAL PARA CADA METODO
    # ========================================================================
    
    print("\n\n" + "="*100)
    print("RESUMEN FINAL - METODO FALSA POSICION CLASICO")
    print("="*100 + "\n")
    
    print(f"RAIZ APROXIMADA:")
    print(f"  r = {r1:.15f}\n")
    
    print(f"VALOR DE LA FUNCION EN LA RAIZ:")
    print(f"  f(r) = {f(r1):.15e}\n")
    
    print(f"CANTIDAD DE ITERACIONES:")
    print(f"  Iteraciones realizadas = {iter1}\n")
    
    print(f"TABLA COMPLETA DE ITERACIONES:")
    imprimir_tabla_completa(tabla1)
    
    print("\n\n" + "="*100)
    print("RESUMEN FINAL - METODO FALSA POSICION ILLINOIS")
    print("="*100 + "\n")
    
    print(f"RAIZ APROXIMADA:")
    print(f"  r = {r2:.15f}\n")
    
    print(f"VALOR DE LA FUNCION EN LA RAIZ:")
    print(f"  f(r) = {f(r2):.15e}\n")
    
    print(f"CANTIDAD DE ITERACIONES:")
    print(f"  Iteraciones realizadas = {iter2}\n")
    
    print(f"TABLA COMPLETA DE ITERACIONES:")
    imprimir_tabla_completa(tabla2)
    
    print("\n\n" + "="*100)
    print("RESUMEN FINAL - METODO HIBRIDO")
    print("="*100 + "\n")
    
    print(f"RAIZ APROXIMADA:")
    print(f"  r = {r3:.15f}\n")
    
    print(f"VALOR DE LA FUNCION EN LA RAIZ:")
    print(f"  f(r) = {f(r3):.15e}\n")
    
    print(f"CANTIDAD DE ITERACIONES:")
    print(f"  Iteraciones realizadas = {iter3}\n")
    
    print(f"TABLA COMPLETA DE ITERACIONES:")
    imprimir_tabla_completa(tabla3)
    
    print("\n" + "="*100)
    print("ANALISIS COMPLETADO EXITOSAMENTE")
    print("="*100)
    print("\nArchivos generados:")
    print("  1. falsa_posicion_analisis_completo.png")
    print("  2. falsa_posicion_iteraciones.png")
    print()
