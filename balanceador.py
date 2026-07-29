import sys


PARES = {
    ")": "(",
    "]": "[",
    "}": "{",
}

APERTURA = set(PARES.values())
CIERRE = set(PARES.keys())


def formato_pila(pila):
    if not pila:
        return "[]"
    return "[" + ", ".join(simbolo for simbolo, _ in pila) + "]"


def validar_balance(expresion):
    pila = []
    pasos = []
    balanceada = True

    for posicion, caracter in enumerate(expresion, start=1):
        if caracter in APERTURA:
            pila.append((caracter, posicion))
            pasos.append(
                f"pos {posicion:02d} | lee '{caracter}' | PUSH | pila = {formato_pila(pila)}"
            )
        elif caracter in CIERRE:
            esperado = PARES[caracter]

            if not pila:
                pasos.append(
                    f"pos {posicion:02d} | lee '{caracter}' | ERROR: cierre sin apertura | pila = {formato_pila(pila)}"
                )
                balanceada = False
                continue

            tope, posicion_tope = pila[-1]
            if tope == esperado:
                pila.pop()
                pasos.append(
                    f"pos {posicion:02d} | lee '{caracter}' | POP '{tope}' | pila = {formato_pila(pila)}"
                )
            else:
                pasos.append(
                    f"pos {posicion:02d} | lee '{caracter}' | ERROR: esperaba cerrar '{tope}' abierto en pos {posicion_tope} | pila = {formato_pila(pila)}"
                )
                balanceada = False

    if pila:
        balanceada = False
        pendientes = ", ".join(
            f"'{simbolo}' en pos {posicion}" for simbolo, posicion in reversed(pila)
        )
        pasos.append(f"FIN       | ERROR: quedaron aperturas sin cerrar: {pendientes}")
    else:
        pasos.append("FIN       | pila vacia")

    return balanceada, pasos


def procesar_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"No se encontro el archivo: {ruta}")
        return 1

    if not lineas:
        print("El archivo esta vacio.")
        return 0

    print(f"Archivo procesado: {ruta}")
    print("=" * 70)

    for numero_linea, linea in enumerate(lineas, start=1):
        expresion = linea.rstrip("\n")

        if not expresion.strip():
            print(f"Linea {numero_linea}: vacia, se omite.")
            print("-" * 70)
            continue

        balanceada, pasos = validar_balance(expresion)
        resultado = "BALANCEADA" if balanceada else "NO BALANCEADA"

        print(f"Linea {numero_linea}: {expresion}")
        print(f"Resultado: {resultado}")
        print("Pasos de la pila:")
        for paso in pasos:
            print(f"  {paso}")
        print("-" * 70)

    return 0


def main():
    ruta = "expresiones.txt"
    if len(sys.argv) > 1:
        ruta = sys.argv[1]

    return procesar_archivo(ruta)


if __name__ == "__main__":
    raise SystemExit(main())
