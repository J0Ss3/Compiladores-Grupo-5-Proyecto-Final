"""
Módulo de definición de la gramática Lark para el Convertidor de Números.

DESCRIPCIÓN DEL PROYECTO:
    Convertidor de sistemas numéricos que toma números enteros en base decimal (base 10)
    y los convierte a diferentes sistemas numéricos según un identificador de destino.
    
FLUJO DE PROCESAMIENTO:
    Entrada (string) → Parser Lark (gramática) → AST → Transformer → Salida (conversión)
    
    Ejemplo:
        • Entrada:   "525Romano$"          → Salida: "DXXV"
        • Entrada:   "525Hexadecimal$"     → Salida: "20D"
        • Entrada:   "525Octal$"           → Salida: "1015"
        • Entrada:   "525Binario$"         → Salida: "1000001101"
        • Entrada:   "525Alternativo$"     → Salida: "ALT-3675" (n * 7)
        • Entrada:   "525Aleatorio$"       → Salida: Aleatorio (20D o DXXV, etc)

COMPONENTES DEL LENGUAJE:
    1. NÚMERO: Cadena de dígitos decimales (0-9)
       Ejemplo: 525, 100, 255
    
    2. SISTEMA DE DESTINO: Identificador que especifica a qué sistema convertir
       • Hexadecimal  : Conversión a base 16 (0-9, A-F)
       • Octal        : Conversión a base 8 (0-7)
       • Binario      : Conversión a base 2 (0-1)
       • Romano       : Numerales romanos (I, V, X, L, C, D, M)
       • Alternativo  : Fórmula especial del grupo (número × 7)
       • Aleatorio    : Elige uno de los anteriores al azar
    
    3. TERMINADOR: Símbolo "$" que marca el final de la instrucción

TOKENS (Componentes léxicos a identificar):
    El análisis léxico debe identificar:
    • NÚMERO       : Secuencia de dígitos (0-9)+
    • SISTEMA      : "Hexadecimal", "Octal", "Binario", "Romano", "Alternativo" o "Aleatorio"
    • FIN          : Símbolo "$"
"""

from lark import Lark

