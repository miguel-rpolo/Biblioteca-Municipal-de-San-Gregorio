# System Patterns

## Architecture Overview
Flask web application following MVC pattern with:
- **Flask** as web framework
- **SQLAlchemy ORM** for database operations
- **Flask-Login** for authentication and session management
- **Blueprint-based** modular architecture
- **SQLite** database for data persistence
- **Jinja2** templating engine for views
- **Bootstrap 5.3.2** for frontend styling

## Application Structure

### Complete Directory Tree
```
app/
├── __init__.py              # Application factory with create_app()
├── config.py                # Configuration class
├── extensions.py            # Shared Flask extensions (db, login_manager)
├── models/                  # Data models (SQLAlchemy)
│   ├── __init__.py         # Empty module initializer
│   ├── user.py             # User model (admin authentication)
│   ├── activity.py         # Activity model
│   └── enrollment.py       # Enrollment model (many-to-one with Activity)
├── routes/                  # Route blueprints
│   ├── __init__.py         # Empty module initializer
│   ├── auth.py             # Authentication routes (MISSING IMPLEMENTATION)
│   ├── activities.py       # Activity and enrollment routes
│   └── admin.py            # Admin routes (EMPTY FILE)
├── services/                # Business logic layer
│   └── enrollment_service.py  # Service layer (EMPTY FILE)
├── static/                  # Static assets (CSS, JS, images)
│   └── (empty directory)
└── templates/               # Jinja2 HTML templates
    ├── base.html           # Base template with Bootstrap navbar
    ├── login.html          # Login form
    ├── activities.html     # Activity listing and enrollment
    └── create_activity.html # Activity creation form
```

## Core Components

### 1. Application Factory (`app/__init__.py`)
**Pattern**: Factory pattern for application creation

**Key Features**:
- Creates Flask app with instance-relative config
- Initializes extensions (db, login_manager)
- Registers blueprints (auth_bp, activities_bp)
- Creates all database tables on startup
- **TEMPORARY CODE**: Seeds admin user (username: "admin", password: "admin123")

**Critical Issues Detected**:
- Contains malformed temporary initialization code (syntax errors in placement)
- Admin seeding code appears BEFORE app context creation (will fail)
- Code duplication in app creation flow

### 2. Configuration (`app/config.py`)
```python
class Config:
    SECRET_KEY = "dev-key-change-in-production"  # ⚠️ Needs production replacement
    SQLALCHEMY_DATABASE_URI = "sqlite:///../instance/app.db"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
```

### 3. Extensions (`app/extensions.py`)
- **db**: SQLAlchemy instance for ORM operations
- **login_manager**: Flask-Login instance with `login_view="auth.login"`

## Database Models

### User Model (`app/models/user.py`)
**Purpose**: Admin authentication for protected operations

```python
class User(db.Model, UserMixin):
    id: Integer (PK)
    username: String(100), unique=True, nullable=False
    password_hash: String(255), nullable=False
    role: String(50), nullable=False
    
    Methods:
    - set_password(password): Hashes using werkzeug.security
    - check_password(password): Validates against hash
```

**Integration**: Flask-Login UserMixin provides session management methods

### Activity Model (`app/models/activity.py`)
**Purpose**: Represents library activities/events

```python
class Activity(db.Model):
    id: Integer (PK)
    title: String(200), nullable=False
    description: Text (nullable)
    date: Date, nullable=False
    max_slots: Integer, nullable=False
    status: String(50), default="borrador"
```

**Status Workflow**:
```
borrador → abierta → cerrada → finalizada
```

**Missing Relationships**: No relationship defined to Enrollment (should have `enrollments` backref)

### Enrollment Model (`app/models/enrollment.py`)
**Purpose**: Tracks participant enrollments in activities

```python
class Enrollment(db.Model):
    id: Integer (PK)
    user_name: String(200), nullable=False
    email: String(200), nullable=False
    activity_id: Integer, ForeignKey("activity.id"), nullable=False
```

**Business Rules Enforced**:
- Email uniqueness per activity (application-level check)
- Foreign key to Activity
- No explicit relationship defined

## Route Blueprints

### Activities Blueprint (`app/routes/activities.py`)
**URL Prefix**: `/activities`

**Routes Implemented**:

