"""Modelo RegistroEntrenamiento: una sesión real de un ejercicio en una fecha dada.

Es el historial usado para graficar progreso; a diferencia de Ejercicio (la
plantilla de rutina semanal), no está atado a lunes-viernes ni a un orden fijo.
"""

from dataclasses import dataclass, field
from datetime import date as _date
from uuid import uuid4

DIAS_SEMANA = ["lunes", "martes", "miercoles", "jueves", "viernes", "sabado", "domingo"]


def dia_de_fecha(fecha: str) -> str:
    return DIAS_SEMANA[_date.fromisoformat(fecha).weekday()]


@dataclass
class RegistroEntrenamiento:
    fecha: str
    ejercicio: str
    series: int
    repeticiones: int
    peso: float = 0.0
    id: str = field(default_factory=lambda: uuid4().hex)

    @property
    def dia(self) -> str:
        return dia_de_fecha(self.fecha)

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "fecha": self.fecha,
            "ejercicio": self.ejercicio,
            "series": self.series,
            "repeticiones": self.repeticiones,
            "peso": self.peso,
        }

    @staticmethod
    def from_dict(data: dict) -> "RegistroEntrenamiento":
        return RegistroEntrenamiento(
            id=data.get("id") or uuid4().hex,
            fecha=data["fecha"],
            ejercicio=data["ejercicio"],
            series=int(data["series"]),
            repeticiones=int(data["repeticiones"]),
            peso=float(data.get("peso", 0) or 0),
        )
