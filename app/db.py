import sqlite3
from typing import List, Dict

DB_PATH = "app/data/demo.db"

def buscar_abonado_por_dni(dni: str) -> Dict:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT nombre, direccion, telefono, email, poliza FROM abonados WHERE dni = ?", (dni,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return {
            "nombre": row[0],
            "direccion": row[1],
            "telefono": row[2],
            "email": row[3],
            "poliza": row[4],
        }
    return {}

def obtener_facturas_por_dni(dni: str) -> List[Dict]:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT fecha, importe, estado FROM facturas WHERE dni_abonado = ?", (dni,))
    rows = cursor.fetchall()
    conn.close()
    return [{"fecha": r[0], "importe": r[1], "estado": r[2]} for r in rows]
