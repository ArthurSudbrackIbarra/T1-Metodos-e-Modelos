from fastapi.testclient import TestClient
from behave import given, when, then
from app.test.mockers.pdf_mocker import build_pdf_with_default_params
from app.main import app
from fastapi import status
from app.api.models.pdf import Status

# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

global_pdf_name = ''
global_response = None
global_data = None

@given('a PDF exists with the name "{pdf_name}"')
def step_given_that_there_is_a_pdf_with_the_name(context, pdf_name):
    global global_pdf_name
    global global_data
    global_pdf_name = pdf_name
    pdf = build_pdf_with_default_params()
    pdf.nome = pdf_name
    test_app.post("/pdfs", json=pdf.dict())

@given('a PDF doesnt exist with the name "{pdf_name}"')
def step_given_pdf_does_not_exist(context, pdf_name):
    pass

@when(u'I send a PATCH request to /pdfs/"{pdf_name}" with the new status "{new_status}"')
def step_when_send_patch_request_by_name(context, pdf_name, new_status):
    global global_pdf_name
    global global_response

    global_pdf_name = pdf_name

    endpoint = f"/pdfs/{global_pdf_name}"
    
    status = getattr(Status, new_status)

    global_response = test_app.patch(endpoint, params={"status": status.value})

@then("the PATCH by name response status code should be 200 OK")
def step_then_check_status_code_ok(context):
    global global_response
    assert global_response.status_code == status.HTTP_200_OK

@then("the PATCH by name response status code should be 400 BAD REQUEST")
def step_then_check_status_code_bad_request(context):
    global global_response
    assert global_response.status_code == status.HTTP_400_BAD_REQUEST