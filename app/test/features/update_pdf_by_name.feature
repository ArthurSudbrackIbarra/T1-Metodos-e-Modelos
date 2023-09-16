Feature: Update a PDF by name

    Narrative:
    As an employee for Sinoserra
    I want to search a PDF by name
    So that I can change the information that it contains

    Scenario: User requests to update a PDF by name
        Given That there is a PDF that needs to be updated with the name "toyota.pdf"
        When I send an UPDATE request to /pdfs/"toyota.pdf"
        Then the UPDATE by name response status code should be 200 OK

    Scenario: User requests to update a PDF by name not found
        Given That there isnt a PDF registered with the name "toiota.pdf"
        When I send an UPDATE request to /pdfs/"toiota.pdf"
        Then the UPDATE by name response status code should be 400 BAD REQUEST
