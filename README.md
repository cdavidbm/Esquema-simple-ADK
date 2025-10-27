===============================================================================
FLUJO DE EJECUCIÓN:
===============================================================================

1. INICIO           → Importar librerías de ADK y Configurar credenciales de Google
2. TOOL             → Definir función que el agente puede usar
3. AGENT            → Crear agente con instrucciones y herramientas
4. SESSION SERVICE  → Crear servicio para guardar conversaciones
5. RUNNER           → Crear ejecutor que conecta todo
6. INTERACCIÓN      → Enviar mensaje y recibir respuesta


===============================================================================
DIAGRAMA VISUAL: ARQUITECTURA DE ADK
===============================================================================
Este diagrama muestra cómo fluye la información en un proyecto ADK


FLUJO DE EJECUCIÓN DE ADK
===========================

┌─────────────────────────────────────────────────────────────────┐
│  1. USUARIO ENVÍA MENSAJE                                       │
│  ↓                                                              │
│  "Saluda a María"                                               │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│  2. RUNNER recibe el mensaje                                    │
│  ↓                                                              │
│  • Prepara el contexto                                          │
│  • Carga el historial de la sesión                              │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│  3. AGENT (el cerebro)                                          │
│  ↓                                                              │
│  • Lee el mensaje                                               │
│  • Analiza qué hacer                                            │
│  • Decide si usar una TOOL                                      │
│                                                                 │
│  Instrucciones:                                                 │
│  "Eres un asistente amigable..."                                │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│  4. TOOL (herramienta)                                          │
│  ↓                                                              │
│  def saludar(nombre: str) -> str:                               │
│      return f"¡Hola {nombre}!"                                  │
│                                                                 │
│  Ejecuta: saludar("María")                                      │
│  Retorna: "¡Hola María!"                                        │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│  5. AGENT procesa el resultado                                  │
│  ↓                                                              │
│  • Recibe "¡Hola María!"                                        │
│  • Formula respuesta final                                      │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│  6. SESSION SERVICE guarda el historial                         │
│  ↓                                                              │
│  Historial:                                                     │
│  [Usuario]: "Saluda a María"                                    │
│  [Agente]: "¡Hola María!"                                       │
└──────────────────────┬──────────────────────────────────────────┘
                       │
                       ↓
┌─────────────────────────────────────────────────────────────────┐
│  7. RUNNER devuelve respuesta al usuario                        │
│  ↓                                                              │
│  "¡Hola María!"                                                 │
└─────────────────────────────────────────────────────────────────┘


COMPONENTES CLAVE
==================

┌─────────────────┐
│     AGENT       │  ← El "cerebro" que toma decisiones
│   (Cerebro)     │
└────────┬────────┘
         │ usa
         ↓
┌─────────────────┐
│      TOOLS      │  ← Funciones que extienden las capacidades
│  (Herramientas) │
└─────────────────┘

┌─────────────────┐
│     RUNNER      │  ← Ejecuta el agente y gestiona el flujo
│   (Ejecutor)    │
└────────┬────────┘
         │ usa
         ↓
┌─────────────────┐
│ SESSION SERVICE │  ← Guarda el historial de conversación
│    (Memoria)    │
└─────────────────┘


ANALOGÍA CON UN RESTAURANTE
=============================

AGENT        = Chef (decide qué cocinar y cómo)
TOOLS        = Utensilios de cocina (sartén, cuchillo, horno)
RUNNER       = Mesero (toma pedidos y entrega comida)
SESSION      = Libreta de pedidos (historial de lo que ha pedido cada cliente)
USER         = Cliente (hace pedidos)


ESTRUCTURA DE ARCHIVOS TÍPICA
==============================

mi_proyecto_adk/
│
├── main.py                 ← Tu código principal
├── .env                    ← API Keys (no subir a git)
├── requirements.txt        ← Dependencias (google-adk)
└── README.md               ← Documentación


CÓDIGO MÍNIMO NECESARIO
========================

import asyncio
import os
from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# 1. Configurar
os.environ["GOOGLE_API_KEY"] = "tu_key"
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"

# 2. Crear Tool
def mi_funcion(param: str) -> str:
    \"\"\"Descripción\"\"\"
    return f"Resultado: {param}"

# 3. Crear Agent
agente = Agent(
    name="mi_agente",
    model="gemini-2.0-flash",
    instruction="Instrucciones",
    tools=[mi_funcion]
)

# 4. Crear Session Service
sesiones = InMemorySessionService()

# 5. Crear Runner
runner = Runner(
    agent=agente,
    app_name="mi_app",
    session_service=sesiones
)

# 6. Interactuar
async def preguntar(texto: str):
    await sesiones.create_session(
        app_name="mi_app",
        user_id="user1",
        session_id="session1"
    )
    mensaje = types.Content(
        role="user",
        parts=[types.Part(text=texto)]
    )
    async for evento in runner.run_async(
        user_id="user1",
        session_id="session1",
        new_message=mensaje
    ):
        if evento.is_final_response() and evento.content:
            for parte in evento.content.parts:
                if hasattr(parte, "text"):
                    print(parte.text)

# 7. Ejecutar
async def main():
    await preguntar("Tu pregunta")

if __name__ == "__main__":
    asyncio.run(main())


FLUJO DE DATOS SIMPLIFICADO
============================

┌─────────┐
│ Usuario │
└────┬────┘
     │ mensaje
     ↓
┌─────────┐
│ Runner  │ ──→ busca historial ──→  ┌─────────────────┐
└────┬────┘                          │ Session Service │
     │                               └─────────────────┘
     │ mensaje + contexto
     ↓
┌─────────┐
│  Agent  │ ──→ necesita función ──→  ┌──────┐
└────┬────┘                           │ Tool │
     │                                └──────┘
     │ respuesta                         ↑
     └───────────────────────────────────┘
     │
     ↓
┌─────────┐
│ Usuario │ ← recibe respuesta
└─────────┘


EJEMPLO PRÁCTICO: AGENTE CALCULADORA
======================================

1. Usuario: "¿Cuánto es 5 + 3?"

2. Agent piensa:
   - Necesito sumar números
   - Tengo la herramienta "calcular"
   - Voy a usarla

3. Agent llama: calcular(5, 3)

4. Tool ejecuta:
   def calcular(a, b):
       return a + b
   Retorna: 8

5. Agent recibe el resultado y responde:
   "El resultado de 5 + 3 es 8"

6. Session Service guarda:
   [Usuario]: "¿Cuánto es 5 + 3?"
   [Agent]: "El resultado de 5 + 3 es 8"



ERRORES COMUNES Y SOLUCIONES
==============================

❌ Error: "API Key not found"
✓ Solución: Verifica que hayas configurado os.environ["GOOGLE_API_KEY"]

❌ Error: "Tool must have docstring"
✓ Solución: Añade docstring a tu función tool

❌ Error: "Event loop is already running"
✓ Solución: Usa await en notebooks, asyncio.run() en scripts

❌ Error: "Session not found"
✓ Solución: Crea la sesión antes de enviar mensajes


===============================================================================
"""











"""
