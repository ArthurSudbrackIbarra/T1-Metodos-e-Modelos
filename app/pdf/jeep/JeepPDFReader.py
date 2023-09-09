import pdfplumber
from io import BytesIO
from pdfplumber.page import Page
from fuzzywuzzy import fuzz
from typing import Dict, List, Union
from re import search


# Method that uses Fuzzy string matching to check if two strings are similar.
# str1: First string to be compared.
# str2: Second string to be compared.
# ratio (optional): Minimum ratio of similarity between the two strings.
def is_similar(str1, str2, ratio: int = 75):
    return fuzz.ratio(str.lower(str1), str.lower(str2)) >= ratio


# Constants.
#
# Vehicle fields.
SIGLA = 'sigla'
ANO = 'ano'
DESC_CAT = 'desc_cat'
LINHA = 'linha'
DESC_RENAVAM = 'desc_renavam'
MARCA = 'marca'
COMBUSTIVEL = 'combustivel'
POTENCIA = 'potencia'
PRECO = 'preco'
PAGINA = 'pagina'
MOTOR = 'motor'
NUM_PASSAG = 'num_passag'

# Column names of the first and only table of the PDF file.
COLUMN_NAMES = [SIGLA, ANO, DESC_CAT, COMBUSTIVEL, PRECO, PAGINA]
#
# Other constants for pattern matching.
COLUMN_NAMES_STRING_MATCH = "MVS MY DESCRIÇÃO COMB. PREÇO(R$) PÁGINA"
TABLE_FOOTER_STRING_MATCH = "Tabela temporária e provisória, sujeita a modificações diárias. Para uso exclusivo e " \
                            "simples consulta por parte do profissional vendedor, não gerando obrigações de venda " \
                            "pelos valores meramente indicativos."
POSSIBLE_FUEL_TYPES = ['flex', 'diesel', 'gasolina']
#
# Regex constants.
REGEX_MAP = {
    POTENCIA: r'Potência máxima \(cv\) : ([0-9]+)',
    MOTOR: r'(?:\*|\.)Motor (.* \b(Diesel|Flex|Gasolina)\b)',
    NUM_PASSAG: r'Capacidade de Passageiro : ([0-9]+)',
}


