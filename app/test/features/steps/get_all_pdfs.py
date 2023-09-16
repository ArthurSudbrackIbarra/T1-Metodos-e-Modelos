from fastapi.testclient import TestClient
from behave import given, when, then
from app.main import app
from fastapi import status
from app.test.mockers.pdf_mocker import build_pdf_with_default_params


# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

global global_response


@given("There are PDFs saved")
def step_given_there_are_pdfs_saved(context):
    pdf = build_pdf_with_default_params()
    response = test_app.post("/pdfs", json=pdf.dict())


@when(r'I send a GET request to /pdfs')
def step_when_send_get_request(context):
    global global_response
    response = test_app.get("/pdfs")
    global_response = response


@then("the GET response status code should be 200 OK")
def step_then_check_status_code(context):
    global global_response
    assert global_response.status_code == 200


@then("the response should contain at least one PDF")
def step_then_check_response_contains_pdf(context):
    global global_response
    response_data = global_response.json()
    assert len(response_data) > 0
