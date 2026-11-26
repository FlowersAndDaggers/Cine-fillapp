import csv
import sys
import math
import time
import json
import os
import random
from collections import deque

#creamos la clase produccion
class Produccion:
    def __init__ (self, id_prod, titulo, tipo, genero, fecha_estreno, puntaje, director, actores):

        #ponemos todos los datos en privado 
        self._id = id_prod
        self._titulo = titulo
        self._tipo = tipo
        
     
        self._genero = [g.strip().lower() for g in genero.split(',')]
        
        self._fecha_estreno = fecha_estreno
        self._puntaje = puntaje
        self._director = director.strip().lower() #Lo pasamos a minúscula para comparar más fácil
        
       
        self._actores = [a.strip().lower() for a in actores.split(',')]

#creamos la llave para los datos
    def get_titulo(self):
        return self._titulo
    def get_fecha_estreno(self):
        return self._fecha_estreno
    def get_puntaje(self):
        return str(self._puntaje)
    def get_director(self):
        return self._director
    def get_actores(self):
        return self._actores
    def get_genero(self):
        return self._genero
    def get_tipo(self):
        return self._tipo

#le decimos como hacer el print
    def __repr__(self):
        return f"[{self._tipo}] {self._titulo} ({self._fecha_estreno[:4]}) dir. {self._director} - {self._puntaje}"

#leemos el archivo csv
mi_catalogo = []

with open('catalogo.csv', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)

#agregamos los datos a la lista
        for fila in lector:
            nueva_prod = Produccion(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7])
            mi_catalogo.append(nueva_prod)


#armamos el arbol general (n-arios)            
#primero nodos
class NodoGeneral:
    def __init__(self, nombre, pelicula=None):
        self.nombre = nombre          # Nombre de la categoría o subcategoría
        self.pelicula = pelicula      
        self.hijos = []               

    def agregar_hijo(self, nodo_hijo):
        self.hijos.append(nodo_hijo)

    def __repr__(self):
        if self.pelicula:
            return f"🎬 {self.pelicula.get_titulo()}"
        return f" [{self.nombre}]"

#clase arbolgeneral
class ArbolGeneral:
    def __init__(self, raiz_nombre="Películas"):
        self.raiz = NodoGeneral(raiz_nombre)

    def recorrido_preorden(self, nodo=None, nivel=0):
        if nodo is None:
            nodo = self.raiz
        
        # imprime la profundidad del arbol
        print("  " * nivel + f"├── {nodo.nombre}" if nivel > 0 else f"🌲 {nodo.nombre}")
        
        if nodo.pelicula:
            print("  " * (nivel + 1) + f" {nodo.pelicula}")
            
        for hijo in nodo.hijos:
            self.recorrido_preorden(hijo, nivel + 1)

    def buscar_en_arbol(self, nodo, termino):
        resultados = []
        if nodo is None:
            return resultados
        
        termino_lower = termino.lower()
        
        #Coincidencias con categoria o subcategoria
        if termino_lower in nodo.nombre.lower():
            resultados.append(nodo)
            self._obtener_todos_los_descendientes(nodo, resultados)
            
        #Coincidencias con los titulos
        elif nodo.pelicula and termino_lower in nodo.pelicula.get_titulo().lower():
            resultados.append(nodo)
            
        #Busqueda recursiva
        for hijo in nodo.hijos:
            sub_res = self.buscar_en_arbol(hijo, termino)
            for r in sub_res:
                if r not in resultados:
                    resultados.append(r)
                    
        return resultados

    def _obtener_todos_los_descendientes(self, nodo, lista_resultados):
        for hijo in nodo.hijos:
            if hijo not in lista_resultados:
                lista_resultados.append(hijo)
            self._obtener_todos_los_descendientes(hijo, lista_resultados)

#para que se construya con la base de datos (arbol de categorias)
def construir_arbol_categorias(catalogo):
    arbol = ArbolGeneral("Películas")

    #categorias generales y subcategorias
    estructura = {
        "Ciencia ficción": {
            "Cyberpunk": ["cyberpunk"],
            "Viajes temporales": ["viajes temporales", "tiempo", "time travel"],
            "Inteligencia artificial": ["inteligencia artificial", "ia", "robot", "androide"],
            "Otros Sci-Fi": []
        },
        "Terror": {
            "Slasher y Sobrenatural": ["slasher", "sobrenatural", "fantasma", "posesion"],
            "Suspenso / Thriller": ["suspenso", "thriller", "misterio", "mystery"],
            "Terror General": ["terror", "horror"],
            "Otros Terror": []
        },
        "Acción": {
            "Aventura": ["aventura", "adventure", "survival"],
            "Guerra": ["guerra", "war", "militar"],
            "Acción General": ["accion", "action"],
            "Otros Acción": []
        },
        "Comedia": {
            "Humor": ["humor", "stand-up"],
            "Comedia General": ["comedia", "comedy"],
            "Otros Comedia": []
        },
        "Drama": {
            "Romance": ["romance", "amor"],
            "Biografía": ["biografia", "biography", "historico"],
            "Drama General": ["drama"],
            "Otros Drama": []
        },
        "Crimen y Policial": {
            "Policial / Misterio": ["policial", "detective", "investigacion", "atraco", "heist"],
            "Crimen General": ["crimen", "crime", "mafia", "gangster"],
            "Otros Crimen": []
        },
        "Animación": {
            "Anime": ["anime", "manga"],
            "Animación General": ["animacion", "animation", "infantil", "family"],
            "Otros Animación": []
        },
        "Fantasía": {
            "Fantasía General": ["fantasia", "fantasy", "magia", "magic"],
            "Otros Fantasía": []
        },
        "Documental": {
            "Documental General": ["documental", "documentary"],
            "Otros Documental": []
        }
    }
    
    #nodos principales y subnodos
    nodos_macros = {}
    nodos_subs = {}
    agregados_por_sub = {}

    for macro, subs in estructura.items():
        nodo_macro = NodoGeneral(macro)
        arbol.raiz.agregar_hijo(nodo_macro)
        nodos_macros[macro] = nodo_macro
        nodos_subs[macro] = {}
        
        for sub in subs.keys():
            nodo_sub = NodoGeneral(sub)
            nodo_macro.agregar_hijo(nodo_sub)
            nodos_subs[macro][sub] = nodo_sub
            agregados_por_sub[(macro, sub)] = set()

    nodo_otros = NodoGeneral("Otros")
    arbol.raiz.agregar_hijo(nodo_otros)
    nodo_otros_gen = NodoGeneral("General")
    nodo_otros.agregar_hijo(nodo_otros_gen)
    agregados_otros = set()

    for peli in catalogo:
        generos_peli = peli.get_genero()
        titulo_peli = peli.get_titulo().lower()
        colocada_en_algun_lado = False

        
        for macro, subs in estructura.items():
            colocada_en_esta_macro = False
            
            for sub, keywords in subs.items():
                if "Otros" in sub:
                    continue
                if any(any(kw in g for kw in keywords) for g in generos_peli):
                    if titulo_peli not in agregados_por_sub[(macro, sub)]:
                        nodo_peli = NodoGeneral(peli.get_titulo(), pelicula=peli)
                        nodos_subs[macro][sub].agregar_hijo(nodo_peli)
                        agregados_por_sub[(macro, sub)].add(titulo_peli)
                    colocada_en_esta_macro = True
                    colocada_en_algun_lado = True
            
            #lo que no coincide con las categorias se lo manda a otros
            if not colocada_en_esta_macro and any(macro.lower() in g for g in generos_peli):
                fallback_sub = [s for s in subs.keys() if "Otros" in s][0]
                if titulo_peli not in agregados_por_sub[(macro, fallback_sub)]:
                    nodo_peli = NodoGeneral(peli.get_titulo(), pelicula=peli)
                    nodos_subs[macro][fallback_sub].agregar_hijo(nodo_peli)
                    agregados_por_sub[(macro, fallback_sub)].add(titulo_peli)
                colocada_en_algun_lado = True
        
        
        if not colocada_en_algun_lado:
            if titulo_peli not in agregados_otros:
                nodo_peli = NodoGeneral(peli.get_titulo(), pelicula=peli)
                nodo_otros_gen.agregar_hijo(nodo_peli)
                agregados_otros.add(titulo_peli)
                        
    return arbol


#Árbol AVL TP4
class NodoAVL:
    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.izquierda = None
        self.derecha = None
        self.altura = 1 

