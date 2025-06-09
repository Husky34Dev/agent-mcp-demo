import re
from app.models import MensajeInput, ResultadoFinal, FilaResultado

def extraer_datos(mensaje: MensajeInput) -> ResultadoFinal:
    texto = mensaje.mensaje.lower().strip()

    intencion = "consulta_general"
    tipo_dato = "desconocido"
    valor_dato = "no_detectado"

    if re.search(r"\bfactura(s)?\b", texto):
        intencion = "obtener_facturas"
    elif re.search(r"\bdato(s)?\b|\binformación personal\b", texto):
        intencion = "ver_datos_personales"
    elif re.search(r"\breclamación(es)?\b|\breclamar\b", texto):
        intencion = "consultar_reclamaciones"
    elif re.search(r"\binspección(es)?\b", texto):
        intencion = "consultar_inspecciones"
    elif re.search(r"\bcorte(s)?\b", texto):
        intencion = "consultar_cortes"
    elif re.search(r"\bcambio(s)?\b", texto):
        intencion = "consultar_cambios"
    elif re.search(r"\breposición(es)?\b", texto):
        intencion = "consultar_reposiciones"

    dni_match = re.search(r"\b\d{8}[a-zA-Z]\b", mensaje.mensaje)

    if dni_match:
        tipo_dato = "dni"
        valor_dato = dni_match.group()

    return ResultadoFinal(
        event="complete",
        data=[FilaResultado(intencion=intencion, tipo_dato=tipo_dato, valor_dato=valor_dato)]
    )
