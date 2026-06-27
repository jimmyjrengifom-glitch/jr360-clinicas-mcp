"""Clasificador de mensajes WhatsApp y respuestas a objeciones — todo por reglas, sin API."""

from dataclasses import dataclass

# ── Clasificador WhatsApp ─────────────────────────────────────────────────────

@dataclass
class WhatsAppClassification:
    intent: str
    priority: str
    summary: str
    recommended_action: str
    requires_human: bool
    suggested_response: str


INTENT_KEYWORDS: list[tuple[str, list[str]]] = [
    ("agendar_cita",       ["agendar", "cita", "turno", "reservar", "quiero ir", "puedo ir", "cuando tienen", "disponibilidad para agendar"]),
    ("confirmar_cita",     ["confirmo", "confirmado", "sí voy", "si voy", "ahí estaré", "confirmar cita", "confirmar mi"]),
    ("cancelar_cita",      ["cancelar", "cancelo", "no puedo ir", "no voy a poder", "cancelar mi cita"]),
    ("reprogramar_cita",   ["reprogramar", "cambiar fecha", "cambiar cita", "mover cita", "otra fecha", "otro día"]),
    ("consultar_precio",   ["precio", "cuánto vale", "cuanto vale", "cuánto cuesta", "cuanto cuesta", "tarifa", "costo", "cobran"]),
    ("consultar_pago",     ["pago", "pagué", "pague", "comprobante", "transferencia", "consignación", "recibo", "factura"]),
    ("resultado_medico",   ["resultado", "examen", "análisis", "diagnóstico", "informe médico"]),
    ("queja",              ["queja", "mal servicio", "mala atención", "reclamo", "problema", "insatisfecho", "pésimo"]),
    ("informacion_servicio", ["información", "informacion", "que servicios", "qué ofrecen", "qué hacen", "tienen", "ofrecen"]),
]

URGENCY_KEYWORDS = ["dolor fuerte", "emergencia", "urgente", "urgencia", "muy grave", "no puedo respirar", "sangrado", "sangre"]

PRIORITY_MAP = {
    "queja": "alta",
    "resultado_medico": "alta",
    "cancelar_cita": "media",
    "reprogramar_cita": "media",
    "consultar_pago": "media",
    "agendar_cita": "media",
    "confirmar_cita": "baja",
    "consultar_precio": "baja",
    "informacion_servicio": "baja",
}

RESPONSES = {
    "agendar_cita": "¡Hola! Con gusto le ayudamos a agendar su cita. ¿Qué servicio necesita y cuál fecha le queda mejor?",
    "confirmar_cita": "Perfecto, gracias por confirmar. Le esperamos en la fecha acordada. ¡Cualquier cambio, escríbanos!",
    "cancelar_cita": "Lamentamos que no pueda asistir. ¿Le gustaría reprogramar para otra fecha conveniente?",
    "reprogramar_cita": "Claro, con gusto le buscamos otro espacio disponible. ¿Qué días y horarios le quedan bien?",
    "consultar_precio": "Los precios varían según el servicio. Un asesor le dará la información exacta en unos minutos. ¿Qué servicio le interesa?",
    "consultar_pago": "Revisaremos el estado de su pago. Por favor indíquenos su nombre completo para verificar.",
    "resultado_medico": "Hemos recibido su mensaje. Un asesor le contactará pronto para atenderle correctamente.",
    "queja": "Lamentamos la situación. Su caso es importante para nosotros. Un responsable le contactará en breve para resolverlo.",
    "informacion_servicio": "¡Bienvenido! Contamos con varios servicios. Un asesor le explicará todo con detalle. ¿Tiene algún servicio específico en mente?",
    "otro": "Gracias por escribirnos. Un asesor revisará su mensaje y le responderá pronto.",
}

