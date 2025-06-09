from fastapi import FastAPI
from fastapi_mcp import FastApiMCP
from pydantic import BaseModel
import sqlite3

app = FastAPI()
mcp = FastApiMCP(app, name="AgenteDB", description="Consulta datos de abonados")

DB_PATH = "app/data/demo.db"

def obtener_conexion():
    return sqlite3.connect(DB_PATH)

class DNIInput(BaseModel):
    dni: str

@mcp.tool()
def consultar_datos_personales(input: DNIInput) -> dict:
    """
    Consulta los datos personales de un abonado.
    """
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

@mcp.tool()
def consultar_facturas(input: DNIInput) -> dict:
    """
    Consulta las facturas de un abonado.
    """
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, importe, estado FROM facturas WHERE dni_abonado = ?", (input.dni,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return {"respuesta": "❌ No hay facturas para este abonado."}
    return {
        "respuesta": "\n".join([f"- {r[0]}: {r[1]}€ ({r[2]})" for r in rows])
    }

# Montar servidor
mcp.mount()
mcp.setup_server()
