import pytest
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.test.mockers.pdf_mocker import build_pdf_with_default_params, build_update_veihcle
from app.api.models.pdf import Status
from copy import deepcopy


# This fixture will be executed before each test.
# It will create a TestClient instance and pass it to the test function.
# The test function will be able to send requests to the application.
@pytest.fixture(scope="module")
def test_app():
    yield TestClient(app=app)


# PDF Mock data.
pdf_data = build_pdf_with_default_params()


# Test cases.
# Create a PDF.
def test_create_pdf(test_app: TestClient):
    response = test_app.post("/pdfs", json=pdf_data.dict())
    assert response.status_code == status.HTTP_200_OK


# Get all PDFs.
def test_get_all_pdfs(test_app: TestClient):
    response = test_app.get("/pdfs")
    assert response.status_code == status.HTTP_200_OK
    assert len(response.json()) > 0


# Get a PDF by nome.
def test_get_pdf_by_nome(test_app: TestClient):
    nome = pdf_data.nome
    response = test_app.get(f"/pdfs/{nome}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["nome"] == nome


# Update a PDF by nome.
def test_update_pdf_by_nome(test_app: TestClient):
    pdf_data.status = Status.CONCLUIDO
    nome = pdf_data.nome
    response = test_app.put(f"/pdfs/{nome}", json=pdf_data.dict())
    assert response.status_code == status.HTTP_200_OK


# Update a PDF by nome assert not found.
def test_update_pdf_by_nome_not_found(test_app: TestClient):
    pdf_data.status = Status.CONCLUIDO
    nome = 'abc'
    response = test_app.put(f"/pdfs/{nome}", json=pdf_data.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# Update Veiculo by sigla.
def test_patch_veiculo_by_sigla(test_app: TestClient):
    pdf_data.status = Status.CONCLUIDO
    nome_pdf = pdf_data.nome
    veiculo_update = build_update_veihcle()
    sigla = veiculo_update.sigla.valor
    response = test_app.patch(
        f"/pdfs/{nome_pdf}/{sigla}", json=veiculo_update.dict())
    assert response.status_code == status.HTTP_200_OK


# Update Veiculo by sigla assert not found.
def test_patch_veiculo_by_sigla_not_found(test_app: TestClient):
    pdf_data.status = Status.CONCLUIDO
    nome_pdf = "abc"
    veiculo_update = build_update_veihcle()
    sigla = veiculo_update.sigla.valor
    response = test_app.patch(
        f"/pdfs/{nome_pdf}/{sigla}", json=veiculo_update.dict())
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# Update PDF status assert not found.
def test_patch_pdf_status_not_found(test_app: TestClient):
    nome_pdf = "abc"
    status_novo = Status.CONCLUIDO
    response = test_app.patch(
        f"/pdfs/{nome_pdf}", params={"status": "concluido"})
    assert response.status_code == status.HTTP_400_BAD_REQUEST


# Update PDF status.
def test_patch_pdf_status(test_app: TestClient):
    nome_pdf = pdf_data.nome
    status_novo = Status.PENDENTE
    response = test_app.patch(
        f"/pdfs/{nome_pdf}", params={"status": status_novo.value})
    assert response.status_code == status.HTTP_200_OK


# Test upload a Jeep PDF file.
def test_upload_pdf_jeep(test_app: TestClient):
    file_path = r'app/test/pdfs_samples/jeep_pdfs/LP Jeep Nacional Commander - Dez 22.pdf'
    with open(file_path, "rb") as file:
        response = test_app.post(
            "/pdfs/upload",
            files={"file": file},
            data={"montadora": "Jeep"},
        )
        assert response.status_code == 200
        assert response.json()["veiculos"][0]["sigla"]["valor"] == "6711210"
        assert response.json()[
            "nome"] == "LP Jeep Nacional Commander - Dez 22.pdf"
        assert response.json()[
            "veiculos"][0]["desc_cat"]["valor"] == "COMMANDER LIMITED T270"


# Test sending a wrong montadora name.
def test_upload_pdf_wrong_montadora(test_app: TestClient):
    file_path = r'app/test/pdfs_samples/jeep_pdfs/LP Jeep Nacional Commander - Dez 22.pdf'
    with open(file_path, "rb") as file:
        response = test_app.post(
            "/pdfs/upload",
            files={"file": file},
            data={"montadora": "ABC"},
        )
        assert response.status_code == 400


# Test upload a Chevrolet PDF file.
def test_upload_pdf_chevrolet(test_app: TestClient):
    file_path = r'app/test/pdfs_samples/chevrolet_pdfs/2023_03_07 - MEV Chevrolet Tracker MY24 (2).pdf'
    with open(file_path, "rb") as file:
        response = test_app.post(
            "/pdfs/upload",
            files={"file": file},
            data={"montadora": "Chevrolet"},
        )
        assert response.status_code == 200
        assert response.json()["veiculos"][0]["sigla"]["valor"] == "5X76HR"
        assert response.json()[
            "nome"] == "2023_03_07 - MEV Chevrolet Tracker MY24 (2).pdf"
        assert response.json()[
            "veiculos"][0]["desc_cat"]["valor"] == "CHEV TRACKER T A"


# Test delete a PDF by nome.
def test_delete_pdf_by_nome(test_app: TestClient):
    nome = pdf_data.nome
    response = test_app.delete(f"/pdfs/{nome}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()[0] == nome


# Test delete many PDFs by nome.
def test_delete_many_pdfs_by_nome(test_app: TestClient):
    # Creating dummy PDFS to delete.
    test_app.post("/pdfs", json=pdf_data.dict())
    pdf_data_2 = deepcopy(pdf_data)
    pdf_data_2.nome = "Test_name.pdf"
    test_app.post("/pdfs", json=pdf_data_2.dict())
    # Using ';' to separate the names.
    nomes = f"{pdf_data.nome};{pdf_data_2.nome}"
    response = test_app.delete(f"/pdfs/{nomes}")
    as_list = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert as_list[0] == pdf_data.nome
    assert as_list[1] == pdf_data_2.nome


# Test get a pdf by nome not found.
def test_get_pdf_by_nome_not_found(test_app: TestClient):
    nome = pdf_data.nome
    response = test_app.get(f"/pdfs/{nome}")
    assert response.status_code == status.HTTP_404_NOT_FOUND
