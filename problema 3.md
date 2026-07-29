# Problema 3 - Shunting Yard para expresiones regulares

## Archivos

- `shunting_yard_regex.py`: implementacion del algoritmo.
- `regex_problema1.txt`: expresiones del Problema 1, una por linea.

## Como ejecutar

```powershell
python .\shunting_yard_regex.py .\regex_problema1.txt
```

Tambien puede ejecutarse sin parametro:

```powershell
python .\shunting_yard_regex.py
```

## Que mostrar en el video

1. Mostrar el archivo que se va a procesar:

```powershell
Get-Content .\regex_problema1.txt
```

2. Ejecutar el programa:

```powershell
python .\shunting_yard_regex.py .\regex_problema1.txt
```

3. Mostrar que por cada linea aparece:

- la expresion original,
- la expresion convertida a postfix,
- los tokens con concatenacion explicita,
- los pasos del algoritmo con pila de operadores y salida.

## Nota sobre el punto

El punto `.` escrito en una expresion se interpreta como caracter literal.
Para evitar confusion, en la salida postfix el punto literal se imprime como `\.`
y el punto `.` sin escape se usa como operador de concatenacion.

## Conversion de extensiones

- `r+` se convierte a `r r * .`
- `r?` se convierte a `r epsilon |`
