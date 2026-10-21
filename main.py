#importamos el archivo csv
import csv
import sys
import math
import time

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
        self._director = director.strip().lower() # Lo pasamos a minúscula para comparar más fácil
        
       
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
        return f"[{self._tipo}] {self._titulo} ({self._fecha_estreno[:4]}) dir. {self._director} - ⭐ {self._puntaje}"

#leemos el archivo csv
mi_catalogo = []

with open('catalogo.csv', encoding='utf-8') as archivo:
        lector = csv.reader(archivo)
        next(lector)

#agregamos los datos a la lista
        for fila in lector:
            nueva_prod = Produccion(fila[0], fila[1], fila[2], fila[3], fila[4], fila[5], fila[6], fila[7])
            mi_catalogo.append(nueva_prod)

#creamos los nodos
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

    # --- RECORRIDOS OBLIGATORIOS tp3 (solo usamos inorder) ---
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
        return f"📁 [{self.nombre}]"

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
            print("  " * (nivel + 1) + f"⭐ {nodo.pelicula}")
            
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

#para que se construya con la base de datos
def construir_arbol_categorias(catalogo):
    arbol = ArbolGeneral("Películas")
    
    #categorias principales y subcategorias
    estructura = {
        "Ciencia ficción": {
            "Cyberpunk": ["cyberpunk"],
            "Viajes temporales": ["viajes temporales", "tiempo", "time travel"],
            "Inteligencia artificial": ["inteligencia artificial", "ia", "robot", "androide"],
            "Otros Sci-Fi": []
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
        }
    }
    
    #nodos principales y subnodos
    nodos_macros = {}
    nodos_subs = {}
    titulos_agregados = set()

    #construimos las macrocategorias y sus subcategorias
    for macro, subs in estructura.items():
        nodo_macro = NodoGeneral(macro)
        arbol.raiz.agregar_hijo(nodo_macro)
        nodos_macros[macro] = nodo_macro
        nodos_subs[macro] = {}
        
        for sub in subs.keys():
            nodo_sub = NodoGeneral(sub)
            nodo_macro.agregar_hijo(nodo_sub)
            nodos_subs[macro][sub] = nodo_sub

    nodo_otros = NodoGeneral("Otros")
    arbol.raiz.agregar_hijo(nodo_otros)
    nodo_otros_gen = NodoGeneral("General")
    nodo_otros.agregar_hijo(nodo_otros_gen)

    #clasificamos las peliculas en su subcategoria correspondiente
    for peli in catalogo:
        generos_peli = peli.get_genero()
        titulo_peli = peli.get_titulo().lower()
        
        if titulo_peli in titulos_agregados:
            continue
            
        colocada = False

        for macro, subs in estructura.items():
            if colocada: 
                break
            for sub, keywords in subs.items():
                if "Otros" in sub:
                    continue
                if any(any(kw in g for kw in keywords) for g in generos_peli):
                    nodo_peli = NodoGeneral(peli.get_titulo(), pelicula=peli)
                    nodos_subs[macro][sub].agregar_hijo(nodo_peli)
                    titulos_agregados.add(titulo_peli)
                    colocada = True
                    break
        
        #si no encaja lo mandamos a "otros"
        if not colocada:
            macro_colocada = False
            for macro, subs in estructura.items():
                if any(macro.lower() in g for g in generos_peli):
                    fallback_sub = [s for s in subs.keys() if "Otros" in s][0]
                    if titulo_peli not in titulos_agregados:
                        nodo_peli = NodoGeneral(peli.get_titulo(), pelicula=peli)
                        nodos_subs[macro][fallback_sub].agregar_hijo(nodo_peli)
                        titulos_agregados.add(titulo_peli)
                    macro_colocada = True
                    colocada = True
                    break
            
            if not macro_colocada:
                if titulo_peli not in titulos_agregados:
                    nodo_peli = NodoGeneral(peli.get_titulo(), pelicula=peli)
                    nodo_otros_gen.agregar_hijo(nodo_peli)
                    titulos_agregados.add(titulo_peli)
                        
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


#buscamos peliculas en el catalogo
#ACÁ ESTA LA ESTRATEGIA DE BUSQUEDA SECUENCIAL
def buscar_peli(catalogo, termino):
    encontrados = [p for p in catalogo if termino.lower() in p.get_titulo().lower()]

    if encontrados:
        for peli in encontrados:
            print(peli)
    else:
        print("\n No se encontraron películas con ese título.")

