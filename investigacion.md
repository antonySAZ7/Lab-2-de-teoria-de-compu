Investigación Sintetizada
El algoritmo Shunting Yard fue creado por Edsger Dijkstra para convertir expresiones en formato infix a postfix, también llamado Reverse Polish Notation. Usa una pila de operadores y una salida. 
La expresión se lee de izquierda a derecha: los operandos se envían directamente a la salida, mientras que los operadores se guardan en la pila según su precedencia.
Cuando aparece un operador nuevo, se comparan las prioridades. Si el operador en la pila tiene mayor o igual prioridad, se saca de la pila y se manda a la salida. 
Los paréntesis permiten alterar el orden: ( se apila y, al encontrar ), se sacan operadores hasta encontrar el paréntesis de apertura.
Aplicado a expresiones regulares, se manejan prioridades como: primero *, +, ?, luego concatenación y por último unión |. 
Además, la concatenación implícita se vuelve explícita. 
Por ejemplo, (a|t)c se convierte internamente en (a|t).c.
Las extensiones se pueden convertir a operadores básicos: r+ equivale a rr*, porque significa una o más repeticiones; y r? equivale a r|epsilon, porque significa cero o una aparición.


Referencias
Dijkstra, E. W. ALGOL 60 Translation: An ALGOL 60 Translator for the X1 and Making a Translator for ALGOL 60. Stichting Mathematisch Centrum, 1961.
https://www.cs.utexas.edu/~EWD/MCReps/MR35.PDF