# 🔢 Convertidor de Números - Grupo 5 UNAH

> **Proyecto Final - Asignatura: Diseño de Compiladores**
> Universidad Nacional Autónoma de Honduras | Facultad de Ingeniería en Sistemas

---

## 📋 Descripción del Proyecto

Compilador/traductor que convierte números enteros en **base decimal (base 10)** a diferentes sistemas numéricos. El proyecto implementa un **parser Lark** con análisis léxico y sintáctico completo, generando un árbol sintáctico abstracto (AST) que es transformado para obtener conversiones precisas.

### 🎯 Objetivo

Demostrar la implementación de un compilador simple pero completo, aplicando conceptos de:
- **Análisis Léxico:** Identificación de tokens
- **Análisis Sintáctico:** Construcción del AST
- **Transformación:** Conversión de números a diferentes bases

---

## 📊 Sistemas de Conversión Soportados

| Sistema | Base | Rango | Ejemplo (525) |
|---------|------|-------|---------------|
| **Hexadecimal** | 16 | 0-9, A-F | `20D` |
| **Octal** | 8 | 0-7 | `1015` |
| **Binario** | 2 | 0-1 | `1000001101` |
| **Romano** | Especial | I,V,X,L,C,D,M | `DXXV` |
| **Alternativo** | Fórmula (n×7) | Especial | `ALT-3675` |
| **Aleatorio** | Random | Cualquiera | `20D` o `DXXV` |

---

## 🏗️ Estructura del Proyecto

```
Compiladores-Grupo-5-Proyecto-Final/
│
├── 📄 README.md                     # Este archivo
├── 📄 .gitignore                    # Configuración de Git
│
├── 🐍 app.py                        # Aplicación Flask (servidor web)
│
├── 📁 conversion/
│   ├── grammar.py                   # Definición de la gramática Lark
│   ├── transformer_utils.py         # Transformer y utilidades
│   └── logica_inicial.py            # Interfaz CLI (línea de comandos)
│
├── 📁 templates/
│   └── index.html                   # Interfaz web (HTML/CSS/JavaScript)
│
└── 📁 python/                       # Reservado (vacío)
```

---

## 🛠️ Requisitos Previos

### Dependencias
```
Flask >= 2.0.0
Lark >= 0.12.0
Python >= 3.8
```

### Instalación

```bash
# Clonar el repositorio
git clone https://github.com/tu-usuario/Compiladores-Grupo-5-Proyecto-Final.git
cd Compiladores-Grupo-5-Proyecto-Final

# Instalar dependencias
pip install flask lark
```

---

## 🚀 Cómo Ejecutar

### Opción 1: Interfaz Web (Recomendado)

```bash
# Iniciar servidor Flask
python app.py
```

Luego accede a:
- **URL:** http://localhost:5000
- **Características:**
  - ✅ Entrada manual de conversiones
  - ✅ Carga de archivos .txt
  - ✅ Visualización de árbol sintáctico con D3.js
  - ✅ Tabla de análisis léxico
  - ✅ Procedimiento paso a paso
  - ✅ Ejemplos predefinidos
  - ✅ Control de zoom interactivo

### Opción 2: Interfaz de Línea de Comandos (CLI)

```bash
# Ejecutar CLI interactiva
python conversion/logica_inicial.py
```

**Ejemplo de uso:**
```
--- CONVERTIDOR DE NÚMEROS ---

Ingrese cadena (ej. 525Romano$) o 'salir': 525Romano$

DETALLE DEL ANALIZADOR LÉXICO:
Línea | Token    | Lexema      | Columna | Longitud | Patrón RE
────────────────────────────────────────────────────────────────
  1   | NUMERO   | 525         | 1       | 3        | \d+
  1   | DESTINO  | Romano      | 4       | 6        | Hex|Rom
  1   | FIN      | $           | 10      | 1        | \$

SALIDA SINTÁCTICA (OPERACIÓN):
-> Resultado: (Sistema: Romano) DXXV
```

---

## 📝 Formato de Entrada

### Sintaxis
```
<número><sistema>$
```

### Ejemplos Válidos

| Entrada | Salida | Sistema |
|---------|--------|---------|
| `525Romano$` | `DXXV` | Romano |
| `525Hexadecimal$` | `20D` | Hexadecimal |
| `525Octal$` | `1015` | Octal |
| `525Binario$` | `1000001101` | Binario |
| `525Alternativo$` | `ALT-3675` | Alternativo (n×7) |
| `525Aleatorio$` | `20D` o `DXXV` | Aleatorio (random) |

### Ejemplos Inválidos (No Aceptados)

