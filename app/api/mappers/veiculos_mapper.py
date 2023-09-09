from typing import List
from pydantic import BaseModel
from app.api.models.veiculo import Veiculo, Motor
from app.api.models.dto.veiculo_csv import VeiculoCSV_DTO


class VeiculoMapper(BaseModel):
    @staticmethod
    def map(veiculo: Veiculo) -> VeiculoCSV_DTO:
        return VeiculoCSV_DTO(
            sigla=veiculo.sigla.valor,
            desc_cat=veiculo.desc_cat.valor,
            desc_renavam=veiculo.desc_renavam.valor,
            pacote_def_modelo=veiculo.pacote_def_modelo.valor,
            versao=veiculo.versao.valor,
            preco=veiculo.preco.valor,
            ano=veiculo.ano.valor,
            marca=veiculo.marca.valor,
            linha=veiculo.linha.valor,
            motor=VeiculoMapper._join_motor(veiculo.motor),
            carga=veiculo.carga.valor,
            num_passag=veiculo.num_passag.valor,
            num_portas=veiculo.num_portas.valor,
            num_renavam=veiculo.num_renavam.valor,
            producao=veiculo.producao.valor,
            desc_vendas=veiculo.desc_vendas.valor,
        )

    @staticmethod
    def map_array(veiculos: List[Veiculo]):
        mapped_veiculos = []
        for veiculo in veiculos:
            mapped_veiculo = VeiculoMapper.map(veiculo)
            mapped_veiculos.append(mapped_veiculo)
        return mapped_veiculos

    @staticmethod
    def _join_motor(motor: Motor):
        new_motor = ""
        new_motor += " modelo: " + motor.modelo.valor
        new_motor += "- cilindradas: " + motor.cilindradas.valor
        new_motor += "- nro_cilindradas: " + motor.nro_cilindradas.valor
        for combustivel in motor.combustiveis:
            new_motor += "- " + combustivel.tipo_combustivel.valor + \
                ": " + combustivel.potencia.valor
        return new_motor
