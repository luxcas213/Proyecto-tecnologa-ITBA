import uuid
import os
import re
import requests
from datetime import datetime
from typing import Dict, List, Optional
from lib.storage import add_user, authenticate, guardar_historial, leer_historial


def generate_userid() -> str:
    return str(uuid.uuid4())


CRITERIOS = [
    ('Mínimo 8 caracteres',                  lambda p: len(p) >= 8),
    ('Al menos una letra mayúscula',          lambda p: bool(re.search(r'[A-Z]', p))),
    ('Al menos una letra minúscula',          lambda p: bool(re.search(r'[a-z]', p))),
    ('Al menos un número',                    lambda p: bool(re.search(r'\d', p))),
    ('Al menos un carácter especial (!@#$%^&*)', lambda p: bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', p))),
]


def validar_password(password: str) -> List[str]:
    return [desc for desc, regla in CRITERIOS if not regla(password)]


def create_user() -> None:
    name = input('Nombre: ').strip()
    if not name:
        print('El nombre no puede estar vacío.')
        return

    while True:
        password = input('Contraseña: ').strip()
        errores = validar_password(password)
        if not errores:
            break
        print('\nTu contraseña no cumple con los siguientes criterios:')
        for e in errores:
            print(f'  ✗ {e}')
        print('\nPara una contraseña más segura, considerá usar:')
        print('  → Una frase larga con mayúsculas, números y símbolos.')
        print('  → Ejemplo: "s0lar-VENTANA^lamina#1847"\n')

    userid = generate_userid()
    try:
        add_user(userid, name, password)
        print(f'\n✓ Usuario creado exitosamente: {name}')
        return {'userid': userid, 'name': name, 'password': password}
    except ValueError as e:
        print('No se pudo crear el usuario:', e)
        return None



def consultar_clima(username: str) -> None:
    ciudad = input('Ingresá el nombre de la ciudad: ').strip()
    if not ciudad:
        print('El nombre de la ciudad no puede estar vacío.')
        return

    print(f'\nConsultando clima para {ciudad}...')
    try:
        respuesta = requests.get(f'https://wttr.in/{ciudad}?format=j1', timeout=10)
        datos = respuesta.json()

        actual = datos['current_condition'][0]
        temperatura = actual['temp_C']
        sensacion   = actual['FeelsLikeC']
        humedad     = actual['humidity']
        viento      = actual['windspeedKmph']
        condicion   = actual['weatherDesc'][0]['value']
        fecha_hora  = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        os.system('cls' if os.name == 'nt' else 'clear')
        print(f'=== Clima en {ciudad} ===')
        print(f'Fecha y hora:      {fecha_hora}')
        print(f'Temperatura:       {temperatura}°C')
        print(f'Sensación térmica: {sensacion}°C')
        print(f'Humedad:           {humedad}%')
        print(f'Viento:            {viento} km/h')
        print(f'Condición:         {condicion}')

        guardar_historial(username, ciudad, fecha_hora, temperatura, condicion, humedad, viento)
        print('\n✓ Consulta guardada en el historial.')

    except requests.exceptions.ConnectionError:
        print('Error: no hay conexión a internet.')
    except requests.exceptions.HTTPError as e:
        print(f'Error HTTP: {e}')
    except (KeyError, ValueError):
        print('Error: respuesta inesperada de la API. Verificá el nombre de la ciudad.')

    input('\nPresioná Enter para volver al menú...')


def login() -> Optional[Dict[str, str]]:
    name = input('Nombre: ').strip()
    password = input('Contraseña: ').strip()
    user = authenticate(name, password)
    if user:
        print(f'Bienvenido {user.get("name")}! Accediendo a la siguiente página...')
        return user
    print('Credenciales inválidas')
    return None




def ver_historial_personal(username: str) -> None:
    from lib.storage import get_userid_by_name
    ciudad = input('Ingresá el nombre de la ciudad: ').strip()
    userid = get_userid_by_name(username)
    registros = [
        r for r in leer_historial()
        if r['UserID'] == userid and r['Ciudad'].lower() == ciudad.lower()
    ]

    os.system('cls' if os.name == 'nt' else 'clear')
    print(f'=== Historial de {username} en {ciudad} ===\n')

    if not registros:
        print('No hay consultas registradas para esa ciudad.')
    else:
        for r in registros:
            print(f"  {r['FechaHora']}  |  {r['Temperatura_C']}°C  |  {r['Condicion_Clima']}  |  Humedad: {r['Humedad_Porcentaje']}%  |  Viento: {r['Viento_kmh']} km/h")

    input('\nPresioná Enter para volver al menú...')


def estadisticas_globales() -> None:
    registros = leer_historial()

    os.system('cls' if os.name == 'nt' else 'clear')
    print('=== Estadísticas Globales de Uso ===\n')

    if not registros:
        print('Todavía no hay consultas registradas.')
        input('\nPresioná Enter para volver al menú...')
        return

    total = len(registros)

    conteo_ciudades: Dict[str, int] = {}
    for r in registros:
        ciudad = r['Ciudad']
        conteo_ciudades[ciudad] = conteo_ciudades.get(ciudad, 0) + 1
    ciudad_top = max(conteo_ciudades, key=lambda c: conteo_ciudades[c])

    temps = []
    for r in registros:
        try:
            temps.append(float(r['Temperatura_C']))
        except ValueError:
            pass
    promedio_temp = sum(temps) / len(temps) if temps else 0

    print(f'  Ciudad más consultada: {ciudad_top} ({conteo_ciudades[ciudad_top]} consultas)')
    print(f'  Total de consultas:    {total}')
    print(f'  Temperatura promedio:  {promedio_temp:.1f}°C')

    input('\nPresioná Enter para volver al menú...')


def consejo_ia(username: str) -> None:
    from lib.storage import get_userid_by_name
    from lib.ia import consejo_vestimenta

    userid = get_userid_by_name(username) or username
    registros = leer_historial()
    mis_registros = [r for r in registros if r['UserID'] == userid]

    os.system('cls' if os.name == 'nt' else 'clear')
    print('=== Consejo IA: ¿Cómo me visto hoy? ===\n')

    if not mis_registros:
        print('No tenés consultas de clima registradas.')
        print('Primero consultá el clima (opción 1) y volvé acá.')
        input('\nPresioná Enter para volver al menú...')
        return

    ultimo = mis_registros[-1]
    print(f"Usando tu última consulta: {ultimo['Ciudad']} — {ultimo['FechaHora']}")
    print(f"  Temperatura: {ultimo['Temperatura_C']}°C  |  {ultimo['Condicion_Clima']}  |  Humedad: {ultimo['Humedad_Porcentaje']}%  |  Viento: {ultimo['Viento_kmh']} km/h")
    print('\nConsultando a la IA...\n')

    consejo = consejo_vestimenta(
        ultimo['Temperatura_C'],
        ultimo['Condicion_Clima'],
        ultimo['Humedad_Porcentaje'],
        ultimo['Viento_kmh'],
    )
    print(f'Consejo: {consejo}')
    input('\nPresioná Enter para volver al menú...')


def acerca_de() -> None:
    os.system('cls' if os.name == 'nt' else 'clear')
    print("""
╔══════════════════════════════════════════════════════════════╗
║           GuardiánClima ITBA — Acerca de la app             ║
╚══════════════════════════════════════════════════════════════╝

DESCRIPCIÓN
  Aplicación de consola en Python que permite consultar el clima
  actual de cualquier ciudad, guardar un historial global de
  consultas, ver estadísticas de uso y obtener consejos de
  vestimenta generados por inteligencia artificial.

──────────────────────────────────────────────────────────────
MENÚ DE ACCESO
  1) Iniciar sesión     → Ingresá tu usuario y contraseña.
  2) Registrar usuario  → Elegí un usuario y una contraseña que
                          cumpla los criterios de seguridad.
                          Si no cumple, el sistema te indica qué
                          mejorar. Al registrarte exitosamente
                          entrás directo al menú principal.
  3) Salir              → Cierra la aplicación.

MENÚ PRINCIPAL
  1) Consultar clima    → Ingresá una ciudad y obtenés temperatura,
                          humedad, viento y condición. La consulta
                          se guarda automáticamente en el historial.
  2) Historial personal → Ingresá una ciudad y ves todas tus
                          consultas previas para esa ciudad.
  3) Estadísticas       → Muestra la ciudad más consultada, el total
                          de consultas y la temperatura promedio
                          global de todos los usuarios.
  4) Consejo IA         → Usa los datos del último clima consultado
                          y le pide a Gemini un consejo de vestimenta.
  5) Acerca de          → Esta pantalla.
  6) Cerrar sesión      → Vuelve al menú de acceso.

──────────────────────────────────────────────────────────────
FUNCIONAMIENTO INTERNO
  • Usuarios: se almacenan en usuarios_simulados.csv. Las contraseñas
    pasan una validación de seguridad pero se guardan en texto plano
    (simulación educativa). En una app real se usaría hashing (bcrypt).
  • Historial: cada consulta de clima se agrega como fila en
    historial_global.csv (compartido entre todos los usuarios).
  • Estadísticas: se calculan leyendo historial_global.csv en tiempo real.
  • IA: se envían los parámetros climáticos a la API de Google Gemini,
    que devuelve un consejo de vestimenta personalizado.

──────────────────────────────────────────────────────────────
EQUIPO DE DESARROLLO
- Equipo numero 1 -
  • Lucas Garbate
  • Tomas Grinstein
  • Bautista Cavalitto
  • Facundo Gatti
""")
    input('Presioná Enter para volver al menú...')
