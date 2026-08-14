"""Persistencia de las rutinas en un archivo JSON local (sin base de datos)."""

import json
from pathlib import Path
from threading import Lock

from .dia import DIAS_VALIDOS, validar_dia
from .ejercicio import Ejercicio

# repo_root/src/gimnasio_rutinas/models/rutina_repository.py -> repo_root
_REPO_ROOT = Path(__file__).resolve().parents[3]
DEFAULT_DATA_PATH = _REPO_ROOT / "data" / "rutinas.json"

_lock = Lock()


class RutinaRepository:
    """Carga y guarda la rutina semanal (lunes-viernes) en un archivo JSON."""

    def __init__(self, data_path: Path = DEFAULT_DATA_PATH):
        self.data_path = Path(data_path)

    def _semana_vacia(self) -> dict:
        return {dia: [] for dia in DIAS_VALIDOS}

    def _leer(self) -> dict:
        if not self.data_path.exists():
            return self._semana_vacia()
        with open(self.data_path, "r", encoding="utf-8") as f:
            raw = json.load(f)
        semana = self._semana_vacia()
        for dia in DIAS_VALIDOS:
            semana[dia] = [Ejercicio.from_dict(e) for e in raw.get(dia, [])]
        return semana

    def _escribir(self, semana: dict) -> None:
        self.data_path.parent.mkdir(parents=True, exist_ok=True)
        serializable = {
            dia: [e.to_dict() for e in ejercicios] for dia, ejercicios in semana.items()
        }
        with open(self.data_path, "w", encoding="utf-8") as f:
            json.dump(serializable, f, ensure_ascii=False, indent=2)

    def obtener_semana(self) -> dict:
        with _lock:
            return self._leer()

    def obtener_dia(self, dia: str) -> list[Ejercicio]:
        validar_dia(dia)
        with _lock:
            return self._leer()[dia]

    def agregar_ejercicio(self, dia: str, ejercicio: Ejercicio) -> None:
        validar_dia(dia)
        with _lock:
            semana = self._leer()
            semana[dia].append(ejercicio)
            self._escribir(semana)

    def editar_ejercicio(self, dia: str, ejercicio_id: str, datos: dict) -> None:
        validar_dia(dia)
        with _lock:
            semana = self._leer()
            for e in semana[dia]:
                if e.id == ejercicio_id:
                    e.nombre = datos.get("nombre", e.nombre)
                    e.series = int(datos.get("series", e.series))
                    e.repeticiones = str(datos.get("repeticiones", e.repeticiones))
                    e.peso = datos.get("peso", e.peso)
                    e.notas = datos.get("notas", e.notas)
                    break
            self._escribir(semana)

    def eliminar_ejercicio(self, dia: str, ejercicio_id: str) -> None:
        validar_dia(dia)
        with _lock:
            semana = self._leer()
            semana[dia] = [e for e in semana[dia] if e.id != ejercicio_id]
            self._escribir(semana)

    def reordenar(self, dia: str, ids_en_orden: list[str]) -> None:
        validar_dia(dia)
        with _lock:
            semana = self._leer()
            por_id = {e.id: e for e in semana[dia]}
            nuevo_orden = [por_id[i] for i in ids_en_orden if i in por_id]
            faltantes = [e for e in semana[dia] if e.id not in ids_en_orden]
            semana[dia] = nuevo_orden + faltantes
            self._escribir(semana)
