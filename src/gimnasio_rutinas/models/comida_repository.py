"""Persistencia de las comidas (registro nutricional) en un archivo JSON local."""

import json
from pathlib import Path
from threading import Lock

from .comida import Comida

_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_PATH = _REPO_ROOT / "data" / "comidas.json"

_lock = Lock()


class ComidaRepository:
    """Carga y guarda las comidas registradas."""

    def __init__(self, data_path: Path = DEFAULT_DATA_PATH):
        self.data_path = Path(data_path)

    def _leer(self) -> list[Comida]:
        if not self.data_path.exists():
            return []
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        return [Comida.from_dict(c) for c in raw]

    def _escribir(self, comidas: list[Comida]) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        serializable = [c.to_dict() for c in comidas]
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    def obtener_por_fecha(self, fecha: str) -> list[Comida]:
        with _lock:
            comidas = self._leer()
        return [c for c in comidas if c.fecha == fecha]

    def agregar(self, comida: Comida) -> None:
        with _lock:
            comidas = self._leer()
            comidas.append(comida)
            self._escribir(comidas)

    def editar(self, comida_id: str, datos: dict) -> None:
        with _lock:
            comidas = self._leer()
            for c in comidas:
                if c.id == comida_id:
                    c.nombre = datos.get("nombre", c.nombre)
                    c.tipo = datos.get("tipo", c.tipo)
                    c.calorias = int(datos.get("calorias", c.calorias))
                    c.proteinas_g = float(datos.get("proteinas_g", c.proteinas_g) or 0)
                    c.carbohidratos_g = float(datos.get("carbohidratos_g", c.carbohidratos_g) or 0)
                    c.grasas_g = float(datos.get("grasas_g", c.grasas_g) or 0)
                    break
            self._escribir(comidas)

    def eliminar(self, comida_id: str) -> None:
        with _lock:
            comidas = self._leer()
            comidas = [c for c in comidas if c.id != comida_id]
            self._escribir(comidas)
