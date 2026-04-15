from flask import Flask, request, jsonify, render_template
from conversion.grammar import parser
from conversion.transformer_utils import TransformadorNumeros, tree_to_dict

app = Flask(__name__)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/parse", methods=["POST"])
def parse():
    data = request.get_json()
    entrada = data.get("entrada", "")

    try:
        arbol = parser.parse(entrada)
        transformador = TransformadorNumeros()
        resultado = transformador.transform(arbol)

        return jsonify({
            "ok": True,
            "tree": tree_to_dict(arbol),
            "resultado": [str(r) for r in resultado.children]
        })

    except Exception:
        return jsonify({
            "ok": False,
            "error": "Entrada no válida. Usa formato: NumeroDestino$ (ej: 525Romano$)"
        })

if __name__ == "__main__":
    app.run(debug=True)
