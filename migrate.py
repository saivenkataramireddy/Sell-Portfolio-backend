import os
from sqlalchemy import create_engine, text
from database import SQLALCHEMY_DATABASE_URL, ca_path

def migrate():
    print("Connecting to database...")
    engine = create_engine(
        SQLALCHEMY_DATABASE_URL,
        connect_args={
            "ssl": {
                "ca": ca_path
            }
        }
    )
    
    with engine.connect() as connection:
        print("Adding missing columns to 'admins' table...")
        try:
            # Check if columns exist before adding (optional but safer)
            # For simplicity in this environment, we'll try to add them and catch errors if they exist
            queries = [
                "ALTER TABLE admins ADD COLUMN full_name VARCHAR(255) NULL;",
                "ALTER TABLE admins ADD COLUMN bio TEXT NULL;",
                "ALTER TABLE admins ADD COLUMN profile_picture VARCHAR(500) NULL;"
            ]
            
            for query in queries:
                try:
                    connection.execute(text(query))
                    print(f"Executed: {query}")
                except Exception as e:
                    if "Duplicate column name" in str(e):
                        print(f"Column already exists: {query.split(' ')[3]}")
                    else:
                        print(f"Error executing {query}: {e}")
            
            connection.commit()
            print("Migration completed successfully!")
            
        except Exception as e:
            print(f"Migration failed: {e}")

if __name__ == "__main__":
    migrate()
