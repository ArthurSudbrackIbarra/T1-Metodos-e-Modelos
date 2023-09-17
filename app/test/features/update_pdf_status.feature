Feature: Update a PDF status

    Narrative:
    As an employee for Sinoserra
    I want to search a PDF by name
    So that I can change its status to a new value

    Scenario: User requests to update a PDF status
        Given a PDF exists with the name "chevrolet.pdf"
        When I send a PATCH request to /pdfs/"chevrolet.pdf" with the new status "PENDENTE"
        Then the PATCH by name response status code should be 200 OK
        And the PDF with the name "chevrolet.pdf" should have its status equal to "PENDENTE"

    Scenario: User requests to update a PDF status that its name is not found
        Given a PDF doesnt exist with the name "chevnolet.pdf"
        When I send a PATCH request to /pdfs/"chevnolet.pdf" with the new status "PENDENTE"
        Then the PATCH by name response status code should be 400 BAD REQUEST
        