from flask import Blueprint, request, redirect, url_for, render_template
from flask_login import login_required
from sqlalchemy import func
from app.extensions import db
from app.models.activity import Activity
from app.models.enrollment import Enrollment


activities_bp = Blueprint("activities", __name__, url_prefix="/activities")


# ==============================
# LISTAR ACTIVIDADES
# ==============================
@activities_bp.route("/")
def index():
    activities = Activity.query.all()

    result = []
    for activity in activities:
        enrolled_count = db.session.query(func.count(Enrollment.id)) \
            .filter_by(activity_id=activity.id) \
            .scalar()

        available_slots = activity.max_slots - enrolled_count

        result.append({
            "id": activity.id,
            "title": activity.title,
            "date": activity.date,
            "status": activity.status,
            "available_slots": available_slots
        })

    return render_template("activities.html", activities=result)


# ==============================
# CREAR ACTIVIDAD (PMV)
# ==============================
@activities_bp.route("/create", methods=["POST"])
@login_required
def create_activity():
    title = request.form.get("title")
    description = request.form.get("description")
    date = request.form.get("date")
    max_slots = request.form.get("max_slots")

    if not title or not date or not max_slots:
        return "Datos incompletos", 400

    activity = Activity(
        title=title,
        description=description,
        date=date,
        max_slots=int(max_slots),
        status="borrador"
    )

    db.session.add(activity)
    db.session.commit()

    return redirect(url_for("activities.index"))


# ==============================
# CAMBIAR ESTADO ACTIVIDAD
# ==============================
@activities_bp.route("/<int:activity_id>/status", methods=["POST"])
@login_required
def change_status(activity_id):
    activity = Activity.query.get_or_404(activity_id)
    new_status = request.form.get("status")

    allowed_states = ["borrador", "abierta", "cerrada", "finalizada"]

    if new_status not in allowed_states:
        return "Estado inválido", 400

    activity.status = new_status
    db.session.commit()

    return redirect(url_for("activities.index"))


# ==============================
# INSCRIPCIÓN CON CONTROL DE PLAZAS
# ==============================
@activities_bp.route("/<int:activity_id>/enroll", methods=["POST"])
def enroll(activity_id):
    activity = Activity.query.get_or_404(activity_id)

    name = request.form.get("name")
    email = request.form.get("email")

    if not name or not email:
        return "Datos incompletos", 400

    # ✅ Evitar duplicidad (email + actividad)
    existing = Enrollment.query.filter_by(
        activity_id=activity_id,
        email=email
    ).first()

    if existing:
        return "Ya estás inscrito en esta actividad", 400

    # ✅ Control automático de plazas
    enrolled_count = db.session.query(func.count(Enrollment.id)) \
        .filter_by(activity_id=activity_id) \
        .scalar()

    if enrolled_count >= activity.max_slots:
        return "No hay plazas disponibles", 400

    enrollment = Enrollment(
        user_name=name,
        email=email,
        activity_id=activity_id
    )

    db.session.add(enrollment)
    db.session.commit()

    return "Inscripción confirmada", 200

@activities_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_activity():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        max_slots = request.form.get("max_slots")

        activity = Activity(
            title=title,
            description=description,
            date=date,
            max_slots=int(max_slots),
            status="borrador"
        )

        db.session.add(activity)
        db.session.commit()

        return redirect(url_for("activities.index"))

    return render_template("create_activity.html")

