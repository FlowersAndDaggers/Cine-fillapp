#importamos el archivo csv
import csv

#creamos la clase produccion
class Produccion:
    def __init__ (self, id_prod, titulo, tipo, genero, fecha_estreno, puntaje, director, actores):

#ponemos todos los datos en privado 
        self._id = id_prod
        self._titulo = titulo
        self._tipo = tipo
        self._genero = genero
        self._fecha_estreno = fecha_estreno
        self._puntaje = puntaje
        self._director = director
        self._actores = actores

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

class Nodo:
    def __init__(self, pelicula):
        self.pelicula = pelicula
        self.izquierda = None
        self.derecha = None

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


#buscamos peliculas en el catalogo
#ACÁ ESTA LA ESTRATEGIA DE BUSQUEDA SECUENCIAL
def buscar_peli(catalogo, termino):
    encontrados = [p for p in catalogo if termino.lower() in p.get_titulo().lower()]
    #######lower es estetica, no sé si ponerlo########

    if encontrados:
        for peli in encontrados:
            print(peli)
    else:
        print("\n No se encontraron películas con ese título.")

#filtramos peliculas en el catalogo
def filtrar_peli(catalogo, termino):
    busqueda = termino.lower().strip()
    #######lo mismo con strip, es estetica como lower#######
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
                ########devuelta lower#######
                
        if coincide:
            encontrados.append(p)
            

    if encontrados:
        print(f"\n--- Resultados para '{termino}' ({len(encontrados)}) ---")
        for peli in encontrados:
            print(peli)
    else:
        print(f"\n No se encontraron coincidencias para '{termino}'.")

        
# ==========================================
# NUEVA FUNCIÓN DE RECOMENDACIÓN todavía no esta terminada
# ==========================================
def recomendar_peli(catalogo):
    print("\n--- RECOMENDACIÓN DE PELÍCULAS ---")
    termino = input("¿En qué película basamos tu recomendación?: ")
    
    # 1. Buscar coincidencias parciales (similar a buscar_peli)
    encontrados = [p for p in catalogo if termino.lower() in p.get_titulo().lower()]
    
    if encontrados:
        print(f"\nEncontramos estas películas para '{termino}':")
        for i, peli in enumerate(encontrados, start=1):
            print(f"{i}. {peli.get_titulo()} ({peli.get_fecha_estreno()[:4]})")
        
        # Acá luego agregaremos la lógica para que el usuario elija un número 
        # y el algoritmo busque películas similares.
        print("\n[Lógica de recomendación todavia en proceso]")
    else:
        print("\n❌ No se encontraron películas con ese título para basar la recomendación.")


def iniciar_menu(catalogo):
    while True:
        print("\n====================")
        print("    CINEFILAPP 🎬   ")
        print("====================")
        print("¿Todavía no decidiste qué mirar? Te ayudamos.\n")
        print("1. Recomendación por película")
        print("2. Listar todo el catálogo")
        print("3. Buscar película por título")
        print("4. Filtrar")
        print("5. Salir")
        
        opcion = input("\nElegí una opción (1-5): ")
        
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
            print("\n¡Gracias por usar CinefilApp! Saliendo...")
            break

        else:
            print("\n❌ Opción no válida. Ingresá un número del 1 al 5.")
#Iniciamos el menu
if __name__ == "__main__":
    iniciar_menu(mi_catalogo)
