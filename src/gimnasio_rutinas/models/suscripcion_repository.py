"""Persistencia del plan de suscripción (estado único y global) en un archivo JSON local."""

import json
from datetime import date
from pathlib import Path
from threading import Lock

from .suscripcion import Suscripcion, validar_plan

_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_PATH = _REPO_ROOT / "data" / "suscripcion.json"

_lock = Lock()


class SuscripcionRepository:
    """Carga y guarda el plan actual de la app (no hay lista de suscripciones)."""

    def __init__(self, data_path: Path = DEFAULT_DATA_PATH):
        self.data_path = Path(data_path)

    def _leer(self) -> Suscripcion:
        if not self.data_path.exists():
            return Suscripcion()
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return Suscripcion.from_dict(raw)

    def _escribir(self, suscripcion: Suscripcion) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(suscripcion.to_dict(), f, ensure_ascii=False, indent=2)

    def obtener(self) -> Suscripcion:
        with _lock:
            return self._leer()

    def cambiar_plan(self, plan: str) -> Suscripcion:
        validar_plan(plan)
        with _lock:
            suscripcion = Suscripcion(plan=plan, fecha_cambio=date.today().isoformat())
            self._escribir(suscripcion)
            return suscripcion

    def es_premium(self) -> bool:
        return self.obtener().plan == "premium"
