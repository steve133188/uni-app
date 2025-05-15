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
                # Show available subjects
                subjects = self.database.load_subjects()
                if not subjects:
                    print("No subjects available for enrollment.")
                    continue
                    
                print("\nAvailable Subjects:")
                for i, subject in enumerate(subjects):
                    print(f"{i+1}. {subject.code}: {subject.name}")
                
                try:
                    choice = int(input("\nEnter subject number to enroll (0 to cancel): "))
                    if choice == 0:
                        continue
                    if choice < 1 or choice > len(subjects):
                        print("Invalid selection.")
                        continue
                        
                    selected_subject = subjects[choice-1]
                    
                    # Create enrollment
                    from models.enrollment import Enrollment
                    enrollment = Enrollment(student.id, selected_subject.id)
                    
                    # Add to database
                    result, message = self.database.add_enrollment(enrollment)
                    print(message)
                except ValueError:
                    print("Please enter a valid number.")
                except Exception as e:
                    print(f"Error: {str(e)}")
                    
            elif choice == "r":
                # Show enrolled subjects
                enrollments = self.database.get_enrollments_by_student_id(student.id)
                if not enrollments:
                    print("You are not enrolled in any subjects.")
                    continue
                    
                print("\nYour Enrollments:")
                for i, enrollment in enumerate(enrollments):
                    subject = self.database.get_subject_by_id(enrollment.subject_id)
                    if subject:
                        print(f"{i+1}. {subject.code}: {subject.name} - Mark: {enrollment.mark}, Grade: {enrollment.grade}")
                
                try:
                    choice = int(input("\nEnter enrollment number to remove (0 to cancel): "))
                    if choice == 0:
                        continue
                    if choice < 1 or choice > len(enrollments):
                        print("Invalid selection.")
                        continue
                        
                    selected_enrollment = enrollments[choice-1]
                    
                    # Remove from database
                    if self.database.remove_enrollment(student.id, selected_enrollment.subject_id):
                        print("Successfully unenrolled from subject.")
                    else:
                        print("Failed to unenroll from subject.")
                except ValueError:
                    print("Please enter a valid number.")
                except Exception as e:
                    print(f"Error: {str(e)}")
            elif choice == "s":
                # Get enrollments from database
                enrollments = self.database.get_enrollments_by_student_id(student.id)
                
                if not enrollments:
                    print("No subjects enrolled.")
                else:
                    print("\nEnrolled Subjects:")
                    for enrollment in enrollments:
                        subject = self.database.get_subject_by_id(enrollment.subject_id)
                        if subject:
                            print(f"Subject: {subject.code}: {subject.name}")
                            print(f"Mark: {enrollment.mark}, Grade: {enrollment.grade}")
                    
                    # Calculate average mark and pass status
                    avg_mark = self.database.calculate_student_average_mark(student.id)
                    is_passing = self.database.is_student_passing(student.id)
                    
                    print(f"\nAverage Mark: {avg_mark:.2f}")
                    print(f"Overall Status: {'Pass' if is_passing else 'Fail'}")
            elif choice == "x":
                print("Exiting post-login menu.")
                break
            else:
                print("Invalid choice. Please try again.")
