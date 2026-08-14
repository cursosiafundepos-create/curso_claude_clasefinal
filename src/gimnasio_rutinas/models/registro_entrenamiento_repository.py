"""Persistencia del historial de entrenamientos en un archivo JSON local."""

import json
from pathlib import Path
from threading import Lock

from .registro_entrenamiento import RegistroEntrenamiento

_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_PATH = _REPO_ROOT / "data" / "entrenamientos.json"

_lock = Lock()


class RegistroEntrenamientoRepository:
    """Carga y guarda el historial de sesiones de entrenamiento reales."""

    def __init__(self, data_path: Path = DEFAULT_DATA_PATH):
        self.data_path = Path(data_path)

    def _leer(self) -> list[RegistroEntrenamiento]:
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [RegistroEntrenamiento.from_dict(r) for r in raw]

    def _escribir(self, registros: list[RegistroEntrenamiento]) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        serializable = [r.to_dict() for r in registros]
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    def listar_ejercicios(self) -> list[str]:
        with _lock:
            registros = self._leer()
        return sorted({r.ejercicio for r in registros})

    def historial_ejercicio(self, ejercicio: str) -> list[RegistroEntrenamiento]:
        with _lock:
            registros = self._leer()
        return sorted((r for r in registros if r.ejercicio == ejercicio), key=lambda r: r.fecha)

    def agregar(self, registro: RegistroEntrenamiento) -> None:
        with _lock:
            registros = self._leer()
            registros.append(registro)
            self._escribir(registros)
