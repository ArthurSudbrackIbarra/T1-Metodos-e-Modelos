from enum import Enum
from pydantic import BaseModel
from typing import List
from app.api.models.veiculo import Veiculo


# Status enum.
class Status(str, Enum):
    NAO_ABERTO = "nao aberto"
    PENDENTE = "pendente"
    CONCLUIDO = "concluido"


# PDF class is used to store the information of a pdf.
class PDF(BaseModel):
    nome: str
    status: Status = Status.NAO_ABERTO
    ultimo_visto: str = ""
    criado: str = ""
    veiculos: List[Veiculo] = []
