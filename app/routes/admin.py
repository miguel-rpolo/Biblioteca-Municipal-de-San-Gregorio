from flask import Blueprint, render_template, request, redirect, url_for, flash, Response
from flask_login import login_required, current_user
from sqlalchemy import func
from app.extensions import db
from app.models.activity import Activity
from app.models.enrollment import Enrollment
from functools import wraps
from datetime import datetime
import csv
from io import StringIO

admin_bp = Blueprint("admin", __name__, url_prefix="/admin")


# ==============================
# DECORADOR DE ADMINISTRADOR
# ==============================
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('No tienes permisos para acceder a esta página', 'error')
            return redirect(url_for('activities.index'))
        return f(*args, **kwargs)
    return decorated_function


# ==============================
# PANEL DE ADMINISTRACIÓN
# ==============================
@admin_bp.route("/")
@login_required
@admin_required
def dashboard():
    """Dashboard principal con resumen de actividades"""
    activities = Activity.query.order_by(Activity.date.desc()).all()
    
    activities_data = []
    for activity in activities:
        enrolled_count = len(activity.enrollments)
        attended_count = sum(1 for e in activity.enrollments if e.attended == True)
        
        activities_data.append({
            'activity': activity,
            'enrolled_count': enrolled_count,
            'attended_count': attended_count,
            'available_slots': activity.max_slots - enrolled_count
        })
    
    return render_template("admin/dashboard.html", activities_data=activities_data)


# ==============================
# VER INSCRITOS DE UNA ACTIVIDAD
# ==============================
@admin_bp.route("/activity/<int:activity_id>/enrollments")
@login_required
@admin_required
def view_enrollments(activity_id):
    """Ver lista de inscritos en una actividad"""
    activity = Activity.query.get_or_404(activity_id)
    enrollments = Enrollment.query.filter_by(activity_id=activity_id).order_by(Enrollment.enrollment_date).all()
    
    return render_template("admin/enrollments.html", activity=activity, enrollments=enrollments)


# ==============================
# MARCAR ASISTENCIA
# ==============================
@admin_bp.route("/enrollment/<int:enrollment_id>/attendance", methods=["POST"])
@login_required
@admin_required
def mark_attendance(enrollment_id):
    """Marcar asistencia o inasistencia"""
    enrollment = Enrollment.query.get_or_404(enrollment_id)
    attended = request.form.get("attended")
    
    if attended == "true":
        enrollment.attended = True
    elif attended == "false":
        enrollment.attended = False
    else:
        enrollment.attended = None
    
    db.session.commit()
    flash("Asistencia actualizada correctamente", "success")
    
    return redirect(url_for("admin.view_enrollments", activity_id=enrollment.activity_id))


# ==============================
# EDITAR ACTIVIDAD
# ==============================
@admin_bp.route("/activity/<int:activity_id>/edit", methods=["GET", "POST"])
@login_required
@admin_required
def edit_activity(activity_id):
    """Editar detalles de una actividad"""
    activity = Activity.query.get_or_404(activity_id)
    
    if request.method == "POST":
        activity.title = request.form.get("title")
        activity.description = request.form.get("description")
        activity.type = request.form.get("type")
        
        # Convert date string to date object
        date_str = request.form.get("date")
        if date_str:
            activity.date = datetime.strptime(date_str, '%Y-%m-%d').date()
        
        activity.time = request.form.get("time")
        duration = request.form.get("duration")
        activity.duration = int(duration) if duration else None
        activity.max_slots = int(request.form.get("max_slots"))
        activity.status = request.form.get("status")
        
        db.session.commit()
        flash("Actividad actualizada correctamente", "success")
        return redirect(url_for("admin.dashboard"))
    
    return render_template("admin/edit_activity.html", activity=activity)


