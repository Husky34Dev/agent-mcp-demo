from pydantic import BaseModel
from typing import List

class MensajeInput(BaseModel):
    mensaje: str

class FilaResultado(BaseModel):
    intencion: str
    tipo_dato: str
    valor_dato: str

class ResultadoFinal(BaseModel):
    event: str
    data: List[FilaResultado]
