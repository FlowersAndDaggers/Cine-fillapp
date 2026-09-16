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
    def get_titulo(self):32008
    
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

#imprimimos la lista de todo el catalogo
print("--- CATÁLOGO ---")
for peli in mi_catalogo:
    print(peli)

#buscamos peliculas en el catalogo
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


    #iniciamos el menu con las opciones
def iniciar_menu(catalogo):
    while True:
        print("\n====================")
        print("   CINE-FILLAPP 🎬  ")
        print("====================")
        print("1. Listar todo el catálogo")
        print("2. Buscar película por título")
        print("3. Filtrar")
        print("4. Salir")
        
        opcion = input("\nElegí una opción (1-4): ")
        
        if opcion == "1":
            print("\n--- LISTADO COMPLETO ---")
            for peli in catalogo:
                print(peli)
        elif opcion == "2":
            termino = input("Ingresá el título a buscar: ")
            buscar_peli(catalogo, termino)
        elif opcion == "3":
            termino = input("Ingresá tipo, género, director, actores,año o calificación:")
            filtrar_peli(catalogo, termino)
        elif opcion == "4":
            print("\n¡Gracias por usar Cine-fillapp! Saliendo...")
            break

        else:
            print("\n Opción no válida. Ingresá 1, 2, 3 o 4.")

#Iniciamos el menu
iniciar_menu(mi_catalogo)

