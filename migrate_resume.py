import pymysql
import os
from dotenv import load_dotenv

load_dotenv("backend/.env")

def migrate():
    connection = pymysql.connect(
        host=os.getenv("DB_HOST"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME"),
        port=int(os.getenv("DB_PORT")),
        ssl={"ca": "backend/ca.pem"}
    )
    
    try:
        with connection.cursor() as cursor:
            # Check if columns exist
            cursor.execute("DESCRIBE admins")
            columns = [col[0] for col in cursor.fetchall()]
            
            if "resume_url" not in columns:
                print("Adding resume_url column...")
                cursor.execute("ALTER TABLE admins ADD COLUMN resume_url VARCHAR(500) NULL")
            
            connection.commit()
            print("Migration successful")
    finally:
        connection.close()

if __name__ == "__main__":
    migrate()
