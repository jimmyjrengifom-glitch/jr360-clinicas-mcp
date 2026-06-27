# Bitácora — JR360 Clínicas MCP

**Proyecto:** jr360-clinicas-mcp  
**Repo GitHub:** https://github.com/jimmyjrengifom-glitch/jr360-clinicas-mcp  
**Responsable:** Jimmy Rengifo — JR360 IA Agency LLC  
**Inicio:** 2026-06-27

---

## Estado actual — 2026-06-27 ✅ OPERATIVO

| Componente | Estado |
|------------|--------|
| Código completo (6 tools) | ✅ |
| GitHub público | ✅ |
| Python 3.12 instalado (Homebrew) | ✅ |
| Venv + dependencias instaladas | ✅ |
| Servidor stdio funcionando | ✅ |
| Claude Desktop conectado | ✅ |

---

## Rutas importantes

| Recurso | Ruta |
|---------|------|
| Proyecto | `/Users/jimmyrengifo/JR360_IA_Agency/mcp/jr360_clinicas_mcp/` |
| Venv Python | `.venv/bin/python` |
| Config Claude Desktop | `~/Library/Application Support/Claude/claude_desktop_config.json` |
| GitHub | https://github.com/jimmyjrengifom-glitch/jr360-clinicas-mcp |

---

## 6 Tools disponibles

| Tool | Función |
|------|---------|
| `jr360_get_clinic_context` | Contexto completo: módulos, precios, posicionamiento |
| `jr360_generate_demo_data` | Datos ficticios COP por tipo de clínica |
| `jr360_classify_whatsapp` | Clasificador de intención sin API externa |
| `jr360_generate_daily_report` | Reporte ejecutivo diario en markdown |
| `jr360_answer_objection` | Respuestas a 12 objeciones frecuentes |
| `jr360_calculate_revenue_loss` | Calculadora fuga ingresos + ROI en COP |

---

## Arquitectura técnica

- **Stack:** Python 3.12 + FastMCP 1.28.1 + Pydantic v2
- **Transporte:** `stdio` para Claude Desktop (default) / `streamable-http` para Easypanel (via `MCP_TRANSPORT=streamable-http`)
- **Sin API externa:** todo local, sin costos
- **4 módulos:** `server.py`, `data_store.py`, `rule_engine.py`, `formatters.py`

---

## Historial de cambios

| Fecha | Cambio |
|-------|--------|
| 2026-06-27 | v1.0 — 6 tools construidas, GitHub publicado, Claude Desktop conectado |
| 2026-06-27 | Fix: host/port van en constructor FastMCP, no en run() |
| 2026-06-27 | Fix: transporte configurable via MCP_TRANSPORT — stdio por defecto |
| 2026-06-27 | Homebrew + Python 3.12 instalados en Mac |

---

## Pendientes

- [ ] Probar las 6 tools en Claude Desktop con casos reales
- [ ] Desplegar en Easypanel con `MCP_TRANSPORT=streamable-http`
- [ ] Agregar más tipos de clínica (oftalmología, pediatría, veterinaria)
- [ ] Soporte multi-moneda (MXN, ARS, PEN, CLP)

---

## Rutina de viernes — MCP Comunidad Latina

Cada viernes 2 horas dedicadas a:
1. Investigar qué herramientas MCP faltan para el mercado latino
2. Diseñar con Claude Desktop
3. Construir con Claude Code
4. Publicar en GitHub

**Próximo viernes:** 2026-07-04 — definir segundo MCP para la comunidad
