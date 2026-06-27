"""Datos en memoria: pacientes, médicos, servicios y contexto del sistema JR360."""

from datetime import date, timedelta
import random

# ── Servicios por tipo de clínica ─────────────────────────────────────────────

SERVICIOS_POR_TIPO = {
    "dental": [
        {"nombre": "Consulta general", "precio": 80_000},
        {"nombre": "Limpieza dental", "precio": 120_000},
        {"nombre": "Blanqueamiento", "precio": 350_000},
        {"nombre": "Ortodoncia (mensualidad)", "precio": 180_000},
        {"nombre": "Extracción", "precio": 150_000},
        {"nombre": "Endodoncia", "precio": 450_000},
    ],
    "estetica": [
        {"nombre": "Consulta inicial", "precio": 100_000},
        {"nombre": "Botox (zona)", "precio": 450_000},
        {"nombre": "Relleno ácido hialurónico", "precio": 600_000},
        {"nombre": "Peeling químico", "precio": 250_000},
        {"nombre": "Hidratación facial", "precio": 180_000},
        {"nombre": "Radiofrecuencia corporal", "precio": 350_000},
    ],
    "bienestar": [
        {"nombre": "Consulta valoración", "precio": 90_000},
        {"nombre": "Sesión terapéutica", "precio": 130_000},
        {"nombre": "Masaje terapéutico", "precio": 120_000},
        {"nombre": "Acupuntura", "precio": 150_000},
        {"nombre": "Nutrición (consulta)", "precio": 100_000},
    ],
    "quiropraxia": [
        {"nombre": "Evaluación inicial", "precio": 100_000},
        {"nombre": "Ajuste quiropráctico", "precio": 130_000},
        {"nombre": "Plan 10 sesiones", "precio": 950_000},
        {"nombre": "Electroestimulación", "precio": 80_000},
    ],
    "deportiva": [
        {"nombre": "Evaluación biomecánica", "precio": 180_000},
        {"nombre": "Rehabilitación (sesión)", "precio": 130_000},
        {"nombre": "Fisioterapia", "precio": 120_000},
        {"nombre": "Nutrición deportiva", "precio": 100_000},
    ],
    "general": [
        {"nombre": "Consulta general", "precio": 120_000},
        {"nombre": "Valoración", "precio": 180_000},
        {"nombre": "Procedimiento menor", "precio": 350_000},
        {"nombre": "Estético", "precio": 450_000},
        {"nombre": "Control", "precio": 90_000},
    ],
}

NOMBRES_PACIENTES = [
    "Laura Martínez", "Carlos Gómez", "Andrea Restrepo", "Diana Salazar",
    "Mateo Herrera", "Valentina Ríos", "Sebastián Ospina", "Juliana Castro",
    "Felipe Morales", "Camila Vargas", "David Peña", "Natalia Jiménez",
    "Juan Rodríguez", "María López", "Andrés Cárdenas", "Carolina Pérez",
]

MEDICOS = [
    "Dra. María Fernanda López",
    "Dr. Andrés Cárdenas",
    "Dra. Carolina Pérez",
    "Dr. Santiago Mejía",
]

ESTADOS_PACIENTE = [
    "Nuevo", "Contactado", "Agendado", "Atendido",
    "Pendiente de pago", "Pagado", "Seguimiento",
]

ESTADOS_CITA = [
    "Pendiente", "Confirmada", "Reprogramada",
    "Cancelada", "Atendida", "No asistió",
]

ESTADOS_FACTURA = ["Pendiente", "Parcial", "Pagado", "Vencido"]

METODOS_PAGO = ["Efectivo", "Transferencia", "Tarjeta débito", "Tarjeta crédito", "Nequi"]


