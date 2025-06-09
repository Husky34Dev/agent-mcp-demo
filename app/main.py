from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from app.tools import get_info_from_message

app = FastAPI()

@app.post("/mcp")
async def mcp_handler(request: dict):
    return await get_info_from_message(request)

mcp = FastApiMCP(app, name="Chatbot Agente", description="Agente con extracción + acción")
mcp.mount()
mcp.setup_server()