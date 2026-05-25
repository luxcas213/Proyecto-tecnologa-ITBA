from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak,
    Table, TableStyle, HRFlowable
)

OUTPUT = "DocumentoProyecto.pdf"

AZUL     = colors.HexColor("#1a3a5c")
AZUL_MED = colors.HexColor("#2e6da4")
GRIS     = colors.HexColor("#f2f4f7")
NEGRO    = colors.HexColor("#1a1a1a")

def build_styles():
    base = getSampleStyleSheet()
    styles = {}

    styles["titulo_doc"] = ParagraphStyle(
        "titulo_doc", parent=base["Title"],
        fontSize=26, textColor=AZUL, spaceAfter=6, leading=32,
    )
    styles["subtitulo_doc"] = ParagraphStyle(
        "subtitulo_doc", parent=base["Normal"],
        fontSize=13, textColor=AZUL_MED, spaceAfter=4,
    )
    styles["h1"] = ParagraphStyle(
        "h1", parent=base["Heading1"],
        fontSize=16, textColor=AZUL, spaceBefore=18, spaceAfter=6,
        borderPad=4,
    )
    styles["h2"] = ParagraphStyle(
        "h2", parent=base["Heading2"],
        fontSize=13, textColor=AZUL_MED, spaceBefore=12, spaceAfter=4,
    )
    styles["body"] = ParagraphStyle(
        "body", parent=base["Normal"],
        fontSize=10.5, textColor=NEGRO, leading=16, spaceAfter=6,
    )
    styles["bullet"] = ParagraphStyle(
        "bullet", parent=base["Normal"],
        fontSize=10.5, textColor=NEGRO, leading=15, spaceAfter=3,
        leftIndent=16, bulletIndent=4,
    )
    styles["code"] = ParagraphStyle(
        "code", parent=base["Code"],
        fontSize=9, backColor=GRIS, leftIndent=12, rightIndent=12,
        spaceBefore=4, spaceAfter=4, leading=14,
    )
    return styles

def hr(story):
    story.append(Spacer(1, 4))
    story.append(HRFlowable(width="100%", thickness=1, color=AZUL_MED))
    story.append(Spacer(1, 8))

def h1(story, s, text):
    story.append(Paragraph(text, s["h1"]))
    story.append(HRFlowable(width="100%", thickness=0.5, color=AZUL_MED))
    story.append(Spacer(1, 4))

def h2(story, s, text):
    story.append(Paragraph(text, s["h2"]))

def p(story, s, text):
    story.append(Paragraph(text, s["body"]))

def b(story, s, text):
    story.append(Paragraph(f"&#8226; {text}", s["bullet"]))

