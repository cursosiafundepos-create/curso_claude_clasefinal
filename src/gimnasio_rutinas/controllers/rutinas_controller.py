"""Controller: rutas web para consultar y gestionar las rutinas de gimnasio."""

from flask import Blueprint, abort, redirect, render_template, request, url_for

from ..models.dia import DIAS_LABEL, DIAS_VALIDOS, DiaInvalidoError, validar_dia
from ..models.ejercicio import Ejercicio
from ..models.rutina_repository import RutinaRepository

rutinas_bp = Blueprint("rutinas", __name__)
repo = RutinaRepository()


@rutinas_bp.route("/")
def index():
    return redirect(url_for("rutinas.ver_semana"))


@rutinas_bp.route("/semana")
def ver_semana():
    semana = repo.obtener_semana()
    return render_template(
        "semana.html", dias=DIAS_VALIDOS, dias_label=DIAS_LABEL, semana=semana
    )


@rutinas_bp.route("/dia/<dia>")
def ver_dia(dia):
    try:
        ejercicios = repo.obtener_dia(dia)
    except DiaInvalidoError:
        abort(404)
    return render_template(
        "dia.html", dia=dia, dia_label=DIAS_LABEL[dia], ejercicios=ejercicios
    )


@rutinas_bp.route("/dia/<dia>/ejercicios", methods=["POST"])
def agregar_ejercicio(dia):
    try:
        validar_dia(dia)
    except DiaInvalidoError:
        abort(404)
    ejercicio = Ejercicio(
        nombre=request.form["nombre"].strip(),
        series=int(request.form["series"]),
        repeticiones=request.form["repeticiones"].strip(),
        peso=request.form.get("peso", "").strip(),
        notas=request.form.get("notas", "").strip(),
    )
    repo.agregar_ejercicio(dia, ejercicio)
    return redirect(url_for("rutinas.ver_dia", dia=dia))


@rutinas_bp.route("/dia/<dia>/ejercicios/<ejercicio_id>/editar", methods=["POST"])
def editar_ejercicio(dia, ejercicio_id):
    try:
        validar_dia(dia)
    except DiaInvalidoError:
        abort(404)
    repo.editar_ejercicio(
        dia,
        ejercicio_id,
        {
            "nombre": request.form["nombre"].strip(),
            "series": request.form["series"],
            "repeticiones": request.form["repeticiones"].strip(),
            "peso": request.form.get("peso", "").strip(),
            "notas": request.form.get("notas", "").strip(),
        },
    )
    return redirect(url_for("rutinas.ver_dia", dia=dia))


@rutinas_bp.route("/dia/<dia>/ejercicios/<ejercicio_id>/eliminar", methods=["POST"])
def eliminar_ejercicio(dia, ejercicio_id):
    try:
        validar_dia(dia)
    except DiaInvalidoError:
        abort(404)
    repo.eliminar_ejercicio(dia, ejercicio_id)
    return redirect(url_for("rutinas.ver_dia", dia=dia))


@rutinas_bp.route("/dia/<dia>/ejercicios/<ejercicio_id>/mover", methods=["POST"])
def mover_ejercicio(dia, ejercicio_id):
    """Reordena moviendo un ejercicio una posición hacia 'arriba' o 'abajo'."""
    try:
        validar_dia(dia)
    except DiaInvalidoError:
        abort(404)
    direccion = request.form.get("direccion")
    ejercicios = repo.obtener_dia(dia)
    ids = [e.id for e in ejercicios]
    idx = ids.index(ejercicio_id) if ejercicio_id in ids else -1
    if idx != -1:
        if direccion == "arriba" and idx > 0:
            ids[idx - 1], ids[idx] = ids[idx], ids[idx - 1]
        elif direccion == "abajo" and idx < len(ids) - 1:
            ids[idx + 1], ids[idx] = ids[idx], ids[idx + 1]
        repo.reordenar(dia, ids)
    return redirect(url_for("rutinas.ver_dia", dia=dia))
