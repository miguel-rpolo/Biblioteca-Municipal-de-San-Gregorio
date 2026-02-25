from flask import Flask
from .config import Config
from .extensions import db, login_manager


def create_app():
#TEMP________
    with app.app_context():
    db.create_all()

    from app.models.user import User

    if not User.query.filter_by(username="admin").first():
        admin = User(username="admin", role="admin")
        admin.set_password("admin123")
        db.session.add(admin)
        db.session.commit()
#TEMP^^
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_object(Config)

    db.init_app(app)
    login_manager.init_app(app)

    from app.models.user import User

    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    from .routes.auth import auth_bp
    from .routes.activities import activities_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(activities_bp)

    with app.app_context():
        db.create_all()

    return app