```
525 Romano       # Falta el $
525$             # Falta el sistema
525 Binario $    # Los espacios pueden causar problemas
525Decimal$      # Sistema no soportado
ABC Binario$     # Entrada no es numérica
```

---

## 🔍 Flujo de Procesamiento

```
┌─────────────────────────────────────────────────────────────────┐
│ 1. ENTRADA DEL USUARIO                                          │
│    "525Romano$"                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 2. ANÁLISIS LÉXICO (Tokenización)                               │
│    • Identifica dígitos: [5][2][5]                              │
│    • Identifica sistema: [Romano]                               │
│    • Identifica terminador: [$]                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 3. ANÁLISIS SINTÁCTICO (Parsing)                                │
│    • Parser Lark construye el AST usando grammar.py             │
│    • Estructura jerárquica de reglas                            │
│    • Validación de sintaxis                                     │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 4. ÁRBOL SINTÁCTICO ABSTRACTO (AST)                             │
│    programa                                                      │
│    └─ instruccion                                               │
│       ├─ conversion                                             │
│       │  ├─ numero: 525                                         │
│       │  └─ tipo_conversion: Romano                             │
│       └─ fin: $                                                 │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 5. TRANSFORMACIÓN (transformer_utils.py)                        │
│    • Extrae valores del AST                                     │
│    • Aplica lógica de conversión                                │
│    • Invoca método correspondiente                              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
┌──────────────────────▼──────────────────────────────────────────┐
│ 6. RESULTADO                                                     │
│    525 (decimal) → DXXV (romano)                                │
└─────────────────────────────────────────────────────────────────┘
```

---

## 📁 Descripción de Archivos

### 🐍 `app.py`
Aplicación Flask que proporciona:
- **GET `/`** - Renderiza la interfaz web (index.html)
- **POST `/parse`** - Endpoint que procesa conversiones
  - Recibe JSON: `{"entrada": "525Romano$"}`
  - Retorna JSON: `{"ok": true, "tree": {...}, "resultado": [...]}`

**Líneas:** 88 | **Estado:** Documentado ✅

### 🐍 `conversion/grammar.py`
Define la gramática EBNF del lenguaje usando Lark:
- Reglas gramaticales (minúsculas): `start`, `programa`, `instruccion`, etc.
- Tokens (MAYÚSCULAS): `DIGITO`, `HEX`, `OCT`, `BIN`, `ROM`, `ALT`, `ALE`, `FIN`
- Símbolos especiales: `?` (inline), `+` (una o más), `|` (disyunción)
- Espacios ignorados: `%import common.WS`, `%ignore WS`

**Líneas:** 300 | **Estado:** Completamente documentado ✅

### 🐍 `conversion/transformer_utils.py`
Implementa la lógica de transformación:
- **`dec_a_romano(n)`** - Convierte decimal a numerales romanos
- **`tree_to_dict(tree)`** - Convierte AST a diccionario JSON
- **`TransformadorNumeros`** - Clase Transformer de Lark
  - `DIGITO()` - Procesa dígitos individuales
  - `entero()` - Forma números enteros
  - `conversion()` - Realiza conversiones numérica
  - `instruccion()` - Procesa instrucciones

**Líneas:** 225 | **Estado:** Completamente documentado ✅

### 🐍 `conversion/logica_inicial.py`
Interfaz CLI para testing:
- **`dec_a_romano(n)`** - Igual que en transformer_utils.py
- **`TransformadorNumeros`** - Transformer para CLI
- **`cuadro_lexico_detallado(entrada)`** - Muestra análisis léxico
- **`ejecutar_traductor()`** - Loop principal interactivo

**Líneas:** 254 | **Estado:** Completamente documentado ✅

### 🌐 `templates/index.html`
Interfaz web moderna y responsiva:
- **HTML:** Estructura de dos paneles (entrada + árbol)
- **CSS:** Diseño con variables de marca UNAH
- **JavaScript:** 17 funciones documentadas
  - Comunicación con backend (Fetch API)
  - Visualización de árboles (D3.js)
  - Interactividad (tabs, modales, acordeones)
  - Análisis léxico en tabla

**Líneas:** 1,793 | **Estado:** Completamente documentado ✅

---

## 🧮 Ejemplos de Uso

### Ejemplo 1: Romano

```
Entrada:  525Romano$
Proceso:  525 ÷ 500 = 1 × D + 25 ÷ 10 = 2 × X + 5 ÷ 5 = 1 × V
Salida:   DXXV
```

### Ejemplo 2: Hexadecimal

```
Entrada:  525Hexadecimal$
Proceso:  
  525 ÷ 16 = 32 residuo 13 (D)
  32 ÷ 16 = 2 residuo 0
  2 ÷ 16 = 0 residuo 2
  Lectura de residuos: 20D
Salida:   20D
```

