"""Formateadores: COP, fechas Colombia, plantillas markdown."""

from datetime import date


def fmt_cop(value: int | float) -> str:
    """$1.200.000 COP"""
    return f"${int(value):,}".replace(",", ".") + " COP"


def fmt_usd(value: int | float) -> str:
    return f"${value:,.0f} USD"


def build_daily_report(clinic_name: str, metrics: dict) -> str:
    hoy = metrics.get("fecha", str(date.today()))
    citas_dia = metrics.get("citas_dia", 0)
    citas_canceladas = metrics.get("citas_canceladas", 0)
    citas_no_asistio = metrics.get("citas_no_asistio", 0)
    pacientes_nuevos = metrics.get("pacientes_nuevos", 0)
    facturas_emitidas = metrics.get("facturas_emitidas", 0)
    facturas_pagadas_cop = metrics.get("facturas_pagadas_cop", 0)
    facturas_pendientes_cop = metrics.get("facturas_pendientes_cop", 0)
    leads_nuevos = metrics.get("leads_nuevos", 0)
    mensajes_whatsapp = metrics.get("mensajes_whatsapp", 0)

    tasa_asistencia = 0
    if citas_dia > 0:
        tasa_asistencia = round(((citas_dia - citas_canceladas - citas_no_asistio) / citas_dia) * 100)

    alertas = []
    if facturas_pendientes_cop > 500_000:
        alertas.append(f"⚠️ Cartera pendiente alta: {fmt_cop(facturas_pendientes_cop)}")
    if citas_no_asistio >= 3:
        alertas.append(f"⚠️ {citas_no_asistio} pacientes no asistieron — revisar seguimiento")
    if leads_nuevos == 0:
        alertas.append("⚠️ Sin leads nuevos hoy — verificar canales de captación")
    if not alertas:
        alertas.append("✅ Sin alertas críticas")

    recomendaciones = []
    if citas_canceladas > 0:
        recomendaciones.append("Activar recordatorio automático 24h antes para reducir cancelaciones")
    if facturas_pendientes_cop > 0:
        recomendaciones.append("Enviar recordatorio de pago a pacientes con facturas vencidas")
    if leads_nuevos < 3:
        recomendaciones.append("Revisar captación por WhatsApp y redes — bajo volumen de leads")
    if not recomendaciones:
        recomendaciones.append("Mantener el ritmo operativo actual")

    lines = [
        f"# Reporte Diario — {clinic_name}",
        f"**Fecha:** {hoy}  |  **Generado por:** JR360 Sistema Operativo",
        "",
        "---",
        "",
        "## Resumen General",
        f"La clínica operó con {citas_dia} citas programadas, {pacientes_nuevos} pacientes nuevos "
        f"y {leads_nuevos} leads entrantes. Tasa de asistencia: **{tasa_asistencia}%**.",
        "",
        "## Citas del Día",
        f"| Concepto | Valor |",
        f"|----------|-------|",
        f"| Programadas | {citas_dia} |",
        f"| Canceladas  | {citas_canceladas} |",
        f"| No asistió  | {citas_no_asistio} |",
        f"| Atendidas   | {max(0, citas_dia - citas_canceladas - citas_no_asistio)} |",
        f"| Tasa asistencia | {tasa_asistencia}% |",
        "",
        "## Facturación",
        f"| Concepto | Valor |",
        f"|----------|-------|",
        f"| Facturas emitidas    | {facturas_emitidas} |",
        f"| Ingresos cobrados    | {fmt_cop(facturas_pagadas_cop)} |",
        f"| Cartera pendiente    | {fmt_cop(facturas_pendientes_cop)} |",
        "",
        "## Pacientes y Leads",
        f"- Pacientes nuevos registrados: **{pacientes_nuevos}**",
        f"- Leads nuevos ingresados: **{leads_nuevos}**",
        f"- Mensajes WhatsApp procesados: **{mensajes_whatsapp}**",
        "",
        "## Alertas",
        *[f"- {a}" for a in alertas],
        "",
        "## Recomendaciones para Mañana",
        *[f"- {r}" for r in recomendaciones],
        "",
        "---",
        "*JR360 Sistema de Control Operativo — jr360iaagency.com*",
    ]
    return "\n".join(lines)


def build_revenue_loss_report(
    clinic_name: str,
    monthly_patients: int,
    missed_rate_pct: float,
    avg_ticket_cop: int,
    followup_recovery_pct: float = 30.0,
) -> str:
    missed_monthly = int(monthly_patients * missed_rate_pct / 100)
    annual_missed = missed_monthly * 12
    monthly_loss = missed_monthly * avg_ticket_cop
    annual_loss = monthly_loss * 12
    recoverable_monthly = int(monthly_loss * followup_recovery_pct / 100)
    recoverable_annual = recoverable_monthly * 12

    setup_usd = 1200
    monthly_usd = 300
    # ponytail: tasa fija para cálculo demo, sin llamada API
    usd_to_cop = 4_100
    setup_cop = setup_usd * usd_to_cop
    monthly_cop = monthly_usd * usd_to_cop
    annual_cost_cop = setup_cop + (monthly_cop * 12)
    roi_pct = round((recoverable_annual / annual_cost_cop) * 100) if annual_cost_cop else 0

    return "\n".join([
        f"# Calculadora de Impacto Económico — {clinic_name}",
        "",
        "## Pérdida actual estimada",
        f"| Concepto | Mensual | Anual |",
        f"|----------|---------|-------|",
        f"| Pacientes que no asisten | {missed_monthly} | {annual_missed} |",
        f"| Pérdida de ingresos | {fmt_cop(monthly_loss)} | {fmt_cop(annual_loss)} |",
        "",
        "## Con el sistema JR360",
        f"| Concepto | Mensual | Anual |",
        f"|----------|---------|-------|",
        f"| Ingresos recuperables (est. {followup_recovery_pct:.0f}%) | {fmt_cop(recoverable_monthly)} | {fmt_cop(recoverable_annual)} |",
        f"| Costo del sistema | {fmt_cop(monthly_cop)} | {fmt_cop(annual_cost_cop)} |",
        f"| **Beneficio neto estimado** | **{fmt_cop(recoverable_monthly - monthly_cop)}** | **{fmt_cop(recoverable_annual - annual_cost_cop)}** |",
        "",
        f"**ROI estimado primer año: {roi_pct}%**",
        "",
        "> Esta calculadora usa el promedio de recuperación observado en clínicas con sistema de confirmación "
        "y seguimiento automático. Los resultados reales dependen de la operación de cada clínica.",
        "",
        "---",
        "*JR360 IA Agency LLC — Sistema de Control Operativo para Clínicas*",
    ])
