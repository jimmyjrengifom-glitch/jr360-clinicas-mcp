# JR360 Clínicas MCP

**MCP server para demos y ventas de sistemas de gestión operativa para clínicas en Colombia (y cualquier país hispanohablante).**

Construido por [JR360 IA Agency LLC](https://jr360iaagency.com) como herramienta open-source para la comunidad.

---

## ¿Qué hace este MCP?

Conecta Claude Desktop (u otro cliente MCP) con 6 herramientas especializadas para demostrar y vender un sistema de control operativo para clínicas médicas, sin depender de ninguna API externa.

Todas las operaciones son **100% locales** — sin costos de API, sin latencia, sin configuración compleja.

---

## 6 Tools disponibles

| Tool | Descripción |
|------|-------------|
| `jr360_get_clinic_context` | Contexto completo del sistema: módulos, posicionamiento, precios, demos |
| `jr360_generate_demo_data` | Genera pacientes, citas y facturas ficticias personalizadas en COP |
| `jr360_classify_whatsapp` | Clasifica intención de mensajes WhatsApp por reglas (sin API) |
| `jr360_generate_daily_report` | Reporte ejecutivo diario en markdown para gerencia |
| `jr360_answer_objection` | Respuestas comerciales a 12 objeciones frecuentes |
| `jr360_calculate_revenue_loss` | Calculadora de fuga de ingresos en COP — argumento de cierre |

---

## Inicio rápido

### Opción A — Local (recomendado para desarrollo)

**Requisito:** Python 3.10+

```bash
git clone https://github.com/jimmyjrengifom-glitch/jr360-clinicas-mcp.git
cd jr360-clinicas-mcp

python3 -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt

python server.py
# Servidor en http://localhost:8080/mcp
```

### Opción B — Docker

```bash
docker build -t jr360-clinicas-mcp .
docker run -p 8080:8080 jr360-clinicas-mcp
```

### Opción C — Easypanel / VPS

1. Fork este repositorio
2. En Easypanel → **New App → GitHub** → seleccionar el fork
3. Variables de entorno:
   ```
   MCP_PORT=8080
   MCP_HOST=0.0.0.0
   ```
4. Activar HTTPS (Traefik automático)
5. Tu servidor queda en `https://tu-dominio.easypanel.host/mcp`

---

## Conectar con Claude Desktop

Abre el archivo de configuración:
- **Mac:** `~/Library/Application Support/Claude/claude_desktop_config.json`
- **Windows:** `%APPDATA%\Claude\claude_desktop_config.json`

Agrega:

```json
{
  "mcpServers": {
    "jr360-clinicas": {
      "url": "http://localhost:8080/mcp",
      "transport": "streamable-http"
    }
  }
}
```

Reinicia Claude Desktop. Las 6 tools aparecen disponibles automáticamente.

---

## Ejemplos de uso en Claude Desktop

```
Usa jr360_get_clinic_context para darme el posicionamiento completo del sistema.
```

```
Usa jr360_generate_demo_data para crear una demo de una clínica dental llamada
"Sonrisa Perfecta" con 10 pacientes.
```

```
Clasifica este mensaje de WhatsApp: "Buenas, quiero agendar cita para el martes,
¿tienen disponibilidad?"
```

```
Dame la respuesta para esta objeción: "Es muy caro para nosotros"
```

```
Calcula la fuga de ingresos para una clínica con 200 pacientes/mes,
25% de ausentismo y ticket promedio de $150.000 COP.
```

```
Genera el reporte diario para "Clínica Salud Total" con estos datos:
{"citas_dia": 18, "citas_canceladas": 3, "pacientes_nuevos": 5,
"facturas_pagadas_cop": 1800000, "facturas_pendientes_cop": 450000, "leads_nuevos": 4}
```

---

## Estructura del proyecto

```
jr360-clinicas-mcp/
├── server.py        # FastMCP — punto de entrada, 6 tools
├── data_store.py    # Datos demo: pacientes, servicios, precios COP por tipo de clínica
├── rule_engine.py   # Clasificador WhatsApp + 12 objeciones con respuestas
├── formatters.py    # Formato COP, reporte diario, calculadora ROI
├── requirements.txt
├── Dockerfile
├── .env.example
└── README.md
```

---

## Stack técnico

- **Python 3.10+**
- **FastMCP** (`mcp[cli]>=1.9.0`) — framework oficial MCP de Anthropic
- **Pydantic v2** — validación de parámetros
- **Transporte:** Streamable HTTP
- **Sin dependencias de API externa** — todo local

---

## Tipos de clínica soportados

`dental` · `estetica` · `bienestar` · `quiropraxia` · `deportiva` · `general`

Cada tipo tiene su propio catálogo de servicios con precios en COP.

---

## Adaptar para otro país o moneda

Los datos de `data_store.py` son fáciles de modificar:

- `SERVICIOS_POR_TIPO` → cambiar precios a la moneda local
- `NOMBRES_PACIENTES` / `MEDICOS` → nombres del mercado objetivo
- En `formatters.py` → función `fmt_cop()` → cambiar símbolo y separadores

---

## Contribuir

Pull requests bienvenidos. Algunas ideas:

- Agregar más tipos de clínica (oftalmología, pediatría, veterinaria)
- Soporte multi-moneda (MXN, ARS, PEN, CLP)
- Tool para generar propuesta comercial en PDF
- Tool para generar guión de demo personalizado
- Integración con Airtable o Notion como backend real

---

## Licencia

MIT — libre para uso personal y comercial.

---

## Créditos

Creado por **Jimmy Rengifo** — [JR360 IA Agency LLC](https://jr360iaagency.com)

Si este proyecto te fue útil, dale una ⭐ al repositorio.

Para consultas comerciales sobre implementación para tu clínica:
- Web: [jr360iaagency.com](https://jr360iaagency.com)
- Demo en vivo: [jr360-demos.netlify.app](https://jr360-demos.netlify.app)
