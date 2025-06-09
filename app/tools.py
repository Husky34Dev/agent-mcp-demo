import re
from app.db import buscar_abonado_por_dni, obtener_facturas_por_dni

async def get_info_from_message(request):
    mensaje = request.get("input", "")
    texto = mensaje.lower().strip()

    intencion = "consulta_general"
    tipo_dato = "desconocido"
    valor_dato = "no_detectado"

    if re.search(r"factura(s)?", texto):
        intencion = "obtener_facturas"
    elif re.search(r"dato(s)?|información personal", texto):
        intencion = "ver_datos_personales"

    dni_match = re.search(r"\b\d{8}[a-zA-Z]\b", mensaje)
    if dni_match:
        tipo_dato = "dni"
        valor_dato = dni_match.group()

    if intencion == "ver_datos_personales" and tipo_dato == "dni":
        datos = buscar_abonado_por_dni(valor_dato)
        if datos:
            respuesta = f"Nombre: {datos['nombre']} | Dirección: {datos['direccion']} | Email: {datos['email']} | Teléfono: {datos['telefono']} | Póliza: {datos['poliza']}"
        else:
            respuesta = "❌ No se encontró ningún abonado con ese DNI."
    elif intencion == "obtener_facturas" and tipo_dato == "dni":
        facturas = obtener_facturas_por_dni(valor_dato)
        if facturas:
            respuesta = "📄 Facturas encontradas:\n" + "\n".join([f"- {f['fecha']}: {f['importe']}€ ({f['estado']})" for f in facturas])
        else:
            respuesta = "❌ No se encontraron facturas para ese DNI."
    else:
        respuesta = "🤖 No se pudo ejecutar ninguna acción clara con tu mensaje."

    return {
        "event": "complete",
        "data": [{"respuesta": respuesta}]
    }