def generate_demo_data(clinic_name: str, clinic_type: str, num_patients: int = 8) -> dict:
    """Genera datos demo ficticios personalizados para una clínica."""
    clinic_type = clinic_type.lower()
    if clinic_type not in SERVICIOS_POR_TIPO:
        clinic_type = "general"

    servicios = SERVICIOS_POR_TIPO[clinic_type]
    hoy = date.today()

    # Pacientes
    pacientes = []
    nombres = random.sample(NOMBRES_PACIENTES, min(num_patients, len(NOMBRES_PACIENTES)))
    for i, nombre in enumerate(nombres):
        servicio = random.choice(servicios)
        estado = ESTADOS_PACIENTE[i % len(ESTADOS_PACIENTE)]
        pacientes.append({
            "id": f"P{i+1:03}",
            "nombre": nombre,
            "telefono": f"310{random.randint(1000000, 9999999)}",
            "servicio_interes": servicio["nombre"],
            "estado": estado,
            "medico_asignado": random.choice(MEDICOS),
            "fecha_registro": str(hoy - timedelta(days=random.randint(1, 30))),
        })

    # Citas (próximos 7 días)
    citas = []
    for i, p in enumerate(pacientes[:6]):
        servicio = next(s for s in servicios if s["nombre"] == p["servicio_interes"])
        fecha_cita = hoy + timedelta(days=random.randint(0, 7))
        estado = ESTADOS_CITA[i % len(ESTADOS_CITA)]
        citas.append({
            "id": f"C{i+1:03}",
            "paciente": p["nombre"],
            "servicio": servicio["nombre"],
            "valor_cop": servicio["precio"],
            "fecha": str(fecha_cita),
            "hora": f"{random.randint(8, 17):02}:{random.choice(['00','30'])}",
            "medico": p["medico_asignado"],
            "estado": estado,
        })

    # Pre-facturas
    facturas = []
    for i, cita in enumerate(citas[:4]):
        estado = ESTADOS_FACTURA[i % len(ESTADOS_FACTURA)]
        facturas.append({
            "id": f"F{i+1:03}",
            "numero": f"PF-2026-{i+1:04}",
            "paciente": cita["paciente"],
            "servicio": cita["servicio"],
            "valor_cop": cita["valor_cop"],
            "metodo_pago": random.choice(METODOS_PAGO),
            "estado": estado,
            "fecha": cita["fecha"],
        })

    # KPIs del dashboard
    total_ingresos = sum(f["valor_cop"] for f in facturas if f["estado"] == "Pagado")
    pendientes = sum(f["valor_cop"] for f in facturas if f["estado"] in ("Pendiente", "Vencido"))

    return {
        "clinica": clinic_name,
        "tipo": clinic_type,
        "fecha_demo": str(hoy),
        "kpis": {
            "total_pacientes": len(pacientes),
            "citas_hoy": sum(1 for c in citas if c["fecha"] == str(hoy)),
            "citas_semana": len(citas),
            "ingresos_pagados_cop": total_ingresos,
            "facturas_pendientes_cop": pendientes,
            "tasa_asistencia_pct": 78,
        },
        "pacientes": pacientes,
        "citas": citas,
        "facturas": facturas,
        "servicios": servicios,
        "medicos": MEDICOS,
    }


# ── Contexto del sistema ──────────────────────────────────────────────────────

SYSTEM_CONTEXT = {
    "nombre_producto": "JR360 Sistema de Control Operativo para Clínicas",
    "empresa": "JR360 IA Agency LLC — Florida, USA",
    "posicionamiento": (
        "Centralizamos la operación de su clínica para que pueda controlar "
        "pacientes, citas, facturación, pagos y atención por WhatsApp desde un solo sistema."
    ),
    "propuesta_valor": [
        "Control operativo total desde un panel central",
        "Orden y trazabilidad en cada proceso",
        "Menos carga manual para el equipo",
        "Mejor visibilidad gerencial en tiempo real",
        "Seguimiento automático de pacientes y prospectos",
        "Atención por WhatsApp estructurada y sin caos",
    ],
    "modulos": [
        {"numero": 1, "nombre": "Centro de Control Gerencial", "descripcion": "KPIs, alertas operativas, actividad reciente, accesos rápidos"},
        {"numero": 2, "nombre": "WhatsApp Operativo", "descripcion": "Clasificación de mensajes, 7 intenciones detectadas, respuesta guiada"},
        {"numero": 3, "nombre": "CRM de Pacientes", "descripcion": "12 campos, 7 estados, alertas de datos incompletos"},
        {"numero": 4, "nombre": "Gestión de Agenda", "descripcion": "8 estados con colores, acciones rápidas, vista semanal"},
        {"numero": 5, "nombre": "Pre-Facturación", "descripcion": "11 campos, 6 estados, validaciones visuales, trazabilidad"},
        {"numero": 6, "nombre": "Calculadora de Impacto Económico", "descripcion": "Muestra cuánto dinero pierde la clínica hoy (argumento de cierre)"},
        {"numero": 7, "nombre": "Roles y Configuración", "descripcion": "6 roles: Admin, Recepción, Facturación, Médico, Comercial, Supervisor"},
    ],
    "tipos_clinica": ["Dental", "Medicina Estética", "Bienestar", "Quiropráctica", "Deportiva", "General"],
    "precios": {
        "setup_usd": 1200,
        "mensualidad_usd": 300,
        "moneda_facturacion": "USD",
        "notas": "Retención Colombia 15% Art.406 E.T. — partner retiene y paga a DIAN. JR360 exento sales tax Florida §212.08.",
    },
    "demos_live": {
        "control_operativo": "https://clinic-control-flow.base44.app",
        "landing_demos": "https://jr360-demos.netlify.app",
    },
    "no_prometer": [
        "Historia clínica médica real",
        "Integración DIAN sin validación previa",
        "Reemplazo de personal",
        "Diagnósticos con IA",
        "Resultados financieros garantizados",
    ],
}
