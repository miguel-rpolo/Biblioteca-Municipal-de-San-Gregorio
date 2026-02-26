# Technical Context

## Technology Stack

### Backend Framework
**Flask 2.x**
- Micro web framework for Python
- Lightweight and flexible
- Excellent for small to medium applications
- Rich ecosystem of extensions

### Database
**SQLite 3**
- File-based relational database
- Location: `instance/app.db`
- No separate server required
- Perfect for development and small deployments
- ACID compliant
- Supports foreign keys and constraints

**SQLAlchemy 2.x**
- Python SQL toolkit and ORM
- Database abstraction layer
- Model-based data access
- Query building and execution
- Migration support (not configured yet)

### Authentication
**Flask-Login**
- Session management for Flask
- User session handling
- Login/logout functionality
- @login_required decorator
- Remember me functionality
- User loader integration

**Werkzeug Security**
- Password hashing (PBKDF2)
- Secure password comparison
- Part of Flask core dependencies

### Frontend
**Bootstrap 5.3.2**
- CSS framework via CDN
- Responsive grid system
- Pre-styled components
- Dark navbar theme in use
- Form validation styles

**Jinja2**
- Python templating engine
- Built into Flask
- Template inheritance
- Control structures (if, for, etc.)
- Filter support
- Auto-escaping for XSS protection

### Python Version
**Python 3.x** (specific version not specified in requirements)
- Modern Python features available
- Type hints supported (not used in codebase)
- F-strings available

## Dependencies

### Core Dependencies (from requirements.txt)
```
Flask==2.3.2
Flask-SQLAlchemy==3.0.5
Flask-Login==0.6.2
Werkzeug==2.3.6
```

### Implied Dependencies
These are automatically installed as dependencies of the above:
- SQLAlchemy (via Flask-SQLAlchemy)
- Jinja2 (via Flask)
- Click (via Flask - CLI tool)
- ItsDangerous (via Flask - session signing)

### Missing Dependencies
Recommended additions:
- `Flask-WTF` - Form handling and CSRF protection
- `Flask-Migrate` - Database migrations (Alembic wrapper)
- `python-dotenv` - Environment variable management
- `email-validator` - Email validation

## Development Environment

### Project Structure
```
Biblioteca-Municipal-de-San-Gregorio/
├── app/                    # Application package
│   ├── models/            # Database models
│   ├── routes/            # Route blueprints
│   ├── services/          # Business logic (empty)
│   ├── static/            # Static files (empty)
│   ├── templates/         # Jinja2 templates
│   ├── __init__.py        # App factory
│   ├── config.py          # Configuration
│   └── extensions.py      # Shared extensions
├── instance/              # Instance-specific files
│   └── app.db            # SQLite database
├── docs/                  # Documentation (PDFs)
├── memory-bank/           # Project documentation
├── requirements.txt       # Python dependencies
├── run.py                # Application entry point
└── README.md             # Project readme
```

### Configuration Management

**Config Class** (`app/config.py`):
```python
class Config:
    SECRET_KEY = "dev-key-change-in-production"
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

**Environment Variables**:
- `SECRET_KEY`: Should be set via environment in production
- Currently no `.env` file support
- No environment-based configuration switching

### Database Configuration

**Connection String**:
```
sqlite:///../instance/app.db
```
- Relative path from app directory
- Creates `instance/app.db` file
- Auto-creates instance directory if needed

**SQLAlchemy Settings**:
- `SQLALCHEMY_TRACK_MODIFICATIONS = False`: Disables event system overhead
- `SQLALCHEMY_ECHO = False`: No SQL logging (default)

### Application Initialization

**Entry Point** (`run.py`):
```python
from app import create_app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
```

**App Factory** (`app/__init__.py`):
1. Creates Flask instance with instance_relative_config
2. Loads Config object
3. Initializes extensions (db, login_manager)
4. Registers user_loader function
5. Registers blueprints (auth_bp, activities_bp)
6. Creates database tables (db.create_all)
7. Seeds admin user (temporary code)

### Flask Extensions Configuration

**Flask-SQLAlchemy**:
```python
from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()
db.init_app(app)
```

**Flask-Login**:
```python
from flask_login import LoginManager
login_manager = LoginManager()
login_manager.login_view = "auth.login"
login_manager.init_app(app)
```

## Development Tools

### Command Line Interface
**Flask CLI** (built-in):
```bash
flask run              # Start development server
flask shell            # Interactive Python shell with app context
```

**Custom Commands** (not implemented):
- Could add database seeding commands
- Could add admin user creation
- Could add database reset commands

### Database Management
**No migration system configured**
- Schema changes require manual intervention
- Current approach: delete database and recreate
- Recommendation: Add Flask-Migrate

**Manual Management**:
```python
with app.app_context():
    db.create_all()    # Create tables
    db.drop_all()      # Drop all tables (dangerous)
