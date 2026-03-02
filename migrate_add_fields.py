import sqlite3
import os

# Database path
DB_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "portfolio.db"))

def migrate():
    print(f"Connecting to database at: {DB_PATH}")
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    try:
        # Add description column
        print("Adding description column...")
        cursor.execute("ALTER TABLE admins ADD COLUMN description TEXT")
    except sqlite3.OperationalError:
        print("description column already exists or table not found.")

    try:
        # Add linkedin_url column
        print("Adding linkedin_url column...")
        cursor.execute("ALTER TABLE admins ADD COLUMN linkedin_url VARCHAR(500)")
    except sqlite3.OperationalError:
        print("linkedin_url column already exists.")

    try:
        # Add github_url column
        print("Adding github_url column...")
        cursor.execute("ALTER TABLE admins ADD COLUMN github_url VARCHAR(500)")
    except sqlite3.OperationalError:
        print("github_url column already exists.")
        
    conn.commit()
    conn.close()
    print("Migration completed successfully.")

if __name__ == "__main__":
    migrate()