# JeepPDFReader class that reads a PDF file and extracts the data from it.
# file_path: Path to the PDF file.
class JeepPDFReader:
    # Constructor of the class.
    def __init__(self, pdf_bytes: BytesIO = None, file_path: str = ''):
        if pdf_bytes is not None and file_path != '':
            raise ValueError(
                'You must provide either a PDF file path or a PDF file bytes, not both.')
        elif pdf_bytes is not None:
            self._target: Union[str, BytesIO] = pdf_bytes
        elif file_path != '':
            self._target: Union[str, BytesIO] = file_path
        else:
            raise ValueError(
                'You must provide either a PDF file path or a PDF file bytes.')
        self._cars: Dict[str, Dict[str, str]] = {}
        self._column_names: List[str] = []
        # Call the method to populate the 'cars' dictionary with basic data.
        self._build_cars_dict()

    # Method that reads the PDF file and extracts the data from it.
    # It is called by the constructor.
    # It fills the 'cars' dictionary with the basic data extracted from the PDF file.
    # The dictionary has the following structure:
    # {
    #   'nome_carro': {
    #       'sigla': '...',
    #       'ano': '...',
    #       'desc_cat': '...',
    #       'desc_renavam': '...',
    #       'marca': '...',
    #       'combustivel': '...'
    #       'linha': '...',
    #       'preco': '...',
    # },
    #   ...
    def _build_cars_dict(self) -> None:
        with pdfplumber.open(self._target) as pdf:
            pages = pdf.pages
            reading_cars = False
            # Iterates through the pages of the PDF file.
            for page in pages:
                page_content = page.extract_text()
                lines = page_content.split('\n')
                # Iterates through the lines of the page.
                for line in lines:
                    # If in the process of reading the cars (first table)...
                    if reading_cars:
                        # If we have reached the end of the table, stop reading the cars.
                        if is_similar(line, TABLE_FOOTER_STRING_MATCH):
                            # Add the missing data to the cars.
                            # Call the _fill_cars_data method.
                            self._fill_cars_data(pages)
                            return
                        # Because of a bad formatting of the 2023 PDF files, the 'sigla', 'ano' and 'desc_cat' values
                        # come glued together. We have to split them. It is known that the 'sigla' value always has 7
                        # digits, the 'ano' value always has 4 digits and the 'desc_cat' is the rest of the string.
                        parts = line.split(' ')
                        if len(parts[0]) > 7:
                            line = line[:7] + ' ' + \
                                line[7:11] + ' ' + line[11:]
                        elif len(parts[1]) > 4:
                            line = line[:7] + ' ' + \
                                line[8:12] + ' ' + line[12:]
                        # Creating the car_data_parsed list.
                        # This list will contain the data of the car.
                        # The name of the car might contain spaces, and when split by spaces, it will be split into
                        # multiple elements. We have to join these elements back together.
                        #
                        # Car data not parsed yet.
                        car_data = line.split(' ')
                        # Car data from positions 3 to the end (CAR NAME PARTS, FUEL TYPE, PRICE and PAGE)
                        card_data_sub = car_data[2:]
                        # Car data from positions 0 to 2. (MVS, MY and DESCRIÇÃO)
                        car_data_parsed = car_data[:3]
                        # Car data parsed with the car name joined back together.
                        car_data_parsed[-1] = ''
                        # Index where the fuel type is located.
                        fuel_type_index = -1
                        for i in range(len(card_data_sub)):
                            data = card_data_sub[i]
                            # If the data is a fuel type, the car name has ended.
                            # Break the for loop.
                            if str.lower(data) in POSSIBLE_FUEL_TYPES:
                                # Ok, we are now reading data from the fuel type column.
                                # Let's trim the car name, which is the last element of the car_data_parsed list.
                                car_data_parsed[-1] = car_data_parsed[-1].strip()
                                # And append the fuel type to the car_data_parsed list.
                                car_data_parsed.append(data)
                                fuel_type_index = i + 1
                                break
                            # If the data is not a fuel type, it is part of the car name.
                            # Join it back together in the last element of the car_data_parsed list.
                            else:
                                car_data_parsed[-1] += ' ' + data
                        # Append the rest of the data to the car_data_parsed list.
                        car_data_parsed += card_data_sub[fuel_type_index:]
                        # Get the 'sigla', which is the key of the car in the dictionary.
                        sigla = car_data[0]
                        # If the 'sigla' is valid it means that we still have cars to process.
                        if len(sigla) == 7:
                            # Get the car name, it will be used as the key of the car in the dictionary.
                            car_name = car_data_parsed[2]
                            self._cars[car_name] = {}
                            for i in range(len(COLUMN_NAMES)):
                                self._cars[car_name][COLUMN_NAMES[i]
                                                     ] = car_data_parsed[i]
                            # Set car's custom attributes.
                            car_parts = self._cars[car_name][DESC_CAT].split(
                                ' ')
                            desc_renavam = car_parts[1:]
                            linha = car_parts[0]
                            self._cars[car_name][LINHA] = linha
                            self._cars[car_name][DESC_RENAVAM] = ' '.join(
                                desc_renavam)
                            self._cars[car_name][MARCA] = 'JEEP'
                        else:
                            # No more cars to process, exit the for loop.
                            break
                    # If not in the process of reading the cars...
                    elif is_similar(line, COLUMN_NAMES_STRING_MATCH):
                        reading_cars = True

    # Method responsible for adding the missing data to the cars.
    # It is called by the _build_cars_dict method.
    # This method currently adds these fields to the cars:
    # {
    #   'nome_carro': {
    #       'potencia': '...',
    #       'motor': '...',
    # },
    def _fill_cars_data(self, pages: List[Page]) -> None:
        car_names = list(self._cars.keys())
        current_car_index = 0
        current_car = car_names[current_car_index]
        next_car_index = 1
        next_car = car_names[next_car_index]
        reading_car = False
        for page in pages:
            page_content = page.extract_text()
            lines = page_content.split('\n')
            for line in lines:
                # If the current_car is None, it means that we have finished reading all the cars.
                # Exit the method.
                if current_car is None:
                    return
                # Check if the line is equal to the next car name.
                # If so, set the reading_car flag to True.
                if str.lower(line).strip() == str.lower(current_car).strip():
                    reading_car = True
                    continue
                # If reading a car...
                if reading_car:
                    # Check if the line is equal to the pdf footer.
                    # If so, we have finished reading the car.
                    # Move on to the next car.
                    if is_similar(line, TABLE_FOOTER_STRING_MATCH):
                        reading_car = False
                        current_car_index = next_car_index
                        current_car = next_car
                        if current_car_index + 1 < len(car_names):
                            next_car_index += 1
                            next_car = car_names[next_car_index]
                        else:
                            next_car = None
                        continue
                    # If the line is not equal to the pdf footer...
                    # We are still reading the car.
                    #
                    # Check for regex matches.
                    for key in REGEX_MAP:
                        regex = REGEX_MAP[key]
                        result = search(regex, line)
                        if result is not None:
                            try:
                                self._cars[current_car][key] = result.group(
                                    1).strip()
                                continue
                            except IndexError:
                                pass

    # Method that returns the cars extracted from the PDF file.
    # It returns a copy of the dictionary, so that the original dictionary is not modified.
    def get_cars(self) -> Dict[str, Dict[str, str]]:
        return self._cars.copy()
