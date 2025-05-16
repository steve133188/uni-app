from UniSystemCLI.models.subject import Subject
from UniSystemCLI.utils.console import console, CONSOLE_COLORS, display_table
from UniSystemCLI.utils.validators import validate_email, validate_password
from UniSystemCLI.models.database import Database
from UniSystemCLI.models.student import Student
from UniSystemCLI.models.enrollment import Enrollment

class StudentController:
    def __init__(self):
        self.database = Database()

    def run(self):
        while True:
            console(
                "\nStudent Subsystem:"
                + "\n(L) Login"
                + "\n(R) Register"
                + "\n(X) Exit",
                CONSOLE_COLORS.YELLOW
            )
            choice = input("Enter your choice: ").strip().lower()

            if choice == "l":self.login()
            elif choice == "r":self.register()
            elif choice == "x":
                console("Exiting Student Subsystem.", CONSOLE_COLORS.GREEN)
                break
            else:console("Invalid choice. Please try again.", CONSOLE_COLORS.RED)


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
        
        # Email validation loop
        while True:
            email = input("Enter your email (or 'x' to cancel): ").strip()
            if email.lower() == 'x':
                console("Registration cancelled.", CONSOLE_COLORS.YELLOW)
                return
                
            if not validate_email(email):
                console("Email must be in a valid format (e.g., user@university.com)", CONSOLE_COLORS.RED)
                continue
                
            # Check if the student already exists
            if self.database.get_student_by_email(email):
                console(f"Student with email {email} already exists", CONSOLE_COLORS.RED)
                continue
                
            break  # Valid email, proceed to password
        
        # Password validation loop
        while True:
            password = input("Enter your password (or 'x' to cancel): ").strip()
            if password.lower() == 'x':
                console("Registration cancelled.", CONSOLE_COLORS.YELLOW)
                return
                
            if not validate_password(password):
                console("Password must be at least 8 characters long and contain at least one digit.", CONSOLE_COLORS.RED)
                continue
                
            break  # Valid password

        # Create and save the new student
        student = Student(name, email, password)
        self.database.add_student(student)  # Save the student to the database
        console(f"Registration successful! Your student ID is: {student.id}", CONSOLE_COLORS.GREEN)

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
                    # Update the student object
                    student.change_password(new_password)
                    # Update the student in the database
                    students = self.database.load_students()
                    for s in students:
                        if s.id == student.id:
                            s.password = student.password  # Use the updated password from student object
                            break
                    self.database.save_students(students)
                    console("Password changed successfully.",CONSOLE_COLORS.GREEN)
                else:
                    console("Invalid password format.",CONSOLE_COLORS.RED)
            elif choice == "e":
                # Get current enrollments to filter out already enrolled subjects
                current_enrollments = self.database.get_enrollments_by_student_id(student.id)
                enrolled_subject_ids = [e.subject_id for e in current_enrollments]
                
                # Show available subjects that are not already enrolled
                all_subjects = self.database.load_subjects()
                available_subjects = [s for s in all_subjects if s.id not in enrolled_subject_ids]
                
                if not available_subjects:
                    console("No subjects available for enrollment.",CONSOLE_COLORS.YELLOW)
                    continue
                
                # Display available subjects in a table
                console("\nAvailable Subjects:",CONSOLE_COLORS.GREEN)
                headers = ["#", "Code", "Name", "Description"]
                rows = [[i+1, subject.code, subject.name, subject.description] 
                        for i, subject in enumerate(available_subjects)]
                display_table(headers, rows, CONSOLE_COLORS.CYAN)
                
                # Allow multiple enrollments
                while True:
                    try:
                        choice_input = input("\nEnter subject number to enroll (0 to finish, x to cancel): ")
                        
                        # Check for cancel option
                        if choice_input.lower() == 'x':
                            console("Enrollment process cancelled.", CONSOLE_COLORS.YELLOW)
                            break
                            
                        choice = int(choice_input)
                        
                        if choice == 0:
                            console(f"Enrollment process completed.", CONSOLE_COLORS.GREEN)
                            break
                            
                        if choice < 1 or choice > len(available_subjects):
                            console("Invalid selection.",CONSOLE_COLORS.RED)
                            continue
                            
                        selected_subject = available_subjects[choice-1]
                        
                        # Create enrollment
                        enrollment = Enrollment(student.id, selected_subject.id)
                        
                        # Add to database
                        result, message = self.database.add_enrollment(enrollment)
                        console(message, CONSOLE_COLORS.GREEN if result else CONSOLE_COLORS.RED)
                        
                        # Remove the enrolled subject from the available list
                        if result:
                            available_subjects.pop(choice-1)
                            # Redisplay the updated table
                            if available_subjects:
                                console("\nRemaining Available Subjects:",CONSOLE_COLORS.GREEN)
                                rows = [[i+1, subject.code, subject.name, subject.description] 
                                        for i, subject in enumerate(available_subjects)]
                                display_table(headers, rows, CONSOLE_COLORS.CYAN)
                            else:
                                console("No more subjects available for enrollment.",CONSOLE_COLORS.YELLOW)
                                break
                    except ValueError:
                        console("Please enter a valid number.",CONSOLE_COLORS.RED)
                    except Exception as e:
                        console(f"Error: {str(e)}",CONSOLE_COLORS.RED)
                    
            elif choice == "r":
                while True:
                    # Show enrolled subjects
                    enrollments = self.database.get_enrollments_by_student_id(student.id)
                    if not enrollments:
                        console("You are not enrolled in any subjects.",CONSOLE_COLORS.YELLOW)
                        break
                        
                    # Display enrollments in a table
                    console("\nYour Enrollments:",CONSOLE_COLORS.YELLOW)
                    headers = ["#", "Code", "Name", "Mark", "Grade"]
                    rows = []
                    
                    for i, enrollment in enumerate(enrollments):
                        subject = self.database.get_subject_by_id(enrollment.subject_id)
                        if subject:
                            rows.append([i+1, subject.code, subject.name, enrollment.mark, enrollment.grade])
                    
                    display_table(headers, rows, CONSOLE_COLORS.CYAN)

                    try:
                        choice_input = input("\nEnter enrollment number to withdraw from (0 to finish, x to cancel): ")
                        
                        # Check for cancel option
                        if choice_input.lower() == 'x':
                            console("Withdrawal process cancelled.", CONSOLE_COLORS.YELLOW)
                            break
                            
                        choice = int(choice_input)
                        
                        if choice == 0:
                            console("Withdrawal process completed.", CONSOLE_COLORS.GREEN)
                            break
                            
                        if choice < 1 or choice > len(enrollments):
                            console("Invalid selection.",CONSOLE_COLORS.RED)
                            continue
                            
                        selected_enrollment = enrollments[choice-1]
                        
                        # Remove from database
                        if self.database.remove_enrollment(student.id, selected_enrollment.subject_id):
                            console("Successfully withdrawn from subject.",CONSOLE_COLORS.GREEN)
                        else:
                            console("Failed to withdraw from subject.",CONSOLE_COLORS.RED)
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
                    
                    # Display enrollments in a table
                    headers = ["Code", "Name", "Description", "Mark", "Grade"]
                    rows = []
                    
                    for enrollment in enrollments:
                        subject = self.database.get_subject_by_id(enrollment.subject_id)
                        if subject:
                            rows.append([subject.code, subject.name, subject.description, 
                                        enrollment.mark, enrollment.grade])
                    
                    display_table(headers, rows, CONSOLE_COLORS.GREEN)
                    
                    # Calculate average mark and pass status
                    avg_mark = self.database.calculate_student_average_mark(student.id)
                    is_passing = self.database.is_student_passing(student.id)
                    
                    # Display summary in a table
                    summary_headers = ["Metric", "Value", "Status"]
                    
                    # Determine mark status
                    mark_status = "Poor"
                    mark_color = CONSOLE_COLORS.RED
                    if avg_mark >= 70:
                        mark_status = "Excellent"
                        mark_color = CONSOLE_COLORS.GREEN
                    elif avg_mark >= 40:
                        mark_status = "Satisfactory"
                        mark_color = CONSOLE_COLORS.YELLOW
                    
                    # Determine overall status
                    status_text = "Pass" if is_passing else "Fail"
                    status_color = CONSOLE_COLORS.GREEN if is_passing else CONSOLE_COLORS.RED
                    
                    console("\nSummary:", CONSOLE_COLORS.CYAN)
                    console(f"Average Mark: {avg_mark:.2f}", mark_color)
                    console(f"Overall Status: {status_text}", status_color)
            elif choice == "x":
                console("Exiting post-login menu.", CONSOLE_COLORS.GREEN)
                break
            else:
                console("Invalid choice. Please try again.",CONSOLE_COLORS.RED)



