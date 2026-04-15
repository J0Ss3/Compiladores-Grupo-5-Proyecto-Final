from lark import Transformer, Tree, Token
import random

# ---------------- UTILIDADES ---------------- #

def dec_a_romano(n):
    n = int(n)
    valores = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    simbolos = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    resultado = ""
    for i in range(len(valores)):
        while n >= valores[i]:
            resultado += simbolos[i]
            n -= valores[i]
    return resultado

def tree_to_dict(tree):
    if isinstance(tree, Tree):
        return {
            "name": tree.data,
            "type": "non-terminal",
            "children": [tree_to_dict(child) for child in tree.children]
        }
    elif isinstance(tree, Token):
        return {
            "name": f"{tree.type}: {tree.value}",
            "type": "terminal"
        }

# ---------------- TRANSFORMADOR ---------------- #

class TransformadorNumeros(Transformer):

    def DIGITO(self, token):
        return int(token)

    def entero(self, items):
        return int("".join(str(d) for d in items))

    def numero(self, items):
        return items[0]

    def tipo_conversion(self, items):
        return items[0].value

    def conversion(self, items):
        num = items[0]
        destino = items[1]

        if destino == "Aleatorio":
            destino = random.choice(["Hexadecimal", "Octal", "Binario", "Romano"])

        if destino == "Binario":
            res = bin(num)[2:]
        elif destino == "Octal":
            res = oct(num)[2:]
        elif destino == "Hexadecimal":
            res = hex(num)[2:].upper()
        elif destino == "Romano":
            res = dec_a_romano(num)
        else:
            res = f"ALT-{num * 7}"

        return f"(Sistema: {destino}) {res}"

    def instruccion(self, items):
        return items[0]