```

## Technical Constraints

### Database Limitations
- **SQLite Concurrency**: Limited write concurrency
  - Only one writer at a time
  - Multiple readers OK
  - May be bottleneck under heavy load
  
- **No Built-in Replication**: Single file, no automatic backup
  
- **Type System**: Flexible typing may cause unexpected behavior
  
- **Foreign Key Support**: Enabled by default in modern SQLite
  - Enforced at database level

### Flask Limitations
- **Single-threaded development server**: Not for production
  - Use Gunicorn/uWSGI for production
  
- **No async support**: Synchronous request handling
  - Each request blocks until complete
  
- **Session Storage**: Server-side sessions in memory
  - Lost on server restart
  - Consider Redis for production

### Security Constraints
- **Secret Key**: Currently hardcoded dev key
  - Must use environment variable in production
  
- **HTTPS**: No enforcement mechanism
  - Should be handled at reverse proxy level
  
- **CSRF Protection**: Not explicitly configured
  - Flask-WTF would provide this

## Development Workflow

### Starting the Application
```bash
# Install dependencies
pip install -r requirements.txt

# Run application
python run.py

# Or using Flask CLI
flask run
```

**Expected Behavior**:
1. Flask starts development server
2. Database file created if doesn't exist
3. Tables auto-created via db.create_all()
4. Admin user seeded (temporary code)
5. Server listens on http://localhost:5000

**Current Issues**:
- Application may fail to start due to auth.py missing implementation
- __init__.py has syntax errors in temporary code

### Database Initialization
**Automatic on First Run**:
```python
with app.app_context():
    db.create_all()
```

**Admin User Seeding** (temporary):
```python
if not User.query.filter_by(username="admin").first():
    admin = User(username="admin", role="admin")
    admin.set_password("admin123")
    db.session.add(admin)
    db.session.commit()
```

**Manual Reset**:
1. Delete `instance/app.db`
2. Restart application
3. Tables and admin user recreated

### Code Organization Patterns

**Blueprint Pattern**:
```python
# In route file
bp = Blueprint("name", __name__, url_prefix="/prefix")

@bp.route("/path")
def view():
    pass

# In __init__.py
app.register_blueprint(bp)
```

**Model Pattern**:
```python
class Model(db.Model):
    __tablename__ = "table_name"  # Optional
    id = db.Column(db.Integer, primary_key=True)
    # ... fields
```

**Extension Pattern**:
```python
# In extensions.py
ext = Extension()

# In __init__.py
ext.init_app(app)
```

## Production Considerations

### Not Production Ready
Current setup is for development only. Production requires:

1. **WSGI Server**:
   - Gunicorn or uWSGI
   - Multiple worker processes
   - Proper timeout configuration

2. **Database**:
   - Consider PostgreSQL for better concurrency
   - Or keep SQLite with read-replica strategy
   - Implement backup strategy

3. **Environment Configuration**:
   - Environment-based config
   - Secure secret key from environment
   - Debug mode disabled
   - Error logging configured

4. **Security Hardening**:
   - HTTPS enforcement
   - CSRF protection (Flask-WTF)
   - Rate limiting
   - Security headers
   - Session configuration

5. **Monitoring**:
   - Application logging
   - Error tracking (Sentry)
   - Performance monitoring
   - Health check endpoint

6. **Deployment**:
   - Containerization (Docker)
   - Process manager (systemd, supervisor)
   - Reverse proxy (nginx)
   - Static file serving

### Recommended Production Stack
```
Internet
  ↓
