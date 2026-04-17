"""
Módulo de definición de la gramática Lark para el convertidor de números.

Define la gramática EBNF que especifica la sintaxis válida para las conversiones
de números decimales a otros sistemas numéricos. Utiliza el parser Lark para
analizar y construir un árbol sintáctico (AST).

Sintaxis de entrada válida:
    - Formato: <número><sistema>$
    - Ejemplos: 525Romano$, 100Binario$, 255Hexadecimal$
"""

from lark import Lark

# -------- DEFINICIÓN DE LA GRAMÁTICA --------
# La gramática define la estructura sintáctica que debe cumplir la entrada
gramatica = r"""
?start: programa

programa: instruccion+

instruccion: conversion fin

conversion: numero tipo_conversion

numero: entero

entero: DIGITO+

DIGITO: /[0-9]/

HEX: "Hexadecimal"
OCT: "Octal"
BIN: "Binario"
ROM: "Romano"
ALT: "Alternativo"
ALE: "Aleatorio"

tipo_conversion: HEX | OCT | BIN | ROM | ALT | ALE

FIN: "$"
fin: FIN

%import common.WS
%ignore WS
"""

# -------- EXPLICACIÓN DE LA GRAMÁTICA --------
# 
# Reglas principales:
#   - start       : Punto de entrada del parser
#   - programa    : Una o más instrucciones
#   - instruccion : Una conversión seguida de '$'
#   - conversion  : Un número seguido de un tipo de conversión
#   - numero      : Uno o más dígitos
#   - entero      : Dígitos consecutivos formando un número
#
# Tokens (terminales):
#   - DIGITO      : Cualquier dígito del 0 al 9
#   - HEX         : Literal "Hexadecimal"
#   - OCT         : Literal "Octal"
#   - BIN         : Literal "Binario"
#   - ROM         : Literal "Romano"
#   - ALT         : Literal "Alternativo"
#   - ALE         : Literal "Aleatorio"
#   - FIN         : Literal "$" (terminador)
#   - WS          : Espacios en blanco (ignorados)
#
# El símbolo '?' en ?start y ?programa indica que estas reglas son "inline"
# (no se crean nodos adicionales en el árbol sintáctico)

# Instancia del parser Lark usando la gramática definida
# start='programa' especifica que el análisis comienza desde la regla 'programa'
parser = Lark(gramatica, start='programa')
