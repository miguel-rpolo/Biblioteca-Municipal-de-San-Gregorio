from flask import Blueprint, request, redirect, url_for, render_template, flash
from flask_login import login_required, current_user
from sqlalchemy import func
from app.extensions import db
from app.models.activity import Activity
from app.models.enrollment import Enrollment
from datetime import datetime


activities_bp = Blueprint("activities", __name__, url_prefix="/activities")


# ==============================
# LISTAR ACTIVIDADES
# ==============================
@activities_bp.route("/")
def index():
    # Only show published activities to regular users, admins can see all
    if current_user.is_authenticated and current_user.role == 'admin':
        activities = Activity.query.all()
    else:
        activities = Activity.query.filter(Activity.status != 'borrador').all()

    result = []
    for activity in activities:
        enrolled_count = db.session.query(func.count(Enrollment.id)) \
            .filter_by(activity_id=activity.id) \
            .scalar()

        available_slots = activity.max_slots - enrolled_count

        # Check if current user is enrolled
        user_enrolled = False
        if current_user.is_authenticated:
            user_enrolled = Enrollment.query.filter_by(
                activity_id=activity.id,
                user_id=current_user.id
            ).first() is not None

        result.append({
            "id": activity.id,
            "title": activity.title,
            "date": activity.date,
            "status": activity.status,
            "available_slots": available_slots,
            "user_enrolled": user_enrolled
        })

    return render_template("activities.html", activities=result)


# ==============================
# CREAR ACTIVIDAD
# ==============================
@activities_bp.route("/create", methods=["POST"])
@login_required
def create_activity():
    title = request.form.get("title")
    description = request.form.get("description")
    activity_type = request.form.get("type")
    date = request.form.get("date")
    time = request.form.get("time")
    duration = request.form.get("duration")
    max_slots = request.form.get("max_slots")

    if not title or not date or not max_slots:
        return "Datos incompletos", 400

    # Convert date string to date object
    date_obj = datetime.strptime(date, '%Y-%m-%d').date() if date else None

    activity = Activity(
        title=title,
        description=description,
        type=activity_type,
        date=date_obj,
        time=time,
        duration=int(duration) if duration else None,
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
@login_required
def enroll(activity_id):
    """Enroll the currently logged-in user in an activity"""
    activity = Activity.query.get_or_404(activity_id)

    # Use current user's data
    name = current_user.name if current_user.name else current_user.username
    email = current_user.email if current_user.email else f"{current_user.username}@biblioteca.com"
    phone = current_user.phone if current_user.phone else ""

    # ✅ Evitar duplicidad - check by user_id
    existing = Enrollment.query.filter_by(
        activity_id=activity_id,
        user_id=current_user.id
    ).first()

    if existing:
        flash("Ya estás inscrito en esta actividad", "warning")
        return redirect(url_for("activities.index"))

    # ✅ Control automático de plazas
    enrolled_count = db.session.query(func.count(Enrollment.id)) \
        .filter_by(activity_id=activity_id) \
        .scalar()

    if enrolled_count >= activity.max_slots:
        flash("No hay plazas disponibles", "error")
        return redirect(url_for("activities.index"))

    # Create enrollment linked to user account
    enrollment = Enrollment(
        user_name=name,
        email=email,
        phone=phone,
        activity_id=activity_id,
        user_id=current_user.id
    )

    db.session.add(enrollment)
    db.session.commit()

    flash(f"Te has inscrito correctamente en: {activity.title}", "success")
    return redirect(url_for("activities.index"))


# ==============================
# DESAPUNTARSE DE ACTIVIDAD
# ==============================
@activities_bp.route("/<int:activity_id>/unenroll", methods=["POST"])
@login_required
def unenroll(activity_id):
    """Unenroll the currently logged-in user from an activity"""
    enrollment = Enrollment.query.filter_by(
        activity_id=activity_id,
        user_id=current_user.id
    ).first()
    
    if not enrollment:
        flash("No estás inscrito en esta actividad", "warning")
        return redirect(url_for("activities.index"))
    
    activity_title = enrollment.activity.title
    db.session.delete(enrollment)
    db.session.commit()
    
    flash(f"Te has desapuntado correctamente de: {activity_title}", "success")
    return redirect(url_for("activities.index"))


@activities_bp.route("/new", methods=["GET", "POST"])
@login_required
def new_activity():
    if request.method == "POST":
        title = request.form.get("title")
        description = request.form.get("description")
        date = request.form.get("date")
        max_slots = request.form.get("max_slots")

        # Convert date string to date object
        date_obj = datetime.strptime(date, '%Y-%m-%d').date() if date else None

        activity = Activity(
            title=title,
            description=description,
            date=date_obj,
            max_slots=int(max_slots),
            status="borrador"
        )

        db.session.add(activity)
        db.session.commit()

        return redirect(url_for("activities.index"))

    return render_template("create_activity.html")
