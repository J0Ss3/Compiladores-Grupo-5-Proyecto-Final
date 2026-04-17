# AGENTS.md - Development Guide

This repository is a number system converter compiler built with Flask and Lark. This guide provides essential information for agentic coding assistants operating in this codebase.

## Project Overview

A compiler/translator that converts decimal numbers to various number systems (binary, octal, hexadecimal, Roman numerals, random, and alternative) using a formal grammar and parser.

**Stack**: Python 3.x, Flask, Lark (parser generator)
**Main Entry Points**: `app.py` (Flask web), `conversion/logica_inicial.py` (CLI)

---

## Build, Test & Execution Commands

### Development Server
```bash
python app.py
```
Runs Flask development server on `http://localhost:5000`

### CLI Version
```bash
python conversion/logica_inicial.py
```
Interactive command-line interface for testing the converter.

### Parse Endpoint (Manual Testing)
```bash
curl -X POST http://localhost:5000/parse \
  -H "Content-Type: application/json" \
  -d '{"entrada":"525Romano$"}'
```

### Code Quality
```bash
# Linting (if available)
flake8 *.py conversion/*.py

# Type checking (if mypy installed)
mypy app.py conversion/
```

**Note**: No pytest tests currently exist. Tests should be added to `tests/` directory following the pattern: `test_<module>.py`

---

## Code Style Guidelines

### File Organization
- **Root level**: `app.py` (Flask routes), `python` (reserved), `templates/` (HTML)
- **conversion/**: Grammar, parsing, transformation logic
- Use snake_case for all filenames and module names

### Imports
- Group in order: stdlib, third-party, local
- Sort alphabetically within groups
- Example:
  ```python
  import random
  import re
  from lark import Lark, Transformer, Tree, Token
  
  from conversion.grammar import parser
  ```

### Formatting
- Follow PEP 8: 4-space indentation, max 79 characters per line
- Use descriptive variable names (avoid single letters except loop indices)
- Separate functions and classes with two blank lines
- Separate methods within classes with one blank line

### Naming Conventions
- **Functions/variables**: `snake_case` (e.g., `dec_a_romano`, `tree_to_dict`)
- **Classes**: `PascalCase` (e.g., `TransformadorNumeros`)
- **Constants**: `UPPER_SNAKE_CASE` (e.g., `DIGITO`, `HEX`)
- **Private methods**: prefix with `_` (e.g., `_parse_tree`)

### Types & Documentation
- Include docstrings for all functions/classes (Google style preferred)
- Example:
  ```python
  def dec_a_romano(n):
      """Convert decimal to Roman numerals.
      
      Args:
          n: Decimal number to convert
          
      Returns:
          String representation in Roman numerals
      """
  ```
- Add type hints for new functions:
  ```python
  def tree_to_dict(tree: Tree | Token) -> dict:
  ```

### Error Handling
- Catch specific exceptions, avoid bare `except:`
- Include context in error messages
- Current pattern uses Flask's `jsonify()` for error responses
- Example:
  ```python
  except ValueError as e:
      return jsonify({"ok": False, "error": str(e)})
  ```

### Grammar (Lark)
- Define in raw strings with `r"""..."""`
- Use lowercase for rule names, UPPERCASE for tokens
- Include comments explaining complex rules
- Example valid input: `525Romano$`

### API Routes
- Use RESTful conventions: GET for retrieval, POST for data submission
- Always return JSON with `"ok"` boolean and `"error"` or `"resultado"` keys
- Validate input before processing

### Comments
- Use `# Comment` for inline explanations
- Use section headers: `# -------- SECTION NAME --------`
- Explain the "why", not the "what" (code is self-documenting)

---

## Project Structure

```
.
├── app.py                          # Flask application & routes
├── conversion/
│   ├── grammar.py                  # Lark grammar definition
│   ├── transformer_utils.py        # Transformer class & utilities
│   └── logica_inicial.py          # CLI version & initial logic
├── templates/
│   └── index.html                  # Web UI
└── README.md                       # (Currently empty)
```

---

## Development Workflow

1. **Making changes**: Edit files in `conversion/` or `app.py`
2. **Testing locally**: Run `python app.py` and test via web UI or curl
3. **CLI testing**: Run `python conversion/logica_inicial.py`
4. **Committing**: Use descriptive messages (e.g., "Add hexadecimal conversion")

---

## Key Dependencies

- **flask**: Web framework
- **lark**: Parser generator & AST building
- **python**: 3.x (standard library only otherwise)

---

## Common Tasks

### Adding a new number system conversion
1. Add token to grammar in `conversion/grammar.py` (e.g., `NEW: "NewSystem"`)
2. Add conversion logic in `TransformadorNumeros.conversion()` method
3. Test via CLI or web interface

### Modifying the grammar
- Edit `conversion/grammar.py` (`gramatica` variable)
- Update both `grammar.py` and `logica_inicial.py` if keeping them in sync
- Test with `python conversion/logica_inicial.py`

### Adding Flask routes
- Edit `app.py`
- Follow existing pattern: request validation → processing → JSON response
- Add template files to `templates/` if needed

---

## Notes

- No existing rule files (.cursorrules, .cursor/rules/, .github/copilot-instructions.md) found
- No test framework configured yet
- Grammar uses Lark's EBNF syntax
- Input format: `<number><destination>$` (e.g., `525Romano$`)
