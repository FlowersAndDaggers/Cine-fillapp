import time
import sys

# Aumentamos el límite de recursión por si el árbol de Kaggle queda desbalanceado
sys.setrecursionlimit(100000)

from main import Produccion, Nodo, ArbolCatalogo, mi_catalogo

def ejecutar_experimentos(catalogo_completo):
    if not catalogo_completo:
        print("Error: El catálogo está vacío.")
        return

    max_datos = len(catalogo_completo)
    tamanos = [1000, 10000, max_datos]
    titulo_prueba = catalogo_completo[-1].get_titulo()

    for N in tamanos:
        muestra = catalogo_completo[:N]
        if len(muestra) == 0:
            continue
            
        # --- busqueda secuencial ---
        inicio_sec = time.perf_counter()
        for peli in muestra:
            if peli.get_titulo().lower() == titulo_prueba.lower():
                break
        fin_sec = time.perf_counter()
        tiempo_sec = (fin_sec - inicio_sec) * 1000

        # --- busqueda en arbol ---
        arbol = ArbolCatalogo()
        for peli in muestra:
            arbol.insertar(peli)
            
        inicio_arbol = time.perf_counter()
        resultado = arbol.buscar(titulo_prueba)
        fin_arbol = time.perf_counter()
        tiempo_arbol = (fin_arbol - inicio_arbol) * 1000

        print(f"| N = {N:<6} | Secuencial: {tiempo_sec:>7.4f} ms | Árbol: {tiempo_arbol:>7.4f} ms |")
    print("==================================================\n")

if __name__ == "__main__":
    ejecutar_experimentos(mi_catalogo)
