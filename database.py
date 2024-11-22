import mysql.connector
import sys

# Connect to MariaDB Platform
try:
    conn = mysql.connector.connect(
        user="root",
        password="root",
        host="localhost",
        port=3306,
        database="user"

    )
except mysel.connector.Error as e:
    print(f"Error connecting to MariaDB Platform: {e}")
    sys.exit(1)

# Get Cursor
cur = conn.cursor()