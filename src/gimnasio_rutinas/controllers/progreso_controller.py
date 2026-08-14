"""Controller: rutas web para registrar entrenamientos y ver el progreso por ejercicio."""

from flask import Blueprint, redirect, render_template, request, url_for

from ..models.registro_entrenamiento import RegistroEntrenamiento
from ..models.registro_entrenamiento_repository import RegistroEntrenamientoRepository
from ..models.suscripcion_repository import SuscripcionRepository

progreso_bp = Blueprint("progreso", __name__)
repo = RegistroEntrenamientoRepository()
suscripcion_repo = SuscripcionRepository()


@progreso_bp.route("/progreso")
def ver_progreso():
    ejercicios = repo.listar_ejercicios()
    return render_template(
        "progreso.html", ejercicios=ejercicios, es_premium=suscripcion_repo.es_premium()
    )


@progreso_bp.route("/progreso/registrar", methods=["POST"])
def registrar_entrenamiento():
    registro = RegistroEntrenamiento(
        fecha=request.form["fecha"],
        ejercicio=request.form["ejercicio"].strip(),
        series=int(request.form["series"]),
        repeticiones=int(request.form["repeticiones"]),
        peso=float(request.form.get("peso") or 0),
    )
    repo.agregar(registro)
    return redirect(url_for("progreso.ver_progreso"))


@progreso_bp.route("/progreso/<ejercicio>")
def ver_progreso_ejercicio(ejercicio):
    es_premium = suscripcion_repo.es_premium()
    historial = repo.historial_ejercicio(ejercicio) if es_premium else []
    return render_template(
        "progreso_ejercicio.html", ejercicio=ejercicio, historial=historial, es_premium=es_premium
    )