# ════════════════════════════════════════════════════════════════════════════════
# EXPLICACIÓN DETALLADA DE LA GRAMÁTICA EBNF
# ════════════════════════════════════════════════════════════════════════════════
#
# La gramática define las reglas que especifican qué cadenas son válidas en nuestro
# lenguaje. Utiliza notación EBNF (Extended Backus-Naur Form).
#
# ESTRUCTURA:
#   - REGLAS (minúsculas): Combinaciones de otros elementos (no terminales)
#   - TOKENS (MAYÚSCULAS): Elementos básicos identificados por lexemas (terminales)
#
# ════════════════════════════════════════════════════════════════════════════════
#
# NIVEL 1: PUNTO DE ENTRADA
# ───────────────────────────
# ?start: programa
#   • Punto de entrada del parser
#   • El símbolo '?' indica que es una regla "inline"
#   • (el nodo 'start' no aparecerá en el árbol sintáctico, se expande directamente)
#   • Delega a la regla 'programa'
#
# ════════════════════════════════════════════════════════════════════════════════
#
# NIVEL 2: ESTRUCTURA PRINCIPAL
# ──────────────────────────────
# programa: instruccion+
#   • Una INSTRUCCIÓN puede tener una o más conversiones (instruccion+)
#   • El símbolo '+' significa una o más repeticiones
#   • Ejemplo válido: "525Romano$ 100Binario$" (dos instrucciones)
#   • El símbolo '?' hace que este nodo sea inline en el AST
#
# instruccion: conversion fin
#   • Una INSTRUCCIÓN consta de DOS partes:
#     1. Una CONVERSIÓN: (número + sistema de destino)
#     2. Un TERMINADOR: ($)
#   • Orden: NÚMERO SISTEMA $
#   • Ejemplo: 525Romano$
#             [NÚMERO] [SISTEMA] [TERMINADOR]
#
# ════════════════════════════════════════════════════════════════════════════════
#
# NIVEL 3: COMPONENTES DE CONVERSIÓN
# ────────────────────────────────────
# conversion: numero tipo_conversion
#   • Una CONVERSIÓN consta de:
#     1. NÚMERO: Un entero en base 10
#     2. TIPO_CONVERSION: El sistema destino (Hexadecimal, Binario, etc)
#   • Estos dos elementos van CONSECUTIVOS sin espacios
#   • Ejemplo: 525Romano
#            [número][tipo_conversion]
#
# numero: entero
#   • NÚMERO es simplemente un ENTERO
#   • Puede ser cualquier valor entero positivo
#
# entero: DIGITO+
#   • UN ENTERO es uno o más DÍGITOS consecutivos
#   • El '+' significa UNA O MÁS repeticiones
#   • Ejemplos válidos: 5, 52, 525, 1000, 999999
#
# DIGITO: /[0-9]/
#   • UN DÍGITO es cualquier carácter entre 0 y 9
#   • Usa expresión regular: [0-9] (cualquier dígito del 0 al 9)
#   • Ejemplos: 0, 1, 2, 3, 4, 5, 6, 7, 8, 9
#
# ════════════════════════════════════════════════════════════════════════════════
#
# NIVEL 4: TOKENS DE SISTEMA DE DESTINO
# ───────────────────────────────────────
# Estos tokens identifican a qué sistema convertir el número.
# Cada uno representa un TÉRMINO LITERAL (cadena exacta).
#
# HEX: "Hexadecimal"
#   • Token que reconoce la cadena exacta "Hexadecimal"
#   • Conversión: Decimal → Base 16 (0-9, A-F)
#   • Ejemplo: 525 → 20D
#
# OCT: "Octal"
#   • Token que reconoce la cadena exacta "Octal"
#   • Conversión: Decimal → Base 8 (0-7)
#   • Ejemplo: 525 → 1015
#
# BIN: "Binario"
#   • Token que reconoce la cadena exacta "Binario"
#   • Conversión: Decimal → Base 2 (0-1)
#   • Ejemplo: 525 → 1000001101
#
# ROM: "Romano"
#   • Token que reconoce la cadena exacta "Romano"
#   • Conversión: Decimal → Numerales romanos (I, V, X, L, C, D, M)
#   • Ejemplo: 525 → DXXV
#
# ALT: "Alternativo"
#   • Token que reconoce la cadena exacta "Alternativo"
#   • Conversión: Fórmula especial del grupo (n × 7)
#   • Ejemplo: 525 → ALT-3675 (525 × 7 = 3675)
#
# ALE: "Aleatorio"
#   • Token que reconoce la cadena exacta "Aleatorio"
#   • Conversión: Elige ALEATORIAMENTE uno de los sistemas anteriores
#   • Ejemplo 1: 525 → 20D (eligió Hexadecimal)
#   • Ejemplo 2: 525 → DXXV (eligió Romano)
#
# tipo_conversion: HEX | OCT | BIN | ROM | ALT | ALE
#   • TIPO_CONVERSION es UNO DE ESTOS tokens
#   • El símbolo '|' significa OR (disyunción)
#   • Valid: Hexadecimal, Octal, Binario, Romano, Alternativo, Aleatorio
#   • Invalid: Decimal, Binari, Hexadeci, etc (no coinciden exactamente)
#
# ════════════════════════════════════════════════════════════════════════════════
#
# NIVEL 5: TERMINADOR
# ────────────────────
# FIN: "$"
#   • Token que reconoce el carácter "$"
#   • Marca el final de una instrucción
#   • Es OBLIGATORIO al final de cada conversión
#
# fin: FIN
#   • Regla que envuelve el token FIN
#   • Permite que sea tratado como una regla en el árbol
#
# ════════════════════════════════════════════════════════════════════════════════
#
# NIVEL 6: ESPACIOS EN BLANCO (IGNORADOS)
# ─────────────────────────────────────────
# %import common.WS
#   • Importa la definición estándar de espacios en blanco (WS = whitespace)
#   • Incluye: espacios, tabs, saltos de línea
#
# %ignore WS
#   • IGNORA completamente los espacios en blanco
#   • Permite entrada como: "525 Romano $" o "525Romano$" (ambas válidas)
#   • Importante: Después de NÚMERO y SISTEMA se ignoran espacios
#
# ════════════════════════════════════════════════════════════════════════════════

