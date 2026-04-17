"""
Módulo CLI (Interfaz de Línea de Comandos) para el convertidor de números.

Proporciona una interfaz interactiva en terminal para probar el convertidor
de sistemas numéricos. Es útil para testing y depuración sin necesidad de
una interfaz web.

Funciones principales:
    - dec_a_romano()            : Convierte decimal a numerales romanos
    - cuadro_lexico_detallado() : Muestra análisis léxico detallado
    - ejecutar_traductor()      : Loop principal interactivo

Formato de entrada: <número><sistema>$ (ej: 525Romano$)
"""

import random
import re
from lark import Lark, Transformer, Tree


def dec_a_romano(n):
    """
    Convierte un número decimal a numerales romanos.
    
    Utiliza una tabla de valores romanos y sus símbolos correspondientes.
    El algoritmo itera sobre los valores de mayor a menor, colocando símbolos
    y restando del número hasta que se haya convertido completamente.
    
    Args:
        n (int|str): Número decimal a convertir (se convierte a int automáticamente)
    
    Returns:
        str: Representación en numerales romanos del número
    
    Ejemplo:
        >>> dec_a_romano(1994)
        'MCMXCIV'
        >>> dec_a_romano(525)
        'DXXV'
    """
    n = int(n)
    valores = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    simbolos = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    resultado = ""
    for i in range(len(valores)):
        while n >= valores[i]:
            resultado += simbolos[i]
            n -= valores[i]
    return resultado


# -------- TRANSFORMER --------

class TransformadorNumeros(Transformer):
    """
    Transformer de Lark que transforma nodos del AST en resultados de conversión.
    
    Versión CLI del transformador. Implementa la conversión de números decimales
    a diferentes sistemas numéricos.
    
    Métodos (corresponden a reglas en la gramática):
        - instruccion() : Procesa una instrucción de conversión
    """

    def instruccion(self, items):
        """
        Procesa una instrucción de conversión numérica.
        
        Extrae el número y el sistema destino, realiza la conversión apropiada
        y retorna un resultado formateado.
        
        Args:
            items (list): Lista con tres elementos:
                - items[0] (str): Token NUMERO como cadena
                - items[1] (str): Token DESTINO como cadena
                - items[2] (str): Token FIN ("$")
        
        Returns:
            str: Cadena con el resultado formateado: "Resultado: (Sistema: X) valor"
        """
        num = int(items[0])
        destino = str(items[1])
        
        # Si es aleatorio, elige un sistema al azar
        if destino == "Aleatorio":
            destino = random.choice(["Hexadecimal", "Octal", "Binario", "Romano"])
        
        # Realiza la conversión según el sistema destino
        if destino == "Binario":
            res = bin(num)[2:]  # bin() devuelve "0b...", extrae solo los dígitos
        elif destino == "Octal":
            res = oct(num)[2:]  # oct() devuelve "0o...", extrae solo los dígitos
        elif destino == "Hexadecimal":
            res = hex(num)[2:].upper()  # hex() devuelve "0x...", extrae y convierte a mayúsculas
        elif destino == "Romano":
            res = dec_a_romano(num)  # Usa la función de conversión romana
        else:
            # Sistema Alternativo: aplica fórmula especial
            res = f"ALT-{num * 7}"
            
        return f"Resultado: (Sistema: {destino}) {res}"


# -------- GRAMÁTICA DEL PARSER --------

gramatica = r"""
?start: programa

programa: instruccion+

instruccion: NUMERO DESTINO FIN

NUMERO: /\d+/

DESTINO: "Hexadecimal" | "Octal" | "Binario" | "Romano" | "Alternativo" | "Aleatorio"

FIN: "$"

%import common.WS
%ignore WS
"""


