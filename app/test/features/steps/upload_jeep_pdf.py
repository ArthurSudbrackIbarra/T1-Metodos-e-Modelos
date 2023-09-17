from fastapi.testclient import TestClient
from behave import given, when, then
from app.test.mockers.pdf_mocker import build_pdf_with_default_params
from app.main import app
from fastapi import status
from os import path, chdir

# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

global_pdf_path = ""
global_response = None


@given('The user uploads the Jeep PDF file located in "{pdf_path}"')
def step_given_upload_chevrolet_pdf(context, pdf_path):
    global global_pdf_path
    global_pdf_path = path.abspath(pdf_path)


@when('I send a POST request to /pdfs/upload with the montadora set to "{montadora}"')
def step_when_send_post_request(context, montadora):
    global global_pdf_path
    global global_response
    with open(global_pdf_path, "rb") as file:
        response = test_app.post(
            "/pdfs/upload",
            files={"file": file},
            data={"montadora": montadora},
        )
        global_response = response


@then('the response status code for the request should be 200 OK')
def step_then_check_response_status(context):
    global global_response
    assert global_response.status_code == status.HTTP_200_OK


@then('the pdf created must have the same name as the uploaded file')
def step_then_check_pdf_name(context):
    global global_pdf_path
    global global_response

    # \\ or / depending on the OS
    if "\\" in global_pdf_path:
        assert global_response.json()[
            "nome"] == global_pdf_path.split("\\")[-1]
    else:
        assert global_response.json()[
            "nome"] == global_pdf_path.split("/")[-1]


@then('the extracted sigla must have the value "{expected_sigla}"')
def step_then_check_extracted_sigla(context, expected_sigla):
    global global_response
    assert global_response.json(
    )["veiculos"][0]["sigla"]["valor"] == expected_sigla


@then('the extracted desc_cat must have the value "{expected_desc_cat}"')
def step_then_check_extracted_desc_cat(context, expected_desc_cat):
    global global_response
    assert global_response.json()[
        "veiculos"][0]["desc_cat"]["valor"] == expected_desc_cat