nginx (reverse proxy, SSL, static files)
  ↓
Gunicorn (WSGI server, 4-8 workers)
  ↓
Flask Application
  ↓
PostgreSQL Database
```

## Testing Infrastructure

### Current State
**No tests implemented**
- No test directory
- No test dependencies
- No test runner configured
- No CI/CD pipeline

### Recommended Testing Setup
```
tests/
├── __init__.py
├── conftest.py           # Pytest fixtures
├── test_models.py        # Model tests
├── test_routes.py        # Route tests
├── test_services.py      # Business logic tests
└── test_integration.py   # End-to-end tests
```

**Testing Dependencies Needed**:
```
pytest==7.4.0
pytest-flask==1.2.0
pytest-cov==4.1.0
factory-boy==3.3.0        # Test fixtures
faker==19.2.0             # Fake data generation
```

## Performance Considerations

### Current Performance Characteristics
- **Small Scale**: Adequate for <100 concurrent users
- **SQLite**: Good for read-heavy workloads
- **N+1 Queries**: Present in activity listing
- **No Caching**: All data fetched from database each request
- **No CDN**: Bootstrap loaded from CDN (good)

### Optimization Opportunities
1. **Eager Loading**: Use SQLAlchemy joinedload/subqueryload
2. **Caching**: Redis for frequently accessed data
3. **Indexing**: Add indexes on foreign keys and commonly filtered fields
4. **Connection Pooling**: SQLAlchemy pool configuration
5. **Static Assets**: Serve via CDN or nginx in production

## Tool Usage Patterns

### Flask-SQLAlchemy Patterns
```python
# Query patterns used
Model.query.all()
Model.query.get(id)
Model.query.get_or_404(id)
Model.query.filter_by(field=value).first()
db.session.query(func.count(Model.id)).scalar()

# Session management
db.session.add(obj)
db.session.commit()
db.session.rollback()  # Not used, but available
```

### Flask-Login Patterns
```python
# Protection
@login_required
def protected_view():
    pass

# User loading
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Access current user
from flask_login import current_user
```

### Jinja2 Patterns Used
```jinja2
{% extends "base.html" %}
{% block content %}{% endblock %}
{% for item in items %}{% endfor %}
{% if condition %}{% endif %}
{{ variable }}
{{ url_for('blueprint.view', param=value) }}
{% with messages = get_flashed_messages() %}{% endwith %}
```

## IDE and Editor Configuration

### VSCode Configuration (Detected)
- Working directory: Long OneDrive path
- Multiple tabs open with project files
- No explicit .vscode configuration found

### Recommended VSCode Extensions
- Python (Microsoft)
- Pylance (Microsoft)
- Python Test Explorer
- SQLite Viewer
- Jinja (wholroyd)
- Better Jinja

### Recommended .vscode/settings.json
```json
{
  "python.linting.enabled": true,
  "python.linting.pylintEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "files.associations": {
    "*.html": "jinja-html"
  }
}
```

## Environment Variables

### Currently Used
- `SECRET_KEY`: Falls back to "dev-key-change-in-production"

### Recommended Variables
```bash
SECRET_KEY=<random-secure-key>
FLASK_APP=run.py
FLASK_ENV=development|production
DATABASE_URL=sqlite:///instance/app.db
DEBUG=True|False
```

### Missing: .env File Support
Recommendation: Add python-dotenv
```python
# In config.py
from dotenv import load_dotenv
load_dotenv()
```

## Version Control Considerations

### Files to Ignore (.gitignore needed)
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/

# Flask
instance/
.webassets-cache

# IDE
.vscode/
.idea/
*.swp
*.swo

# Database
*.db
*.sqlite

# Environment
.env
.env.local

# OS
.DS_Store
Thumbs.db
```

### Currently Tracked
- ✅ Source code (app/)
- ✅ Requirements.txt
- ✅ Run.py
- ✅ Documentation (docs/, memory-bank/)
- ⚠️ Instance directory (should be ignored)
- ⚠️ Database file (should be ignored)
- ⚠️ __pycache__ (should be ignored)
