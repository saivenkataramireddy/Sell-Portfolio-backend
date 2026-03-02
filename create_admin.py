import sys
import os

# Add the parent directory to sys.path to allow importing from 'backend'
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import SessionLocal
from backend.models import Admin
from backend.auth import get_password_hash

def create_admin(email, password):
    db = SessionLocal()
    try:
        # Check if admin already exists
        existing_admin = db.query(Admin).filter(Admin.email == email).first()
        if existing_admin:
            print(f"Admin with email {email} already exists.")
            return

        hashed_password = get_password_hash(password)
        new_admin = Admin(email=email, hashed_password=hashed_password)
        db.add(new_admin)
        db.commit()
        print(f"Admin {email} created successfully!")
    except Exception as e:
        print(f"Error creating admin: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python create_admin.py <email> <password>")
    else:
        create_admin(sys.argv[1], sys.argv[2])
