import random
import re
from lark import Lark, Transformer,Tree

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

class TransformadorNumeros(Transformer):
    def instruccion(self, items):
        num = int(items[0])
        destino = str(items[1])
        if destino == "Aleatorio":
            destino = random.choice(["Hexadecimal", "Octal", "Binario", "Romano"])
        
        if destino == "Binario": res = bin(num)[2:]
        elif destino == "Octal": res = oct(num)[2:]
        elif destino == "Hexadecimal": res = hex(num)[2:].upper()
        elif destino == "Romano": res = dec_a_romano(num)
        else: res = f"ALT-{num * 7}"
            
        return f"Resultado: (Sistema: {destino}) {res}"




gramatica = r""" #definimos la gramatica
?start: programa
programa: instruccion+
instruccion: NUMERO DESTINO FIN
NUMERO: /\d+/
DESTINO: "Hexadecimal" | "Octal" | "Binario" | "Romano" | "Alternativo" | "Aleatorio"
FIN: "$"
%import common.WS
%ignore WS
"""




def cuadro_lexico_detallado(entrada): #version2 con detalles 
    print("\nDETALLE DEL ANALIZADOR LÉXICO:")
    header = f"{'Línea':<6} | {'Token':<12} | {'Lexema':<12} | {'Columna':<8} | {'Longitud':<9} | {'Patrón RE'}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    match = re.match(r"(\d+)([a-zA-Z]+)(\$)", entrada) #expresión regular
    if match:
        for i in range(1, 4):
            lexema = match.group(i)
            if lexema.isdigit(): 
                tipo = "NUMERO"
                patron = r"\d+"
            elif lexema == "$": 
                tipo = "FIN"
                patron = r"\$"
            else: 
                tipo = "DESTINO"
                patron = r"Hex|Rom"
            
            columna = match.start(i) + 1
            longitud = len(lexema)
            print(f"{1:<6} | {tipo:<12} | {lexema:<12} | {columna:<8} | {longitud:<9} | {patron}")

def ejecutar_traductor():
    print("--- CONVERTIDOR DE NÚMEROS ---")
    parser = Lark(gramatica, start='programa')
    
    while True:
        try:
            entrada = input("\nIngrese cadena (ej. 525Romano$) o 'salir': ").strip()
            if entrada.lower() == 'salir': break
            if not entrada: continue

            cuadro_lexico_detallado(entrada)

            arbol = parser.parse(entrada)
            print("\nSALIDA SINTÁCTICA (OPERACIÓN):")
            transformador = TransformadorNumeros()
            resultados = transformador.transform(arbol)
            for r in resultados.children:
                print(f"-> {r}")

        except Exception:
            print(f"\n[Error]: Entrada no reconocida. Use el formato 'NumeroDestino$'.")



if __name__ == "__main__":
    ejecutar_traductor()