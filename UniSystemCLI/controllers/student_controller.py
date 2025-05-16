from UniSystemCLI.utils.console import console, CONSOLE_COLORS
from UniSystemCLI.utils.validators import validate_email, validate_password
from UniSystemCLI.models.database import Database
from UniSystemCLI.models.student import Student

class StudentController:
    def __init__(self):
        self.database = Database()

    def run(self):
        while True:
            console(
                "\nStudent Subsystem:"
                + "\n(L) Login"
                + "\n(R) Register"
                + "\n(X) Exit"
            )
            choice = input("Enter your choice: ").strip().lower()

            if choice == "l":self.login()
            elif choice == "r":self.register()
            elif choice == "x":
                console("Exiting Student Subsystem.")
                break
            else:console("Invalid choice. Please try again.")


    def login(self):
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()

        student = self.database.get_student_by_email(email)
        if student and student.password == password:
            console(f"Welcome, {student.name}!",CONSOLE_COLORS.GREEN)
            self.post_login_menu(student)
        else:
            console("Invalid email or password.",CONSOLE_COLORS.RED)

    def register(self):
        console("Student Sign Up", CONSOLE_COLORS.GREEN)
        name = input("Enter your name: ").strip()
        email = input("Enter your email: ").strip()
        password = input("Enter your password: ").strip()

        # Validate email format
        if not validate_email(email) or not validate_password(password):
            console("Invalid email or password format.",CONSOLE_COLORS.RED)
            return

        # Check if the student already exists
        if self.database.get_student_by_email(email):
            console(f"Student {email} already exists",CONSOLE_COLORS.RED)
            return

        # Create and save the new student
        student = Student(name, email, password)
        self.database.add_student(student)  # Save the student to the database
        console("Registration successful!",CONSOLE_COLORS.GREEN)

    def post_login_menu(self, student):
        while True:
            console(
                "\nPost-login Actions:"
                + "\n(C) Change Password"
                + "\n(E) Enrol in a Subject"
                + "\n(R) Remove a Subject"
                + "\n(S) Show Enrolled Subjects, Marks, Grades"
                + "\n(X) Exit"
            )

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
                    console("Password changed successfully.",CONSOLE_COLORS.GREEN)
                else:
                    console("Invalid password format.",CONSOLE_COLORS.RED)
            elif choice == "e":
                # Show available subjects
                subjects = self.database.load_subjects()
                if not subjects:
                    console("No subjects available for enrollment.",CONSOLE_COLORS.YELLOW)
                    continue
                    
                console("\nAvailable Subjects:",CONSOLE_COLORS.GREEN)
                for i, subject in enumerate(subjects):
                    console(f"{i+1}. {subject.code}: {subject.name}")
                
                try:
                    choice = int(input("\nEnter subject number to enroll (0 to cancel): "))
                    if choice == 0:
                        continue
                    if choice < 1 or choice > len(subjects):
                        console("Invalid selection.",CONSOLE_COLORS.RED)
                        continue
                        
                    selected_subject = subjects[choice-1]
                    
                    # Create enrollment
                    from UniSystemCLI.models.enrollment import Enrollment
                    enrollment = Enrollment(student.id, selected_subject.id)
                    
                    # Add to database
                    result, message = self.database.add_enrollment(enrollment)
                    console(message)
                except ValueError:
                    console("Please enter a valid number.",CONSOLE_COLORS.RED)
                except Exception as e:
                    console(f"Error: {str(e)}",CONSOLE_COLORS.RED)
                    
            elif choice == "r":
                # Show enrolled subjects
                enrollments = self.database.get_enrollments_by_student_id(student.id)
                if not enrollments:
                    console("You are not enrolled in any subjects.",CONSOLE_COLORS.YELLOW)
                    continue
                    
                console("\nYour Enrollments:",CONSOLE_COLORS.YELLOW)
                for i, enrollment in enumerate(enrollments):
                    subject = self.database.get_subject_by_id(enrollment.subject_id)
                    if subject:
                        console(f"{i+1}. {subject.code}: {subject.name} - Mark: {enrollment.mark}, Grade: {enrollment.grade}",CONSOLE_COLORS.CYAN)
                
                try:
                    choice = int(input("\nEnter enrollment number to remove (0 to cancel): "))
                    if choice == 0:
                        continue
                    if choice < 1 or choice > len(enrollments):
                        console("Invalid selection.",CONSOLE_COLORS.RED)
                        continue
                        
                    selected_enrollment = enrollments[choice-1]
                    
                    # Remove from database
                    if self.database.remove_enrollment(student.id, selected_enrollment.subject_id):
                        console("Successfully withdrawn from subject.")
                    else:
                        console("Failed to withdrawn from subject.",CONSOLE_COLORS.RED)
                except ValueError:
                    console("Please enter a valid number.",CONSOLE_COLORS.RED)
                except Exception as e:
                    console(f"Error: {str(e)}",CONSOLE_COLORS.RED)
            elif choice == "s":
                # Get enrollments from database
                enrollments = self.database.get_enrollments_by_student_id(student.id)
                
                if not enrollments:
                    console("No subjects enrolled.",CONSOLE_COLORS.YELLOW)
                else:
                    console("\nEnrolled Subjects:",CONSOLE_COLORS.YELLOW)
                    for enrollment in enrollments:
                        subject = self.database.get_subject_by_id(enrollment.subject_id)
                        if subject:
                            console(f"Subject: {subject.code}: {subject.name}",CONSOLE_COLORS.GREEN)
                            console(f"Mark: {enrollment.mark}, Grade: {enrollment.grade}",CONSOLE_COLORS.GREEN)
                    
                    # Calculate average mark and pass status
                    avg_mark = self.database.calculate_student_average_mark(student.id)
                    is_passing = self.database.is_student_passing(student.id)
                    
                    console(f"\nAverage Mark: {avg_mark:.2f}",CONSOLE_COLORS.CYAN)
                    console(f"Overall Status: {'Pass' if is_passing else 'Fail'}",CONSOLE_COLORS.GREEN if not is_passing else CONSOLE_COLORS.RED)
            elif choice == "x":
                console("Exiting post-login menu.", CONSOLE_COLORS.GREEN)
                break
            else:
                console("Invalid choice. Please try again.",CONSOLE_COLORS.RED)



