import httpx  # Cliente HTTP para hacer solicitudes a APIs (más rápido y moderno que requests)
import json    # Para procesar respuestas en formato JSON

GROQ_API_KEY = "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" # Clave de API de Groq 
MODEL = "llama3-8b-8192"  # Nombre del modelo de lenguaje a usar en la API de Groq

def analizar_con_ia(descripcion, tipo_servicio):
    prompt = f"""
Responde únicamente en JSON como este ejemplo, respetando los valores posibles:

{{
  "complejidad": "Baja" | "Media" | "Alta",
  "ajuste_precio": "0%" | "25%" | "50%",
  "servicios_adicionales": ["..."],
  "propuesta_texto": "Texto profesional en español de 2 a 3 párrafos (máx. 10 líneas)"
}}

NO inventes valores diferentes. Usa solo los indicados.

Caso: {descripcion}
Tipo de servicio: {tipo_servicio}
"""
    try:
        headers = {
            "Authorization": f"Bearer {GROQ_API_KEY}",
            "Content-Type": "application/json"
        }

        body = {
            "model": MODEL,
            "messages": [
                {"role": "system", "content": "Responde como abogado profesional legal. Solo devuelve JSON."},
                {"role": "user", "content": prompt}
            ]
        }

        # Llamada a la API de Groq (simula el comportamiento de OpenAI Chat)
        response = httpx.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers=headers,
            json=body,
            timeout=20 # Tiempo máximo de espera de respuesta segundos
        )

        response.raise_for_status()

        content = response.json()["choices"][0]["message"]["content"]
        print("[IA] Respuesta:\n", content)

        resultado = json.loads(content)

        return {
            "complejidad": resultado.get("complejidad"),
            "ajuste_precio": resultado.get("ajuste_precio"),
            "servicios_adicionales": resultado.get("servicios_adicionales"),
            "propuesta_texto": resultado.get("propuesta_texto")
        }

    except json.JSONDecodeError:
        print("[ERROR] JSON inválido:\n", content)
    except httpx.HTTPStatusError as e: # Manejo de errores HTTP específicos
        print("[HTTP ERROR]", e.response.status_code, e.response.text)
    except Exception as e:   # Captura cualquier otro error inesperado
        print("[ERROR]", str(e))

    return {
        "complejidad": None,
        "ajuste_precio": None,
        "servicios_adicionales": None,
        "propuesta_texto": None
    }
