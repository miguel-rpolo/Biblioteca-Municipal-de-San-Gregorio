# Active Context

## Current Focus
Deep analysis of the `/app` directory completed. Comprehensive documentation of the codebase structure, patterns, and issues has been added to the memory bank.

## Recent Changes
- **Memory Bank Updated**: systemPatterns.md now contains complete application architecture documentation
- **Code Analysis Complete**: All files in app/ directory have been read and analyzed
- **Issues Identified**: Multiple critical bugs and missing implementations discovered

## Critical Issues Discovered

### 1. Broken Application Factory (HIGH PRIORITY)
**File**: `app/__init__.py`
**Problem**: Contains syntax errors in temporary admin seeding code
- Commented-out code block appears BEFORE the app context is created
- Code will fail to execute properly
- Admin user seeding logic is malformed

**Impact**: Application may not start correctly

### 2. Missing Authentication Implementation (HIGH PRIORITY)
**File**: `app/routes/auth.py`
**Problem**: File exists but contains NO authentication routes
- No `auth_bp` blueprint defined
- No login route implementation
- No logout route implementation
- Template `login.html` exists but has no corresponding route to render it

**Impact**: 
- Protected routes (@login_required) will redirect to non-existent route
- Admin cannot log in to create/manage activities
- System is essentially non-functional for admin operations

### 3. Empty Service Layer
**File**: `app/services/enrollment_service.py`
**Status**: Completely empty file
**Impact**: Business logic is in routes instead of service layer (not critical, but poor architecture)

### 4. Empty Admin Routes
**File**: `app/routes/admin.py`
**Status**: Completely empty file
**Impact**: No admin dashboard or management interface

### 5. Template Issue
**File**: `app/templates/base.html`
**Problem**: Duplicate `<div class="container">` blocks
- One container wraps flash messages
- Second empty container block follows immediately
**Impact**: Minor layout issue, redundant HTML

## Application State Assessment

### What Works
✅ Activity model defined correctly
✅ Enrollment model with foreign key relationship
✅ User model with password hashing
✅ Activity listing route (GET /activities/)
✅ Activity creation routes (POST /activities/new and /activities/create)
✅ Enrollment route with business logic (POST /activities/<id>/enroll)
✅ Status change route (POST /activities/<id>/status)
✅ Templates are complete and properly structured
✅ Bootstrap 5.3.2 integrated for styling
✅ Flask-Login configured in extensions

### What's Broken/Missing
❌ Authentication routes not implemented (auth.py empty)
❌ Application factory has syntax errors
❌ No way for admin to actually log in
❌ Service layer not utilized
❌ Admin dashboard not implemented
❌ No database relationships defined in models
❌ No unique constraint on (email, activity_id) in database

## Technical Patterns Observed

### Good Patterns
1. **Blueprint Architecture**: Clean separation between activities and (intended) auth
2. **Model Separation**: Clear model definitions with appropriate fields
3. **Password Security**: Using werkzeug for hashing
4. **Enrollment Business Logic**: Duplicate checking and slot validation
5. **Template Inheritance**: Proper use of base template
6. **Form Validation**: Basic validation before database operations

### Anti-Patterns/Issues
1. **Missing Relationships**: Models don't define SQLAlchemy relationships
2. **N+1 Queries**: Activity listing counts enrollments individually for each activity
3. **Race Conditions**: Slot checking not atomic (no database constraint)
4. **Business Logic in Routes**: Should be in service layer
5. **No Error Handling**: Forms don't display validation errors to users
6. **Duplicate Routes**: Two different endpoints for activity creation (/new and /create)

## Database Schema Insights

### Current Tables
1. **user**: Admin authentication
2. **activity**: Events/activities 
3. **enrollment**: Participant registrations

### Missing Elements
- No indexes on foreign keys
- No unique constraint on (activity_id, email)
- No timestamps (created_at, updated_at)
- No soft delete capability
- No cascade delete rules
- No relationship definitions in ORM models

### Recommended Improvements
- Add unique constraint: `(activity_id, email)`
- Add indexes on commonly queried fields
- Add relationships: `Activity.enrollments`, `Enrollment.activity`
- Add timestamps for audit trail

## Activity Status Workflow

**Current Implementation**:
```
borrador → abierta → cerrada → finalizada
```

**Rules**:
- Only "abierta" activities allow enrollment
- Any status can transition to any other status (no enforcement)
- Status changes require authentication

