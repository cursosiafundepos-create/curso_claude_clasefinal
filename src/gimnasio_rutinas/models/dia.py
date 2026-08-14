"""Modelo Día: los únicos días válidos para una rutina son lunes a viernes."""

DIAS_VALIDOS = ["lunes", "martes", "miercoles", "jueves", "viernes"]

DIAS_LABEL = {
    "lunes": "Lunes",
    "martes": "Martes",
    "miercoles": "Miércoles",
    "jueves": "Jueves",
    "viernes": "Viernes",
}


class DiaInvalidoError(ValueError):
    """Se intentó usar un día que no es lunes-viernes."""


def validar_dia(dia: str) -> str:
    if dia not in DIAS_VALIDOS:
        raise DiaInvalidoError(
            f"'{dia}' no es un día válido. Los días válidos son: {', '.join(DIAS_VALIDOS)}."
        )
    return dia
