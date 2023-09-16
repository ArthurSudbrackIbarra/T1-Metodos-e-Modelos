from fastapi.testclient import TestClient
from behave import given, when, then
from app.test.mockers.pdf_mocker import build_pdf_with_default_params
from app.main import app
from fastapi import status


# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

global_pdf_name = ''
global_response = None


@given("That there is a PDF with the name {pdf_name}")
def step_given_that_there_is_a_pdf_with_the_name(context, pdf_name):
    global global_pdf_name
    global_pdf_name = pdf_name
    pdf = build_pdf_with_default_params()
    pdf.nome = pdf_name
    test_app.post("/pdfs", json=pdf.dict())


@when(r'I send a GET request to /pdfs/{pdf_name}')
def step_when_send_get_request_by_name(context, pdf_name):
    global global_response
    endpoint = f"/pdfs/{pdf_name}"

    # Send the GET request
    response = test_app.get(endpoint)
    global_response = response


@then("the GET by name response status code should be 200 OK")
def step_then_check_status_code(context):
    global global_response
    assert global_response.status_code == status.HTTP_200_OK


@then("the response should contain a PDF with the same name requested")
def step_then_check_response_contains_pdf_with_name(context):
    global global_pdf_name
    global global_response
    assert global_response.json()["nome"] == global_pdf_name


@given("That there isnt a PDF with the name {pdf_name}")
def step_given_that_there_isnt_a_pdf_with_the_name(context, pdf_name):
    global global_pdf_name
    global_pdf_name = pdf_name


@then("the GET by name response status code should be 404 not found")
def step_then_check_status_code(context):
    global global_response
    print(global_response)
    assert global_response.status_code == status.HTTP_404_NOT_FOUND
