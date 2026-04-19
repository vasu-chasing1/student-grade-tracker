import os
import sys

# Add package path
sys.path.insert(0, os.path.dirname(__file__))

from student_grade_pkg import create_database, StudentManager, GradeManager
# Database initialize
create_database()

# Managers
student_mgr = StudentManager()
grade_mgr = GradeManager()

# Add students
student_mgr.add_student('S001', 'Raj Kumar')
student_mgr.add_student('S002', 'Priya Singh')

# Add grades
grade_mgr.add_grades('S001', 'Maths', 'Test', 85, 1)
grade_mgr.add_grades('S001', 'English', 'Test', 78, 1)
grade_mgr.add_grades('S002', 'Maths', 'Test', 92, 1)

# Get student grades
print("S001 Grades:", grade_mgr.get_student_grades('S001'))
print("S001 Average:", grade_mgr.get_average('S001'))
print("S001 Semester 1:", grade_mgr.get_by_semester('S001', 1))