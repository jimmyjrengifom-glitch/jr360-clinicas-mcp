"""JR360 Clínicas MCP — 6 tools, Streamable HTTP, sin API externa."""

import json
import os
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from data_store import SYSTEM_CONTEXT, generate_demo_data
from formatters import build_daily_report, build_revenue_loss_report
from rule_engine import answer_objection, classify_whatsapp

mcp = FastMCP(
    name="jr360-clinicas",
    instructions=(
        "Servidor MCP de JR360 IA Agency para demos y ventas del sistema de control operativo "
        "para clínicas en Colombia. NUNCA mencionar 'IA' al cliente — siempre hablar de "
        "'sistema de control operativo centralizado'. Todos los valores monetarios en COP."
    ),
    host=os.getenv("MCP_HOST", "0.0.0.0"),
    port=int(os.getenv("MCP_PORT", "8080")),
)


@mcp.tool()
def jr360_get_clinic_context() -> str:
    """
    Devuelve el contexto completo del sistema JR360 para clínicas:
    módulos, posicionamiento, precios, demos en vivo y restricciones comerciales.
    """
    ctx = SYSTEM_CONTEXT
    sections = [
        f"# {ctx['nombre_producto']}",
        f"**Empresa:** {ctx['empresa']}",
        "",
        "## Posicionamiento",
        ctx["posicionamiento"],
        "",
        "## Propuesta de valor",
        *[f"- {v}" for v in ctx["propuesta_valor"]],
        "",
        "## Módulos del sistema",
        *[f"{m['numero']}. **{m['nombre']}** — {m['descripcion']}" for m in ctx["modulos"]],
        "",
        "## Tipos de clínica soportados",
        ", ".join(ctx["tipos_clinica"]),
        "",
        "## Precios",
        f"- Setup único: ${ctx['precios']['setup_usd']:,} USD",
        f"- Mensualidad: ${ctx['precios']['mensualidad_usd']:,} USD",
        f"- {ctx['precios']['notas']}",
        "",
        "## Demos en vivo",
        *[f"- {k.replace('_', ' ').title()}: {v}" for k, v in ctx["demos_live"].items()],
        "",
        "## NO prometer en ninguna demo",
        *[f"- {x}" for x in ctx["no_prometer"]],
    ]
    return "\n".join(sections)


@mcp.tool()
def jr360_generate_demo_data(
    clinic_name: Annotated[str, Field(description="Nombre de la clínica, ej: Sonrisa Perfecta")],
    clinic_type: Annotated[
        str,
        Field(description="Tipo: dental | estetica | bienestar | quiropraxia | deportiva | general"),
    ],
    num_patients: Annotated[int, Field(description="Cantidad de pacientes demo (4-12)", ge=4, le=12)] = 8,
) -> str:
    """
    Genera datos demo ficticios personalizados para una clínica colombiana:
    pacientes, citas, pre-facturas y KPIs del dashboard en COP.
    """
    data = generate_demo_data(clinic_name, clinic_type, num_patients)
    return json.dumps(data, ensure_ascii=False, indent=2)


@mcp.tool()
def jr360_classify_whatsapp(
    message: Annotated[str, Field(description="Texto del mensaje de WhatsApp a clasificar")],
) -> str:
    """
    Clasifica la intención de un mensaje de WhatsApp por reglas de keywords.
    Devuelve: intent, priority, summary, recommended_action, requires_human, suggested_response.
    Sin llamada a API externa — clasificación instantánea.
    """
    result = classify_whatsapp(message)
    output = {
        "intent": result.intent,
        "priority": result.priority,
        "summary": result.summary,
        "recommended_action": result.recommended_action,
        "requires_human": result.requires_human,
        "suggested_response": result.suggested_response,
    }
    return json.dumps(output, ensure_ascii=False, indent=2)


@mcp.tool()
def jr360_generate_daily_report(
    clinic_name: Annotated[str, Field(description="Nombre de la clínica")],
    metrics: Annotated[
        str,
        Field(
            description=(
                "JSON con métricas del día. Campos opcionales: "
                "fecha, citas_dia, citas_canceladas, citas_no_asistio, pacientes_nuevos, "
                "facturas_emitidas, facturas_pagadas_cop, facturas_pendientes_cop, "
                "leads_nuevos, mensajes_whatsapp"
            )
        ),
    ],
) -> str:
    """
    Genera un reporte ejecutivo diario en markdown para gerencia de la clínica.
    Incluye: resumen, citas, facturación, leads, alertas y recomendaciones.
    """
    try:
        data = json.loads(metrics)
    except json.JSONDecodeError:
        return "Error: el parámetro 'metrics' debe ser un JSON válido."
    return build_daily_report(clinic_name, data)


@mcp.tool()
def jr360_answer_objection(
    objection: Annotated[str, Field(description="Objeción del prospecto tal como la dijo")],
) -> str:
    """
    Devuelve la respuesta comercial adecuada para la objeción del prospecto.
    Cubre 12 objeciones frecuentes. NUNCA menciona 'IA' — siempre habla de
    control operativo, orden y ahorro de tiempo.
    """
    result = answer_objection(objection)
    return json.dumps(result, ensure_ascii=False, indent=2)


@mcp.tool()
def jr360_calculate_revenue_loss(
    clinic_name: Annotated[str, Field(description="Nombre de la clínica")],
    monthly_patients: Annotated[int, Field(description="Pacientes atendidos por mes", ge=1)],
    missed_rate_pct: Annotated[
        float, Field(description="Porcentaje de ausentismo/cancelaciones (ej: 20 para 20%)", ge=0, le=100)
    ],
    avg_ticket_cop: Annotated[int, Field(description="Valor promedio del servicio en COP", ge=1)],
    followup_recovery_pct: Annotated[
        float,
        Field(description="% de pacientes perdidos que se recuperan con seguimiento automático (default 30)", ge=0, le=100),
    ] = 30.0,
) -> str:
    """
    Calcula la fuga mensual y anual de ingresos por ausentismo.
    Muestra el beneficio neto del sistema vs costo y ROI estimado primer año.
    Argumento de cierre para la venta.
    """
    return build_revenue_loss_report(
        clinic_name, monthly_patients, missed_rate_pct, avg_ticket_cop, followup_recovery_pct
    )


if __name__ == "__main__":
    mcp.run(transport="streamable-http")
