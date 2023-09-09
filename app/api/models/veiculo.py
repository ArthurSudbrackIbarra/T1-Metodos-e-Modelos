from pydantic import BaseModel
from typing import List


# Most fields are optional because there will be times when it will not
# be possible to get all the information. It will depend on how the pdf
# extraction is done.


# Copiavel class is used to store the value of a field and whether it
# has been copied or not in the frontend.
class Copiavel(BaseModel):
    valor: str = ""
    copiado: bool = False


# Combustivel class is used to store the fuel type and power of a
# vehicle.
class Combustivel(BaseModel):
    potencia: Copiavel = Copiavel()
    tipo_combustivel: Copiavel = Copiavel()


# Motor class is used to store the engine information of a vehicle.
class Motor(BaseModel):
    modelo: Copiavel = Copiavel()
    cilindradas: Copiavel = Copiavel()
    nro_cilindradas: Copiavel = Copiavel()
    combustiveis: List[Combustivel] = []


# Veiculo class is used to store the information of a vehicle.
class Veiculo(BaseModel):
    desc_cat: Copiavel = Copiavel()
    desc_renavam: Copiavel = Copiavel()
    sigla: Copiavel
    pacote_def_modelo: Copiavel = Copiavel()
    versao: Copiavel = Copiavel()
    preco: Copiavel = Copiavel()
    ano: Copiavel = Copiavel()
    marca: Copiavel = Copiavel()
    linha: Copiavel = Copiavel()
    motor: Motor = Motor()
    carga: Copiavel = Copiavel()
    num_passag: Copiavel = Copiavel()
    num_portas: Copiavel = Copiavel()
    num_renavam: Copiavel = Copiavel()
    producao: Copiavel = Copiavel()
    desc_vendas: Copiavel = Copiavel()
