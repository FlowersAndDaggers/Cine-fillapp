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


ENTREGA DE TRABAJO INTEGRADOR 02 COMPLEJIDAD PONÉ UN ÁRBOL EN TU SISTEMA
FECHA 30/09

Editamos la función que ya teníamos de listar las peliculas para implementar el árbol binario. La clave de ordenamiento que usamos fue alfabética y el recorrido inorder, aunque los demás también quedaron en el código sin uso por ahora. En comparación a la búsqueda secuencial en la función de buscar pelicula por nombre esta es mas rápida y no necesita devolver datos parecidos a la búsqueda ya que es solamente mostrar el listado de todas las pelis, por eso nos pareció que era correcta para esta función. Estamos pensando ya el algoritmo para hacer las recomendaciones pero todavía no lo tenemos terminado.
