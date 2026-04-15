# Compiladores-Grupo-5-Proyecto-Final

El `README.md` que has redactado es muy claro, pero para que sea funcional con la estructura de carpetas que tienes (donde `app.py` está en la raíz y la lógica en `conversion/`), hay un detalle técnico importante: **las importaciones**.

Aquí tienes la versión corregida y optimizada de tu `README.md`, junto con un pequeño ajuste necesario para que Python encuentre los módulos correctamente.

---

### README.md corregido

```markdown
# Convertidor de Números y Analizador Sintáctico

Proyecto académico para la asignatura de Compiladores. Permite convertir números decimales a sistemas: Hexadecimal, Octal, Binario, Romano, Alternativo o Aleatorio, visualizando el árbol de derivación.

## 🚀 Características
* **Análisis Léxico/Sintáctico**: Uso de `Lark` para procesamiento de gramáticas.
* **Transformación**: Clase `TransformadorNumeros` para convertir el árbol en resultados.
* **Visualización**: Interfaz web con `D3.js` para renderizar el árbol sintáctico.
* **Backend**: API REST con `Flask`.

## 🛠 Estructura
```text
project/
├── app.py                # Servidor Flask
├── conversion/           # Módulos de lógica
│   ├── __init__.py       # Necesario para importar como paquete
│   ├── grammar.py        # Gramática Lark
│   └── transformer_utils.py # Transformador y utilidades
├── templates/
│   └── index.html        # Frontend
└── README.md
```

## ⚙️ Instalación

1. **Clonar/Descargar** el proyecto.
2. **Entorno Virtual** (Recomendado):
   ```bash
   python -m venv venv
   # Windows: venv\Scripts\activate
   # Linux/Mac: source venv/bin/activate
   ```
3. **Instalar dependencias**:
   ```bash
   pip install flask lark
   ```

## 🏃‍♂️ Cómo ejecutar el proyecto

Para que Python reconozca los módulos dentro de la carpeta `conversion/`, ejecuta el servidor desde la raíz (`project/`) usando el flag de módulo `-m`:

```bash
python -m app
```
*Nota: Si prefieres ejecutar `python app.py`, asegúrate de que el archivo `__init__.py` exista dentro de la carpeta `conversion/`.*

## 📋 Uso
1. Ingresa al navegador: `http://127.0.0.1:5000`
2. Formato de entrada: `NumeroDestino$` (ej. `525Romano$`).
3. El árbol sintáctico aparecerá automáticamente en pantalla.
```

---

### Ajustes técnicos que debes realizar para que esto funcione:

1.  **Crea el archivo `conversion/__init__.py`**:
    * Ve a la carpeta `conversion/` y crea un archivo llamado `__init__.py` (puede estar vacío). Sin este archivo, Python no reconocerá `conversion` como un paquete y fallará el `from conversion.grammar import parser`.
2.  **Ajusta tus imports en `app.py`**:
    * Al ejecutar `python -m app` (o `python app.py` con el `__init__`), asegúrate de que los imports dentro de `app.py` se mantengan como los tienes ahora:
        ```python
        from conversion.grammar import parser
        from conversion.transformer_utils import TransformadorNumeros, tree_to_dict
        ```
3.  **¿Por qué `pip install re` no es necesario?**
    * En tu comando de instalación (`pip install flask lark re`), eliminé `re` porque es una **librería estándar de Python** (viene instalada por defecto). No necesitas instalarla.

Con estos cambios, la estructura que definiste será totalmente funcional y profesional. ¡Éxito con tu proyecto final de Compiladores!