# DEFINICIÓN DE LA GRAMÁTICA EBNF
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

# ════════════════════════════════════════════════════════════════════════════════
# EJEMPLOS DE ANÁLISIS SINTÁCTICO (AST)
# ════════════════════════════════════════════════════════════════════════════════
#
# EJEMPLO 1: "525Romano$"
# ────────────────────────
# Tokens identificados: [5][2][5] [Romano] [$]
#
# Árbol sintáctico (AST):
#   programa
#   └─ instruccion
#      ├─ conversion
#      │  ├─ numero
#      │  │  └─ entero: 525
#      │  └─ tipo_conversion: Romano (token ROM)
#      └─ fin: $ (token FIN)
#
# Proceso de transformación:
#   1. Parser extrae: número=525, sistema=Romano
#   2. Transformer identifica: 525 es Romano
#   3. Conversión: 525 (decimal) → DXXV (romano)
#
# ════════════════════════════════════════════════════════════════════════════════
#
# EJEMPLO 2: "100Hexadecimal$ 255Binario$"
# ───────────────────────────────────────────
# Tokens identificados: [1][0][0] [Hexadecimal] [$] [2][5][5] [Binario] [$]
#
# Árbol sintáctico (AST):
#   programa
#   ├─ instruccion
#   │  ├─ conversion
#   │  │  ├─ numero: 100
#   │  │  └─ tipo_conversion: Hexadecimal
#   │  └─ fin: $
#   └─ instruccion
#      ├─ conversion
#      │  ├─ numero: 255
#      │  └─ tipo_conversion: Binario
#      └─ fin: $
#
# Proceso de transformación:
#   Instrucción 1: 100 (decimal) → 64 (hexadecimal)
#   Instrucción 2: 255 (decimal) → 11111111 (binario)
#
# ════════════════════════════════════════════════════════════════════════════════
# TABLA DE RECONOCIMIENTO DE TOKENS (ANÁLISIS LÉXICO)
# ════════════════════════════════════════════════════════════════════════════════
#
# ┌─────────────────┬────────┬───────────────────────────────────┬──────────────┐
# │ Lexema          │ Token  │ Descripción                       │ Ejemplo      │
# ├─────────────────┼────────┼───────────────────────────────────┼──────────────┤
# │ [0-9]           │ DIGITO │ Un solo dígito                    │ 5            │
# │ [0-9]+          │ NÚMERO │ Secuencia de dígitos              │ 525          │
# │ Hexadecimal     │ HEX    │ Sistema hexadecimal (base 16)     │ "Hex..."     │
# │ Octal           │ OCT    │ Sistema octal (base 8)            │ "Oct..."     │
# │ Binario         │ BIN    │ Sistema binario (base 2)          │ "Bin..."     │
# │ Romano          │ ROM    │ Numerales romanos                 │ "Rom..."     │
# │ Alternativo     │ ALT    │ Fórmula del grupo (n × 7)         │ "Alt..."     │
# │ Aleatorio       │ ALE    │ Sistema aleatorio (random)        │ "Ale..."     │
# │ $               │ FIN    │ Terminador de instrucción         │ "$"          │
# └─────────────────┴────────┴───────────────────────────────────┴──────────────┘
#
# ════════════════════════════════════════════════════════════════════════════════
# INSTANCIA DEL PARSER
# ════════════════════════════════════════════════════════════════════════════════

parser = Lark(gramatica, start='programa')

"""
PARÁMETROS:
    • gramatica: La gramática EBNF como string
    • start='programa': Especifica que el análisis comienza desde la regla 'programa'
      (esto permite múltiples instrucciones en una sola entrada)

USO TÍPICO:
    >>> arbol = parser.parse("525Romano$")
    # Retorna el AST para ser procesado por el Transformer
    
SALIDA (AST):
    Tree('programa', [
        Tree('instruccion', [
            Tree('conversion', [
                Tree('numero', [Tree('entero', [Token('DIGITO', '5'), Token('DIGITO', '2'), Token('DIGITO', '5')])]),
                Token('ROM', 'Romano')
            ]),
            Tree('fin', [Token('FIN', '$')])
        ])
    ])
"""