#filtramos peliculas en el catalogo
def filtrar_peli(catalogo, termino):
    busqueda = termino.lower().strip()

    encontrados = []

    #evaluamos la categorias si es un número para calificación o es una palabra
    es_numero = False
    try:
        numero_base = float(busqueda)
        es_numero = True
    except ValueError:
        es_numero = False

    for p in catalogo:
        coincide = False
        
        #si es un numero del 1 al 10 buscamos en las calificaciones
        if es_numero:
            try:
                puntaje_peli = float(p.get_puntaje())
                if numero_base <= puntaje_peli < numero_base + 1:
                    coincide = True
            except ValueError:
                pass

        #buscamos en el resto si no es un número
        if not coincide:
            if (busqueda in p.get_tipo().lower() or
                busqueda in p.get_genero().lower() or
                busqueda in p.get_director().lower() or
                busqueda in p.get_actores().lower() or
                busqueda in p.get_puntaje().lower() or
                busqueda in p.get_fecha_estreno().lower()):
                coincide = True
                
        if coincide:
            encontrados.append(p)
            

    if encontrados:
        print(f"\n--- Resultados para '{termino}' ({len(encontrados)}) ---")
        for peli in encontrados:
            print(peli)
    else:
        print(f"\n No se encontraron coincidencias para '{termino}'.")

        
# funcion de recomendación en beta

def recomendar_peli(catalogo):
    print("\n--- RECOMENDACIÓN DE PELÍCULAS ---")
    termino = input("¿En qué película basamos tu recomendación?: ")
    
   
    encontrados = [p for p in catalogo if termino.lower() in p.get_titulo().lower()]
    
    if encontrados:
        print(f"\nEncontramos estas películas para '{termino}':")
        for i, peli in enumerate(encontrados, start=1):
            print(f"{i}. {peli.get_titulo()} ({peli.get_fecha_estreno()[:4]})")
        
     
        try:
            seleccion = int(input("\nIngresá el número de la película exacta (o 0 para cancelar): "))
            
            if seleccion == 0:
                return 
                
            if 1 <= seleccion <= len(encontrados):
                pelicula_base = encontrados[seleccion - 1]
                print(f"\n🎬 Analizando '{pelicula_base.get_titulo()}'...")
                print("Generando recomendaciones... (Esto puede tardar un segundo)")
                
                
                generar_recomendaciones(catalogo, pelicula_base)
                
            else:
                print("\n❌ Número fuera de rango.")
        except ValueError:
            print("\n❌ Entrada inválida. Debés ingresar un número.")
    else:
        print("\n❌ No se encontraron películas con ese título para basar la recomendación.")

def generar_recomendaciones(catalogo, pelicula_base):
    recomendaciones = []
    
    
    director_base = pelicula_base.get_director()
    actores_base = set(pelicula_base.get_actores())
    generos_base = set(pelicula_base.get_genero())
    
    for peli in catalogo:
      
        if peli.get_titulo().lower() == pelicula_base.get_titulo().lower():
            continue
            
        puntaje_similitud = 0
        

        if peli.get_director() == director_base and director_base != "":
            puntaje_similitud += 30
            
    
        actores_peli = set(peli.get_actores())
        actores_comun = actores_base.intersection(actores_peli)
        puntaje_similitud += len(actores_comun) * 15
        
  
        generos_peli = set(peli.get_genero())
        generos_comun = generos_base.intersection(generos_peli)
        puntaje_similitud += len(generos_comun) * 10
        

        if puntaje_similitud > 0:
            try:
                calificacion = float(peli.get_puntaje())
                puntaje_similitud += (calificacion * 3)
            except ValueError:
                pass 
                
   
        if puntaje_similitud > 0:
            recomendaciones.append((puntaje_similitud, peli))
            
   
    recomendaciones.sort(key=lambda x: x[0], reverse=True)
    
  
    print("\n🏆 TOP 10 RECOMENDACIONES:")
    if not recomendaciones:
        print("❌ No encontramos películas lo suficientemente similares en el catálogo.")
    else:
        for i, (pts, peli) in enumerate(recomendaciones[:10], start=1):
            titulo = peli.get_titulo()
            anio = peli.get_fecha_estreno()[:4]
            estrellas = peli.get_puntaje()

            print(f"{i}. {titulo} ({anio}) | ⭐ {estrellas} | ⚡ Score: {pts:.1f} pts")

# Consigna enfermar el árbol tp4

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
        print("\n🌲 Construyendo Árbol SANO (datos mezclados)...")
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
        print("📊 DIAGNÓSTICO DEL ÁRBOL SANO")
        print("="*50)
        print(f"Muestra procesada:     {len(datos_insertar)} películas")
        print(f"Altura ideal O(log n): {altura_ideal} pisos")
        print(f"Altura REAL:           {altura_sano} pisos")
        print(f"Tiempo de armado:      {tiempo_sano:.5f} segundos")
        print("="*50)
        print("✅ DIAGNÓSTICO: Al ingresar datos desordenados, el árbol se balancea naturalmente.")
        print("Para ver cómo este mismo árbol colapsa, volvé a entrar y elegí la opción 2.")
        
    elif opc == "2":
        print("\n🥀 Construyendo Árbol ENFERMO (datos ordenados A-Z)...")
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
        print("📊 DIAGNÓSTICO DEL ÁRBOL ENFERMO")
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
            print("\n✨ Construyendo Árbol AVL (curando los datos sobre la marcha)...")
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
            print("🏆 COMPARACIÓN DEFINITIVA: BST ENFERMO vs AVL SANO")
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

