import sqlite3
import bcrypt



def register(name, email ,pwd):
    db_path = "../database/signinrobot.db"  
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, email, pwd)
            VALUES (?, ?, ?);
        """, (name, email, pwd,))

        conn.commit()
        print("User inserted successfully!")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting user: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
    conn.close()

def insert_schedule():
    db_path = "../database/signinrobot.db"  
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO schedule (school_id, date, time_from, time_to)
            VALUES (?, ?, ?, ?);
        """, (school_id, schedule, start_time, end_time))

        conn.commit()
        print("Schedule inserted successfully!")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting schedule: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
    conn.close()

def get_schedule(school_id, date):
    db_path = "../database/signinrobot.db"  
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            SELECT school_id, date, time_from, time_to FROM schedule
            WHERE school_id = ? AND date = ?;
        """, (school_id, date,))

        data = cursor.fetchall()
        
    except Exception as e:
        print(f"Unexpected error: {e}")

    conn.close()
    return data

def check_login(email, password):
    db_path = "../database/signinrobot.db"

    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute("""
                        SELECT pwd FROM users 
                        WHERE email = ?;
                        """, (email,))
        db_pwd = cursor.fetchone()
    except Exception as e:
        print(f"Unexpedted error: {e}")
    
    conn.close()

    if db_pwd and bcrypt.checkpw(password.encode('utf-8'),  db_pwd[0].encode('utf-8')):
        print("login sucessful!!")
        return True
    else:
        return False