def build():
    doc = SimpleDocTemplate(
        OUTPUT, pagesize=A4,
        leftMargin=2.5*cm, rightMargin=2.5*cm,
        topMargin=2.5*cm, bottomMargin=2.5*cm,
    )
    s = build_styles()
    story = []

    # ── PORTADA ──────────────────────────────────────────────────────────
    story.append(Spacer(1, 3*cm))
    story.append(Paragraph("GuardiánClima ITBA", s["titulo_doc"]))
    story.append(Paragraph("Documento del Proyecto — Challenge Tecnológico Integrador", s["subtitulo_doc"]))
    story.append(Spacer(1, 0.5*cm))
    hr(story)
    story.append(Spacer(1, 0.3*cm))

    data_portada = [
        ["Equipo", "Equipo Numero 1"],
        ["Integrantes", "Lucas Garbate, Tomas Grinstein,\nBautista Cavalitto, Facundo Gatti"],
        ["Materia", "Tecnología ITBA"],
        ["Fecha", "Mayo 2026"],
    ]
    t = Table(data_portada, colWidths=[4*cm, 11*cm])
    t.setStyle(TableStyle([
        ("BACKGROUND", (0,0), (0,-1), GRIS),
        ("TEXTCOLOR",  (0,0), (0,-1), AZUL),
        ("FONTNAME",   (0,0), (0,-1), "Helvetica-Bold"),
        ("FONTSIZE",   (0,0), (-1,-1), 10),
        ("ROWBACKGROUND", (0,0), (-1,-1), [colors.white, GRIS]),
        ("GRID",       (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN",     (0,0), (-1,-1), "MIDDLE"),
        ("TOPPADDING", (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING", (0,0), (-1,-1), 8),
    ]))
    story.append(t)
    story.append(PageBreak())

    # ── 1. INTRODUCCIÓN ──────────────────────────────────────────────────
    h1(story, s, "1. Introducción")
    p(story, s, "GuardiánClima ITBA es una aplicación de consola desarrollada en Python como parte del Challenge Tecnológico Integrador. La aplicación permite a los usuarios consultar el clima actual de cualquier ciudad, guardar un historial global de consultas, visualizar estadísticas de uso y recibir consejos de vestimenta generados por inteligencia artificial.")
    story.append(Spacer(1, 6))

    h2(story, s, "1.1 Objetivos")
    b(story, s, "Desarrollar una aplicación funcional de consola en Python.")
    b(story, s, "Integrar conceptos de Programación, Ciberseguridad, Análisis de Datos, Inteligencia Artificial y Cloud Computing.")
    b(story, s, "Implementar validación de contraseñas con criterios de seguridad reales.")
    b(story, s, "Conectar la aplicación a APIs externas (clima e IA).")
    b(story, s, "Gestionar datos persistentes mediante archivos CSV.")
    story.append(Spacer(1, 6))

    h2(story, s, "1.2 Tecnologías utilizadas")
    data_tech = [
        ["Componente",        "Tecnología / Servicio"],
        ["Lenguaje",          "Python 3.x"],
        ["API de Clima",      "wttr.in (gratuita, sin API key)"],
        ["API de IA",         "Google Gemini (gemini-flash-latest via REST)"],
        ["Persistencia",      "Archivos CSV (users.csv, historial_global.csv)"],
        ["HTTP",              "Librería requests"],
        ["Variables de entorno", "python-dotenv"],
    ]
    t2 = Table(data_tech, colWidths=[5.5*cm, 9.5*cm])
    t2.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL),
        ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9.5),
        ("ROWBACKGROUND", (0,1), (-1,-1), [colors.white, GRIS]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("TOPPADDING",    (0,0), (-1,-1), 5),
        ("BOTTOMPADDING", (0,0), (-1,-1), 5),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(t2)
    story.append(PageBreak())

    # ── 2. DISEÑO Y ARQUITECTURA ─────────────────────────────────────────
    h1(story, s, "2. Diseño y Arquitectura")

    h2(story, s, "2.1 Estructura de archivos")
    story.append(Paragraph(
        "src/main.py &nbsp;&nbsp;— Punto de entrada. Maneja los dos menus y el estado de sesion.<br/>"
        "src/service.py &nbsp;— Logica de negocio: registro, login, clima, historial, estadisticas, IA, acerca de.<br/>"
        "src/lib/storage.py — Lectura y escritura de los archivos CSV.<br/>"
        "src/lib/ia.py &nbsp;&nbsp;&nbsp;&nbsp;— Integracion con la API de Google Gemini via HTTP.<br/>"
        "src/lib/clima.py &nbsp;— Script auxiliar de prueba para la API de clima.<br/>"
        "db/users.csv &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;— Almacena los usuarios registrados.<br/>"
        "db/historial_global.csv — Historial de todas las consultas de clima.",
        s["code"]
    ))
    story.append(Spacer(1, 8))

    h2(story, s, "2.2 Flujo de datos")
    p(story, s, "El flujo de la aplicación se divide en dos etapas principales:")
    b(story, s, "<b>Pre-login:</b> el usuario puede registrarse o iniciar sesión. Las credenciales se validan contra <i>users.csv</i>. Tras un registro o login exitoso la sesión queda activa.")
    b(story, s, "<b>Post-login:</b> el usuario accede al menú principal. Las consultas de clima se guardan en <i>historial_global.csv</i> con el UserID del usuario. Las estadísticas y el historial personal se calculan leyendo ese mismo archivo.")
    story.append(Spacer(1, 8))

    h2(story, s, "2.3 Decisiones de diseño")
    b(story, s, "<b>wttr.in en lugar de OpenWeatherMap:</b> no requiere API key ni registro, lo que simplifica la configuración del entorno.")
    b(story, s, "<b>Gemini via HTTP directo:</b> se usa requests en lugar de la librería google-generativeai para mayor control del endpoint y evitar dependencias pesadas.")
    b(story, s, "<b>UserID en el historial:</b> se almacena el UUID del usuario en lugar del nombre para mayor consistencia interna, aunque el nombre se usa en la UI.")
    b(story, s, "<b>Modularidad:</b> la lógica se separó en service.py (negocio) y lib/ (integraciones externas y datos), dejando main.py exclusivamente para la navegación de menús.")
    b(story, s, "<b>.env para las API keys:</b> se usa python-dotenv para cargar las claves desde un archivo .env excluido del repositorio por .gitignore.")
    story.append(PageBreak())

    # ── 3. GUÍA DE USUARIO ───────────────────────────────────────────────
    h1(story, s, "3. Guía de Usuario Detallada")

    h2(story, s, "3.1 Menú de Acceso")
    p(story, s, "Al iniciar la aplicación se presenta el Menú de Acceso con tres opciones:")

    data_acceso = [
        ["Opción", "Descripción"],
        ["1) Crear usuario",
         "Solicita nombre de usuario y contraseña. La contraseña debe cumplir los 5 criterios de seguridad. Si falla, informa qué reglas no se cumplieron y sugiere cómo mejorarla. Tras el registro exitoso se inicia sesión automáticamente."],
        ["2) Iniciar sesión",
         "Solicita nombre y contraseña. Si las credenciales son correctas accede al Menú Principal. Si no, muestra un error y permite reintentar."],
        ["3) Salir",
         "Termina la ejecución del programa."],
    ]
    t3 = Table(data_acceso, colWidths=[4*cm, 11*cm])
    t3.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL),
        ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9.5),
        ("ROWBACKGROUND", (0,1), (-1,-1), [colors.white, GRIS]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(t3)
    story.append(Spacer(1, 10))

    h2(story, s, "3.2 Criterios de seguridad de contraseña")
    p(story, s, "La contraseña debe cumplir <b>todos</b> los siguientes criterios:")
    criterios = [
        "Minimo 8 caracteres",
        "Al menos una letra mayuscula",
        "Al menos una letra minuscula",
        "Al menos un numero",
        "Al menos un caracter especial (!@#$%^&*(),.?\":{}|&lt;&gt;)",
    ]
    for c_text in criterios:
        b(story, s, c_text)
    p(story, s, "Ejemplo de contraseña válida: <b>MiPerro#Tiene7Annos!</b>")
    story.append(Spacer(1, 10))

    h2(story, s, "3.3 Menú Principal")
    data_main = [
        ["Opción", "Descripción"],
        ["1) Consultar clima",
         "Ingresa una ciudad y muestra temperatura, sensación térmica, humedad, viento y condición. La consulta se guarda automáticamente en historial_global.csv."],
        ["2) Historial personal",
         "Ingresa una ciudad y muestra todas tus consultas previas para esa ciudad, ordenadas cronológicamente."],
        ["3) Estadísticas globales",
         "Muestra la ciudad más consultada por todos los usuarios, el total de consultas y la temperatura promedio global."],
        ["4) Consejo IA",
         "Toma los datos de tu última consulta de clima y consulta a Google Gemini para obtener un consejo de vestimenta personalizado."],
        ["5) Acerca de",
         "Descripción de la app, guía de uso de cada opción, funcionamiento interno y datos del equipo."],
        ["6) Cerrar sesión",
         "Finaliza la sesión actual y vuelve al Menú de Acceso."],
    ]
    t4 = Table(data_main, colWidths=[4*cm, 11*cm])
    t4.setStyle(TableStyle([
        ("BACKGROUND",    (0,0), (-1,0), AZUL),
        ("TEXTCOLOR",     (0,0), (-1,0), colors.white),
        ("FONTNAME",      (0,0), (-1,0), "Helvetica-Bold"),
        ("FONTSIZE",      (0,0), (-1,-1), 9.5),
        ("ROWBACKGROUND", (0,1), (-1,-1), [colors.white, GRIS]),
        ("GRID",          (0,0), (-1,-1), 0.4, colors.HexColor("#cccccc")),
        ("VALIGN",        (0,0), (-1,-1), "TOP"),
        ("TOPPADDING",    (0,0), (-1,-1), 6),
        ("BOTTOMPADDING", (0,0), (-1,-1), 6),
        ("LEFTPADDING",   (0,0), (-1,-1), 8),
    ]))
    story.append(t4)
    story.append(PageBreak())

    # ── 4. DESAFÍOS Y SOLUCIONES ─────────────────────────────────────────
    h1(story, s, "4. Desafíos y Soluciones")

    desafios = [
        (
            "API de clima con cuota agotada (OpenWeatherMap)",
            "Al intentar usar OpenWeatherMap, la activación de la API key tardaba demasiado. Se reemplazó por wttr.in, un servicio completamente gratuito y sin registro que devuelve los mismos datos en formato JSON.",
        ),
        (
            "Cuota agotada en Google Gemini",
            "La primera API key de Gemini tenía límite 0 en el free tier, probablemente por restricciones regionales. Se generó una nueva key y se cambió el modelo a gemini-flash-latest, que resultó ser el correcto para esa cuenta.",
        ),
        (
            "Error 404 en el endpoint de Gemini",
            "El nombre del modelo gemini-2.0-flash-latest no existía en el endpoint v1beta. Se consultó la lista de modelos disponibles directamente via la API (/v1beta/models) y se identificó gemini-flash-latest como el modelo correcto.",
        ),
        (
            "Rutas de archivos CSV al mover a carpeta db/",
            "Al reorganizar el proyecto y mover los CSV a /db y storage.py a src/lib/, las rutas relativas quedaron incorrectas. Se corrigieron usando os.path.dirname(__file__) con la cantidad correcta de niveles (.., ..).",
        ),
        (
            "Auto-login tras el registro",
            "La función create_user() originalmente no devolvía nada. Se modificó para retornar el diccionario del usuario recién creado, y main.py usa ese retorno para iniciar sesión automáticamente.",
        ),
    ]

    for titulo, desc in desafios:
        h2(story, s, titulo)
        p(story, s, desc)
        story.append(Spacer(1, 4))

    story.append(PageBreak())

    # ── 5. CONCLUSIONES ──────────────────────────────────────────────────
    h1(story, s, "5. Conclusiones y Aprendizajes")

    p(story, s, "El desarrollo de GuardiánClima ITBA nos permitió integrar de forma práctica varios conceptos trabajados a lo largo de la materia:")

    aprendizajes = [
        "<b>Programación:</b> aplicamos funciones, módulos, manejo de archivos CSV, estructuras de control y buenas prácticas de modularidad separando la lógica en capas (main, service, lib).",
        "<b>Ciberseguridad:</b> implementamos validación de contraseñas con criterios reales (longitud, mayúsculas, minúsculas, números y caracteres especiales), y entendimos la diferencia entre almacenamiento en texto plano (simulación educativa) y el uso de hashing (bcrypt) en aplicaciones reales.",
        "<b>Cloud Computing y Conectividad:</b> consumimos dos APIs REST externas (wttr.in y Google Gemini) usando la librería requests, manejando errores de red, HTTP y respuestas inesperadas.",
        "<b>Inteligencia Artificial:</b> integramos Google Gemini para generar consejos de vestimenta en lenguaje natural a partir de parámetros climáticos, aprendiendo a diseñar prompts efectivos.",
        "<b>Análisis de Datos:</b> procesamos el historial global en CSV para calcular estadísticas (ciudad más consultada, temperatura promedio, total de consultas) y generamos un archivo listo para graficar en Excel.",
    ]

    for ap in aprendizajes:
        b(story, s, ap)
        story.append(Spacer(1, 3))

    story.append(Spacer(1, 16))
    p(story, s, "El proyecto nos desafió a resolver problemas reales como incompatibilidades de APIs, errores de rutas al reorganizar el proyecto y restricciones de cuota. Cada obstáculo se convirtió en un aprendizaje concreto sobre cómo funciona el desarrollo de software en la práctica.")

    story.append(Spacer(1, 24))
    hr(story)
    story.append(Paragraph("Equipo Numero 1 — Lucas Garbate, Tomas Grinstein, Bautista Cavalitto, Facundo Gatti", s["subtitulo_doc"]))

    doc.build(story)
    print(f"PDF generado: {OUTPUT}")

if __name__ == "__main__":
    build()
