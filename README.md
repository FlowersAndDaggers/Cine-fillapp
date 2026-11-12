TP Integrador de estructura de datos: Cine-fillap

integrantes del grupo 29:

Hidalgo, Diego
D.N.I.: 38.526.547

Hidalgo, Ángel
D.N.I.: 37.387.604

Rojas, Leandro 
D.N.I.: 33.747.674

ENTREGA DE TRABAJO INTEGRADOR 02 COMPLEJIDAD
FECHA 23/09

TABLA DE RESULTADOS: 
  
 | Cantidad de Datos | Tiempo en Secuencial | Tiempo en Árbol Binario |
| :--- | :--- | :--- |
| N = 1000 | Secuencial: 0.1300 ms | Árbol: 0.0084 ms |
| N = 10000 | Secuencial: 1.1395 ms | Árbol: 0.0051 ms |
| N = 85855 | Secuencial: 10.7731 ms | Árbol: 0.0060 ms |

*Usamos como 85.855 cantidad de datos como máximo porque la base de datos que conseguimos tiene esa cantidad de peliculas. 

Conclusión técnica: Pudimos ver que en velocidad la estrategia de árbol binario es mas eficiente pero si tenemos en cuenta el contexto de una búsqueda en una aplicación de peliculas el hecho de que en la estrategia secuencial no tengamos que ser exactos en el nombre de la peli a buscar si no que con poner parte del nombre nos aparezcan todas las pelis que puedan llegar a ser la que buscamos terminamos considerando que la búsqueda secuencial es la mejor para este caso. 


ENTREGA DE TRABAJO INTEGRADOR 03 COMPLEJIDAD PONÉ UN ÁRBOL EN TU SISTEMA
FECHA 30/09

Editamos la función que ya teníamos de listar las peliculas para implementar el árbol binario. La clave de ordenamiento que usamos fue alfabética y el recorrido inorder, aunque los demás también quedaron en el código sin uso por ahora. En comparación a la búsqueda secuencial en la función de buscar pelicula por nombre esta es mas rápida y no necesita devolver datos parecidos a la búsqueda ya que es solamente mostrar el listado de todas las pelis, por eso nos pareció que era correcta para esta función. Estamos pensando ya el algoritmo para hacer las recomendaciones pero todavía no lo tenemos terminado.


ENTREGA DE TRABAJO INTEGRADOR 04 EL ÁRBOL TAMBIEN PUEDE ENFERMARSE

Agregamos una función nueva solamente para hacer el experimento utilizando nuestra función de listar todo el catalogo en la cual usábamos un Árbol como técnica. Primero podemos seleccionar listar un árbol tal cual esta ahora (sano) para ver cuantos pisos tiene y en que velocidad hace la tarea. Después podemos enfermar el árbol dándole datos ya ordenados (en el archivo main.py esta comentado esa parte del código) y nos devuelve la lista con los datos de pisos y velocidad nuevamente, después de ahí podemos usar el árbol avl y nos devuelve la comparación en velocidad y en pisos con el árbol enfermo. En conclusión el árbol una vez enfermo pierde velocidad ya que pasa a tener 800 pisos (uno por pelicula) y una vez cambiamos a una árbol avl vuelve a recuperar la velocidad y los pocos pisos que tenia como árbol sano.    

Entrega de trabajo integrador 05 Organiza tu universo

Se implemento el árbol general en una búsqueda de categorías y sub categorías por genero. Recorridos (Preorden), se agrego el recorrido en preorden (recorrido_preorden) que visita la gerarquia padre y despues baja a los hijio. Esto permite visualizar la jerarquía completa en la terminal con una estructura escalonada, como un sistema de carpetas.

Búsquedas Recursivas: Se agrego un algoritmo (buscar_en_arbol) que busca un termimo especifico, como el nombre de un genero dentro de la jerarquía, devolviendo el nodo exacto y toda la rama de elementos que descienden de él.

ENTREGA DE TRABAJO INTEGRADOR 06 Que el sistema elija primero:
Se implementa un heap para obtener un top 5 de peliculas en general y según su género, ya que al tener una base datos tan extensa, generar un top con todas las peliculas cada vez que cambie algún factor, haría un uso excesivo de memoria o tardaría mucho el proceso. Por lo tanto un heap de 5 elemenos, establece los primeros 5 y luego compara con el resto dinamicamente por lo cuál recorre todos los elemenos pero no los enlista, solo enlista los 5 primeros, para luego comparar e ir agregando o quitando pero sin enlistar el total de películas. En este caso elegimos priorizar las calificaciones y la "frescura" de las películas. Esta "frescura" está dada por la fecha de estreno de las películas.

ENTREGA DE TRABAJO INTEGRADOR 07 Conecta las cosas

Agregamos los grafos donde los vértices son cada pelicula unica, y estan conectados por artistas (director o actor). 
El tipo de grafo es no dirigido porque la relación es bidimensional y mutua, si una peli comparte actor con la otra la otra comparte con la primera también. Es pesado porque tiene un valor (fuerza) que se calcula sumando puntos por director o actor compartido.
La representamos con una lista de adyacencia porque la densidad del grafo es baja solo comparte actores y directores. Si hubiéramos usando una matriz se desperdiciaría mucha memorias almacenando conexiones inexistentes. 

ENTREGA DE TRABAJO INTEGRADOR 08 Explorá la red
Agregamos a los grafos la busqueda en profundidad DFS y la busqueda en anchura BFS, ya que cada una nos permite responder diferentes preguntas.
¿Qué tan relacionads están dos películas? Ahí es una búsqueda en anchura, que nos sirve para encontrar el cámino más corto en la red a partir de dos películas dada. Para ver que películas tengo que  ver para entender ambas películas por completo.
¿Qué películas están relacionadas al universo cinématográfico? En este caso conviene una busqueda en profundidad en donde busca todas las películas relacionadas y las da en orden de prioridad del árbol.
La complejidad en ambos casos depende de la forma del árbol, en donde dependen de los nodos y aristas.
