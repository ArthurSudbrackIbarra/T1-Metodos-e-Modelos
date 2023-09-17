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

@given('That there is a PDF that needs to be updated with the name "{pdf_name}"')
def step_given_that_there_is_a_pdf_with_the_name(context, pdf_name):
    global global_pdf_name
    global global_data
    global_pdf_name = pdf_name
    pdf = build_pdf_with_default_params()
    pdf.nome = pdf_name
    global_data = pdf.dict()
    test_app.post("/pdfs", json=pdf.dict())

@given('That there isnt a PDF registered with the name "{pdf_name}"')
def step_given_that_there_is_a_pdf_with_the_name(context, pdf_name):
    pass

@when(u'I send an UPDATE request to /pdfs/"{pdf_name}"')
def step_when_send_update_request_by_name(context, pdf_name):
    global global_response
    global global_pdf_name

    # Store the expected PDF name for later validation
    global_pdf_name = pdf_name

    endpoint = f"/pdfs/{global_pdf_name}"

    global_data['status'] = Status.CONCLUIDO
    updated_data = global_data

    # Send the UPDATE request
    global_response = test_app.put(endpoint, json=updated_data)

@then("the UPDATE by name response status code should be 200 OK")
def step_then_check_status_code_ok(context):
    global global_response
    assert global_response.status_code == status.HTTP_200_OK

@then("the UPDATE by name response status code should be 400 BAD REQUEST")
def step_then_check_status_code_bad_request(context):
    global global_response
    assert global_response.status_code == status.HTTP_400_BAD_REQUEST

@then('the PDF with the name "{pdf_name}" status should be "{new_status}"')
def step_then_the_pdf_with_the_name_should_have_status(context, pdf_name, new_status):
    global global_response
    endpoint = f"/pdfs/{pdf_name}"
    response = test_app.get(endpoint)
    global_response = response
    assert global_response.json()["status"] == getattr(Status, new_status)