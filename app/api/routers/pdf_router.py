from typing import List
from app.api.models.pdf import PDF, Status
from app.api.models.veiculo import Veiculo
from fastapi import APIRouter, File, Form, UploadFile
from app.api.repositories.pdf_repository import PDFRepository
from app.api.services.pdf_service import PDFService
from app.database.mongo import get_database

# PDF router.
#
# Here we define the routes for the pdf resource.
# This router also acts as the controller for the pdf resource.
# It receives the requests, calls the service and returns the response.

# These variables start with an underscore to indicate that they are 'private'.
# They are not meant to be used outside of this file.
_database = get_database()
_pdf_repository = PDFRepository(_database)
_pdf_service = PDFService(_pdf_repository)
_pdf_router = APIRouter(prefix="/pdfs")


## Routes - START ##

@_pdf_router.get("/")
def get_pdfs() -> List[PDF]:
    return _pdf_service.get_all()


@_pdf_router.get("/{nome}")
def get_pdf(nome: str) -> PDF:
    return _pdf_service.get_by_nome(nome)


@_pdf_router.get("/csv/{nome}")
def get_pdf_as_csv(nome: str) -> str:
    return _pdf_service.get_pdf_as_csv(nome)


@_pdf_router.post("/")
def create_pdf(pdf_data: PDF) -> PDF:
    return _pdf_service.create(pdf_data)


@_pdf_router.put("/{nome}")
def update_pdf(nome: str, pdf_data: PDF) -> PDF:
    return _pdf_service.update(nome, pdf_data)


@_pdf_router.patch("/{nome}/{sigla}")
def update_pdf_veiculo(nome: str, sigla: str, veiculo_data: Veiculo) -> None:
    return _pdf_service.update_veiculo(nome, sigla, veiculo_data)


@_pdf_router.patch("/{nome}")
def update_pdf_status(nome: str, status: Status) -> None:
    return _pdf_service.update_pdf_status(nome, status)


@_pdf_router.delete("/{nomes}")
def delete_pdf(nomes: str) -> List[str]:
    return _pdf_service.delete_many(nomes)


@_pdf_router.post("/upload")
def create_pdf_by_pdf(file: UploadFile = File(...), montadora: str = Form(...)) -> PDF:
    pdf_bytes = file.file.read()
    file_name = file.filename
    return _pdf_service.create_by_pdf(file_name, pdf_bytes, montadora)

## Routes - END ##


# This function is used to get the car router.
# It is used in the main.py file to include the router in the FastAPI app.
def get_pdf_router() -> APIRouter:
    return _pdf_router