class ArbolAVL:
    def __init__(self):
        self.raiz = None

    def insertar(self, pelicula):
        self.raiz = self._insertar_recursivo(self.raiz, pelicula)

    def _insertar_recursivo(self, nodo, nueva_pelicula):
       
        if not nodo:
            return NodoAVL(nueva_pelicula)
        
        titulo_nuevo = nueva_pelicula.get_titulo().lower()
        titulo_actual = nodo.pelicula.get_titulo().lower()
        
        if titulo_nuevo < titulo_actual:
            nodo.izquierda = self._insertar_recursivo(nodo.izquierda, nueva_pelicula)
        else:
            nodo.derecha = self._insertar_recursivo(nodo.derecha, nueva_pelicula)

        nodo.altura = 1 + max(self._obtener_altura(nodo.izquierda), self._obtener_altura(nodo.derecha))

        balance = self._obtener_balance(nodo)

  
        if balance > 1 and titulo_nuevo < nodo.izquierda.pelicula.get_titulo().lower():
            return self._rotacion_derecha(nodo)

  
        if balance < -1 and titulo_nuevo >= nodo.derecha.pelicula.get_titulo().lower():
            return self._rotacion_izquierda(nodo)

   
        if balance > 1 and titulo_nuevo >= nodo.izquierda.pelicula.get_titulo().lower():
            nodo.izquierda = self._rotacion_izquierda(nodo.izquierda)
            return self._rotacion_derecha(nodo)


        if balance < -1 and titulo_nuevo < nodo.derecha.pelicula.get_titulo().lower():
            nodo.derecha = self._rotacion_derecha(nodo.derecha)
            return self._rotacion_izquierda(nodo)

        return nodo

    def _obtener_altura(self, nodo):
        if not nodo: return 0
        return nodo.altura

    def _obtener_balance(self, nodo):
        if not nodo: return 0
        return self._obtener_altura(nodo.izquierda) - self._obtener_altura(nodo.derecha)

    def _rotacion_derecha(self, z):
        y = z.izquierda
        T3 = y.derecha
        y.derecha = z
        z.izquierda = T3
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        return y

    def _rotacion_izquierda(self, z):
        y = z.derecha
        T2 = y.izquierda
        y.izquierda = z
        z.derecha = T2
        z.altura = 1 + max(self._obtener_altura(z.izquierda), self._obtener_altura(z.derecha))
        y.altura = 1 + max(self._obtener_altura(y.izquierda), self._obtener_altura(y.derecha))
        return y

    def recorrido_inorder(self):
        self._inorder_recursivo(self.raiz)

    def _inorder_recursivo(self, nodo):
        if nodo is not None:
            self._inorder_recursivo(nodo.izquierda)
            print(nodo.pelicula)
            self._inorder_recursivo(nodo.derecha)            


#Recomendar peli (Opción 1)      
def obtener_o_cargar_grafo(catalogo):
    #Cargar o crear grafo
    grafo = GrafoPeliculas()
    archivo_grafo = "red_peliculas_cache.json"
    if os.path.exists(archivo_grafo):
        with open(archivo_grafo, 'r', encoding='utf-8') as f:
            grafo.adyacencia = json.load(f)
    else:
        print(" Construyendo red de conexiones por primera vez...")
        grafo = construir_red_peliculas(catalogo)
        with open(archivo_grafo, 'w', encoding='utf-8') as f:
            json.dump(grafo.adyacencia, f)
    return grafo

def recomendar_peli(catalogo, grafo, watchlist, perfil):
    print("\n--- 🎬 SISTEMA DE RECOMENDACIÓN INTELIGENTE (GRAFO + HEAP) ---")
    print("1. Recomendación clásica (basada en 1 película)")
    print("2. Recomendación por grupo (de 2 a 5 películas usando Camino Mínimo)")
    print("3. Joyas ocultas (conexiones profundas en red usando DFS)")
    modo = input("Elegí una opción (1-3): ").strip()

    if modo == "1":
        termino = input("\n¿En qué película basamos tu recomendación?: ").strip()
        encontrados = [
            p for p in catalogo 
            if termino.lower() in p.get_titulo().lower() and p.get_titulo().lower() in grafo.adyacencia
        ]
        
        if encontrados:
            print(f"\nEncontramos estas películas en la red para '{termino}':")
            for i, peli in enumerate(encontrados[:10], start=1):
                print(f"{i}. {peli.get_titulo()} ({peli.get_fecha_estreno()[:4]}) - [{', '.join(peli.get_genero())}]")
            
            try:
                seleccion = int(input("\nIngresá el número de la película exacta (o 0 para cancelar): "))
                if seleccion == 0:
                    return 
                if 1 <= seleccion <= len(encontrados[:10]):
                    pelicula_base = encontrados[seleccion - 1]
                    generar_recomendaciones(catalogo, pelicula_base, grafo, watchlist, perfil)
                else:
                    print("\n❌ Número fuera de rango.")
            except ValueError:
                print("\n❌ Entrada inválida. Debés ingresar un número.")
        else:
            print("\n❌ No se encontraron películas con ese título dentro de la red activa.")

    elif modo == "2":
        peliculas_grupo = []
        print("\n MODO GRUPO: Elegí entre 2 y 5 películas para cruzar sus conexiones.")
        
        while len(peliculas_grupo) < 5:
            prompt = f"\nIngresá el título de la película #{len(peliculas_grupo) + 1}"
            if len(peliculas_grupo) >= 2:
                prompt += " (o escribí 'fin' para generar recomendaciones): "
            else:
                prompt += ": "
                
            termino = input(prompt).strip()
            
            if termino.lower() == 'fin':
                if len(peliculas_grupo) < 2:
                    print("⚠️ Tenés que elegir al menos 2 películas para usar el modo grupo.")
                    continue
                break

            encontrados = [
                p for p in catalogo 
                if termino.lower() in p.get_titulo().lower() and p.get_titulo().lower() in grafo.adyacencia
            ]

            if not encontrados:
                print("❌ No encontramos esa película en la red activa. Probá con otra.")
                continue

            print(f"\nCoincidencias para '{termino}':")
            for i, peli in enumerate(encontrados[:10], start=1):
                print(f"{i}. {peli.get_titulo()} ({peli.get_fecha_estreno()[:4]}) - [{', '.join(peli.get_genero())}]")

            try:
                sel = int(input("Seleccioná el número exacto (0 para buscar otra): "))
                if sel == 0:
                    continue
                if 1 <= sel <= len(encontrados[:10]):
                    elegida = encontrados[sel - 1]
                    if elegida not in peliculas_grupo:
                        peliculas_grupo.append(elegida)
                        print(f"✅ Agregada ({len(peliculas_grupo)}/5): {elegida.get_titulo()}")
                    else:
                        print("⚠️ Ya agregaste esa película al grupo.")
                else:
                    print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Ingresá un número válido.")

        if len(peliculas_grupo) >= 2:
            generar_recomendaciones_grupo(catalogo, peliculas_grupo, grafo, watchlist)

    elif modo == "3":
        termino = input("\n ¿Desde qué película querés explorar joyas ocultas?: ").strip()
        encontrados = [
            p for p in catalogo 
            if termino.lower() in p.get_titulo().lower() and p.get_titulo().lower() in grafo.adyacencia
        ]
        
        if encontrados:
            print(f"\nEncontramos estas películas en la red para '{termino}':")
            for i, peli in enumerate(encontrados[:10], start=1):
                print(f"{i}. {peli.get_titulo()} ({peli.get_fecha_estreno()[:4]}) - [{', '.join(peli.get_genero())}]")
            
            try:
                seleccion = int(input("\nIngresá el número de la película exacta (o 0 para cancelar): "))
                if seleccion == 0:
                    return 
                if 1 <= seleccion <= len(encontrados[:10]):
                    pelicula_base = encontrados[seleccion - 1]
                    generar_joyas_ocultas(catalogo, pelicula_base, grafo, watchlist)
                else:
                    print("\n❌ Número fuera de rango.")
            except ValueError:
                print("\n❌ Entrada inválida. Debés ingresar un número.")
        else:
            print("\n❌ No se encontraron películas con ese título dentro de la red activa.")
    else:
        print("\n❌ Opción no válida.")


