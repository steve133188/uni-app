from models.subject import Subject
from utils.validators import validate_email, validate_password
from models.database import Database
from models.student import Student

class StudentController:
    def __init__(self):
        self.database = Database()

    def run(self):
        while True:
            print("\nStudent Subsystem:")
            print("(L) Login")
            print("(R) Register")
            print("(X) Exit")
            choice = input("Enter your choice: ").strip().lower()

            if choice == "l":
                self.login()
            elif choice == "r":
                self.register()
            elif choice == "x":
                print("Exiting Student Subsystem.")
                break
            else:
                print("Invalid choice. Please try again.")

    def login(self):
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()

        student = self.database.get_student_by_email(email)
        if student and student.password == password:
            print(f"Welcome, {student.name}!")
            self.post_login_menu(student)
        else:
            print("Invalid email or password.")

    def register(self):
        name = input("Enter your name: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()

        # Validate email format
        if not validate_email(email) or not validate_password(password):
            print("Invalid email or password format.")
            return

        # Check if the student already exists
        if self.database.get_student_by_email(email):
            print("Student already exists.")
            return

        # Create and save the new student
        student = Student(name, email, password)
        self.database.add_student(student)  # Save the student to the database
        print("Registration successful!")

    def post_login_menu(self, student):
        while True:
            print("\nPost-login Actions:")
            print("(C) Change Password")
            print("(E) Enrol in a Subject")
            print("(R) Remove a Subject")
            print("(S) Show Enrolled Subjects, Marks, Grades")
            print("(X) Exit")
            choice = input("Enter your choice: ").strip().lower()

            if choice == "c":
                new_password = input("Enter new password: ").strip()
                if validate_password(new_password):
                    student.change_password(new_password)
                    students = self.database.load_students()
                    for s in students:
                        if s.id == student.id:
                            s.password = new_password
                            break
                    self.database.save_students(students)
                    print("Password changed successfully.")
                else:
                    print("Invalid password format.")
            elif choice == "e":
                if len(student.subjects) >= 4:
                    print("Cannot enrol in more than 4 subjects.")
                else:
                    subject = Subject()
                    student.enrol(subject)
                    students = self.database.load_students()
                    for s in students:
                        if s.id == student.id:
                            s.subjects = student.subjects
                            break
                    self.database.save_students(students)
                    print(f"Enrolled in subject {subject.id}.")
            elif choice == "r":
                subject_id = input("Enter subject ID to remove: ").strip()
                if student.remove_subject(subject_id):
                    students = self.database.load_students()
                    for s in students:
                        if s.id == student.id:
                            s.subjects = student.subjects
                            break
                    self.database.save_students(students)
                    print(f"Subject {subject_id} removed.")
                else:
                    print("Subject not found.")
            elif choice == "s":
                print("Enrolled Subjects:")
                for subject in student.subjects:
                    print(f"ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}")
                print(f"Average Mark: {student.average_mark():.2f}")
                print(f"Pass Status: {'PASS' if student.is_pass() else 'FAIL'}")
            elif choice == "x":
                print("Exiting post-login menu.")
                break
            else:
                print("Invalid choice. Please try again.")
