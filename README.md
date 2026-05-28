# GuardiánClima ITBA

Aplicación de consola en Python que permite consultar el clima actual de cualquier ciudad, guardar un historial global de consultas, ver estadísticas de uso y obtener consejos de vestimenta generados por inteligencia artificial.

## Requisitos

- Python 3.x
- Las siguientes librerías (ver instalación abajo):
  - `requests`
  - `python-dotenv`

## Instalación

### 1. Clonar el repositorio

```bash
git clone <URL-del-repositorio>
cd Proyecto-tecnologa-ITBA
```

### 2. Instalar dependencias

```bash
pip install requests python-dotenv
```

### 3. Configurar las API Keys

#### Clima — sin API Key

Para obtener datos del clima usamos [wttr.in](https://wttr.in), un servicio gratuito y público que no requiere registro ni API key. La app se conecta directamente sin ninguna configuración adicional. porq no nos funcionaba el openweatherapp.

#### IA — Gemini API Key

Crear un archivo `.env` en la raíz del proyecto con el siguiente contenido:

```
GEMINI_API_KEY=TU_API_KEY_DE_GEMINI
```

Cómo obtener la API Key de Gemini:
1. Entrá a [Google AI Studio](https://aistudio.google.com)
2. Creá un proyecto y generá una API Key
3. Copiá la key y pegala en el archivo `.env`

## Estructura del proyecto

```
Proyecto-tecnologa-ITBA/
├── src/
│   ├── main.py          # Punto de entrada, menús
│   ├── service.py       # Lógica de negocio
│   └── lib/
│       ├── storage.py   # Lectura/escritura de CSVs
│       ├── ia.py        # Integración con Gemini API
│       └── clima.py     # Script de la API de clima
├── db/
│   ├── users.csv              # Usuarios registrados
│   └── historial_global.csv   # Historial de consultas de clima
├── .env                 # API Keys (no subir al repo)
├── .gitignore
└── README.md
```
el main.py es el que maneja todo, y llama a las funciones de service que estas llaman a las funciones dentro de la carpeta de lib. como IA , Clima, DB

la carpeta db tiene los csv qu actuan como bases de datos

## Ejecución

Desde la raíz del proyecto:

```bash
python src/main.py
```

## Flujo de la aplicación

### Menú de Acceso (sin sesión iniciada)

```
=== Menú ===
1) Crear usuario
2) Iniciar sesión
3) Salir
```

- **Crear usuario:** pedirá nombre de usuario y contraseña. La contraseña debe cumplir los 5 criterios de seguridad. Si no los cumple, el sistema indica qué reglas falló y ofrece sugerencias. Al registrarse exitosamente, se inicia sesión automáticamente.
- **Iniciar sesión:** pedirá las credenciales y, si son correctas, accederá al menú principal.

### Menú Principal (con sesión iniciada)

```
=== GuardiánClima ITBA — [usuario] ===
1) Consultar clima actual
2) Ver mi historial personal por ciudad
3) Estadísticas globales de uso
4) Consejo IA: ¿Cómo me visto hoy?
5) Acerca de...
6) Cerrar sesión
```

| Opción | Descripción |
|--------|-------------|
| 1 | Ingresás una ciudad y muestra temperatura, sensación térmica, humedad, viento y condición. La consulta se guarda automáticamente en `historial_global.csv`. |
| 2 | Ingresás una ciudad y muestra todas tus consultas previas para esa ciudad. |
| 3 | Muestra la ciudad más consultada, el total de consultas de todos los usuarios y la temperatura promedio global. |
| 4 | Usa los datos de tu última consulta de clima y le pide a Gemini un consejo de vestimenta. |
| 5 | Descripción de la app, guía de uso y datos del equipo. |
| 6 | Cierra la sesión y vuelve al menú de acceso. |

## Criterios de seguridad de contraseña

La contraseña debe cumplir **todos** los siguientes criterios:

1. Mínimo 8 caracteres
2. Al menos una letra mayúscula
3. Al menos una letra minúscula
4. Al menos un número
5. Al menos un carácter especial (`!@#$%^&*(),.?":{}|<>`)

Ejemplo de contraseña válida: `MiPerro#Tiene7Años!`

## Equipo de desarrollo

**Grupo: Equipo numero 1**

- Lucas Garbate
- Tomas Grinstein
- Bautista Cavalitto
- Facundo Gatti