def cuadro_lexico_detallado(entrada):
    """
    Muestra el análisis léxico detallado de la entrada.
    
    Utiliza expresiones regulares para tokenizar la entrada y muestra
    cada token en una tabla formateada. Es útil para depuración y
    comprensión de cómo se procesan las entradas.
    
    Tabla mostrada:
        - Línea     : Número de línea (siempre 1 para entrada simple)
        - Token     : Tipo de token (NUMERO, DESTINO, FIN)
        - Lexema    : El valor del token
        - Columna   : Posición en la cadena
        - Longitud  : Número de caracteres del token
        - Patrón RE : Expresión regular que lo define
    
    Args:
        entrada (str): Cadena de entrada a analizar (ej: "525Romano$")
    
    Returns:
        None (imprime a stdout)
    
    Ejemplo:
        >>> cuadro_lexico_detallado("525Romano$")
        DETALLE DEL ANALIZADOR LÉXICO:
        ...
    """
    print("\nDETALLE DEL ANALIZADOR LÉXICO:")
    # Encabezado con las columnas de la tabla
    header = f"{'Línea':<6} | {'Token':<12} | {'Lexema':<12} | {'Columna':<8} | {'Longitud':<9} | {'Patrón RE'}"
    print("-" * len(header))
    print(header)
    print("-" * len(header))
    
    # Expresión regular para extraer componentes de la entrada
    # Captura: 1) números, 2) letras (sistema), 3) "$" (fin)
    match = re.match(r"(\d+)([a-zA-Z]+)(\$)", entrada)
    
    if match:
        # Itera sobre los 3 grupos capturados
        for i in range(1, 4):
            lexema = match.group(i)
            
            # Determina el tipo de token basado en el contenido
            if lexema.isdigit(): 
                tipo = "NUMERO"
                patron = r"\d+"
            elif lexema == "$": 
                tipo = "FIN"
                patron = r"\$"
            else: 
                tipo = "DESTINO"
                patron = r"Hex|Rom"  # Simplificado para el ejemplo
            
            # Calcula la posición de inicio del token en la cadena
            columna = match.start(i) + 1
            longitud = len(lexema)
            
            # Imprime la fila de la tabla
            print(f"{1:<6} | {tipo:<12} | {lexema:<12} | {columna:<8} | {longitud:<9} | {patron}")


def ejecutar_traductor():
    """
    Loop principal interactivo de la aplicación CLI.
    
    Solicita entradas del usuario, las procesa con el parser Lark,
    las transforma usando TransformadorNumeros y muestra los resultados.
    
    Flujo:
        1. Inicializa el parser con la gramática
        2. Entra en un loop infinito solicitando entrada
        3. Permite 'salir' como comando para terminar
        4. Muestra análisis léxico detallado
        5. Analiza y transforma la entrada
        6. Muestra los resultados
        7. Captura excepciones para entradas inválidas
    
    Formato de entrada: <número><sistema>$ (ej: 525Romano$)
    
    Sistemas soportados:
        - Binario
        - Octal
        - Hexadecimal
        - Romano
        - Alternativo
        - Aleatorio (elige al azar)
    
    Returns:
        None (función de efecto principal)
    """
    print("--- CONVERTIDOR DE NÚMEROS ---")
    # Crea una instancia del parser con la gramática definida
    parser = Lark(gramatica, start='programa')
    
    # Loop principal
    while True:
        try:
            # Solicita entrada al usuario
            entrada = input("\nIngrese cadena (ej. 525Romano$) o 'salir': ").strip()
            
            # Comando para salir
            if entrada.lower() == 'salir':
                break
            
            # Ignora líneas vacías
            if not entrada:
                continue

            # Muestra el análisis léxico detallado
            cuadro_lexico_detallado(entrada)

            # Analiza sintácticamente la entrada
            arbol = parser.parse(entrada)
            print("\nSALIDA SINTÁCTICA (OPERACIÓN):")
            
            # Transforma el árbol sintáctico en resultados
            transformador = TransformadorNumeros()
            resultados = transformador.transform(arbol)
            
            # Muestra cada resultado
            for r in resultados.children:
                print(f"-> {r}")

        except Exception:
            # Manejo de excepciones: entrada no reconocida
            print(f"\n[Error]: Entrada no reconocida. Use el formato 'NumeroDestino$'.")


# Punto de entrada
if __name__ == "__main__":
    ejecutar_traductor()