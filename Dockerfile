FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV MCP_PORT=8080
ENV MCP_HOST=0.0.0.0
ENV MCP_LOG_LEVEL=info

EXPOSE 8080

CMD ["python", "server.py"]
