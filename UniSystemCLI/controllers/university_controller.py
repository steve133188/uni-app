from UniSystemCLI.controllers.student_controller import StudentController
from UniSystemCLI.controllers.admin_controller import AdminController
from UniSystemCLI.utils.console import console, CONSOLE_COLORS


class UniversityController:
    def __init__(self):
        self.student_controller = StudentController()
        self.admin_controller = AdminController()

    def run(self):
        while True:
            console("\nUniversity System Main Menu:\n(S) Student Subsystem\n(A) Admin Subsystem\n(X) Exit")
            console("Choose an option:", CONSOLE_COLORS.YELLOW)
            choice = input("Enter your choice: ").strip().upper()

            if choice == "A":self.admin_controller.run()
            elif choice == "S":self.student_controller.run()
            elif choice == "X":
                print("Exiting the system. Goodbye!")
                break
            else:print("Invalid choice. Please try again.")
