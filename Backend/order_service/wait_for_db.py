import time
import pymysql
import os


DB_HOST = os.getenv("DB_HOST")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_NAME = os.getenv("DB_NAME")


while True:
    try:
        conn = pymysql.connect(
            host=DB_HOST,
            user=DB_USER,
            password=DB_PASS,
            database=DB_NAME,
            port=3306
        )

        conn.close()
        print("✅ MySQL is ready!")
        break

    except:
        print("⏳ Waiting for MySQL...")
        time.sleep(3)