ACTION_MAP = {
    "agendar_cita": "Verificar disponibilidad y proponer horarios",
    "confirmar_cita": "Actualizar estado de cita a Confirmada",
    "cancelar_cita": "Marcar cita como Cancelada y ofrecer reprogramación",
    "reprogramar_cita": "Buscar nuevo horario disponible",
    "consultar_precio": "Enviar tarifario del servicio consultado",
    "consultar_pago": "Verificar factura y estado de pago en el sistema",
    "resultado_medico": "Escalar a profesional clínico — requiere atención humana",
    "queja": "Escalar inmediatamente a supervisor",
    "informacion_servicio": "Enviar catálogo de servicios",
    "otro": "Revisar mensaje y asignar a responsable",
}


def classify_whatsapp(message: str) -> WhatsAppClassification:
    msg = message.lower()

    # Detectar urgencia primero
    is_urgent = any(kw in msg for kw in URGENCY_KEYWORDS)

    # Detectar intención
    intent = "otro"
    for intent_name, keywords in INTENT_KEYWORDS:
        if any(kw in msg for kw in keywords):
            intent = intent_name
            break

    priority = "urgente" if is_urgent else PRIORITY_MAP.get(intent, "baja")
    requires_human = intent in ("queja", "resultado_medico", "otro") or is_urgent

    return WhatsAppClassification(
        intent=intent,
        priority=priority,
        summary=f"Mensaje de {intent.replace('_', ' ')} — prioridad {priority}",
        recommended_action=ACTION_MAP.get(intent, "Revisar manualmente"),
        requires_human=requires_human,
        suggested_response=RESPONSES.get(intent, RESPONSES["otro"]),
    )


# ── Respuestas a objeciones ───────────────────────────────────────────────────

