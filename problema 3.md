# Problema 3 - Shunting Yard para expresiones regulares

## Archivos

- `shunting_yard_regex.py`: implementacion del algoritmo.
- `regex_problema1.txt`: expresiones del Problema 1, una por linea.



## Nota sobre el punto

El punto `.` escrito en una expresion se interpreta como caracter literal.
Para evitar confusion, en la salida postfix el punto literal se imprime como `\.`
y el punto `.` sin escape se usa como operador de concatenacion.

## Conversion de extensiones

- `r+` se convierte a `r r * .`
- `r?` se convierte a `r epsilon |`
