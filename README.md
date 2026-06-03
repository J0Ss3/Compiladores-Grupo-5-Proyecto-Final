# Convertidor de Números - Grupo 5 UNAH

> **Proyecto Final - Asignatura: Diseño de Compiladores**  
> Universidad Nacional Autónoma de Honduras | Facultad de Ingeniería en Sistemas

---

## Descripción

Compilador/traductor que convierte números enteros en **base decimal (base 10)** a diferentes sistemas numéricos usando un **parser Lark** con análisis léxico y sintáctico completo.

### Sistemas de Conversión Soportados

| Sistema         | Base     | Ejemplo (525) |
| --------------- | -------- | ------------- |
| Hexadecimal     | 16       | `20D`         |
| Octal           | 8        | `1015`        |
| Binario         | 2        | `1000001101`  |
| Romano          | Especial | `DXXV`        |
| Alternativo     | n×7      | `ALT-3675`    |
| Aleatorio       | Random   | Cualquiera    |

---

## Requisitos

- [Docker Desktop](https://www.docker.com/products/docker-desktop) instalado y corriendo

---

## Correr con Docker

**1. Clonar el repositorio**
```bash
git clone https://github.com/J0Ss3/Compiladores-Grupo-5-Proyecto-Final.git
cd Compiladores-Grupo-5-Proyecto-Final
```

**2. Crear los archivos Docker** (PowerShell en Windows)
```powershell
@'
FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends git && rm -rf /var/lib/apt/lists/*
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 5000
ENV FLASK_APP=app.py
ENV FLASK_ENV=development
ENV FLASK_DEBUG=1
ENV PYTHONUNBUFFERED=1
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]
'@ | Set-Content Dockerfile

@'
version: "3.9"
services:
  compiladores:
    build: .
    container_name: compiladores-grupo5
    ports:
      - "5000:5000"
    volumes:
      - .:/app
    environment:
      - FLASK_APP=app.py
      - FLASK_ENV=development
      - FLASK_DEBUG=1
    restart: unless-stopped
'@ | Set-Content docker-compose.yml

@'
Flask>=2.0.0
lark>=1.0.0
'@ | Set-Content requirements.txt
```

**3. Levantar el proyecto**
```bash
docker compose up --build
```

**4. Abrir en el navegador**

`http://localhost:5000`

---

## Comandos útiles

```bash
# Detener el contenedor
docker compose down

# Ver logs
docker compose logs -f

# Reiniciar
docker compose restart
```

---

## Formato de Entrada

```
<número><sistema>$
```

| Entrada           | Salida       |
| ----------------- | ------------ |
| `525Romano$`      | `DXXV`       |
| `525Hexadecimal$` | `20D`        |
| `525Octal$`       | `1015`       |
| `525Binario$`     | `1000001101` |
| `525Alternativo$` | `ALT-3675`   |

---

## Integrantes del Grupo 5

| Carné       | Nombre                         |
| ----------- | ------------------------------ |
| 20131001536 | Michael Hernan Archaga Nuñez   |
| 20181006565 | Idalia Ivón Zelaya Cruz        |
| 20191005514 | Sara Nicolle Salinas Ramos     |
| 20191032481 | Diego Fernando Rubio Godoy     |
| 20221001175 | José Francisco Vargas Carrasco |

---

> Proyecto de uso educativo — UNAH, Período 1-2026