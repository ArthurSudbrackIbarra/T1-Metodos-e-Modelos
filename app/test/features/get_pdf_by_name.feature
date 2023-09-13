Feature: Get a PDF by name

    Narrative:
    As an employee for Sinoserra
    I want to search a PDF by name
    So that I can check the information that it contains

    Scenario: User requests to get a PDF by name
        Given That there is a PDF with the name "jeep.pdf"
        When I send a GET request to /pdfs/"jeep.pdf"
        Then the GET by name response status code should be 200 OK
        And the response should contain a PDF with the same name requested