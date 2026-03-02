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
        cursor.execute("SHOW COLUMNS FROM admins")
        columns = cursor.fetchall()
        print("Columns in 'admins' table:")
        for col in columns:
            print(col[0])
finally:
    conn.close()
