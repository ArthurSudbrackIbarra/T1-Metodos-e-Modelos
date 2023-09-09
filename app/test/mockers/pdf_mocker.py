from app.api.models.pdf import PDF, Status
from app.api.models.veiculo import Combustivel, Copiavel, Motor, Veiculo
from app.utils.utils import current_date


# This function returns a Veiculo instance with mocked data.
def mock_veiculo_with_default_params() -> Veiculo:
    return Veiculo(
        desc_cat=Copiavel(valor="desc"),
        renavam_desc=Copiavel(valor="renavam"),
        sigla=Copiavel(valor="1234Test"),
        pacote_def_modelo=Copiavel(valor="pacote"),
        versao=Copiavel(valor="versao"),
        ano=Copiavel(valor="ano"),
        marca=Copiavel(valor="marca"),
        linha=Copiavel(valor="linha"),
        motor=Motor(
            modelo=Copiavel(valor="modelo"),
            cilindradas=Copiavel(valor="cilindradas"),
            nro_cilindradas=Copiavel(valor="nro_cilindradas"),
            combustiveis=[Combustivel(
                potencia=Copiavel(valor="potencia"),
                tipo_combustivel=Copiavel(valor="tipo_combustivel")
            )]
        ),
        carga=Copiavel(valor="carga"),
        num_passag=Copiavel(valor="num_passag"),
        num_portas=Copiavel(valor="num_portas"),
        num_renavam=Copiavel(valor="num_renavam")
    )


# This function returns a PDF instance with mocked data.
def build_pdf_with_default_params() -> PDF:
    created_date = current_date()
    return PDF(
        nome="TEST Example PDF",
        status=Status.NAO_ABERTO,
        ultimo_visto=created_date,
        criado=created_date,
        veiculos=[mock_veiculo_with_default_params()]
    )


def build_update_veihcle() -> Veiculo:
    return Veiculo(
        desc_cat=Copiavel(valor="desc", copiado=True),
        desc_renavam=Copiavel(valor="renavam"),
        sigla=Copiavel(valor="1234Test"),
        pacote_def_modelo=Copiavel(valor="pacote"),
        versao=Copiavel(valor="versao"),
        ano=Copiavel(valor="ano"),
        marca=Copiavel(valor="marca"),
        linha=Copiavel(valor="linha"),
        motor=Motor(
            modelo=Copiavel(valor="modelo"),
            cilindradas=Copiavel(valor="cilindradas"),
            nro_cilindradas=Copiavel(valor="nro_cilindradas"),
            combustiveis=[Combustivel(
                potencia=Copiavel(valor="potencia"),
                tipo_combustivel=Copiavel(valor="tipo_combustivel")
            )]
        ),
        carga=Copiavel(valor="carga"),
        num_passag=Copiavel(valor="num_passag"),
        num_portas=Copiavel(valor="num_portas"),
        num_renavam=Copiavel(valor="num_renavam")
    )