def iniciar_menu(catalogo):
    while True:
        print("\n====================")
        print("    CINEFILLAPP 🎬   ")
        print("====================")
        print("¿Todavía no decidiste qué mirar? Te ayudamos.\n")
        print("1. Recomendación por película")
        print("2. Listar todo el catálogo")
        print("3. Buscar película por título")
        print("4. Filtrar")
        print("5. Explorar categorías (Árbol n-ario)")
        print("6. Salir")
        print("7. ⚠️ EXPERIMENTO TP4: Enfermar al árbol")
        
        opcion = input("\nElegí una opción (1-7): ")
        
        if opcion == "1":
            recomendar_peli(catalogo)
            
        elif opcion == "2":
            print("\n--- CATÁLOGO COMPLETO (A-Z) ---")
            print("Listando peliculas... por favor espere.")
            arbol_catalogo = ArbolCatalogo()
            for peli in catalogo:
                arbol_catalogo.insertar(peli)
            arbol_catalogo.recorrido_inorder()
            print("-------------------------------")
            
        elif opcion == "3":
            termino = input("Ingresá el título a buscar: ")
            buscar_peli(catalogo, termino)
            
        elif opcion == "4":
            termino = input("Ingresá tipo, género, director, actores, año o calificación: ")
            filtrar_peli(catalogo, termino)
            
        elif opcion == "5":
            print("\n--- 🌲 EXPLORADOR INTERACTIVO DE CATEGORÍAS ---")
            print("Construyendo jerarquía de categorías...")
            arbol_universo = construir_arbol_categorias(catalogo)
            
            # Obtenemos las macrocategorías (los hijos directos de la raíz)
            macro_categorias = arbol_universo.raiz.hijos
            if not macro_categorias:
                print("❌ No hay categorías disponibles.")
                continue
                
            print("\n📁 Categorías principales:")
            for i, macro in enumerate(macro_categorias, start=1):
                print(f"{i}. {macro.nombre}")
                
            try:
                opc_macro = int(input("\nIngresá el número de la categoría principal (o 0 para volver): "))
                if opc_macro == 0:
                    continue
                
                if 1 <= opc_macro <= len(macro_categorias):
                    macro_seleccionada = macro_categorias[opc_macro - 1]
                    
                    # Obtenemos las subcategorías de la macrocategoría elegida
                    sub_categorias = macro_seleccionada.hijos
                    if not sub_categorias:
                        print(f"\n❌ La categoría '{macro_seleccionada.nombre}' no tiene subcategorías.")
                        continue
                        
                    print(f"\n📁 Subcategorías dentro de '{macro_seleccionada.nombre}':")
                    for j, sub in enumerate(sub_categorias, start=1):
                        print(f"{j}. {sub.nombre} ({len(sub.hijos)} elementos)")
                        
                    opc_sub = int(input("\nIngresá el número de la subcategoría (o 0 para volver): "))
                    if opc_sub == 0:
                        continue
                        
                    if 1 <= opc_sub <= len(sub_categorias):
                        sub_seleccionada = sub_categorias[opc_sub - 1]
                        
                        # Filtramos los nodos que tengan películas asociadas
                        peliculas_sub = [hijo for hijo in sub_seleccionada.hijos if hijo.pelicula is not None]
                        
                        print(f"\n🎬 Películas en [{macro_seleccionada.nombre} ➔ {sub_seleccionada.nombre}] ({len(peliculas_sub)}):")
                        print("=" * 60)
                        if peliculas_sub:
                            for idx, nodo_peli in enumerate(peliculas_sub, start=1):
                                print(f"{idx}. {nodo_peli.pelicula}")
                        else:
                            print("❌ No hay películas registradas en esta subcategoría.")
                        print("=" * 60)
                    else:
                        print("\n❌ Número de subcategoría fuera de rango.")
                else:
                    print("\n❌ Número de categoría fuera de rango.")
            except ValueError:
                print("\n❌ Entrada inválida. Debés ingresar un número.")
     
        
        elif opcion == "6":
            print("\n¡Gracias por usar CinefillApp! Saliendo...")
            break
            
        elif opcion == "7":
           
            experimento_desbalance(catalogo)

        else:
            print("\n❌ Opción no válida. Ingresá un número del 1 al 7.")


if __name__ == "__main__":
    iniciar_menu(mi_catalogo)
