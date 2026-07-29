import sys
from dataclasses import dataclass


CONCAT = "."
ALT = "|"
STAR = "*"
PLUS = "+"
QUESTION = "?"
LPAREN = "("
RPAREN = ")"
EPSILON = "epsilon"

PRECEDENCIA = {
    ALT: 1,
    CONCAT: 2,
}


@dataclass
class Token:
    tipo: str
    valor: str


@dataclass
class Nodo:
    tipo: str
    valor: str = ""
    izquierdo: object = None
    derecho: object = None


def escapar_salida(valor):
    if valor == ".":
        return r"\."
    if valor == EPSILON:
        return EPSILON
    return valor


def postfix(nodo):
    if nodo.tipo == "operando":
        return [escapar_salida(nodo.valor)]
    if nodo.tipo == "star":
        return postfix(nodo.izquierdo) + [STAR]
    if nodo.tipo == "plus":
        base = postfix(nodo.izquierdo)
        return base + base + [STAR, CONCAT]
    if nodo.tipo == "question":
        return postfix(nodo.izquierdo) + [EPSILON, ALT]
    if nodo.tipo == "concat":
        return postfix(nodo.izquierdo) + postfix(nodo.derecho) + [CONCAT]
    if nodo.tipo == "alt":
        return postfix(nodo.izquierdo) + postfix(nodo.derecho) + [ALT]
    raise ValueError(f"Nodo desconocido: {nodo.tipo}")


def texto_postfix(nodos):
    if not nodos:
        return ""
    if len(nodos) == 1:
        return " ".join(postfix(nodos[0]))
    partes = []
    for nodo in nodos:
        partes.extend(postfix(nodo))
    return " ".join(partes)


def texto_operadores(operadores):
    if not operadores:
        return "[]"
    return "[" + ", ".join(operadores) + "]"


def tokeniza(expresion):
    tokens = []
    i = 0

    while i < len(expresion):
        actual = expresion[i]

        if actual.isspace():
            i += 1
            continue

        if actual == "\\":
            if i + 1 >= len(expresion):
                raise ValueError("Backslash al final de la expresion")
            tokens.append(Token("operando", "\\" + expresion[i + 1]))
            i += 2
            continue

        if actual == "[":
            inicio = i
            i += 1
            escapado = False
            while i < len(expresion):
                if escapado:
                    escapado = False
                elif expresion[i] == "\\":
                    escapado = True
                elif expresion[i] == "]":
                    break
                i += 1

            if i >= len(expresion) or expresion[i] != "]":
                raise ValueError("Clase de caracteres '[' sin cierre ']'")

            tokens.append(Token("operando", expresion[inicio : i + 1]))
            i += 1
            continue

        if expresion.startswith("epsilon", i):
            tokens.append(Token("operando", EPSILON))
            i += len("epsilon")
            continue

        if actual == "ε":
            tokens.append(Token("operando", EPSILON))
        elif actual == LPAREN:
            tokens.append(Token("lparen", actual))
        elif actual == RPAREN:
            tokens.append(Token("rparen", actual))
        elif actual == ALT:
            tokens.append(Token("binario", actual))
        elif actual in {STAR, PLUS, QUESTION}:
            tokens.append(Token("unario", actual))
        else:
            tokens.append(Token("operando", actual))

        i += 1

    return insertar_concatenacion(tokens)


def termina_expresion(token):
    return token.tipo in {"operando", "rparen", "unario"}


def inicia_expresion(token):
    return token.tipo in {"operando", "lparen"}


def insertar_concatenacion(tokens):
    con_concat = []

    for i, token in enumerate(tokens):
        if i > 0 and termina_expresion(tokens[i - 1]) and inicia_expresion(token):
            con_concat.append(Token("binario", CONCAT))
        con_concat.append(token)

    return con_concat


