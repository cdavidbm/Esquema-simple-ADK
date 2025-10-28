# cd ejercicios_con_llm
# adk web

import os
from google.adk.agents import Agent
from dotenv import load_dotenv

load_dotenv()
os.environ["GOOGLE_API_KEY"] = os.getenv("GEMINI_API_KEY")
os.environ["GOOGLE_GENAI_USE_VERTEXAI"] = "False"


# =============================================================================
# HERRAMIENTAS (TOOLS)
# =============================================================================
def saludar(nombre: str) -> str:
    """
    Saluda a una persona de forma amigable

    Args:
        nombre: El nombre de la persona a saludar

    Returns:
        Un mensaje de saludo personalizado
    """
    return f"¡Hola {nombre}! Es un placer conocerte. ¿En qué puedo ayudarte hoy?"


def calcular_suma(a: float, b: float) -> float:
    """
    Suma dos números

    Args:
        a: Primer número
        b: Segundo número

    Returns:
        La suma de a y b
    """
    return a + b


def calcular_area_circulo(radio: float) -> float:
    """
    Calcula el área de un círculo dado su radio

    Args:
        radio: El radio del círculo

    Returns:
        El área del círculo (π * r²)
    """
    import math

    return math.pi * radio**2


def convertir_temperatura(celsius: float) -> dict:
    """
    Convierte temperatura de Celsius a Fahrenheit y Kelvin

    Args:
        celsius: Temperatura en grados Celsius

    Returns:
        Diccionario con las conversiones
    """
    fahrenheit = (celsius * 9 / 5) + 32
    kelvin = celsius + 273.15

    return {"celsius": celsius, "fahrenheit": fahrenheit, "kelvin": kelvin}


# =============================================================================
# AGENTE PRINCIPAL
# =============================================================================
# IMPORTANTE: El agente DEBE llamarse "root_agent" para que ADK Web lo detecte
root_agent = Agent(
    name="asistente_multiproposito",
    model="gemini-2.0-flash",
    description="Asistente versátil que puede saludar, hacer cálculos y conversiones",
    instruction="""
    Eres un asistente amigable y eficiente llamado "Asistente ADK".

    CAPACIDADES:
    - Puedes saludar a las personas usando la herramienta "saludar"
    - Puedes realizar sumas usando "calcular_suma"
    - Puedes calcular áreas de círculos usando "calcular_area_circulo"
    - Puedes convertir temperaturas usando "convertir_temperatura"

    COMPORTAMIENTO:
    - Siempre sé cortés y profesional
    - Usa las herramientas apropiadas para cada tarea
    - Explica brevemente lo que estás haciendo
    - Si te piden algo que no puedes hacer, explica amablemente tus limitaciones

    ESTILO:
    - Mantén respuestas concisas pero informativas
    - Usa emojis ocasionalmente para ser más amigable
    - Confirma los resultados de tus cálculos
    """,
    tools=[saludar, calcular_suma, calcular_area_circulo, convertir_temperatura],
)


# =============================================================================
# NOTAS DE USO
# =============================================================================
"""
PREGUNTAS DE PRUEBA PARA LA INTERFAZ WEB:

1. Saludos:
   - "Hola, me llamo María"
   - "Salúdame, soy Carlos"

2. Cálculos:
   - "¿Cuánto es 15 + 27?"
   - "Suma 100 y 250"

3. Geometría:
   - "¿Cuál es el área de un círculo con radio 5?"
   - "Calcula el área de un círculo de 10 metros de radio"

4. Temperatura:
   - "Convierte 25 grados Celsius"
   - "¿A cuántos Fahrenheit equivalen 0 grados Celsius?"

5. Conversación mixta:
   - "Hola, soy Pedro. ¿Puedes calcular el área de un círculo con radio 7?"
   - "Buenos días. Suma 50 y 75, luego convierte el resultado a Fahrenheit"


==========================================================================

La Diferencia Fundamental entre usar el modo web y no usarlo:

Con Código Python Directo (asyncio.run), hay que crear y gestionar TODO:

from google.adk.agents import Agent
from google.adk.sessions import InMemorySessionService
from google.adk.runners import Runner
from google.genai import types

# 1. Crear el agente
agente = Agent(...)

# 2. Crear el SessionService (TÚ lo creas)
session_service = InMemorySessionService()

# 3. Crear el Runner (TÚ lo creas)
runner = Runner(
    agent=agente,
    app_name="mi_app",
    session_service=session_service
)

# 4. Crear la sesión (TÚ la gestionas)
await session_service.create_session(...)

# 5. Enviar mensajes (TÚ gestionas el flujo)
mensaje = types.Content(...)
async for evento in runner.run_async(...):
    ...


Con Interfaz Web (adk web):

# Solo se define el agente:
from google.adk.agents import Agent
root_agent = Agent(...)

# ¡FIN! ADK Web hace el resto automáticamente

¿Dónde Están el Runner y Session? Están ahí, pero ADK los crea y gestiona.

Cuando se ejecuta `adk web`, el servidor web de ADK automáticamente:

1. Detecta el `root_agent`
2. Crea un `Runner` para ese agente
3. Crea un `SessionService` (InMemorySessionService por defecto)
4. Gestiona las sesiones de cada conversación
5. Maneja el flujo async de mensajes
6. Renderiza la UI en el navegador

Todo esto ocurre detrás de escena en el código del servidor web de ADK.


Veamos el Código Real de ADK Web

Si quisieras ver dónde ADK crea estos componentes, está en el código fuente de ADK:

¿Qué Método Usar?

Usa Código Python Directo cuando:
- Necesitas control total del flujo
- Quieres personalizar Session/State avanzado
- Estás automatizando procesos
- Vas a producción

Usa ADK Web cuando:
- Estás desarrollando un nuevo agente
- Necesitas iterar rápido
- Quieres depurar visualmente
- Estás haciendo demos
- Estás enseñando ADK
- Quieres probar múltiples agentes

Analogía con Frameworks Web

Es similar a cómo funcionan los frameworks web:

# Flask/FastAPI (manual - como código Python directo)
from flask import Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Hello"

if __name__ == "__main__":
    app.run()  # TÚ controlas cuándo y cómo se ejecuta

# vs

# Django (automático - como adk web)
# solo defines:
def home(request):
    return HttpResponse("Hello")

# Django gestiona automáticamente:
# - El servidor
# - Las rutas
# - Las sesiones
# - Las peticiones HTTP
# Tú solo ejecutas: python manage.py runserver


"""
