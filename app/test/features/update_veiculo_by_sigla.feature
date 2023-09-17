Feature: Update a Veiculo by sigla

    Narrative:
    As an employee for Sinoserra
    I want to update a Veiculo by its sigla inside a PDF that is searched by its name
    So that I can change the information about the Veiculo that has this sigla

    Scenario: User requests to update a Veiculo by sigla
        Given a PDF with the name "carrinho.pdf" exists
        And there is a Veiculo with the sigla "1" in the PDF
        When I send a PATCH request to /pdfs/"carrinho.pdf"/"1" with the updated Veiculo data
        Then the PATCH by sigla response status code should be 200 OK

    Scenario: User requests to update a Veiculo by sigla
        Given a PDF with the name "caminhonete.pdf" exists
        And there isnt a Veiculo with the sigla "-1" in the PDF
        When I send a PATCH request to /pdfs/"caminhonete.pdf"/"-1" with the updated Veiculo data
        Then the PATCH by sigla response status code should be 400 BAD REQUEST