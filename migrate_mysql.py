import os
import pymysql
from dotenv import load_dotenv

load_dotenv()

conn = pymysql.connect(
    host=os.getenv("DB_HOST"),
    port=int(os.getenv("DB_PORT")),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME"),
    ssl={"ssl": True}
)

try:
    with conn.cursor() as cursor:
        print("Adding description column...")
        try:
            cursor.execute("ALTER TABLE admins ADD COLUMN description TEXT")
        except Exception as e:
            print(f"Description error: {e}")

        print("Adding linkedin_url column...")
        try:
            cursor.execute("ALTER TABLE admins ADD COLUMN linkedin_url VARCHAR(500)")
        except Exception as e:
            print(f"Linkedin error: {e}")

        print("Adding github_url column...")
        try:
            cursor.execute("ALTER TABLE admins ADD COLUMN github_url VARCHAR(500)")
        except Exception as e:
            print(f"Github error: {e}")
            
    conn.commit()
    print("Migration successful.")
finally:
    conn.close()
