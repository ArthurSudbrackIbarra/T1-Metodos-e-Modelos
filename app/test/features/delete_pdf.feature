Feature: Delete PDF

    Narrative:
    As an employee for Sinoserra
    I want to delete a PDF
    So that I can remove a PDF from the system

    Scenario: Delete one PDF
        Given A PDF with name "teste.pdf" exists in the system
        When I send a DELETE request to /pdfs/"teste.pdf"
        Then the response status code has to be 200 OK
        And the pdf must not exist in the system anymore

    Scenario: Delete multiple PDFs
        Given two PDFs with name "teste1.pdf" and "teste2.pdf" exist in the system
        When I send a DELETE request to the route /pdfs/"teste1.pdf";"teste2.pdf"
        Then the response status code has to be 200 OK
        And both pdfs must not exist in the system anymore
