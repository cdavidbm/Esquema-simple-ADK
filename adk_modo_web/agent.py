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

"""
