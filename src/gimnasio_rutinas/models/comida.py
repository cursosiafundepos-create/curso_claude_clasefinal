"""Modelo Comida: registro nutricional de una comida en una fecha dada."""

from dataclasses import dataclass, field
from uuid import uuid4

TIPOS_VALIDOS = ["desayuno", "almuerzo", "cena", "snack"]

TIPOS_LABEL = {
    "desayuno": "Desayuno",
    "almuerzo": "Almuerzo",
    "cena": "Cena",
    "snack": "Snack",
}


class TipoComidaInvalidoError(ValueError):
    """Se intentó usar un tipo de comida que no es válido."""


def validar_tipo(tipo: str) -> str:
    if tipo not in TIPOS_VALIDOS:
        raise TipoComidaInvalidoError(
            f"'{tipo}' no es un tipo de comida válido. Los tipos válidos son: {', '.join(TIPOS_VALIDOS)}."
        )
    return tipo


@dataclass
class Comida:
    fecha: str
    tipo: str
    nombre: str
    calorias: int
    proteinas_g: float = 0.0
    carbohidratos_g: float = 0.0
    grasas_g: float = 0.0
    id: str = field(default_factory=lambda: uuid4().hex)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fecha": self.fecha,
            "tipo": self.tipo,
            "nombre": self.nombre,
            "calorias": self.calorias,
            "proteinas_g": self.proteinas_g,
            "carbohidratos_g": self.carbohidratos_g,
            "grasas_g": self.grasas_g,
        }

    @staticmethod
    def from_dict(data: dict) -> "Comida":
        return Comida(
            id=data.get("id") or uuid4().hex,
            fecha=data["fecha"],
            tipo=data["tipo"],
            nombre=data["nombre"],
            calorias=int(data["calorias"]),
            proteinas_g=float(data.get("proteinas_g", 0) or 0),
            carbohidratos_g=float(data.get("carbohidratos_g", 0) or 0),
            grasas_g=float(data.get("grasas_g", 0) or 0),
        )
