# Balanceador de expresiones infix

Este programa lee un archivo de texto linea por linea y valida si cada expresion esta balanceada.
Para hacerlo utiliza una pila con los simbolos de apertura `(`, `[`, `{` y los compara contra sus
respectivos cierres `)`, `]`, `}`.

## Archivos

- `balanceador.py`: programa principal.
- `expresiones.txt`: archivo de entrada con una expresion por linea.

## Como ejecutar

```powershell
python .\balanceador.py .\expresiones.txt
```

Tambien puede ejecutarse sin parametro, porque por defecto busca `expresiones.txt`:

```powershell
python .\balanceador.py
```

## Que mostrar en el video

1. Mostrar el archivo de entrada:

```powershell
Get-Content .\expresiones.txt
```

2. Ejecutar el programa:

```powershell
python .\balanceador.py .\expresiones.txt
```

3. Mostrar que para cada linea aparece:

- la expresion procesada,
- si esta `BALANCEADA` o `NO BALANCEADA`,
- la secuencia de pasos de la pila con operaciones `PUSH`, `POP` y errores.
