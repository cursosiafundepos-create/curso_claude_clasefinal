"""Modelo Suscripcion: plan global de la app (free/premium), sin pagos reales."""

from dataclasses import dataclass

PLANES_VALIDOS = ["free", "premium"]

PLANES_LABEL = {"free": "Free", "premium": "Premium"}


class PlanInvalidoError(ValueError):
    """Se intentó usar un plan que no es válido."""


def validar_plan(plan: str) -> str:
    if plan not in PLANES_VALIDOS:
        raise PlanInvalidoError(
            f"'{plan}' no es un plan válido. Los planes válidos son: {', '.join(PLANES_VALIDOS)}."
        )
    return plan


@dataclass
class Suscripcion:
    plan: str = "free"
    fecha_cambio: str = ""

    def to_dict(self) -> dict:
        return {"plan": self.plan, "fecha_cambio": self.fecha_cambio}

    @staticmethod
    def from_dict(data: dict) -> "Suscripcion":
        return Suscripcion(
            plan=data.get("plan", "free"),
            fecha_cambio=data.get("fecha_cambio", ""),
        )
