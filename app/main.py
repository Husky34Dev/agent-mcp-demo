from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
import sqlite3

app = FastAPI()
mcp = FastApiMCP(app, name="AgenteDB", description="Consulta datos de abonados")

DB_PATH = "app/data/demo.db"

def obtener_conexion():
    return sqlite3.connect(DB_PATH)

# Entrada esperada
class DNIInput(BaseModel):
    dni: str

# Herramienta: consultar datos personales
@app.post("/datos_personales", operation_id="consultar_datos_personales")
def consultar_datos_personales(input: DNIInput):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, direccion, telefono, email, poliza FROM abonados WHERE dni = ?", (input.dni,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "respuesta": f"Nombre: {row[0]}, Dirección: {row[1]}, Teléfono: {row[2]}, Email: {row[3]}, Póliza: {row[4]}"
        }
    return {"respuesta": "❌ No se encontró ningún abonado con ese DNI."}

# Herramienta: consultar facturas
@app.post("/facturas", operation_id="consultar_facturas")
def consultar_facturas(input: DNIInput):
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, importe, estado FROM facturas WHERE dni_abonado = ?", (input.dni,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return {"respuesta": "❌ No hay facturas para este abonado."}
    return {
        "respuesta": "\\n".join([f"- {r[0]}: {r[1]}€ ({r[2]})" for r in rows])
    }

# Activar MCP
mcp.mount()
mcp.setup_server()
