"""
Migration script to add phone column to enrollments table
"""
from app import create_app
from app.extensions import db

app = create_app()

with app.app_context():
    # Add phone column to enrollments table if it doesn't exist
    try:
        from sqlalchemy import text
        
        # Check if column exists
        result = db.session.execute(text("PRAGMA table_info(enrollment)"))
        columns = [row[1] for row in result]
        
        if 'phone' not in columns:
            print("Adding 'phone' column to enrollment table...")
            db.session.execute(text("ALTER TABLE enrollment ADD COLUMN phone VARCHAR(20)"))
            db.session.commit()
            print("✓ Migration completed successfully!")
        else:
            print("✓ 'phone' column already exists. No migration needed.")
            
    except Exception as e:
        print(f"✗ Migration failed: {e}")
        db.session.rollback()