#a partir de una pelicula
def generar_recomendaciones(catalogo, pelicula_base, grafo, watchlist, perfil):
    titulo_base = pelicula_base.get_titulo().lower()
    vecinos = grafo.obtener_vecinos(titulo_base)
    
    if not vecinos:
        print(f"\n❌ '{pelicula_base.get_titulo()}' no tiene conexiones registradas en la red.")
        return

    mapa_peliculas = {p.get_titulo().lower(): p for p in catalogo}
    heap_recomendaciones = ColaPrioridadHeap(capacidad=10)
    
    for titulo_vecino, peso_grafo in vecinos.items():
        # Si ya la vio y le puso menos de 8, la excluimos de las recomendaciones
        if perfil.ya_vista(titulo_vecino) and perfil.puntaje_usuario(titulo_vecino) < 8.0:
            continue

        peli_obj = mapa_peliculas.get(titulo_vecino)
        if not peli_obj:
            continue
            
        try:
            rating = float(peli_obj.get_puntaje())
        except ValueError:
            rating = 0.0
            
        score_final = peso_grafo + (rating / 10.0)
        heap_recomendaciones.insertar_con_score(score_final, peli_obj)
        
    top_10 = heap_recomendaciones.obtener_ranking_ordenado()
    
    dir_base = pelicula_base.get_director()
    gen_base = set(pelicula_base.get_genero())
    act_base = set(pelicula_base.get_actores())
    
    print(f"\n TOP {len(top_10)} RECOMENDACIONES PARA '{pelicula_base.get_titulo().upper()}':")
    print("=" * 85)
    for i, (score, peli) in enumerate(top_10, start=1):
        titulo = peli.get_titulo()
        anio = peli.get_fecha_estreno()[:4]
        estrellas = peli.get_puntaje()
        peso_puro = int(score)
        
        coincidencias = []
        if peli.get_director() == dir_base and dir_base != "":
            coincidencias.append(f"Dir: {dir_base.title()}")
            
        generos_comunes = gen_base.intersection(set(peli.get_genero()))
        if generos_comunes:
            gens_str = ", ".join([g.title() for g in generos_comunes])
            coincidencias.append(f"Género: {gens_str}")
            
        actores_comunes = act_base.intersection(set(peli.get_actores()))
        if actores_comunes:
            acts_str = ", ".join([a.title() for a in actores_comunes])
            coincidencias.append(f"Elenco: {acts_str}")
            
        detalle_comun = " | ".join(coincidencias) if coincidencias else "Sin datos detallados"
        etiqueta_vista = f" [Ya vista - Tu nota:  {perfil.puntaje_usuario(titulo)} | Ideal para remirar]" if perfil.ya_vista(titulo) else ""
        
        print(f"{i}. {titulo} ({anio}) |  {estrellas} | Afinidad: {peso_puro} pts{etiqueta_vista}")
        print(f"   Comparten: {detalle_comun}")
    print("=" * 85)

    print("\n¿Querés guardar alguna de estas recomendaciones en tu Watchlist?")
    while True:
        eleccion = input("Ingresá el número (1-10) para agregar (o '0' para volver): ").strip()
        
        if eleccion == "0":
            break
            
        try:
            idx = int(eleccion)
            if 1 <= idx <= len(top_10):
                pelicula_elegida = top_10[idx - 1][1]
                watchlist.agregar(pelicula_elegida)
            else:
                print(f"❌ Ingresá un número entre 1 y {len(top_10)}.")
        except ValueError:
            print("❌ Entrada inválida. Ingresá un número.")

#a partir de varias peliculas (camino más corto)
def generar_recomendaciones_grupo(catalogo, peliculas_grupo, grafo, watchlist):
    titulos_grupo = {p.get_titulo().lower() for p in peliculas_grupo}
    mapa_peliculas = {p.get_titulo().lower(): p for p in catalogo}
    
    # Acumulador de puntos por candidato: { "titulo": peso_total }
    candidatos_scores = {}
    
    #Sumamos afinidad directa
    for peli in peliculas_grupo:
        t_base = peli.get_titulo().lower()
        vecinos = grafo.obtener_vecinos(t_base)
        for vecino, peso in vecinos.items():
            if vecino not in titulos_grupo:
                candidatos_scores[vecino] = candidatos_scores.get(vecino, 0) + peso

    #Aplicamos Camino Mínimo
    pelis_puente = set()
    lista_titulos = list(titulos_grupo)
    
    for i in range(len(lista_titulos)):
        for j in range(i + 1, len(lista_titulos)):
            camino = grafo.bfs_camino(lista_titulos[i], lista_titulos[j])
            if camino and len(camino) > 2:
                # Los nodos intermedios son el puente mínimo entre ambas películas
                for nodo_intermedio in camino[1:-1]:
                    if nodo_intermedio not in titulos_grupo:
                        pelis_puente.add(nodo_intermedio)
                        # Bonus por conectar caminos mínimos entre el grupo
                        candidatos_scores[nodo_intermedio] = candidatos_scores.get(nodo_intermedio, 0) + 20

    if not candidatos_scores:
        print("\n❌ No se encontraron conexiones ni caminos mínimos entre estas películas.")
        return

    #Filtramos con ColaPrioridadHeap y desempatamos con el puntaje (rating)
    heap_recomendaciones = ColaPrioridadHeap(capacidad=10)
    
    for titulo_cand, peso_acumulado in candidatos_scores.items():
        peli_obj = mapa_peliculas.get(titulo_cand)
        if not peli_obj:
            continue
            
        try:
            rating = float(peli_obj.get_puntaje())
        except ValueError:
            rating = 0.0
            
        score_final = peso_acumulado + (rating / 10.0)
        heap_recomendaciones.insertar_con_score(score_final, peli_obj)

    top_10 = heap_recomendaciones.obtener_ranking_ordenado()

    # Preparamos los conjuntos combinados de todo el grupo para mostrar qué comparten
    dirs_grupo = {p.get_director() for p in peliculas_grupo if p.get_director() != ""}
    gens_grupo = set().union(*(set(p.get_genero()) for p in peliculas_grupo))
    acts_grupo = set().union(*(set(p.get_actores()) for p in peliculas_grupo))

    nombres_grupo = " + ".join([p.get_titulo() for p in peliculas_grupo])
    print(f"\n TOP {len(top_10)} RECOMENDACIONES PARA EL GRUPO [{nombres_grupo}]:")
    print("=" * 85)
    
    for i, (score, peli) in enumerate(top_10, start=1):
        titulo = peli.get_titulo()
        anio = peli.get_fecha_estreno()[:4]
        estrellas = peli.get_puntaje()
        peso_puro = int(score)
        
        coincidencias = []
        if peli.get_director() in dirs_grupo:
            coincidencias.append(f"Dir: {peli.get_director().title()}")
            
        generos_comunes = gens_grupo.intersection(set(peli.get_genero()))
        if generos_comunes:
            gens_str = ", ".join([g.title() for g in generos_comunes])
            coincidencias.append(f"Género: {gens_str}")
            
        actores_comunes = acts_grupo.intersection(set(peli.get_actores()))
        if actores_comunes:
            acts_str = ", ".join([a.title() for a in actores_comunes])
            coincidencias.append(f"Elenco: {acts_str}")
            
        detalle_comun = " | ".join(coincidencias) if coincidencias else "Conexión indirecta en red"
        etiqueta_puente = " [Puente Camino Mínimo]" if titulo.lower() in pelis_puente else ""
        
        print(f"{i}. {titulo} ({anio}) |  {estrellas} |  Afinidad: {peso_puro} pts{etiqueta_puente}")
        print(f"   Comparten con el grupo: {detalle_comun}")
    print("=" * 85)

    #Opción para guardar en la Watchlist
    print("\n¿Querés guardar alguna de estas recomendaciones en tu Watchlist?")
    while True:
        eleccion = input("Ingresá el número (1-10) para agregar (o '0' para volver): ").strip()
        
        if eleccion == "0":
            break
            
        try:
            idx = int(eleccion)
            if 1 <= idx <= len(top_10):
                pelicula_elegida = top_10[idx - 1][1]
                watchlist.agregar(pelicula_elegida)
            else:
                print(f"❌ Ingresá un número entre 1 y {len(top_10)}.")
        except ValueError:
            print("❌ Entrada inválida. Ingresá un número.")
def generar_joyas_ocultas(catalogo, pelicula_base, grafo, watchlist):
    titulo_base = pelicula_base.get_titulo().lower()
    candidatos_dfs = grafo.dfs_joyas_ocultas(titulo_base, prof_min=3, prof_max=6, limite_candidatos=50)

    if not candidatos_dfs:
        print(f"\n❌ No se encontraron joyas ocultas en profundidad para '{pelicula_base.get_titulo()}'.")
        return

    mapa_peliculas = {p.get_titulo().lower(): p for p in catalogo}
    caminos_por_titulo = {}
    heap_joyas = ColaPrioridadHeap(capacidad=10)

    for titulo_cand, profundidad, camino in candidatos_dfs:
        peli_obj = mapa_peliculas.get(titulo_cand)
        if not peli_obj:
            continue

        try:
            rating = float(peli_obj.get_puntaje())
        except ValueError:
            rating = 0.0

        # Priorizamos buen rating + un leve bonus por profundidad equilibrada
        score_joya = (rating * 10.0) + profundidad
        heap_joyas.insertar_con_score(score_joya, peli_obj)
        caminos_por_titulo[titulo_cand] = (profundidad, camino)

    top_joyas = heap_joyas.obtener_ranking_ordenado()

    print(f"\n TOP {len(top_joyas)} JOYAS OCULTAS (DFS PROFUNDO) DESDE '{pelicula_base.get_titulo().upper()}':")
    print("=" * 85)
    for i, (score, peli) in enumerate(top_joyas, start=1):
        titulo = peli.get_titulo()
        anio = peli.get_fecha_estreno()[:4]
        estrellas = peli.get_puntaje()
        generos = ", ".join(g.title() for g in peli.get_genero())
        prof, camino = caminos_por_titulo[titulo.lower()]
        ruta_str = " ➔ ".join(t.title() for t in camino)

        print(f"{i}. {titulo} ({anio}) |  {estrellas} |  Profundidad DFS: {prof} saltos")
        print(f"   Géneros: {generos}")
        print(f"   Cadena de conexión: {ruta_str}")
    print("=" * 85)

    peliculas_joyas = [peli for _, peli in top_joyas]
    ofrecer_guardar_watchlist(peliculas_joyas, watchlist)

