"""
Enums para unidades de medida
"""
from enum import Enum


class MeasurementUnit(str, Enum):
    """Unidades de medida disponibles para sectores"""
    PALLET = "palet"
    GRANEL = "granel"
    PALLET_GRANEL = "palet_granel"
    
    @classmethod
    def get_display_name(cls, value: str) -> str:
        """Obtener nombre de visualización para la unidad de medida"""
        display_names = {
            cls.PALLET: "Palet",
            cls.GRANEL: "Granel",
            cls.PALLET_GRANEL: "Palet/Granel"
        }
        return display_names.get(value, value)
    
    @classmethod
    def get_description(cls, value: str) -> str:
        """Obtener descripción para la unidad de medida"""
        descriptions = {
            cls.PALLET: "Mercancía en palets",
            cls.GRANEL: "Mercancía a granel",
            cls.PALLET_GRANEL: "Mercancía mixta (palets y granel)"
        }
        return descriptions.get(value, "") 