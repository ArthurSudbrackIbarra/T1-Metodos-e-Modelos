from behave import given, when, then
from fastapi.testclient import TestClient
from fastapi import status
from app.main import app
from app.api.models.pdf import PDF
from app.test.mockers.pdf_mocker import build_pdf_with_default_params


# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

global_pdf_name = ""
global_pdf_names = []
global_response = None


@given('A PDF with name "{pdf_name}" exists in the system')
def step_given_pdf_exists(context, pdf_name):
    global global_pdf_name
    global_pdf_name = pdf_name
    pdf = build_pdf_with_default_params()
    pdf.nome = pdf_name
    test_app.post("/pdfs", json=pdf.dict())


@when('I send a DELETE request to /pdfs/"{pdf_name}"')
def step_when_send_delete_request(context, pdf_name):
    global global_response
    global_response = test_app.delete(f"/pdfs/{pdf_name}")


@then('the response status code has to be 200 OK')
def step_then_check_response_status(context):
    global global_response
    assert global_response.status_code == status.HTTP_200_OK


@then('the pdf must not exist in the system anymore')
def step_then_check_pdf_not_exist(context):
    global global_pdf_name
    response = test_app.get(f"/pdfs/{global_pdf_name}")
    assert response.status_code == status.HTTP_404_NOT_FOUND


@given('two PDFs with name "{pdf_name_1}" and "{pdf_name_2}" exist in the system')
def step_given_two_pdfs_exist(context, pdf_name_1, pdf_name_2):
    global global_pdf_names
    global_pdf_names = [pdf_name_1, pdf_name_2]
    pdf = build_pdf_with_default_params()
    pdf.nome = pdf_name_1
    test_app.post("/pdfs", json=pdf.dict())
    pdf.nome = pdf_name_2
    test_app.post("/pdfs", json=pdf.dict())


@when('I send a DELETE request to the route /pdfs/"{pdf_name_1}";"{pdf_name_2}"')
def step_when_send_multiple_delete_request(context, pdf_name_1, pdf_name_2):
    global global_response
    global_response = test_app.delete(f"/pdfs/{pdf_name_1};{pdf_name_2}")


@then('both pdfs must not exist in the system anymore')
def step_then_check_both_pdfs_not_exist(context):
    global global_pdf_names
    for pdf_name in global_pdf_names:
        response = test_app.get(f"/pdfs/{pdf_name}")
        assert response.status_code == status.HTTP_404_NOT_FOUND