#Videoteca (Opción 2)
def videoteca(catalogo, watchlist):
    while True:
        print("\n--- 🎞️ VIDEOTECA CINEFILLAPP ---")
        print("1. Buscar película por título")
        print("2. Buscar por actor / actriz")
        print("3. Buscar por director / directora")        
        print("4. Explorar categorías (Árbol n-ario + Filtro)")
        print("5. Volver al menú principal")
        
        opc = input("\nElegí una opción (1-5): ").strip()
        
        if opc == "1":
            termino = input("Ingresá el título a buscar: ")
            buscar_peli(catalogo, termino, watchlist)

        elif opc == "2":
            actor = input("Ingresá el nombre del actor o actriz: ")
            buscar_por_actor(catalogo, actor, watchlist)
            
        elif opc == "3":
            director = input("Ingresá el nombre del director o directora: ")
            buscar_por_director(catalogo, director, watchlist)
        
        elif opc == "4":
            print("\nEXPLORADOR INTERACTIVO DE CATEGORÍAS")
            print("Construyendo jerarquía de categorías...")
            arbol_universo = construir_arbol_categorias(catalogo)
            
            macro_categorias = arbol_universo.raiz.hijos
            if not macro_categorias:
                print("❌ No hay categorías disponibles.")
                continue
                
            print("\n Categorías principales:")
            for i, macro in enumerate(macro_categorias, start=1):
                print(f"{i}. {macro.nombre}")
                
            try:
                opc_macro = int(input("\nIngresá el número de la categoría principal (o 0 para volver): "))
                if opc_macro == 0:
                    continue
                
                if 1 <= opc_macro <= len(macro_categorias):
                    macro_seleccionada = macro_categorias[opc_macro - 1]
                    sub_categorias = macro_seleccionada.hijos
                    
                    if not sub_categorias:
                        print(f"\n❌ La categoría '{macro_seleccionada.nombre}' no tiene subcategorías.")
                        continue
                        
                    print(f"\n Subcategorías dentro de '{macro_seleccionada.nombre}':")
                    for j, sub in enumerate(sub_categorias, start=1):
                        print(f"{j}. {sub.nombre} ({len(sub.hijos)} elementos)")
                        
                    opc_sub = int(input("\nIngresá el número de la subcategoría (o 0 para volver): "))
                    if opc_sub == 0:
                        continue
                        
                    if 1 <= opc_sub <= len(sub_categorias):
                        sub_seleccionada = sub_categorias[opc_sub - 1]
                        peliculas_sub = [hijo.pelicula for hijo in sub_seleccionada.hijos if hijo.pelicula is not None]
                        
                        print(f"\n Películas en [{macro_seleccionada.nombre} ➔ {sub_seleccionada.nombre}] ({len(peliculas_sub)}):")
                        print("=" * 60)
                        if peliculas_sub:
                            for idx, peli in enumerate(peliculas_sub, start=1):
                                print(f"{idx}. {peli}")
                            print("=" * 60)
                            
                            # Nuevo menú de acciones sobre los resultados de esta categoría
                            print("\n¿Qué querés hacer con estos resultados?")
                            print("1. Filtrar estos resultados (por año, puntaje, actor, director, etc.)")
                            print("2. Guardar alguna en mi Watchlist")
                            print("3. Volver")
                            accion_cat = input("Elegí una opción (1-3): ").strip()
                            
                            if accion_cat == "1":
                                criterio = input("Ingresá el criterio de filtro (ej: 2014, 8, nolan, keanu): ")
                                filtrar_peli(peliculas_sub, criterio, watchlist)
                            elif accion_cat == "2":
                                ofrecer_guardar_watchlist(peliculas_sub, watchlist)
                        else:
                            print("❌ No hay películas registradas en esta subcategoría.")
                            print("=" * 60)
                    else:
                        print("\n❌ Número de subcategoría fuera de rango.")
                else:
                    print("\n❌ Número de categoría fuera de rango.")
            except ValueError:
                print("\n❌ Entrada inválida. Debés ingresar un número.")
                          
        elif opc == "5":
            break
        else:
            print("\n❌ Opción no válida. Ingresá un número del 1 al 5.")

#buscar y filtrar pelis
def buscar_peli(catalogo, termino, watchlist):
    encontrados = [p for p in catalogo if termino.lower() in p.get_titulo().lower()]

    if encontrados:
        print(f"\n Resultados para '{termino}' ({len(encontrados)}):")
        print("=" * 65)
        for i, peli in enumerate(encontrados, start=1):
            print(f"{i}. {peli}")
        print("=" * 65)
        
        # Ofrecemos agregar cualquiera de los resultados a la watchlist
        ofrecer_guardar_watchlist(encontrados, watchlist)
    else:
        print("\n❌ No se encontraron películas con ese título.")

def buscar_por_actor(catalogo, actor_buscado, watchlist):
    busqueda = actor_buscado.lower().strip()
    encontrados = [
        p for p in catalogo 
        if any(busqueda in actor for actor in p.get_actores())
    ]

    if encontrados:
        print(f"\n Películas con '{actor_buscado}' ({len(encontrados)}):")
        print("=" * 65)
        for i, peli in enumerate(encontrados, start=1):
            print(f"{i}. {peli} | Elenco: {', '.join(peli.get_actores()).title()}")
        print("=" * 65)
        ofrecer_guardar_watchlist(encontrados, watchlist)
    else:
        print(f"\n❌ No se encontraron películas con el actor/actriz '{actor_buscado}'.")

def buscar_por_director(catalogo, director_buscado, watchlist):
    busqueda = director_buscado.lower().strip()
    encontrados = [
        p for p in catalogo 
        if busqueda in p.get_director().lower()
    ]

    if encontrados:
        print(f"\n Películas dirigidas por '{director_buscado}' ({len(encontrados)}):")
        print("=" * 65)
        for i, peli in enumerate(encontrados, start=1):
            print(f"{i}. {peli}")
        print("=" * 65)
        ofrecer_guardar_watchlist(encontrados, watchlist)
    else:
        print(f"\n❌ No se encontraron películas del director/a '{director_buscado}'.")

#filtramos peliculas en el catalogo
def filtrar_peli(lista_peliculas, termino, watchlist=None):
    busqueda = termino.lower().strip()
    encontrados = []

    es_numero = False
    try:
        numero_base = float(busqueda)
        es_numero = True
    except ValueError:
        es_numero = False

    for p in lista_peliculas:
        coincide = False
        
        if es_numero:
            try:
                puntaje_peli = float(p.get_puntaje())
                if numero_base <= puntaje_peli < numero_base + 1:
                    coincide = True
            except ValueError:
                pass

        if not coincide:
            generos_texto = " ".join(p.get_genero()).lower()
            actores_texto = " ".join(p.get_actores()).lower()
            
            if (busqueda in p.get_tipo().lower() or
                busqueda in generos_texto or
                busqueda in p.get_director().lower() or
                busqueda in actores_texto or
                busqueda in p.get_puntaje().lower() or
                busqueda in p.get_fecha_estreno().lower()):
                coincide = True
                
        if coincide:
            encontrados.append(p)

    if encontrados:
        print(f"\n--- Resultados filtrados para '{termino}' ({len(encontrados)}) ---")
        print("=" * 65)
        for i, peli in enumerate(encontrados, start=1):
            print(f"{i}. {peli}")
        print("=" * 65)
        
        if watchlist is not None:
            ofrecer_guardar_watchlist(encontrados, watchlist)
    else:
        print(f"\n❌ No se encontraron coincidencias para '{termino}'.")
        
    return encontrados


#Top 10 (Opción 3)
class ColaPrioridadHeap:
    def __init__(self, capacidad=10): #top 10
        self.capacidad = capacidad
        self.heap = []             

    def _calcular_prioridad(self, pelicula): #prioridad por calificación y más nueva
       
        try:
            rating = float(pelicula.get_puntaje())
        except ValueError:
            rating = 0.0
            
        try:
            anio = int(pelicula.get_fecha_estreno()[:4])
        except (ValueError, IndexError):
            anio = 2000   #si no se da año, se utiliza el 2000 como generico
            
        # Fórmula prioriza: 90% el puntaje + 10% por año
        prioridad = (rating * 10.0) + (anio / 1000.0)
        return prioridad

    def insertar(self, pelicula):
        prioridad = self._calcular_prioridad(pelicula)
        elemento = (prioridad, pelicula)

        if len(self.heap) < self.capacidad:
            self.heap.append(elemento)
            self._sift_up(len(self.heap) - 1)