1. **GET /activities/** - `index()`
   - Lists all activities with available slots calculation
   - PUBLIC access
   - Uses SQLAlchemy `func.count()` for enrollment counting
   - Returns: activities list with availability

2. **GET/POST /activities/new** - `new_activity()`
   - Form to create new activity
   - PROTECTED (@login_required)
   - Creates activity in "borrador" status
   - Redirects to index after creation

3. **POST /activities/create** - `create_activity()`
   - Alternative creation endpoint
   - PROTECTED (@login_required)
   - Validates required fields (title, date, max_slots)
   - Returns: 400 on validation error

4. **POST /activities/<id>/status** - `change_status()`
   - Updates activity status
   - PROTECTED (@login_required)
   - Validates against allowed states
   - Returns: 400 on invalid status

5. **POST /activities/<id>/enroll** - `enroll()`
   - Public enrollment endpoint
   - Validates required fields (name, email)
   - **Business Logic**:
     - Checks for duplicate enrollment (email + activity)
     - Validates available slots
     - Automatic enrollment counting
   - Returns: 200/400 with messages

**Key Patterns**:
- Uses `func.count()` for aggregate queries
- `get_or_404()` for safe resource retrieval
- Form data validation before DB operations
- Status-based conditional rendering

### Auth Blueprint (`app/routes/auth.py`)
**Status**: ⚠️ **MISSING IMPLEMENTATION**

**Expected Routes**:
- GET/POST /auth/login - Login form and authentication
- POST /auth/logout - Logout and session cleanup

**Current State**: File exists but contains no blueprint definition or routes

### Admin Blueprint (`app/routes/admin.py`)
**Status**: ⚠️ **EMPTY FILE**

## Templates

### Base Template (`app/templates/base.html`)
**Purpose**: Layout wrapper for all pages

**Features**:
- Bootstrap 5.3.2 CDN integration
- Dark navbar with site branding
- Flash message display with categories
- Content block for page-specific content

**Issue Detected**: Duplicate `<div class="container">` blocks (one with flash messages, one empty)

### Login Template (`app/templates/login.html`)
**Extends**: base.html

**Features**:
- Centered login form
- Username and password fields
- Bootstrap form styling
- POST method form submission

### Activities Template (`app/templates/activities.html`)
**Extends**: base.html

**Features**:
- Activity listing in table format
- "Nueva actividad" button (links to create form)
- Enrollment form inline per activity
- Conditional enrollment display:
  - Shows form only if status="abierta" AND available_slots > 0
  - Otherwise shows "No disponible"

**Columns Displayed**:
- Title, Date, Status, Available slots, Enrollment form

### Create Activity Template (`app/templates/create_activity.html`)
**Extends**: base.html

**Features**:
- Form with fields: title, description, date, max_slots
- Bootstrap form styling
- POST method to create activity
- Required field validation (HTML5)

## Critical Implementation Patterns

### 1. Enrollment Control Logic
**Location**: `app/routes/activities.py::enroll()`

**Protection Mechanisms**:
```python
# Duplicate prevention
existing = Enrollment.query.filter_by(
    activity_id=activity_id,
    email=email
).first()

# Slot availability check
enrolled_count = db.session.query(func.count(Enrollment.id))\
    .filter_by(activity_id=activity_id)\
    .scalar()
    
if enrolled_count >= activity.max_slots:
    return "No hay plazas disponibles", 400
```

**Potential Race Condition**: No database-level uniqueness constraint on (email, activity_id)

### 2. Activity Status Management
**Allowed Transitions**: Any status can change to any other (no workflow enforcement)

**Allowed States**:
- `borrador`: Draft, not visible for enrollment
- `abierta`: Open for enrollment
- `cerrada`: Closed, enrollment disabled
- `finalizada`: Completed activity

### 3. Authentication Flow
**Implementation Status**: INCOMPLETE

**Expected Flow**:
1. User visits protected route
2. @login_required decorator redirects to `auth.login`
3. Login form validates credentials
4. Flask-Login creates session
5. User redirected to original destination

**Current Gap**: auth.login route not implemented

### 4. Slot Availability Calculation
**Pattern**: Computed on-demand (not cached)

**Query Pattern**:
```python
enrolled_count = db.session.query(func.count(Enrollment.id))\
    .filter_by(activity_id=activity_id)\
    .scalar()
    
available_slots = activity.max_slots - enrolled_count
```

**Performance Consideration**: N+1 query problem in activity listing (executes count for each activity)

## Technical Debt & Missing Features

### High Priority Issues
1. **Missing auth.py implementation**: Login/logout routes not implemented
2. **Broken __init__.py**: Syntax errors in temporary admin seeding code
3. **No relationship mappings**: Models lack SQLAlchemy relationships
4. **Race condition risk**: Enrollment slot checking not atomic
5. **Duplicate container**: base.html has redundant container divs

### Medium Priority
1. **Empty service layer**: enrollment_service.py not utilized
2. **Empty admin.py**: Admin routes not implemented
3. **N+1 query problem**: Activity listing inefficient
4. **No unique constraint**: (email, activity_id) should be DB-enforced
5. **Production secret key**: Still using dev key

### Low Priority
1. **Empty static directory**: No custom CSS/JS
2. **No error handling**: Forms don't show validation errors properly
3. **No pagination**: Activity listing unbounded
4. **Missing timestamps**: Created/updated tracking not implemented

## Security Considerations

### Currently Implemented
- Password hashing with werkzeug
- Flask-Login session management
- @login_required decorator for protected routes
- CSRF protection (implicit via Flask-WTF if used)

### Security Gaps
- Dev secret key in use
- No rate limiting on enrollment endpoint
- No email validation beyond HTML5
- No session timeout configuration
- No HTTPS enforcement mechanism

## Extension Points

### Planned Service Layer
`app/services/enrollment_service.py` exists but is empty. Intended pattern:
- Move business logic from routes to services
- Centralize enrollment validation
- Enable transaction management
- Facilitate testing

### Admin Routes
`app/routes/admin.py` exists but is empty. Intended features:
- Activity management dashboard
- Enrollment viewing/management
- User management
- System configuration

## Database Considerations

### Current Schema
- No indexes defined beyond primary keys
- No foreign key constraints at DB level (SQLAlchemy handles ORM-level)
- No cascade delete rules defined
- No check constraints

### Recommended Indexes
```sql
CREATE INDEX idx_enrollment_activity ON enrollment(activity_id);
CREATE INDEX idx_enrollment_email ON enrollment(email);
CREATE UNIQUE INDEX idx_enrollment_unique ON enrollment(activity_id, email);
CREATE INDEX idx_activity_status ON activity(status);
CREATE INDEX idx_activity_date ON activity(date);
```

## Development Workflow

### Application Startup
1. `run.py` calls `create_app()` from `app/__init__.py`
2. App factory initializes configuration and extensions
3. Blueprints registered
4. `db.create_all()` ensures tables exist
5. Temporary admin user seeded (if not exists)
6. Flask development server starts

### Database Initialization
- Uses SQLite file at `instance/app.db`
- Tables auto-created on first run
- No migration system (Flask-Migrate not configured)
- Schema changes require manual DB deletion/recreation
