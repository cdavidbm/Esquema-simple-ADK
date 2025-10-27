# --- PASO 1: CONFIGURACIÓN ---

# pip install google-adk python-dotenv

import asyncio
import os

from dotenv import load_dotenv
from google.adk.agents import Agent
from google.adk.runners import Runner
from google.adk.sessions import InMemorySessionService
from google.genai import types

# Cargar variables de entorno
load_dotenv()

# Configurar API key desde .env
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


# --- PASO 2: CREAR HERRAMIENTA ---
def mi_herramienta(texto: str) -> str:
    """
    [REEMPLAZA] Descripción de tu herramienta.

    Args:
        texto: [REEMPLAZA] Descripción del parámetro

    Returns:
        Resultado de la operación
    """
    # [REEMPLAZA] Tu lógica aquí
    resultado = f"Procesé: {texto}"
    return resultado


# --- PASO 3: CREAR AGENTE ---
mi_agente = Agent(
    name="mi_agente",  # [REEMPLAZA] Nombre del agente
    model="gemini-2.0-flash",  # [REEMPLAZA] Modelo a usar
    instruction="""
    [REEMPLAZA] Instrucciones para tu agente.
    Ejemplo: Eres un asistente útil que procesa texto.
    """,
    tools=[mi_herramienta],  # [REEMPLAZA] Lista de herramientas
)

# --- PASO 4: CREAR SESSION SERVICE ---
session_service = InMemorySessionService()

# --- PASO 5: CREAR RUNNER ---
runner = Runner(
    agent=mi_agente,
    app_name="mi_aplicacion",  # [REEMPLAZA] Nombre de tu app
    session_service=session_service,
)


# --- PASO 6: FUNCIÓN PARA ENVIAR MENSAJES ---
async def enviar_mensaje(pregunta: str):
    """Envía un mensaje al agente y muestra la respuesta"""

    # Crear la sesión
    session = await session_service.create_session(
        app_name="mi_aplicacion",  # [REEMPLAZA] Mismo nombre que en runner
        user_id="usuario_01",  # [REEMPLAZA] ID del usuario
        session_id="sesion_01",  # [REEMPLAZA] ID de la sesión
    )

    # Crear el mensaje
    mensaje = types.Content(role="user", parts=[types.Part(text=pregunta)])

    # Enviar al agente y recibir respuesta
    respuesta_texto = ""
    async for evento in runner.run_async(
        user_id="usuario_01",    # [REEMPLAZA] Mismo user_id
        session_id="sesion_01",  # [REEMPLAZA] Mismo session_id
        new_message=mensaje,
    ):
        if evento.is_final_response() and evento.content:
            for parte in evento.content.parts:
                if hasattr(parte, "text") and parte.text:
                    respuesta_texto += parte.text

    return respuesta_texto


# =============================================================================
# USAR
# =============================================================================
async def main():
    """Función principal que ejecuta el ejemplo"""

    print("🤖 Iniciando agente...\n")

    # [REEMPLAZA] Tu pregunta al agente
    pregunta = "Procesa el texto: Hola Mundo"

    print(f"👤 Usuario: {pregunta}\n")

    # Enviar mensaje y obtener respuesta
    respuesta = await enviar_mensaje(pregunta)

    print(f"🤖 Agente: {respuesta}\n")


# =============================================================================
# EJECUTAR
# =============================================================================
if __name__ == "__main__":
    asyncio.run(main())