#si el heap está lleno, compara y quita
        else:
            if prioridad > self.heap[0][0]:
                self.heap[0] = elemento
                self._sift_down(0)

    def insertar_con_score(self, score_personalizado, pelicula):
        #Peso de grafo + rating
        elemento = (score_personalizado, pelicula)
        if len(self.heap) < self.capacidad:
            self.heap.append(elemento)
            self._sift_up(len(self.heap) - 1)
        else:
            if score_personalizado > self.heap[0][0]:
                self.heap[0] = elemento
                self._sift_down(0)

    def _sift_up(self, indice):
        padre = (indice - 1) // 2
        if padre >= 0 and self.heap[indice][0] < self.heap[padre][0]:
            self.heap[indice], self.heap[padre] = self.heap[padre], self.heap[indice]
            self._sift_up(padre)

    def _sift_down(self, indice):
        menor = indice
        izq = 2 * indice + 1
        der = 2 * indice + 2

        if izq < len(self.heap) and self.heap[izq][0] < self.heap[menor][0]:
            menor = izq
        if der < len(self.heap) and self.heap[der][0] < self.heap[menor][0]:
            menor = der

        if menor != indice:
            self.heap[indice], self.heap[menor] = self.heap[menor], self.heap[indice]
            self._sift_down(menor)

    def obtener_ranking_ordenado(self):
        elementos_copia = list(self.heap)
        elementos_copia.sort(key=lambda x: x[0], reverse=True)
        return elementos_copia

def mostrar_top_peliculas(catalogo, watchlist, n=10):
    print(f"\nTOP {n} MEJORES PELÍCULAS (ÁRBOL N-ARIO + HEAP)")
    
    #Elegimos género o subgénero en el que buscar
    termino = input("¿Qué género o subgénero buscás? \n(Dejar en blanco para todo el catálogo): ").strip().lower()
    
    if termino:
        #usamor un arbol n-ario
        arbol_categorias = construir_arbol_categorias(catalogo)
        nodos_encontrados = arbol_categorias.buscar_en_arbol(arbol_categorias.raiz, termino)
        
        catalogo_filtrado = []
        titulos_vistos = set()
        
        for nodo in nodos_encontrados:
            if nodo.pelicula is not None:
                titulo_clave = nodo.pelicula.get_titulo().lower()
                if titulo_clave not in titulos_vistos:
                    titulos_vistos.add(titulo_clave)
                    catalogo_filtrado.append(nodo.pelicula)
                    
        print(f"\ Rama encontrada para '{termino}': {len(catalogo_filtrado)} películas.")
    else:
        catalogo_filtrado = catalogo
        print("\nAnalizando todo el catálogo completo...")
        
    if not catalogo_filtrado:
        print(f"❌ No se encontraron películas asociadas a '{termino}'.")
        return
    
    #procesamos para armar el top 10
    heap = ColaPrioridadHeap(capacidad=n)
    for peli in catalogo_filtrado:
        heap.insertar(peli)
        
    ranking = heap.obtener_ranking_ordenado()
    
    print("\n" + "=" * 75)
    for i, (prio, peli) in enumerate(ranking, start=1):
        titulo = peli.get_titulo()
        anio = peli.get_fecha_estreno()[:4]
        rating = peli.get_puntaje()
        generos = ", ".join(peli.get_genero())
        
        print(f"{i:2}. {titulo:<25} ({anio}) |  {rating} |  [{generos}] | Score: {prio:.2f}")
    print("=" * 75)

    #agregar a watchlist
    peliculas_top = [peli for _, peli in ranking]
    ofrecer_guardar_watchlist(peliculas_top, watchlist)


#Whatchlist (Opción 4)
class Watchlist:
    def __init__(self, catalogo=None, archivo="watchlist_guardada.json"):
        # Usamos deque como Cola (FIFO): la primera peli que agregás es la primera que te sugiere ver
        self.cola = deque()
        # Set auxiliar para verificar duplicados
        self.titulos_guardados = set()
        self.archivo = archivo
        
        if catalogo is not None:
            self.cargar_desde_archivo(catalogo)

    def guardar_en_archivo(self):
        """Guarda los títulos de la cola en orden FIFO dentro de un JSON"""
        titulos_ordenados = [p.get_titulo() for p in self.cola]
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(titulos_ordenados, f, ensure_ascii=False, indent=2)

    def cargar_desde_archivo(self, catalogo):
        """Recupera la cola al iniciar el programa cruzando los títulos con el catálogo"""
        if not os.path.exists(self.archivo):
            return
            
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                titulos_guardados = json.load(f)
                
            mapa_catalogo = {p.get_titulo().lower(): p for p in catalogo}
            for titulo in titulos_guardados:
                clave = titulo.lower()
                peli_obj = mapa_catalogo.get(clave)
                if peli_obj and clave not in self.titulos_guardados:
                    self.cola.append(peli_obj)
                    self.titulos_guardados.add(clave)
        except (json.JSONDecodeError, IOError):
            print("⚠️ No se pudo leer el archivo previo de Watchlist. Se iniciará una lista nueva.")

    def agregar(self, pelicula):
        titulo_clave = pelicula.get_titulo().lower()
        if titulo_clave in self.titulos_guardados:
            print(f"⚠️ '{pelicula.get_titulo()}' ya estaba en tu Watchlist.")
            return False
        
        self.cola.append(pelicula)
        self.titulos_guardados.add(titulo_clave)
        self.guardar_en_archivo()
        print(f"✅ '{pelicula.get_titulo()}' agregada a tu Watchlist y guardada.")
        return True

    def ver_siguiente(self, perfil=None):
        """Muestra y saca de la lista la próxima película a mirar (Popleft O(1)) y la registra en el perfil"""
        if not self.cola:
            print("\n Tu Watchlist está vacía.")
            return None
        
        siguiente = self.cola.popleft()
        self.titulos_guardados.remove(siguiente.get_titulo().lower())
        self.guardar_en_archivo()
        print(f"\n ¡A preparar pochoclos! Te toca mirar: {siguiente}")

        if perfil is not None:
            while True:
                try:
                    entrada = input(f" Puntuala del 1 al 10 para guardarla como YA VISTA en tu perfil (o '0' para omitir): ").strip()
                    if entrada == "0":
                        print(" No se registró puntaje en el perfil.")
                        break
                    nota = float(entrada)
                    if 1.0 <= nota <= 10.0:
                        perfil.registrar_vista(siguiente, round(nota, 1))
                        break
                    else:
                        print("❌ El puntaje debe estar entre 1 y 10.")
                except ValueError:
                    print("❌ Entrada inválida. Ingresá un número del 1 al 10 (o '0' para omitir).")

        return siguiente

    def eliminar_por_indice(self, indice_usuario):
        """Elimina una película puntual según su posición (1 a N) manteniendo el orden de la cola"""
        if not self.cola:
            print("\n Tu Watchlist está vacía.")
            return False
            
        if 1 <= indice_usuario <= len(self.cola):
            # Convertimos temporalmente para extraer por índice
            lista_temp = list(self.cola)
            eliminada = lista_temp.pop(indice_usuario - 1)
            
            self.cola = deque(lista_temp)
            self.titulos_guardados.remove(eliminada.get_titulo().lower())
            self.guardar_en_archivo()
            
            print(f" '{eliminada.get_titulo()}' fue eliminada de tu Watchlist.")
            return True
        else:
            print(f"❌ Ingresá un número válido entre 1 y {len(self.cola)}.")
            return False

    def mostrar_lista(self):
        if not self.cola:
            print("\n Tu Watchlist está vacía. ¡Agregá películas desde el recomendador o la videoteca!")
            return False
            
        print(f"\n MI WATCHLIST ({len(self.cola)} pendientes - Orden de llegada):")
        print("=" * 65)
        for i, peli in enumerate(self.cola, start=1):
            print(f"{i}. {peli}")
        print("=" * 65)
        return True

def gestionar_watchlist(watchlist, perfil=None):
    while True:
        print("\n--- 🔖 MI WATCHLIST ---")
        print("1. Ver mi lista de pendientes")
        print("2. Marcar como vista / Sacar la próxima película a mirar (FIFO)")
        print("3. Eliminar una película específica de la lista")
        print("4. Volver al menú principal")
        
        opc = input("Elegí una opción (1-4): ").strip()
        
        if opc == "1":
            watchlist.mostrar_lista()
        elif opc == "2":
            watchlist.ver_siguiente(perfil)
        elif opc == "3":
            if watchlist.mostrar_lista():
                try:
                    num = int(input("\nIngresá el número de la película que querés eliminar (o 0 para cancelar): "))
                    if num != 0:
                        watchlist.eliminar_por_indice(num)
                except ValueError:
                    print("❌ Entrada inválida. Debés ingresar un número.")
        elif opc == "4":
            break
        else:
            print("❌ Opción no válida.")
