"""
Script to populate the database with sample data for testing
"""
from app import create_app
from app.extensions import db
from app.models.user import User
from app.models.activity import Activity
from app.models.enrollment import Enrollment
from datetime import datetime, timedelta

app = create_app()

with app.app_context():
    print("🌱 Seeding database with sample data...")
    
    # Clear existing data
    print("Clearing existing data...")
    Enrollment.query.delete()
    Activity.query.delete()
    User.query.delete()
    db.session.commit()
    
    # Create admin user
    print("Creating users...")
    admin = User(username="admin", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    
    # Create normal user
    normal_user = User(
        username="usuario",
        role="user",
        name="Usuario Normal",
        email="usuario@biblioteca.com",
        phone="666123456"
    )
    normal_user.set_password("usuario123")
    db.session.add(normal_user)
    
    # Create sample activities
    print("Creating sample activities...")
    
    activities = [
        Activity(
            title="Taller de Lectura Rápida",
            description="Aprende técnicas para mejorar tu velocidad de lectura sin perder comprensión. Ideal para estudiantes y profesionales.",
            type="taller",
            date=(datetime.now() + timedelta(days=7)).date(),
            time="18:00",
            duration=90,
            max_slots=25,
            status="abierta"
        ),
        Activity(
            title="Club de Lectura: Clásicos Españoles",
            description="Este mes leemos 'La Regenta' de Leopoldo Alas Clarín. Ven a compartir tus impresiones y debatir.",
            type="club_lectura",
            date=(datetime.now() + timedelta(days=14)).date(),
            time="19:30",
            duration=120,
            max_slots=15,
            status="abierta"
        ),
        Activity(
            title="Cuentacuentos Infantil: Aventuras Mágicas",
            description="Sesión de cuentos para niños de 4 a 8 años. Historias mágicas y divertidas con actividades interactivas.",
            type="infantil",
            date=(datetime.now() + timedelta(days=3)).date(),
            time="17:00",
            duration=60,
            max_slots=30,
            status="abierta"
        ),
        Activity(
            title="Introducción a la Búsqueda Digital",
            description="Aprende a usar catálogos digitales, bases de datos y recursos electrónicos de la biblioteca.",
            type="formativo",
            date=(datetime.now() + timedelta(days=10)).date(),
            time="11:00",
            duration=120,
            max_slots=20,
            status="abierta"
        ),
        Activity(
            title="Presentación: Autores Locales",
            description="Encuentro con autores de San Gregorio. Presentación de nuevas obras y sesión de firmas.",
            type="cultural",
            date=(datetime.now() + timedelta(days=21)).date(),
            time="19:00",
            duration=90,
            max_slots=50,
            status="abierta"
        ),
        Activity(
            title="Taller de Encuadernación (COMPLETO)",
            description="Taller práctico de encuadernación artesanal. Aprende técnicas básicas y crea tu propio cuaderno.",
            type="taller",
            date=(datetime.now() + timedelta(days=12)).date(),
            time="17:30",
            duration=120,
            max_slots=10,
            status="abierta"
        ),
        Activity(
            title="Club de Lectura Juvenil (COMPLETO)",
            description="Sesión especial para jóvenes. Este mes leemos 'El Principito'.",
            type="club_lectura",
            date=(datetime.now() + timedelta(days=5)).date(),
            time="18:00",
            duration=90,
            max_slots=12,
            status="abierta"
        ),
        Activity(
            title="Taller de Escritura Creativa (PASADO)",
            description="Taller completo sobre técnicas de escritura creativa y narrativa.",
            type="taller",
            date=(datetime.now() - timedelta(days=15)).date(),
            time="18:00",
            duration=120,
            max_slots=20,
            status="finalizada"
        ),
        Activity(
            title="Club de Lectura: Novela Histórica (PASADO)",
            description="Sesión sobre 'El Nombre de la Rosa' de Umberto Eco.",
            type="club_lectura",
            date=(datetime.now() - timedelta(days=8)).date(),
            time="19:00",
            duration=90,
            max_slots=15,
            status="finalizada"
        ),
        Activity(
            title="Taller de Poesía (Borrador)",
            description="Taller experimental sobre poesía contemporánea.",
            type="taller",
            date=(datetime.now() + timedelta(days=30)).date(),
            time="18:30",
            duration=90,
            max_slots=15,
            status="borrador"
        ),
    ]
    
    for activity in activities:
        db.session.add(activity)
    
    db.session.commit()
    print(f"✓ Created {len(activities)} activities")
    
    # Create sample enrollments for past activities
    print("Creating sample enrollments...")
    
    past_activities = Activity.query.filter_by(status="finalizada").all()
    
    sample_participants = [
        ("María García López", "maria.garcia@email.com", "666111222"),
        ("Juan Pérez Martínez", "juan.perez@email.com", "666222333"),
        ("Ana Rodríguez Silva", "ana.rodriguez@email.com", "666333444"),
        ("Carlos Fernández Ruiz", "carlos.fernandez@email.com", "666444555"),
        ("Laura Sánchez Gómez", "laura.sanchez@email.com", "666555666"),
        ("Miguel Ángel Torres", "miguel.torres@email.com", "666666777"),
        ("Isabel Martín Díaz", "isabel.martin@email.com", "666777888"),
        ("Francisco López Pérez", "francisco.lopez@email.com", "666888999"),
        ("Carmen Jiménez Ruiz", "carmen.jimenez@email.com", "666999000"),
        ("Antonio González Cruz", "antonio.gonzalez@email.com", "666000111"),
    ]
    
    enrollment_count = 0
    for activity in past_activities:
        # Add enrollments (varying numbers)
        num_enrollments = min(activity.max_slots, len(sample_participants))
        
        for i in range(num_enrollments):
            participant = sample_participants[i % len(sample_participants)]
            enrollment = Enrollment(
                user_name=participant[0],
                email=f"{i}.{participant[1]}",  # Make unique
                phone=participant[2],
                activity_id=activity.id,
                status="confirmada",
                attended=(i < num_enrollments - 2)  # Most attended, some didn't
            )
            db.session.add(enrollment)
            enrollment_count += 1
    
    # Add some enrollments for open activities
    open_activities = Activity.query.filter_by(status="abierta").all()
    
    for activity in open_activities:
        # Fill "COMPLETO" activities completely, others partially
        if "COMPLETO" in activity.title:
            num_enrollments = activity.max_slots  # Fill completely
        else:
            num_enrollments = min(5, activity.max_slots)  # Add 3-5 enrollments
        
        for i in range(num_enrollments):
            participant = sample_participants[i % len(sample_participants)]
            enrollment = Enrollment(
                user_name=participant[0],
                email=f"open.{activity.id}.{i}.{participant[1]}",  # Make unique
                phone=participant[2],
                activity_id=activity.id,
                status="confirmada"
            )
            db.session.add(enrollment)
            enrollment_count += 1
    
    db.session.commit()
    print(f"✓ Created {enrollment_count} enrollments")
    
    print("\n✅ Database seeded successfully!")
    print("\n📊 Summary:")
    print(f"   - Users: {User.query.count()}")
    print(f"   - Activities: {Activity.query.count()}")
    print(f"   - Enrollments: {Enrollment.query.count()}")
    print("\n🔐 Admin credentials:")
    print("   Username: admin")
    print("   Password: admin123")
