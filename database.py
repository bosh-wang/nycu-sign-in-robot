import sqlite3


def insert_user(username, pwd, email, school_id):
    db_path = "../database/signinrobot.db"  
    
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO users (username, pwd, email, school_id)
            VALUES (?, ?, ?, ?);
        """, (username, pwd, email, school_id))

        conn.commit()
        print("User inserted successfully!")

    except sqlite3.IntegrityError as e:
        print(f"Error inserting user: {e}")

    except Exception as e:
        print(f"Unexpected error: {e}")
    conn.close()


def insert_schedule(school_id, schedule, start_time, end_time):
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





