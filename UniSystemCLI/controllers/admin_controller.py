from UniSystemCLI.models.database import Database
from UniSystemCLI.models.student import Student
from UniSystemCLI.utils.console import console


class AdminController:
    def __init__(self):
        self.database = Database()

    def run(self):
        while True:
            console(
                "\nAdmin Subsystem:\n(C) Clear Database\n(G) Group Students by Grade\n"
                +"(P) Partition Students into PASS/FAIL"
                +"\n(R) Remove a Student by ID\n(S) Show All Students\n(X) Exit"
            )
            choice = input("Enter your choice: ").strip().lower()

            if choice == "c":self.database.clear()
            elif choice == "g":self.group_students_by_grade()
            elif choice == "p":self.partition_students()
            elif choice == "r":
                student_id = input("Enter student ID to remove: ").strip()
                if self.database.remove_student(student_id):console(f"Student {student_id} removed.")
                else:console("Student not found.")
            elif choice == "s":self.show_all_students()
            elif choice == "x":
                console("Exiting Admin Subsystem.")
                break
            else:console("Invalid choice. Please try again.")

    def group_students_by_grade(self):
        students:[Student] = self.database.load_students()
        grades = {}
        for student in students:
            if(len(student.subjects)>0):
                for subject in student.subjects:
                    grades.setdefault(subject.grade, []).append(student)
        for grade, students in grades.items():
            console(f"Grade {grade}: {[student.name for student in students]}")

    def partition_students(self):
        students:[Student] = self.database.load_students()
        passed = [student for student in students if student.is_passed()]
        failed = [student for student in students if not student.is_passed()]
        console("PASS:")
        for student in passed:
            console(f"{student.name} (ID: {student.id})")
        console("FAIL:")
        for student in failed:console(f"{student.name} (ID: {student.id})")

    def show_all_students(self):
        students = self.database.load_students()
        for student in students:
            console(f"ID: {student.id}, Name: {student.name}, Email: {student.email}")
