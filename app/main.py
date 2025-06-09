from fastapi import FastAPI
from fastapi_mcp import FastApiMCP, tool
import sqlite3

app = FastAPI()
mcp = FastApiMCP(app, name="AgenteDB", description="Herramientas para consultar datos", version="1.0")

DB_PATH = "app/data/demo.db"

def obtener_conexion():
    return sqlite3.connect(DB_PATH)

@tool(name="consultar_datos_personales", description="Consulta los datos personales de un abonado por su DNI.")
def consultar_datos_personales(dni: str) -> str:
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, direccion, telefono, email, poliza FROM abonados WHERE dni = ?", (dni,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return f"Nombre: {row[0]}, Dirección: {row[1]}, Teléfono: {row[2]}, Email: {row[3]}, Póliza: {row[4]}"
    return "❌ No se encontró ningún abonado con ese DNI."

@tool(name="consultar_facturas", description="Consulta las facturas asociadas a un abonado por su DNI.")
def consultar_facturas(dni: str) -> str:
    conn = obtener_conexion()
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, importe, estado FROM facturas WHERE dni_abonado = ?", (dni,))
    rows = cursor.fetchall()
    conn.close()
    if not rows:
        return "❌ No hay facturas para este abonado."
    return "\\n".join([f"- {r[0]}: {r[1]}€ ({r[2]})" for r in rows])

mcp.mount(app)
mcp.setup_server()
