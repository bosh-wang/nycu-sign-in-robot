import sqlite3

def init_db():

    script = '''
        CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        pwd TEXT NOT NULL, 
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );

        CREATE TABLE IF NOT EXISTS schedules (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        email TEXT NOT NULL, 
        password TEXT NOT NULL,
        school_id TEXT NOT NULL,
        schedule_from DATE NOT NULL, 
        schedule_to DATE NOT NULL, 
        start_time TIME NOT NULL, 
        end_time TIME NOT NULL, 
        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        );

    '''

    conn = sqlite3.connect('./database/signinrobot.db')  
    conn.executescript(script)
    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