OBJECTIONS: dict[str, dict] = {
    "es_muy_caro": {
        "keywords": ["caro", "costoso", "precio alto", "mucho dinero", "no tenemos presupuesto", "no alcanza"],
        "response": (
            "Entiendo. Comparemos: ¿cuánto pierde la clínica hoy por citas perdidas, facturas mal "
            "registradas y pacientes que nunca regresan porque no hubo seguimiento? La mayoría de "
            "nuestros clientes recuperan la inversión en los primeros dos meses. Y el setup es único: "
            "$1.200 USD. La mensualidad de $300 USD es menos de lo que cuesta una mala semana de "
            "operación desordenada."
        ),
    },
    "no_tenemos_tiempo": {
        "keywords": ["no tenemos tiempo", "muy ocupados", "no hay tiempo", "implementarlo"],
        "response": (
            "Por eso existe este sistema. No requiere que usted aprenda algo nuevo ni dedique semanas "
            "a configurarlo — nosotros nos encargamos de todo. En 5 días hábiles su equipo ya tiene "
            "el sistema funcionando. El tiempo que invierte ahora le ahorra horas cada semana."
        ),
    },
    "ya_tenemos_sistema": {
        "keywords": ["ya tenemos", "ya usamos", "tenemos excel", "tenemos whatsapp", "usamos excel"],
        "response": (
            "Perfecto. Entonces ya sabe el dolor de operar con herramientas dispersas. ¿Su sistema "
            "actual le muestra en tiempo real cuántas citas tiene hoy, cuántas facturas están "
            "vencidas y cuántos pacientes no regresaron? El nuestro sí. No reemplazamos lo que "
            "funciona — integramos lo que falta."
        ),
    },
    "necesito_pensarlo": {
        "keywords": ["necesito pensarlo", "voy a pensar", "lo consulto", "consultarlo", "lo hablo"],
        "response": (
            "Con gusto. ¿Qué parte necesita evaluar con más detalle? Si es el precio, el alcance "
            "o cómo funciona en la práctica — podemos resolverlo ahora mismo. "
            "Lo que sí le pido es que mientras 'lo piensa', calcule cuánto le cuesta cada semana "
            "seguir operando sin esto."
        ),
    },
    "no_me_fio_de_la_tecnologia": {
        "keywords": ["no me fío", "no confío", "tecnología", "complicado", "difícil de usar", "no entiendo"],
        "response": (
            "Es una preocupación válida. Por eso tenemos una demo en vivo: usted lo usa hoy, "
            "sin instalar nada, sin compromisos. Si en 10 minutos no ve valor real para su clínica, "
            "no seguimos. El sistema está diseñado para que recepción lo use desde el primer día, "
            "sin capacitación técnica."
        ),
    },
    "no_es_el_momento": {
        "keywords": ["no es el momento", "más adelante", "el año que viene", "después", "ahora no"],
        "response": (
            "Entiendo. Pero el desorden operativo no espera. Cada semana que pasa sin sistema "
            "centralizado es facturación mal registrada, pacientes perdidos y carga manual evitable. "
            "¿Qué tendría que pasar para que fuera el momento correcto?"
        ),
    },
    "no_veo_el_valor": {
        "keywords": ["no veo el valor", "para qué", "no lo necesito", "no entiendo para qué sirve"],
        "response": (
            "Perfecto punto. Hagamos el ejercicio: ¿cuántos pacientes agenda por semana y cuántos "
            "no asisten? Multiplique eso por el valor del servicio. Ese es el dinero que ya está "
            "perdiendo. Nuestro sistema reduce el ausentismo, automatiza confirmaciones y le avisa "
            "antes de que el paciente se pierda."
        ),
    },
    "prefiero_contratar_empleado": {
        "keywords": ["contratar", "empleado", "persona", "secretaria", "recepcionista"],
        "response": (
            "Un empleado cuesta entre $1.500.000 y $2.500.000 COP mensuales, más prestaciones. "
            "Este sistema cuesta $300 USD mensuales y trabaja 24/7, no se enferma y no comete "
            "errores de digitación. No reemplaza a su equipo — lo potencia."
        ),
    },
    "tengo_que_aprobarlo_con_alguien": {
        "keywords": ["aprobarlo", "socios", "directivos", "junta", "gerente", "dueño"],
        "response": (
            "Claro. ¿Cuándo se reúnen? Puedo prepararles un informe ejecutivo de una página con "
            "el impacto económico esperado, las funciones clave y el plan de implementación. "
            "Algo que su gerencia pueda revisar en 5 minutos y tomar la decisión."
        ),
    },
    "lo_hace_mi_sobrino": {
        "keywords": ["sobrino", "familiar", "conocido", "alguien que sabe", "ya tengo quien"],
        "response": (
            "Genial que tenga apoyo técnico. La pregunta es: ¿ese sistema tendrá soporte, "
            "actualizaciones y garantía? Nuestro servicio incluye soporte continuo, mejoras "
            "periódicas y alguien que responde cuando algo falla — no en tres días, hoy."
        ),
    },
    "prefiero_esperar_a_ver_resultados": {
        "keywords": ["resultados", "pruebas", "ver si funciona", "primero ver"],
        "response": (
            "Por eso ofrecemos la demo en vivo: usted ve cómo funciona con el nombre de su clínica, "
            "sus servicios y datos reales antes de pagar un peso. No le pedimos fe — le mostramos evidencia."
        ),
    },
    "ya_lo_intentamos_y_no_funciono": {
        "keywords": ["ya lo intentamos", "ya probamos", "no funcionó", "mala experiencia", "antes tuvimos"],
        "response": (
            "Lo entiendo. ¿Qué sistema probaron y qué falló específicamente? Con esa información "
            "puedo decirle con precisión cómo este caso es diferente — o si no lo es, "
            "prefiero decírselo ahora."
        ),
    },
}


def answer_objection(objection_text: str) -> dict:
    """Detecta la objeción por keywords y devuelve la respuesta comercial."""
    obj_lower = objection_text.lower()

    for key, data in OBJECTIONS.items():
        if any(kw in obj_lower for kw in data["keywords"]):
            return {
                "objecion_detectada": key,
                "texto_original": objection_text,
                "respuesta": data["response"],
                "nota": "Nunca mencionar 'IA' — hablar siempre de sistema operativo y control.",
            }

    return {
        "objecion_detectada": "no_identificada",
        "texto_original": objection_text,
        "respuesta": (
            "Cuénteme más sobre su situación actual. Quiero entender exactamente cuál es "
            "su preocupación para darle una respuesta útil, no un discurso de ventas."
        ),
        "nota": "Objeción no clasificada — usar escucha activa.",
    }