**Missing**:
- No validation of status transitions (should follow workflow)
- No audit trail of status changes
- No automatic status changes (e.g., auto-close when full)

## Enrollment Logic Flow

**Current Implementation** (`app/routes/activities.py::enroll()`):
1. Validate required fields (name, email)
2. Check for duplicate (email + activity_id)
3. Count current enrollments
4. Verify slots available
5. Create enrollment record
6. Commit to database

**Vulnerabilities**:
- Race condition between check and insert
- No transaction isolation
- Application-level validation only (no DB constraint)

**Recommended Fix**:
```python
# Add to Enrollment model
__table_args__ = (
    db.UniqueConstraint('email', 'activity_id', name='unique_enrollment'),
)
```

## Frontend Observations

### Bootstrap Integration
- Using CDN version 5.3.2
- Dark navbar theme
- Responsive table layouts
- Form styling with Bootstrap classes

### User Experience
- Simple, functional interface
- Inline enrollment forms in activity table
- Flash messages for user feedback (configured but not used)
- No JavaScript (pure server-side rendering)

### Missing UX Features
- No loading indicators
- No client-side validation
- No confirmation dialogs
- No success/error messages displayed
- No pagination for long activity lists

## Next Steps Required

### Immediate Priorities (Blocking)
1. **Fix app/__init__.py**: Remove syntax errors, fix admin seeding
2. **Implement auth.py**: Create login/logout routes with proper authentication
3. **Test authentication flow**: Verify admin can log in and access protected routes

### High Priority (Core Functionality)
4. **Add database constraints**: Unique constraint on (email, activity_id)
5. **Add model relationships**: Define backref relationships
6. **Fix base.html**: Remove duplicate container div
7. **Improve error handling**: Display form validation errors to users

### Medium Priority (Quality)
8. **Implement service layer**: Move business logic from routes
9. **Fix N+1 query**: Use join/eager loading for enrollment counts
10. **Add admin dashboard**: Implement admin.py routes
11. **Add timestamps**: created_at/updated_at to models

### Low Priority (Enhancement)
12. **Add pagination**: For activity listing
13. **Add search/filter**: For activities
14. **Add email validation**: Server-side email format check
15. **Add custom styling**: Use static/css for branding
16. **Add JavaScript**: Client-side enhancements

## Important Project Learnings

### Code Quality
- Project follows Flask best practices overall
- Blueprint structure is well-organized
- Models are simple and focused
- Templates are clean and maintainable

### Architecture Decisions
- **SQLite**: Appropriate for small-scale deployment
- **Server-side rendering**: Simpler, no API needed
- **Bootstrap CDN**: Quick styling without custom CSS
- **Flask-Login**: Standard choice for Flask auth

### Business Logic
- **Slot management**: Automatically calculated, not stored
- **Email-based enrollment**: No user accounts for participants
- **Status workflow**: Admin controls activity lifecycle
- **Public enrollment**: No authentication needed to sign up

## Development Environment

### Technologies
- Python 3.x
- Flask web framework
- SQLAlchemy ORM
- Flask-Login for sessions
- SQLite database
- Jinja2 templates
- Bootstrap 5.3.2 (CDN)

### File Organization
- Clean separation: models, routes, templates
- Instance folder for database file
- Memory bank for documentation
- Docs folder with requirements (PDFs)

### Running the Application
```bash
python run.py
# Expected to start Flask dev server
# Currently WILL FAIL due to auth.py missing implementation
```

## Questions to Consider

1. **Should status transitions be enforced?** Currently any status can change to any other
2. **Should enrollment have waitlist?** When activity is full
3. **Should there be email notifications?** For enrollment confirmation
4. **Should activities auto-close?** When max_slots reached
5. **Should there be enrollment cancellation?** Currently no way to unenroll
6. **Should admin see enrollment list?** Currently no view of who's enrolled
7. **Is role field used?** User model has role but it's not checked anywhere

## Memory Bank Status

### Files Updated This Session
- ✅ **systemPatterns.md**: Complete application architecture documented
- ✅ **activeContext.md**: Current state and issues documented (this file)

### Files To Update Next
- 📝 **progress.md**: Should reflect current implementation status
- 📝 **techContext.md**: May need updates based on findings

### Files Already Complete
- ✅ **projectbrief.md**: Requirements documented
- ✅ **productContext.md**: Business context documented
