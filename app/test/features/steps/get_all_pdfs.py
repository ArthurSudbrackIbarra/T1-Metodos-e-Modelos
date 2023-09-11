from fastapi.testclient import TestClient
from behave import given, when, then
from app.main import app
from app.api.models.pdf import PDF

# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

@given("I am using the application")
def step_given_application_running(context):
    pass

@when(r'I send a GET request to "/pdfs"')
def step_when_send_get_request(context):
    response = test_app.get("/pdfs")
    context.response = response

@then("the GET response status code should be 200 OK")
def step_then_check_status_code(context):
    assert context.response.status_code == 200

@then("the response should contain at least one PDF")
def step_then_check_response_contains_pdf(context):
    response_data = context.response.json()
    assert len(response_data) > 0