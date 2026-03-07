# My Course Agent

Descripción breve de lo que hace tu agente (ej. Agente conversacional construido con LangGraph para el curso de Platzi).

## Prerrequisitos

- Python >= 3.12
- [uv](https://docs.astral.sh/uv/) (Gestor de paquetes y proyectos)

## Instalación

1. **Instalar depedencias:**

```bash
uv pip install -e .
```

2. **Configurar .env**

OPENAI_API_KEY=sk-...

3. **Levantar LangSmith**

```bash
langgraph dev
```