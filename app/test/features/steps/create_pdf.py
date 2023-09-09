from behave import given, when, then
from fastapi.testclient import TestClient
from app.main import app
from app.api.models.pdf import PDF


# Create a TestClient instance to interact with the FastAPI application
test_app = TestClient(app=app)

# Define a placeholder for the PDF data JSON
pdf_data_json = None


# Define the step for the "Given the application is running" scenario
@given('the application is running')
def step_given_application_running(context):
    pass  # This step is already defined in the feature


# Define the step for the "When I send a POST request to '/pdfs' with the following JSON" scenario
@when(u'I send a POST request to "/pdfs" with the following JSON')
def step_when_send_post_request_with_json(context):
    global pdf_data_json
    pdf_data_json = context.text
    print(pdf_data_json)
    json = PDF.parse_raw(pdf_data_json).dict()
    response = test_app.post("/pdfs", json=json)
    context.response = response


# Define the step for the "Then the response status code should be 200 OK" scenario
@then('the response status code should be 200 OK')
def step_then_response_status_code_200(context):
    response = context.response
    assert response.status_code == 200
