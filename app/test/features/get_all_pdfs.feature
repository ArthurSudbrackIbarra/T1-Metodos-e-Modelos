Feature: Get all PDFs

    Narrative:
    As an employee for Sinoserra
    I want to see all the PDFs
    So that I can check all the information that they contain

    Scenario: User requests to get all PDFs
        Given There are PDFs saved
        When I send a GET request to /pdfs
        Then the GET response status code should be 200 OK
        And the response should contain at least one PDF
