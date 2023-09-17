Feature: Upload Chevrolet PDF

    Narrative:
    As an employee for Sinoserra
    I want to upload Chevrolet PDFs
    So that I can extract data from them

    Scenario: Extract data from Chevrolet PDF
        Given The user uploads the Chevrolet PDF file located in "app/test/pdfs_samples/chevrolet_pdfs/2023_03_07 - MEV Chevrolet Tracker MY24 (2).pdf"
        When I send a POST request to /pdfs/upload with montadora set to "chevrolet"
        Then the response status code for my request should be 200 OK
        And the created pdf must have the same name as the uploaded file
        And the extracted sigla must be "5X76HR"
        And the extracted desc_cat must be "CHEV TRACKER T A"
