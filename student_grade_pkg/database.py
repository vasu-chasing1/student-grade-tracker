import sqlite3
import logging
import os
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def create_database():
    db_path = os.path.join(os.path.dirname(__file__),'grades.db')
    try:
        conn = sqlite3.connect(db_path)
        cursor = conn.cursor()
        cursor.execute('''
                   CREATE TABLE IF NOT EXISTS students(
                   student_id TEXT PRIMARY KEY,
                   name TEXT NOT NULL
                   )
                   ''')
        cursor.execute('''
                       CREATE TABLE IF NOT EXISTS grades(
                       id INTEGER PRIMARY KEY AUTOINCREMENT,
                       student_id TEXT NOT NULL,
                       subject TEXT NOT NULL,
                       grade_type TEXT NOT NULL,
                       grade_value INTEGER NOT NULL,
                       semester INTEGER NOT NULL,
                       FOREIGN KEY (student_id) REFERENCES students(student_id))
                       ''')
        conn.commit()
        conn.close()
        logging.info("Database initialized successfully")

    except Exception as e:
        logging.error(f"Error creating database: {e}")
