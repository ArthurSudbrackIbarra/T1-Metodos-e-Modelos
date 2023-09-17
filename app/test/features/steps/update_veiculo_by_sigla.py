from fastapi.testclient import TestClient
from behave import given, when, then
from app.test.mockers.pdf_mocker import build_pdf_with_default_params, build_update_veihcle
from app.main import app
from fastapi import status

# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

global_pdf_name = ''
global_data = None
global_response = None
global_sigla = ''

@given('a PDF with the name "{pdf_name}" exists')
def step_given_a_pdf_with_the_name_exists(context, pdf_name):
    global global_pdf_name
    global global_data
    global_pdf_name = pdf_name
    pdf = build_pdf_with_default_params()
    pdf.nome = pdf_name
    global_data = pdf    

@given('there is a Veiculo with the sigla "{sigla}" in the PDF')
def step_given_there_is_a_veiculo_with_the_sigla(context, sigla):
    global global_data
    global_data.veiculos[0].sigla.valor = sigla
    response = test_app.post("/pdfs", json=global_data.dict())

@given('there isnt a Veiculo with the sigla "{sigla}" in the PDF')
def step_given_there_isnt_a_veiculo_with_the_sigla(context, sigla):
    global global_data
    response = test_app.post("/pdfs", json=global_data.dict())

@when('I send a PATCH request to /pdfs/"{pdf_name}"/"{sigla}" with the updated Veiculo data')
def step_when_send_patch_request_to_sigla_with_veiculo_data(context, pdf_name, sigla):
    global global_response
    global global_pdf_name
    global global_data
    global global_sigla

    global_pdf_name = pdf_name
    global_sigla = sigla
    endpoint = f"/pdfs/{global_pdf_name}/{global_sigla}"
    veiculo_update = build_update_veihcle()
    veiculo_update.ano.valor = "2020"
    veiculo_update.sigla.valor = global_sigla

    global_response = test_app.patch(endpoint, json=veiculo_update.dict())


@then("the PATCH by sigla response status code should be 200 OK")
def step_then_check_status_code_ok(context):
    global global_response
    assert global_response.status_code == status.HTTP_200_OK

@then("the PATCH by sigla response status code should be 400 BAD REQUEST")
def step_then_check_status_code_bad_request(context):
    global global_response
    assert global_response.status_code == status.HTTP_400_BAD_REQUEST