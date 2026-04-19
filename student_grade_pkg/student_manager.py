import sqlite3
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class StudentManager:
    def __init__(self, db_name='grades.db'):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)

    def add_student(self, student_id, name):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('INSERT INTO students (student_id, name) VALUES (?, ?)', (student_id, name))
            conn.commit()
            conn.close()
            logging.info(f"Student {name} added successfully with ID {student_id}")
        except sqlite3.IntegrityError:
            logging.error(f"Student with ID {student_id} already exists")
        except Exception as e:
            logging.error(f"Error adding student: {e}")

    def get_student(self, student_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students WHERE student_id = ?', (student_id,))
            student = cursor.fetchone()
            conn.close()
            return student
        except Exception as e:
            logging.error(f"Error fetching student: {e}")
            return None

    def get_all_students(self):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM students')
            students = cursor.fetchall()
            conn.close()
            return students
        except Exception as e:
            logging.error(f"Error fetching all students: {e}")
            return []

    def update_student(self, student_id, name):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('UPDATE students SET name = ? WHERE student_id = ?', (name, student_id))
            conn.commit()
            conn.close()
            logging.info(f"Student {student_id} updated successfully")
        except Exception as e:
            logging.error(f"Error updating student: {e}")

    def delete_student(self, student_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('DELETE FROM students WHERE student_id = ?', (student_id,))
            conn.commit()
            conn.close()
            logging.info(f"Student {student_id} deleted successfully")
        except Exception as e:
            logging.error(f"Error deleting student: {e}")

def add_grade(self, student_id, subject, marks):
    try:
        conn = sqlite3.connect(self.db_name)
        cursor = conn.cursor()
        cursor.execute('''
                       INSERT INTO grades(student_id, subject, marks))
                       VALUES (?,?,?)''',(student_id, subject, marks))
        conn.commit()
        conn.close()
        logging.info(f"Grade added for {student_id} in {subject}: {marks}")

    except Exception as e:
        logging.error(f"Error adding grade: {e}")

        