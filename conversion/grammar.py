from lark import Lark

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

parser = Lark(gramatica, start='programa')
