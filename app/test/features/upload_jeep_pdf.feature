Feature: Upload Jeep PDF

    Narrative:
    As an employee for Sinoserra
    I want to upload Jeep PDFs
    So that I can extract data from them

    Scenario: Extract data from Jeep PDF
        Given The user uploads the Jeep PDF file located in "app/test/pdfs_samples/jeep_pdfs/LP Jeep Nacional Commander - Dez 22.pdf"
        When I send a POST request to /pdfs/upload with the montadora set to "jeep"
        Then the response status code for the request should be 200 OK
        And the pdf created must have the same name as the uploaded file
        And the extracted sigla must have the value "6711210"
        And the extracted desc_cat must have the value "COMMANDER LIMITED T270"