class PerfilUsuario:
    def __init__(self, nombre_usuario, catalogo, archivo="perfiles_usuarios.json"):
        self.nombre = nombre_usuario.strip()
        self.archivo = archivo
        # Diccionario Hash O(1): { "titulo_lower": puntaje_float }
        self.vistas = {}
        self.cargar(catalogo)

    def _leer_todos_los_perfiles(self):
        if not os.path.exists(self.archivo):
            return {}
        try:
            with open(self.archivo, 'r', encoding='utf-8') as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError):
            return {}

    def guardar(self):
        datos = self._leer_todos_los_perfiles()
        datos[self.nombre] = self.vistas
        with open(self.archivo, 'w', encoding='utf-8') as f:
            json.dump(datos, f, ensure_ascii=False, indent=2)

    def cargar(self, catalogo):
        datos = self._leer_todos_los_perfiles()
        guardadas = datos.get(self.nombre, {})
        titulos_validos = {p.get_titulo().lower() for p in catalogo}
        # Validamos que existan en el catálogo activo
        self.vistas = {
            t.lower(): float(pts)
            for t, pts in guardadas.items()
            if t.lower() in titulos_validos
        }

    def ya_vista(self, titulo):
        return titulo.lower() in self.vistas

    def puntaje_usuario(self, titulo):
        return self.vistas.get(titulo.lower(), None)

    def registrar_vista(self, pelicula, puntaje):
        clave = pelicula.get_titulo().lower()
        es_actualizacion = clave in self.vistas
        self.vistas[clave] = puntaje
        self.guardar()
        if es_actualizacion:
            print(f"🔄 Puntaje actualizado: '{pelicula.get_titulo()}' ➔  {puntaje}/10")
        else:
            print(f"✅ Agregada a tu perfil ({self.nombre}): '{pelicula.get_titulo()}' ➔  {puntaje}/10")

    def eliminar_vista(self, titulo):
        clave = titulo.lower()
        if clave in self.vistas:
            del self.vistas[clave]
            self.guardar()
            print(f" '{titulo}' eliminada de tu historial.")
            return True
        return False

    def mostrar_perfil(self, catalogo):
        print(f"\n👤 PERFIL DE: {self.nombre.upper()} ({len(self.vistas)} películas vistas)")
        print("=" * 70)
        if not self.vistas:
            print(" Todavía no registraste películas vistas. ¡Agregá algunas para activar 'Tirar los dados'!")
            print("=" * 70)
            return

        mapa = {p.get_titulo().lower(): p for p in catalogo}
        ordenado = sorted(self.vistas.items(), key=lambda x: x[1], reverse=True)
        for i, (clave, pts) in enumerate(ordenado, start=1):
            peli = mapa.get(clave)
            if peli:
                print(f"{i}. {peli.get_titulo()} ({peli.get_fecha_estreno()[:4]}) | Tu puntaje:  {pts}/10 | Catálogo: {peli.get_puntaje()}")
        print("=" * 70)


def gestionar_perfil(perfil, catalogo):
    while True:
        print(f"\n--- 👤 MI PERFIL ({perfil.nombre}) ---")
        print("1. Ver mi historial de películas vistas y puntuadas")
        print("2. Registrar / Puntuar una película vista")
        print("3. Eliminar una película de mi historial")
        print("4. Volver al menú principal")

        opc = input("Elegí una opción (1-4): ").strip()

        if opc == "1":
            perfil.mostrar_perfil(catalogo)

        elif opc == "2":
            termino = input("\nIngresá el título de la película que viste: ").strip()
            encontrados = [p for p in catalogo if termino.lower() in p.get_titulo().lower()]
            if not encontrados:
                print("❌ No se encontraron películas con ese título.")
                continue

            print(f"\nResultados para '{termino}':")
            for i, p in enumerate(encontrados[:10], start=1):
                marca = f" [Ya vista:  {perfil.puntaje_usuario(p.get_titulo())}]" if perfil.ya_vista(p.get_titulo()) else ""
                print(f"{i}. {p.get_titulo()} ({p.get_fecha_estreno()[:4]}){marca}")

            try:
                sel = int(input("\nSeleccioná el número (0 para cancelar): "))
                if sel == 0:
                    continue
                if 1 <= sel <= len(encontrados[:10]):
                    elegida = encontrados[sel - 1]
                    nota = float(input(f"¿Qué puntaje le ponés a '{elegida.get_titulo()}' (1 a 10)?: "))
                    if 1.0 <= nota <= 10.0:
                        perfil.registrar_vista(elegida, round(nota, 1))
                    else:
                        print("❌ El puntaje debe estar entre 1 y 10.")
                else:
                    print("❌ Número fuera de rango.")
            except ValueError:
                print("❌ Entrada inválida.")

        elif opc == "3":
            if not perfil.vistas:
                print("\n Tu historial está vacío.")
                continue
            perfil.mostrar_perfil(catalogo)
            ordenado = sorted(perfil.vistas.items(), key=lambda x: x[1], reverse=True)
            try:
                num = int(input("Ingresá el número a eliminar (0 para cancelar): "))
                if 1 <= num <= len(ordenado):
                    perfil.eliminar_vista(ordenado[num - 1][0])
            except ValueError:
                print("❌ Entrada inválida.")

        elif opc == "4":
            break
        else:
            print("❌ Opción no válida.")
def tirar_los_dados(catalogo, perfil, grafo, watchlist):
    print("\n--- 🎲 TIRAR LOS DADOS (RECOMENDACIÓN EXPRESS POR PERFIL) ---")
    if not perfil.vistas:
        print(f"⚠️ {perfil.nombre}, necesitás agregar películas vistas a tu perfil para poder usar 'Tirar los dados'.")
        print(" Entrá a 'Mi Perfil' en el menú principal y puntuá al menos una película.")
        return

    mapa_peliculas = {p.get_titulo().lower(): p for p in catalogo}
    candidatos_scores = {}

    # Recorremos las películas vistas del perfil y propagamos afinidad en el grafo
    for titulo_visto, nota_usuario in perfil.vistas.items():
        # Multiplicador según cuánto le gustó al usuario (ej: nota 10 -> x2.0, nota 5 -> x1.0, nota 2 -> x0.4)
        factor_gusto = nota_usuario / 5.0
        vecinos = grafo.obtener_vecinos(titulo_visto)

        for vecino, peso in vecinos.items():
            # Excluimos películas que el usuario ya vio
            if perfil.ya_vista(vecino):
                continue
            candidatos_scores[vecino] = candidatos_scores.get(vecino, 0.0) + (peso * factor_gusto)

    if not candidatos_scores:
        print("❌ Ya viste todas las películas conectadas en este catálogo. ¡Increíble!")
        return

    # Usamos el Heap para quedarnos con las 15 mejores candidatas según tu perfil
    heap_dados = ColaPrioridadHeap(capacidad=15)
    for titulo_cand, score_acum in candidatos_scores.items():
        peli_obj = mapa_peliculas.get(titulo_cand)
        if not peli_obj:
            continue
        try:
            rating = float(peli_obj.get_puntaje())
        except ValueError:
            rating = 0.0
        heap_dados.insertar_con_score(score_acum + (rating / 10.0), peli_obj)

    mejores_candidatas = heap_dados.obtener_ranking_ordenado()

    while True:
        score_elegido, peli_elegida = random.choice(mejores_candidatas)
        print("\n ¡Los dados hablaron! Basado en tus gustos, te recomendamos:")
        print("=" * 75)
        print(f" {peli_elegida.get_titulo()} ({peli_elegida.get_fecha_estreno()[:4]}) |  {peli_elegida.get_puntaje()}")
        print(f" Géneros: {', '.join(g.title() for g in peli_elegida.get_genero())}")
        print(f" Director: {peli_elegida.get_director().title()}")
        print(f" Elenco: {', '.join(a.title() for a in peli_elegida.get_actores())}")
        print(f" Afinidad con tu perfil: {int(score_elegido)} pts")
        print("=" * 75)

        print("\n1. Guardar en mi Watchlist")
        print("2. Volver a tirar los dados")
        print("3. Volver al menú")
        acc = input("Elegí una opción (1-3): ").strip()

        if acc == "1":
            watchlist.agregar(peli_elegida)
            break
        elif acc == "2":
            continue
        else:
            break

#agregar a watchlist en las opciones
def ofrecer_guardar_watchlist(lista_peliculas, watchlist):    
    if not lista_peliculas:
        return
        
    print("\n¿Querés guardar alguna de estas películas en tu Watchlist?")
    while True:
        eleccion = input(f"Ingresá el número (1-{len(lista_peliculas)}) para agregar (o '0' para volver): ").strip()
        
        if eleccion == "0":
            break
            
        try:
            idx = int(eleccion)
            if 1 <= idx <= len(lista_peliculas):
                pelicula_elegida = lista_peliculas[idx - 1]
                watchlist.agregar(pelicula_elegida)
            else:
                print(f"❌ Ingresá un número entre 1 y {len(lista_peliculas)}.")
        except ValueError:
            print("❌ Entrada inválida. Ingresá un número.")