def aplica_unario(operador, salida):
    if not salida:
        raise ValueError(f"Operador '{operador}' sin expresion previa")

    hijo = salida.pop()
    if operador == STAR:
        salida.append(Nodo("star", izquierdo=hijo))
    elif operador == PLUS:
        salida.append(Nodo("plus", izquierdo=hijo))
    elif operador == QUESTION:
        salida.append(Nodo("question", izquierdo=hijo))
    else:
        raise ValueError(f"Operador unario desconocido: {operador}")


def aplica_binario(operadores, salida):
    operador = operadores.pop()

    if len(salida) < 2:
        raise ValueError(f"Operador '{operador}' sin suficientes operandos")

    derecho = salida.pop()
    izquierdo = salida.pop()
    tipo = "concat" if operador == CONCAT else "alt"
    salida.append(Nodo(tipo, izquierdo=izquierdo, derecho=derecho))


def convertir_a_postfix(expresion):
    tokens = tokeniza(expresion)
    salida = []
    operadores = []
    pasos = []

    pasos.append("Tokens con concatenacion explicita: " + " ".join(t.valor for t in tokens))

    for token in tokens:
        if token.tipo == "operando":
            salida.append(Nodo("operando", token.valor))
            accion = f"agrega operando '{escapar_salida(token.valor)}' a salida"

        elif token.tipo == "unario":
            aplica_unario(token.valor, salida)
            if token.valor == PLUS:
                accion = "convierte extension '+' como r r * ."
            elif token.valor == QUESTION:
                accion = "convierte extension '?' como r epsilon |"
            else:
                accion = "aplica cerradura '*' a la expresion anterior"

        elif token.tipo == "lparen":
            operadores.append(token.valor)
            accion = "push '(' en pila de operadores"

        elif token.tipo == "rparen":
            while operadores and operadores[-1] != LPAREN:
                aplica_binario(operadores, salida)

            if not operadores:
                raise ValueError("Parentesis de cierre sin apertura")

            operadores.pop()
            accion = "procesa operadores hasta '(' y descarta parentesis"

        elif token.tipo == "binario":
            while (
                operadores
                and operadores[-1] != LPAREN
                and PRECEDENCIA[operadores[-1]] >= PRECEDENCIA[token.valor]
            ):
                aplica_binario(operadores, salida)

            operadores.append(token.valor)
            accion = f"push operador '{token.valor}'"

        else:
            raise ValueError(f"Token desconocido: {token}")

        pasos.append(
            f"lee '{token.valor}' | {accion} | operadores = {texto_operadores(operadores)} | salida = {texto_postfix(salida)}"
        )

    while operadores:
        if operadores[-1] == LPAREN:
            raise ValueError("Parentesis de apertura sin cierre")
        aplica_binario(operadores, salida)
        pasos.append(
            f"fin | pop operador pendiente | operadores = {texto_operadores(operadores)} | salida = {texto_postfix(salida)}"
        )

    if len(salida) != 1:
        raise ValueError("La expresion no pudo reducirse a un solo resultado")

    return " ".join(postfix(salida[0])), pasos


def procesar_archivo(ruta):
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            lineas = archivo.readlines()
    except FileNotFoundError:
        print(f"No se encontro el archivo: {ruta}")
        return 1

    print(f"Archivo procesado: {ruta}")
    print("=" * 90)

    for numero, linea in enumerate(lineas, start=1):
        expresion = linea.strip()
        if not expresion:
            continue

        print(f"Linea {numero}: {expresion}")
        try:
            resultado, pasos = convertir_a_postfix(expresion)
            print(f"Postfix: {resultado}")
            print("Pasos:")
            for paso in pasos:
                print(f"  {paso}")
        except ValueError as error:
            print(f"ERROR: {error}")

        print("-" * 90)

    return 0


def main():
    ruta = "regex_problema1.txt"
    if len(sys.argv) > 1:
        ruta = sys.argv[1]
    return procesar_archivo(ruta)


if __name__ == "__main__":
    raise SystemExit(main())