# ==============================
# INSCRIPCIÓN INTERNA (PRESENCIAL)
# ==============================
@admin_bp.route("/activity/<int:activity_id>/enroll", methods=["GET", "POST"])
@login_required
@admin_required
def internal_enrollment(activity_id):
    """Inscripción interna por parte del personal administrativo"""
    activity = Activity.query.get_or_404(activity_id)
    
    if request.method == "POST":
        name = request.form.get("name")
        email = request.form.get("email")
        phone = request.form.get("phone")
        
        if not name or not email:
            flash("Nombre y email son obligatorios", "error")
            return redirect(url_for("admin.internal_enrollment", activity_id=activity_id))
        
        # Check for duplicates
        existing = Enrollment.query.filter_by(activity_id=activity_id, email=email).first()
        if existing:
            flash("Esta persona ya está inscrita en la actividad", "error")
            return redirect(url_for("admin.internal_enrollment", activity_id=activity_id))
        
        # Check available slots
        enrolled_count = len(activity.enrollments)
        if enrolled_count >= activity.max_slots:
            flash("No hay plazas disponibles", "error")
            return redirect(url_for("admin.internal_enrollment", activity_id=activity_id))
        
        enrollment = Enrollment(
            user_name=name,
            email=email,
            phone=phone,
            activity_id=activity_id
        )
        
        db.session.add(enrollment)
        db.session.commit()
        
        flash("Inscripción realizada correctamente", "success")
        return redirect(url_for("admin.view_enrollments", activity_id=activity_id))
    
    # Get recent participants for quick selection
    recent_emails = db.session.query(Enrollment.email, Enrollment.user_name, Enrollment.phone)\
        .distinct(Enrollment.email)\
        .order_by(Enrollment.email, Enrollment.created_at.desc())\
        .limit(20)\
        .all()
    
    return render_template("admin/internal_enrollment.html", activity=activity, recent_participants=recent_emails)


# ==============================
# EXPORTAR INSCRITOS A CSV
# ==============================
@admin_bp.route("/activity/<int:activity_id>/export")
@login_required
@admin_required
def export_enrollments(activity_id):
    """Exportar lista de inscritos a CSV"""
    activity = Activity.query.get_or_404(activity_id)
    enrollments = Enrollment.query.filter_by(activity_id=activity_id).all()
    
    # Create CSV in memory
    si = StringIO()
    writer = csv.writer(si)
    
    # Header
    writer.writerow(['Nombre', 'Email', 'Teléfono', 'Fecha de inscripción', 'Estado', 'Asistencia'])
    
    # Data
    for e in enrollments:
        attended_str = 'Asistió' if e.attended == True else ('No asistió' if e.attended == False else 'Pendiente')
        writer.writerow([
            e.user_name,
            e.email,
            e.phone or '',
            e.enrollment_date.strftime('%Y-%m-%d %H:%M') if e.enrollment_date else '',
            e.status,
            attended_str
        ])
    
    output = si.getvalue()
    si.close()
    
    # Return as downloadable file
    return Response(
        output,
        mimetype="text/csv",
        headers={"Content-Disposition": f"attachment;filename=inscritos_{activity.title.replace(' ', '_')}.csv"}
    )


# ==============================
# ELIMINAR ACTIVIDAD
# ==============================
@admin_bp.route("/activity/<int:activity_id>/delete", methods=["POST"])
@login_required
@admin_required
def delete_activity(activity_id):
    """Eliminar una actividad y todas sus inscripciones"""
    activity = Activity.query.get_or_404(activity_id)
    
    # Las inscripciones se eliminan automáticamente por cascade
    db.session.delete(activity)
    db.session.commit()
    
    flash(f"Actividad '{activity.title}' eliminada correctamente", "success")
    return redirect(url_for("admin.dashboard"))


# ==============================
# INFORMES BÁSICOS
# ==============================
@admin_bp.route("/reports")
@login_required
@admin_required
def reports():
    """Vista de informes básicos"""
    
    # Total de actividades por estado
    activities_by_status = db.session.query(
        Activity.status, 
        func.count(Activity.id)
    ).group_by(Activity.status).all()
    
    # Actividades con más inscripciones
    top_activities = db.session.query(
        Activity,
        func.count(Enrollment.id).label('enrollment_count')
    ).outerjoin(Enrollment).group_by(Activity.id).order_by(func.count(Enrollment.id).desc()).limit(10).all()
    
    # Estadísticas generales
    total_activities = Activity.query.count()
    total_enrollments = Enrollment.query.count()
    total_attended = Enrollment.query.filter_by(attended=True).count()
    
    return render_template("admin/reports.html", 
                         activities_by_status=activities_by_status,
                         top_activities=top_activities,
                         total_activities=total_activities,
                         total_enrollments=total_enrollments,
                         total_attended=total_attended)