#LISTAR CATÁLOGO (Código interno 1)
#creamos los nodos para arbol
class Nodo:
    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.izquierda = None
        self.derecha = None

#creamos el arbol del catalogo
class ArbolCatalogo:
    def __init__(self):
        self.raiz = None

    def insertar(self, pelicula):
        if self.raiz is None:
            self.raiz = Nodo(pelicula)
        else:
            self._insertar_recursivo(self.raiz, pelicula)

    def _insertar_recursivo(self, nodo_actual, nueva_pelicula):
        if nueva_pelicula.get_titulo().lower() < nodo_actual.pelicula.get_titulo().lower():
            if nodo_actual.izquierda is None:
                nodo_actual.izquierda = Nodo(nueva_pelicula)
            else:
                self._insertar_recursivo(nodo_actual.izquierda, nueva_pelicula)
        else:
            if nodo_actual.derecha is None:
                nodo_actual.derecha = Nodo(nueva_pelicula)
            else:
                self._insertar_recursivo(nodo_actual.derecha, nueva_pelicula)

    
    def recorrido_inorder(self):
        self._inorder_recursivo(self.raiz)

    def _inorder_recursivo(self, nodo):
        if nodo is not None:
            self._inorder_recursivo(nodo.izquierda)
            print(nodo.pelicula)
            self._inorder_recursivo(nodo.derecha)

    def recorrido_preorder(self):
        self._preorder_recursivo(self.raiz)

    def _preorder_recursivo(self, nodo):
        if nodo is not None:
            print(nodo.pelicula.get_titulo())
            self._preorder_recursivo(nodo.izquierda)
            self._preorder_recursivo(nodo.derecha)

    def recorrido_postorder(self):
        self._postorder_recursivo(self.raiz)

    def _postorder_recursivo(self, nodo):
        if nodo is not None:
            self._postorder_recursivo(nodo.izquierda)
            self._postorder_recursivo(nodo.derecha)
            print(nodo.pelicula.get_titulo())


#ENFERMAR ARBOL (Código interno 2)
def calcular_altura(nodo):
    if nodo is None: return 0
    return 1 + max(calcular_altura(nodo.izquierda), calcular_altura(nodo.derecha))

def experimento_desbalance(catalogo):
    sys.setrecursionlimit(5000) 
    
    print("\n--- ⚠️ EXPERIMENTO TP4: BST SANO VS ENFERMO ---")
    print("1. Listar catálogo con Árbol Sano (Datos originales)")
    print("2. Listar catálogo con Árbol Enfermo (Datos ya ordenados A-Z)")
    
    opc = input("\nElegí una opción (1-2): ")
    muestra = catalogo[:800] 
    
    if opc == "1":
        print("\n Construyendo Árbol SANO (datos mezclados)...")
        datos_insertar = muestra
        
        arbol_sano = ArbolCatalogo()
        
        inicio_tiempo = time.time()
        for peli in datos_insertar:
            arbol_sano.insertar(peli)
        fin_tiempo = time.time()
        tiempo_sano = fin_tiempo - inicio_tiempo
        
        altura_sano = calcular_altura(arbol_sano.raiz)
        altura_ideal = math.ceil(math.log2(len(datos_insertar)))
        
        print("\n--- LISTADO DE PELÍCULAS (ÁRBOL SANO) ---")
        arbol_sano.recorrido_inorder()
        
        print("\n" + "="*50)
        print(" DIAGNÓSTICO DEL ÁRBOL SANO")
        print("="*50)
        print(f"Muestra procesada:     {len(datos_insertar)} películas")
        print(f"Altura ideal O(log n): {altura_ideal} pisos")
        print(f"Altura REAL:           {altura_sano} pisos")
        print(f"Tiempo de armado:      {tiempo_sano:.5f} segundos")
        print("="*50)
        print("✅ DIAGNÓSTICO: Al ingresar datos desordenados, el árbol se balancea naturalmente.")
        print("Para ver cómo este mismo árbol colapsa, volvé a entrar y elegí la opción 2.")
        
    elif opc == "2":
        print("\n Construyendo Árbol ENFERMO (datos ordenados A-Z)...")
        datos_insertar = sorted(muestra, key=lambda x: x.get_titulo().lower())
        
        arbol_enfermo = ArbolCatalogo()
        
        inicio_tiempo = time.time()
        for peli in datos_insertar:
            arbol_enfermo.insertar(peli)
        fin_tiempo = time.time()
        tiempo_enf = fin_tiempo - inicio_tiempo
        
        altura_enf = calcular_altura(arbol_enfermo.raiz)
        altura_ideal = math.ceil(math.log2(len(datos_insertar)))
        
        print("\n--- LISTADO DE PELÍCULAS (ÁRBOL ENFERMO) ---")
        arbol_enfermo.recorrido_inorder()
        
        print("\n" + "="*50)
        print(" DIAGNÓSTICO DEL ÁRBOL ENFERMO")
        print("="*50)
        print(f"Altura ideal O(log n): {altura_ideal} pisos")
        print(f"Altura REAL (O(n)):    {altura_enf} pisos")
        print(f"Tiempo de armado:      {tiempo_enf:.5f} segundos")
        print("="*50)
        
        print("\nEl árbol colapsó. ¿Qué hacemos ahora?")
        print("1. Listar datos con Árbol AVL y comparar")
        print("2. Volver al menú principal")
        
        opc_avl = input("Elegí una opción (1-2): ")
        
        if opc_avl == "1":
            print("\n Construyendo Árbol AVL (curando los datos sobre la marcha)...")
            arbol_avl = ArbolAVL()
            
            inicio_avl = time.time()
            for peli in datos_insertar:
                arbol_avl.insertar(peli)
            fin_avl = time.time()
            tiempo_avl = fin_avl - inicio_avl
            
            altura_avl = arbol_avl._obtener_altura(arbol_avl.raiz)
            
            print("\n--- LISTADO DE PELÍCULAS (ÁRBOL AVL) ---")
            arbol_avl.recorrido_inorder()
            
            print("\n" + "="*65)
            print(" COMPARACIÓN DEFINITIVA: BST ENFERMO vs AVL SANO")
            print("="*65)
            print(f"Muestra procesada: {len(datos_insertar)} películas ya ordenadas")
            print("-" * 65)
            print(f"{'MÉTRICA':<15} | {'BST TRADICIONAL (ENFERMO)':<25} | {'ÁRBOL AVL (CURADO)'}")
            print("-" * 65)
            print(f"{'Altura (pisos)':<15} | {altura_enf:<25} | {altura_avl}")
            print(f"{'Tiempo (seg)':<15} | {tiempo_enf:<25.5f} | {tiempo_avl:.5f}")
            print("="*65)
            
            if altura_avl <= altura_ideal + 1:
                print("✅ ÉXITO: El AVL aplicó sus rotaciones y recuperó la eficiencia O(log n).")
            print("="*65)
            
    else:
        print("\n❌ Opción no válida.")


