"""
Módulo de transformación y utilidades para el convertidor de números.

Contiene la clase Transformer de Lark que convierte el árbol sintáctico
abstracto (AST) generado por el parser en resultados de conversión numérica.
También incluye funciones de utilidad para la conversión a diferentes sistemas.

Funciones:
    - dec_a_romano()   : Convierte decimal a numerales romanos
    - tree_to_dict()   : Convierte árbol sintáctico a diccionario

Clases:
    - TransformadorNumeros : Transformer que procesa nodos del AST
"""

from lark import Transformer, Tree, Token
import random

# -------- UTILIDADES --------

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
    
    # Tabla de valores y sus símbolos romanos correspondientes (de mayor a menor)
    valores = [1000, 900, 500, 400, 100, 90, 50, 40, 10, 9, 5, 4, 1]
    simbolos = ["M", "CM", "D", "CD", "C", "XC", "L", "XL", "X", "IX", "V", "IV", "I"]
    
    resultado = ""
    
    # Itera sobre cada valor romano
    for i in range(len(valores)):
        # Mientras el número sea mayor o igual al valor actual, agrega el símbolo
        while n >= valores[i]:
            resultado += simbolos[i]
            n -= valores[i]
    
    return resultado


def tree_to_dict(tree):
    """
    Convierte un árbol sintáctico de Lark a una estructura de diccionario.
    
    Recursivamente transforma nodos del árbol sintáctico (Tree) y tokens (Token)
    en diccionarios JSON-serializable. Utilizada para enviar el AST al cliente web.
    
    Args:
        tree (Tree|Token): Nodo del árbol sintáctico o terminal a convertir
    
    Returns:
        dict: Diccionario con estructura:
            Para nodos (Tree):
                {
                    "name": "nombre_regla",
                    "type": "non-terminal",
                    "children": [...]  # Lista de hijos convertidos recursivamente
                }
            Para terminales (Token):
                {
                    "name": "TIPO: valor",
                    "type": "terminal"
                }
    
    Ejemplo:
        >>> arbol = parser.parse("525Romano$")
        >>> tree_to_dict(arbol)
        {'name': 'programa', 'type': 'non-terminal', 'children': [...]}
    """
    if isinstance(tree, Tree):
        # Caso: nodo no-terminal
        return {
            "name": tree.data,
            "type": "non-terminal",
            "children": [tree_to_dict(child) for child in tree.children]
        }
    elif isinstance(tree, Token):
        # Caso: nodo terminal (token)
        return {
            "name": f"{tree.type}: {tree.value}",
            "type": "terminal"
        }


# -------- TRANSFORMADOR --------

class TransformadorNumeros(Transformer):
    """
    Transformer de Lark que transforma nodos del AST en resultados de conversión.
    
    Hereda de Transformer de Lark. Cada método transforma un nodo específico
    de la gramática. Los métodos se llaman automáticamente según el nombre
    de la regla/token en la gramática.
    
    Métodos (corresponden a reglas en la gramática):
        - DIGITO()           : Procesa un dígito individual
        - entero()           : Procesa un número entero completo
        - numero()           : Procesa la regla número
        - tipo_conversion()  : Extrae el tipo de conversión
        - conversion()       : Realiza la conversión numérica
        - instruccion()      : Procesa una instrucción completa
    """

    def DIGITO(self, token):
        """
        Transforma un dígito tokenizado en su valor entero.
        
        Args:
            token (Token): Token de Lark representando un dígito
        
        Returns:
            int: El dígito como número entero
        """
        return int(token)

    def entero(self, items):
        """
        Transforma una lista de dígitos en un número entero.
        
        Concatena los dígitos individuales y los convierte a un número.
        
        Args:
            items (list): Lista de dígitos ya procesados por DIGITO()
        
        Returns:
            int: El número entero resultante
        """
        return int("".join(str(d) for d in items))

    def numero(self, items):
        """
        Transforma la regla 'numero' en su valor.
        
        Args:
            items (list): Lista con un elemento: el entero procesado
        
        Returns:
            int: El número (primer elemento de items)
        """
        return items[0]

    def tipo_conversion(self, items):
        """
        Extrae el tipo de conversión (sistema numérico destino).
        
        Args:
            items (list): Lista con un token que contiene el tipo de conversión
        
        Returns:
            str: El nombre del sistema destino (ej: "Romano", "Binario")
        """
        return items[0].value

    def conversion(self, items):
        """
        Realiza la conversión del número decimal al sistema especificado.
        
        Implementa las conversiones a los siguientes sistemas:
            - Binario      : Base 2
            - Octal        : Base 8
            - Hexadecimal  : Base 16
            - Romano       : Numerales romanos
            - Alternativo  : Fórmula especial (ALT = n * 7)
            - Aleatorio    : Elige un sistema al azar
        
        Args:
            items (list): Lista con dos elementos:
                - items[0] (int): Número decimal
                - items[1] (str): Sistema de conversión destino
        
        Returns:
            str: Cadena formateada con el resultado: "(Sistema: X) resultado"
        """
        num = items[0]
        destino = items[1]

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

        # Retorna el resultado formateado
        return f"(Sistema: {destino}) {res}"

    def instruccion(self, items):
        """
        Procesa una instrucción completa (una conversión).
        
        Args:
            items (list): Lista con un elemento: el resultado de conversion()
        
        Returns:
            str: El resultado formateado de la conversión
        """
        return items[0]
