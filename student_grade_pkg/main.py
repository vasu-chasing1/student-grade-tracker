from student_grade_pkg import create_database, StudentManager, GradeManager

create_database()

student_mgr = StudentManager()
grade_mgr = GradeManager()

student_mgr.add_student('S001', 'Raj kumar')
student_mgr.add_student('S002', 'Priya Singh')

grade_mgr.add_grades('S001', 'Maths', 'Test', 85, 1)
grade_mgr.add_grades('S001', 'English', 'Test', 78, 1)


print("S001 Grades: ", grade_mgr.get_student_grades('S001'))
print("S001 Grades: ", grade_mgr.get_average('S001'))
print("S001 Grades: ", grade_mgr.get_by_semester('S001',1))
