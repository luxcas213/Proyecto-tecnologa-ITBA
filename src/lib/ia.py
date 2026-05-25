import os
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

GEMINI_URL = 'https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent'


def consejo_vestimenta(temperatura: str, condicion: str, humedad: str, viento: str) -> str:
    api_key = os.getenv('GEMINI_API_KEY')
    if not api_key:
        return 'Error de configuración: no se encontró GEMINI_API_KEY en el archivo .env'

    prompt = (
        f"El clima actual es: temperatura {temperatura}°C, condición '{condicion}', "
        f"humedad {humedad}%, viento {viento} km/h. "
        f"Dame un consejo breve y práctico (máximo 3 oraciones) sobre cómo vestirse "
        f"para salir con este clima. Respondé en español."
    )

    payload = {
        'contents': [
            {'parts': [{'text': prompt}]}
        ]
    }

    try:
        respuesta = requests.post(
            GEMINI_URL,
            headers={
                'Content-Type': 'application/json',
                'X-goog-api-key': api_key,
            },
            json=payload,
            timeout=15,
        )
        respuesta.raise_for_status()
        datos = respuesta.json()
        return datos['candidates'][0]['content']['parts'][0]['text'].strip()
    except requests.exceptions.ConnectionError:
        return 'Error: no hay conexión a internet.'
    except requests.exceptions.HTTPError as e:
        return f'Error HTTP: {e}'
    except (KeyError, ValueError):
        return 'Error: respuesta inesperada de la API.'
