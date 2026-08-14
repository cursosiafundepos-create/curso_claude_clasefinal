"""Modelo Ejercicio: una entrada dentro de la rutina de un día."""

from dataclasses import dataclass, field
from uuid import uuid4


@dataclass
class Ejercicio:
    nombre: str
    series: int
    repeticiones: str
    peso: str = ""
    notas: str = ""
    id: str = field(default_factory=lambda: uuid4().hex)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "nombre": self.nombre,
            "series": self.series,
            "repeticiones": self.repeticiones,
            "peso": self.peso,
            "notas": self.notas,
        }

    @staticmethod
    def from_dict(data: dict) -> "Ejercicio":
        return Ejercicio(
            id=data.get("id") or uuid4().hex,
            nombre=data["nombre"],
            series=int(data["series"]),
            repeticiones=str(data["repeticiones"]),
            peso=data.get("peso", ""),
            notas=data.get("notas", ""),
        )