#GRAFO (Código interno 3)
class GrafoPeliculas:
    def __init__(self):
        # Lista de adyacencia: { "Titulo": { "Titulo_Vecino": peso, ... } }
        self.adyacencia = {}

    def agregar_vertice(self, titulo):
        if titulo not in self.adyacencia:
            self.adyacencia[titulo] = {}

    def agregar_arista(self, titulo1, titulo2, peso):
        # Grafo no dirigido
        self.adyacencia[titulo1][titulo2] = peso
        self.adyacencia[titulo2][titulo1] = peso

    def obtener_vecinos(self, titulo):
        return self.adyacencia.get(titulo, {})

    def bfs_camino(self, inicio, objetivo):
        """Busca el camino más corto (en saltos) entre dos películas"""
        if inicio not in self.adyacencia or objetivo not in self.adyacencia:
            return None

        visitados = set([inicio])
        cola = deque([[inicio]]) 

        while cola:
            camino = cola.popleft()
            nodo_actual = camino[-1]

            if nodo_actual == objetivo:
                return camino

            for vecino in self.adyacencia.get(nodo_actual, {}):
                if vecino not in visitados:
                    visitados.add(vecino)
                    nuevo_camino = list(camino)
                    nuevo_camino.append(vecino)
                    cola.append(nuevo_camino)
        return None

    def dfs_explorar(self, inicio, limite=10):
        #Explora la red en profundidad
        
        if inicio not in self.adyacencia:
            return []
        
        visitados = set()
        resultado = []
        
        def _dfs_recursivo(nodo):
            if nodo in visitados or len(resultado) >= limite:
                return
            visitados.add(nodo)
            resultado.append(nodo)
            
            #Ordenamos los vecinos
            vecinos_ordenados = sorted(self.adyacencia.get(nodo, {}).items(), key=lambda x: x[1], reverse=True)
            for vecino, _ in vecinos_ordenados:
                if len(resultado) >= limite:
                    break
                _dfs_recursivo(vecino)
                
        _dfs_recursivo(inicio)
        return resultado
    def dfs_joyas_ocultas(self, inicio, prof_min=3, prof_max=6, limite_candidatos=40):
        """Recorre el grafo en profundidad (DFS) buscando nodos conectados a distancia intermedia"""
        if inicio not in self.adyacencia:
            return []

        vecinos_directos = set(self.adyacencia.get(inicio, {}).keys())
        visitados = set([inicio])
        candidatos = []  # Guardará tuplas: (titulo, profundidad, camino_recorrido)

        def _dfs(nodo_actual, profundidad, camino):
            if len(candidatos) >= limite_candidatos or profundidad > prof_max:
                return

            # Si estamos en la profundidad ideal y NO es una recomendación obvia (vecino directo)
            if profundidad >= prof_min and nodo_actual not in vecinos_directos:
                candidatos.append((nodo_actual, profundidad, list(camino)))

            # Ordenamos vecinos por mayor afinidad para seguir una cadena coherente
            vecinos_ordenados = sorted(
                self.adyacencia.get(nodo_actual, {}).items(),
                key=lambda x: x[1],
                reverse=True
            )

            for vecino, _ in vecinos_ordenados:
                if len(candidatos) >= limite_candidatos:
                    break
                if vecino not in visitados:
                    visitados.add(vecino)
                    camino.append(vecino)
                    _dfs(vecino, profundidad + 1, camino)
                    camino.pop()

        _dfs(inicio, 0, [inicio])
        return candidatos

def construir_red_peliculas(catalogo):
    grafo = GrafoPeliculas()
    
    #Preprocesamos los datos para evitar cálculos repetitivos
    print("   -> (Optimizando datos para la red...)")
    datos_procesados = []
    for p in catalogo:
        titulo = p.get_titulo().lower()
        grafo.agregar_vertice(titulo)
        #Convertimos los actores a set UNA SOLA VEZ por película
        datos_procesados.append({
            "titulo": titulo,
            "director": p.get_director(),
            "actores": set(p.get_actores()),
            "generos": set(p.get_genero()) 
        })
        
    #Calculamos las conexiones cruzando los datos optimizados
    total = len(datos_procesados)
    print(f"   -> (Calculando conexiones entre {total} películas. Esto tomará unos segundos...)")
    
    for i in range(total):
        #Mini reporte de progreso para saber que no está colgado
        if i % 1000 == 0 and i > 0:
            print(f"      ... {i} películas cruzadas ...")
            
        p1 = datos_procesados[i]
        for j in range(i + 1, total):
            p2 = datos_procesados[j]
            
            peso = 0
            # Por director: 20 puntos
            if p1["director"] == p2["director"] and p1["director"] != "":
                peso += 20

            # Por cada actor en común: 10 puntos
            comunes = p1["actores"].intersection(p2["actores"])
            if comunes:
                peso += len(comunes) * 10

            # Por cada género en común: 8 puntos
            generos_comunes = p1["generos"].intersection(p2["generos"])
            if generos_comunes:
                peso += len(generos_comunes) * 8
            
            if peso > 0:
                grafo.agregar_arista(p1["titulo"], p2["titulo"], peso)
                
    return grafo
           
def explorar_grafo(grafo):
    print("\n🕸️ RED DE PELÍCULAS (GRAFO ACTIVO)...")
    print(f" Red lista con {len(grafo.adyacencia)} producciones conectadas.")
            
    print("\n--- MENÚ DEL GRAFO y RECORRIDOS ---")
    print("1. Ver conexiones directas de una película (Consulta TP)")
    print("2. Encontrar camino más corto entre dos películas (BFS)")
    print("3. Explorar red en profundidad (DFS)")
    print("4. Volver al menú principal")
    opc = input("Elegí una opción (1-4): ").strip()
    
    if opc == "1":
        termino = input("Ingresá el título de la película: ").strip().lower()
        vecinos = grafo.obtener_vecinos(termino)
        if vecinos:
            print(f"\n Películas conectadas directamente con '{termino.title()}':")
            vecinos_ordenados = sorted(vecinos.items(), key=lambda x: x[1], reverse=True)
            for v, peso in vecinos_ordenados[:10]: 
                print(f"   - {v.title()} (Fuerza de conexión: {peso})")
        else:
            print("❌ Película no encontrada o no tiene conexiones en este catálogo.")
            
    elif opc == "2":
        inicio = input("Película de origen: ").strip().lower()
        objetivo = input("Película de destino: ").strip().lower()
        camino = grafo.bfs_camino(inicio, objetivo)
        if camino:
            print(f"\n Camino más corto encontrado ({len(camino) - 1} saltos):")
            for idx, p in enumerate(camino):
                print(f"   {idx}. {p.title()}")
        else:
            print("❌ No se encontró un camino conectando ambas películas.")

    elif opc == "3":
        inicio = input("Película inicial para explorar en profundidad: ").strip().lower()
        profundidad = grafo.dfs_explorar(inicio, limite=10)
        if profundidad:
            print(f"\n Exploración en profundidad (DFS) desde '{inicio.title()}':")
            for idx, p in enumerate(profundidad, start=1):
                print(f"   {idx}. {p.title()}")
        else:
            print("❌ Película no encontrada en la red.")
    
    elif opc == "4":
        return
    else:
        print("❌ Opción no válida.")




#Menú
#Menú
def iniciar_menu(catalogo):
    grafo_peliculas = obtener_o_cargar_grafo(catalogo)
    mi_watchlist = Watchlist(catalogo)

    nombre_perfil = input("\n👤 Ingresá tu nombre de usuario (para cargar o crear tu perfil): ").strip() or "Invitado"
    mi_perfil = PerfilUsuario(nombre_perfil, catalogo)
    print(f"✨ ¡Bienvenido/a, {mi_perfil.nombre}! ({len(mi_perfil.vistas)} películas vistas cargadas)")
    
    while True:
        print("\n ")
        print("    -CINEFILLAPP-   ")
        print(" ")
        print("\n")
        print("1. ✨  Recomendación inteligente (Grafo + Heap + DFS)")
        print("2. 🎞️  Videoteca (Buscar y Explorar Categorías)")
        print("3. 🥇  Ver top 10 (Heap)")
        print("4. 🔖  Mi Watchlist (Cola FIFO)")
        print("5. 🎲  Tirar los dados (Recomendación rápida por perfil)")
        print("6. 👤  Mi Perfil (Películas vistas y puntajes)")
        print("7. 🚪  Salir")

        opcion = input("\nElegí una opción (1-7): ").strip()
        
        if opcion == "1":
            recomendar_peli(catalogo, grafo_peliculas, mi_watchlist, mi_perfil)
            
        elif opcion == "2":
            videoteca(catalogo, mi_watchlist)

        elif opcion == "3":
            mostrar_top_peliculas(catalogo, mi_watchlist, n=10)

        elif opcion == "4":
            gestionar_watchlist(mi_watchlist, mi_perfil)

        elif opcion == "5":
            tirar_los_dados(catalogo, mi_perfil, grafo_peliculas, mi_watchlist)

        elif opcion == "6":
            gestionar_perfil(mi_perfil, catalogo)

        elif opcion == "7":
            print("\n¡Gracias por usar CinefillApp! Saliendo...")
            break

        #SUBMENÚ OCULTO
        elif opcion.upper() in ("CÓDIGO", "CODIGO"):
            print("\n--- OPCIONES DE CÓDIGO INTERNO ---")
            print("1.  Listar todo el catálogo (BST)")
            print("2.  EXPERIMENTO TP4: Enfermar al árbol")
            print("3.  Explorar Red de Películas (Grafos / BFS / DFS)")
            print("4.   Volver al menú principal")

            sub_opcion = input("\nElegí una opción (1-4): ").strip()

            if sub_opcion == "1":
                print("\n--- CATÁLOGO COMPLETO (A-Z) ---")
                print("Listando películas... por favor espere.")
                arbol_catalogo = ArbolCatalogo()
                for peli in catalogo:
                    arbol_catalogo.insertar(peli)
                arbol_catalogo.recorrido_inorder()
                print("-------------------------------")

            elif sub_opcion == "2":
                experimento_desbalance(catalogo)

            elif sub_opcion == "3":
                explorar_grafo(grafo_peliculas)

            elif sub_opcion == "4":
                continue

            else:
                print("\n❌ Opción no válida. Ingresá un número del 1 al 4.")
            
        else:
            print("\n❌ Opción no válida. Ingresá un número del 1 al 7.")

#Inicio del menú
if __name__ == "__main__":
    iniciar_menu(mi_catalogo)