### Ejemplo 3: Binario

```
Entrada:  525Binario$
Proceso:
  525 ÷ 2 = 262 residuo 1
  262 ÷ 2 = 131 residuo 0
  ... (continúa hasta 0)
  Lectura de residuos: 1000001101
Salida:   1000001101
```

### Ejemplo 4: Alternativo (Fórmula del Grupo)

```
Entrada:  525Alternativo$
Proceso:  525 × 7 = 3675
Salida:   ALT-3675
```

### Ejemplo 5: Aleatorio

```
Entrada:  525Aleatorio$
Proceso:  Elige al azar entre Hexadecimal, Octal, Binario, Romano, Alternativo
Salida 1: 20D (eligió Hexadecimal)
Salida 2: DXXV (eligió Romano)
Salida 3: ALT-3675 (eligió Alternativo)
```

---

## 🧩 Gramática EBNF

```ebnf
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
```

### Explicación de la Gramática

- **`?start: programa`** - Punto de entrada del parser (inline)
- **`programa: instruccion+`** - Una o más instrucciones
- **`instruccion: conversion fin`** - Conversión + terminador ($)
- **`conversion: numero tipo_conversion`** - Número + Sistema
- **`numero: entero`** - Un número entero
- **`entero: DIGITO+`** - Uno o más dígitos
- **`DIGITO: /[0-9]/`** - Expresión regular para dígitos
- **Tokens de sistema** - 6 opciones (HEX, OCT, BIN, ROM, ALT, ALE)
- **Espacios ignorados** - Se pueden usar espacios opcionales

---

## 🔧 Análisis Léxico (Tokenización)

El análisis léxico identifica los siguientes componentes:

| Lexema | Token | Tipo | Ejemplo |
|--------|-------|------|---------|
| [0-9] | DIGITO | Dígito individual | `5` |
| [0-9]+ | NÚMERO | Secuencia de dígitos | `525` |
| Hexadecimal | HEX | Literal (base 16) | `"Hexadecimal"` |
| Octal | OCT | Literal (base 8) | `"Octal"` |
| Binario | BIN | Literal (base 2) | `"Binario"` |
| Romano | ROM | Literal (romanos) | `"Romano"` |
| Alternativo | ALT | Literal (fórmula n×7) | `"Alternativo"` |
| Aleatorio | ALE | Literal (random) | `"Aleatorio"` |
| $ | FIN | Terminador | `"$"` |

---

## 📊 Árbol Sintáctico Abstracto (AST)

### Ejemplo: "525Romano$"

```
programa
└─ instruccion
   ├─ conversion
   │  ├─ numero
   │  │  └─ entero: 525
   │  └─ tipo_conversion: Romano (token ROM)
   └─ fin: $ (token FIN)
```

### Ejemplo: "100Hexadecimal$ 255Binario$"

```
programa
├─ instruccion
│  ├─ conversion
│  │  ├─ numero: 100
│  │  └─ tipo_conversion: Hexadecimal
│  └─ fin: $
└─ instruccion
   ├─ conversion
   │  ├─ numero: 255
   │  └─ tipo_conversion: Binario
   └─ fin: $
```

---

## 👥 Integrantes del Grupo 5

| Carné | Nombre |
|-------|--------|
| 20131001536 | Michael Hernan Archaga Nuñez |
| 20181006565 | Idalia Ivón Zelaya Cruz |
| 20191005514 | Sara Nicolle Salinas Ramos |
| 20191032481 | Diego Fernando Rubio Godoy |
| 20221001175 | José Francisco Vargas Carrasco |

---

## 📚 Documentación Adicional

- **`conversion/grammar.py`** - Documentación exhaustiva de la gramática
  - 6 niveles explicados
  - Tabla de tokens
  - Ejemplos de AST
  - Casos de uso

- **Archivos Python** - Comentarios inline detallados
  - Docstrings completos
  - Explicación de algoritmos
  - Ejemplos de uso

---

## 📖 Referencias

### Herramientas Utilizadas

- **Lark** - Parser generator (https://lark-parser.readthedocs.io/)
- **Flask** - Web framework (https://flask.palletsprojects.com/)
- **D3.js** - Visualización de árboles (https://d3js.org/)
- **Python 3.8+** - Lenguaje de programación

---

## 📝 Licencia

Este proyecto es de uso educativo exclusivamente.

**Asignatura:** Diseño de Compiladores  
**Universidad:** UNAH (Universidad Nacional Autónoma de Honduras)  
**Período:** 1-2026


