from pydantic import BaseModel


# DTO = Data Transfer Object
# DTO to represent a Veiculo in a CSV file.
class VeiculoCSV_DTO(BaseModel):
    desc_cat: str
    desc_renavam: str
    sigla: str
    pacote_def_modelo: str
    versao: str
    preco: str
    ano: str
    marca: str
    linha: str
    motor: str
    carga: str
    num_passag: str
    num_portas: str
    num_renavam: str
    producao: str
    desc_vendas: str
