"""
Aplicación Flask para el convertidor de sistemas numéricos.

Este módulo proporciona una interfaz web para convertir números decimales
a diferentes sistemas numéricos (binario, octal, hexadecimal, Romano, etc).

Rutas:
    - GET  /          : Página principal (renderiza index.html)
    - POST /parse     : Endpoint para procesar conversiones de números
"""

from flask import Flask, request, jsonify, render_template
from conversion.grammar import parser
from conversion.transformer_utils import TransformadorNumeros, tree_to_dict

# Inicialización de la aplicación Flask
app = Flask(__name__)


@app.route("/")
def home():
    """
    Ruta principal de la aplicación.
    
    Returns:
        str: Renderiza el archivo index.html con la interfaz web.
    """
    return render_template("index.html")


@app.route("/parse", methods=["POST"])
def parse():
    """
    Endpoint para procesar y convertir números entre sistemas.
    
    Recibe una petición POST con un número en formato JSON y lo convierte
    al sistema numérico especificado usando el parser Lark.
    
    Formato esperado:
        {
            "entrada": "525Romano$"
        }
    
    Returns:
        dict: JSON con la siguiente estructura:
            - Si es exitoso:
                {
                    "ok": true,
                    "tree": {...},  # Árbol sintáctico en formato dict
                    "resultado": [...]  # Lista de resultados de conversión
                }
            - Si hay error:
                {
                    "ok": false,
                    "error": "Mensaje de error"
                }
    """
    # Extrae los datos JSON de la petición
    data = request.get_json()
    entrada = data.get("entrada", "")

    try:
        # Realiza el análisis sintáctico de la entrada
        arbol = parser.parse(entrada)
        
        # Crea una instancia del transformador y aplica las conversiones
        transformador = TransformadorNumeros()
        resultado = transformador.transform(arbol)

        # Retorna la respuesta exitosa con el árbol sintáctico y resultados
        return jsonify({
            "ok": True,
            "tree": tree_to_dict(arbol),
            "resultado": [str(r) for r in resultado.children]
        })

    except Exception:
        # Manejo de excepciones: entrada no válida
        return jsonify({
            "ok": False,
            "error": "Entrada no válida. Usa formato: NumeroDestino$ (ej: 525Romano$)"
        })


# Punto de entrada de la aplicación
if __name__ == "__main__":
    # Inicia el servidor Flask en modo debug (recargar automático en cambios)
    app.run(debug=True)
