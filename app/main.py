from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from app.extractor import extraer_datos
from app.models import MensajeInput, ResultadoFinal

app = FastAPI()

@app.post("/extraer", response_model=ResultadoFinal, operation_id="extraer_datos")
def endpoint_extraer(mensaje: MensajeInput):
    return extraer_datos(mensaje)

# Activamos MCP al final
mcp = FastApiMCP(app, name="Extractor", description="Extrae intención desde lenguaje natural")
mcp.mount()
mcp.setup_server()
