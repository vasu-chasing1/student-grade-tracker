import sqlite3
import logging 
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class GradeManager:
    def __init__(self, db_name='grades.db'):
        self.db_name = os.path.join(os.path.dirname(__file__), db_name)

    def add_grades(self, student_id, subject, grade_type, grade_value, semester):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                       INSERT INTO grades(student_id, subject, grade_type, grade_value, semester)
                       VALUES (?,?,?,?,?)''',(student_id, subject, grade_type, grade_value, semester))
            conn.commit()
            conn.close()
            logging.info(f"Grade added for {student_id} in {subject}: {grade_value} ({grade_type})")


        except Exception as e:
            logging.error(f"Error adding grade: {e}")
    def get_student_grades(self, student_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('SELECT subject, grade_type, grade_value, semester FROM grades WHERE student_id = ?', (student_id,))
            grades = cursor.fetchall()
            conn.close()
            return grades
        except Exception as e:
            logging.error(f"Error fetching grades: {e}")
            return []
                    

    def get_average(self, student_id):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT AVG(grade_value) FROM grades WHERE student_id = ?''', (student_id,))
            average = cursor.fetchone()
            conn.close()
            return average[0] if average[0] else 0
        except Exception as e:
            logging.error(f"Error calculating average: {e}")
            return 0
    
    def get_by_semester(self, student_id, semester):
        try:
            conn = sqlite3.connect(self.db_name)
            cursor = conn.cursor()
            cursor.execute('''
                           SELECT subject, grade_type, grade_value FROM grades WHERE student_id = ? AND semester = ?''',(student_id, semester))
            grades = cursor.fetchall()
            conn.close()
            return grades
        except Exception as e:
            logging.error(f"Error fetching semester grades: {e}")
            return []
        