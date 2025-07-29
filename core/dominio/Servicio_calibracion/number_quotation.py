from datetime import datetime
from typing import List, Optional, Any


class QuotationNumberGenerator:
    
    MIN_SEQUENCE = 1
    MAX_SEQUENCE = 999
    VALID_TYPES = ['C', 'H']  

    @classmethod
    def generate(cls) -> str:
        quotation_type = cls._get_quotation_type()
        year = cls._get_current_year()
        sequence_number = cls._get_sequence_number()
        return f"{quotation_type}{year}{sequence_number:03d}"

    @classmethod
    def _get_quotation_type(cls, quotation_type: str) -> str:
        quotation_type = quotation_type.upper().strip()
        if quotation_type not in cls.VALID_TYPES:
            raise ValueError("El tipo de cotización debe ser 'C' para Clinica o 'H' para Hospital")
        return quotation_type

    @staticmethod
    def _get_current_year() -> int:
        return datetime.now().year

    @classmethod
    def _get_sequence_number(cls) -> int:
        try:
            sequence_input = input(
                f"Ingrese el número secuencial ({cls.MIN_SEQUENCE:03d}-{cls.MAX_SEQUENCE:03d}): "
            )
            sequence_number = int(sequence_input)

            if not cls.MIN_SEQUENCE <= sequence_number <= cls.MAX_SEQUENCE:
                raise ValueError(
                    f"El número secuencial debe estar entre {cls.MIN_SEQUENCE} y {cls.MAX_SEQUENCE}"
                )

            return sequence_number

        except ValueError as error:
            if "invalid literal" in str(error):
                raise ValueError("Debe ingresar un número válido") from error
            raise

    @classmethod
    def validate_quotation_format(cls, quotation_number: str) -> bool:

        if not quotation_number or len(quotation_number) != 8:
            return False
            
        quotation_type = quotation_number[0]
        year_part = quotation_number[1:5]
        sequence_part = quotation_number[5:8]
        
        try:
            year = int(year_part)
            sequence = int(sequence_part)
            
            return (quotation_type in cls.VALID_TYPES and 
                   2000 <= year <= 9999 and 
                   cls.MIN_SEQUENCE <= sequence <= cls.MAX_SEQUENCE)
        except ValueError:
            return False


class QuotationFinder:
    
    @staticmethod
    def find_by_number(quotation_number: str, quotations_list: List[Any]) -> Optional[Any]:

        if not quotation_number or not isinstance(quotation_number, str):
            return None
            
        if not QuotationNumberGenerator.validate_quotation_format(quotation_number):
            raise ValueError(f"Formato de cotización inválido: {quotation_number}")
            
        for quotation in quotations_list:
            if hasattr(quotation, 'num_quotation') and quotation.num_quotation == quotation_number:
                return quotation
        return None

    @staticmethod
    def find_by_type(quotation_type: str, quotations_list: List[Any]) -> List[Any]:

        if quotation_type not in QuotationNumberGenerator.VALID_TYPES:
            raise ValueError("El tipo debe ser 'C' o 'H'")
            
        result = []
        for quotation in quotations_list:
            if (hasattr(quotation, 'num_quotation') and 
                quotation.num_quotation and 
                quotation.num_quotation.startswith(quotation_type)):
                result.append(quotation)
        return result