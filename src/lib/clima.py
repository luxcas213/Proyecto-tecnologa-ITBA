import requests

def obtener_clima(ciudad: str) -> None:
    url = f'https://wttr.in/{ciudad}?format=j1'
    try:
        respuesta = requests.get(url, timeout=10)
        respuesta.raise_for_status()
        datos = respuesta.json()

        actual = datos['current_condition'][0]
        temperatura    = actual['temp_C']
        sensacion      = actual['FeelsLikeC']
        humedad        = actual['humidity']
        viento_kmh     = actual['windspeedKmph']
        descripcion    = actual['weatherDesc'][0]['value']

        print(f'\n=== Clima en {ciudad} ===')
        print(f'Temperatura:      {temperatura}°C')
        print(f'Sensación térmica:{sensacion}°C')
        print(f'Humedad:          {humedad}%')
        print(f'Viento:           {viento_kmh} km/h')
        print(f'Condición:        {descripcion}')

    except requests.exceptions.ConnectionError:
        print('Error: no hay conexión a internet.')
    except requests.exceptions.HTTPError as e:
        print(f'Error HTTP: {e}')
    except (KeyError, ValueError):
        print('Error: respuesta inesperada de la API.')


if __name__ == '__main__':
    ciudad = input('Ciudad: ').strip()
    obtener_clima(ciudad)
