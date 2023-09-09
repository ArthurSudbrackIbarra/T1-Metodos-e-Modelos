Feature: Create a PDF

    Narrative:
    As an employee for Sinoserra
    I want to create a vehicle PDF
    So that I can store the vehicle information

    Scenario: Creating a PDF
        Given the application is running
        When I send a POST request to "/pdfs" with the following JSON:
            """
            {
                "nome": "ExamplePDF.pdf",
                "status": "nao aberto",
                "ultimo_visto": "2023-09-09T00:00:00Z",
                "criado": "2023-09-09T00:00:00Z",
                "veiculos": [
                    {
                        "desc_cat": {
                            "valor": "desc"
                        },
                        "renavam_desc": {
                            "valor": "renavam"
                        },
                        "sigla": {
                            "valor": "1234Test"
                        },
                        "pacote_def_modelo": {
                            "valor": "pacote"
                        },
                        "versao": {
                            "valor": "versao"
                        },
                        "ano": {
                            "valor": "ano"
                        },
                        "marca": {
                            "valor": "marca"
                        },
                        "linha": {
                            "valor": "linha"
                        },
                        "motor": {
                            "modelo": {
                                "valor": "modelo"
                            },
                            "cilindradas": {
                                "valor": "cilindradas"
                            },
                            "nro_cilindradas": {
                                "valor": "nro_cilindradas"
                            },
                            "combustiveis": [
                                {
                                    "potencia": {
                                        "valor": "potencia"
                                    },
                                    "tipo_combustivel": {
                                        "valor": "tipo_combustivel"
                                    }
                                }
                            ]
                        },
                        "carga": {
                            "valor": "carga"
                        },
                        "num_passag": {
                            "valor": "num_passag"
                        },
                        "num_portas": {
                            "valor": "num_portas"
                        },
                        "num_renavam": {
                            "valor": "num_renavam"
                        }
                    }
                ]
            }
            """
        Then the response status code should be 200 OK
