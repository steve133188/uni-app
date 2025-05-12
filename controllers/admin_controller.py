from models.database import Database

class AdminController:
    def __init__(self):
        self.database = Database()

    def run(self):
        while True:
            print("\nAdmin Subsystem:")
            print("(C) Clear Database")
            print("(G) Group Students by Grade")
            print("(P) Partition Students into PASS/FAIL")
            print("(R) Remove a Student by ID")
            print("(S) Show All Students")
            print("(X) Exit")
            choice = input("Enter your choice: ").strip().lower()

            if choice == "c":
                self.database.clear()
                print("Database cleared.")
            elif choice == "g":
                self.group_students_by_grade()
            elif choice == "p":
                self.partition_students()
            elif choice == "r":
                student_id = input("Enter student ID to remove: ").strip()
                if self.database.remove_student(student_id):
                    print(f"Student {student_id} removed.")
                else:
                    print("Student not found.")
            elif choice == "s":
                self.show_all_students()
            elif choice == "x":
                print("Exiting Admin Subsystem.")
                break
            else:
                print("Invalid choice. Please try again.")

    def group_students_by_grade(self):
        students = self.database.load_students()
        grades = {}
        for student in students:
            for subject in student.subjects:
                grades.setdefault(subject.grade, []).append(student)
        for grade, students in grades.items():
            print(f"Grade {grade}: {[student.name for student in students]}")

    def partition_students(self):
        students = self.database.load_students()
        passed = [student for student in students if student.is_pass()]
        failed = [student for student in students if not student.is_pass()]
        print("PASS:")
        for student in passed:
            print(f"{student.name} (ID: {student.id})")
        print("FAIL:")
        for student in failed:
            print(f"{student.name} (ID: {student.id})")

    def show_all_students(self):
        students = self.database.load_students()
        for student in students:
            print(f"ID: {student.id}, Name: {student.name}, Email: {student.email}")
