from UniSystemCLI.controllers.student_controller import StudentController
from UniSystemCLI.controllers.admin_controller import AdminController

class UniversityController:
    def __init__(self):
        self.student_controller = StudentController()
        self.admin_controller = AdminController()

    def run(self):
        while True:
            print("\nUniversity System Main Menu:\n(A) Admin Subsystem\n(S) Student Subsystem\n(X) Exit")
            # print("(A) Admin Subsystem")
            # print("(S) Student Subsystem")
            # print("(X) Exit")
            choice = input("Enter your choice: ").strip().upper()

            if choice == "A":self.admin_controller.run()
            elif choice == "S":self.student_controller.run()
            elif choice == "X":
                print("Exiting the system. Goodbye!")
                break
            else:print("Invalid choice. Please try again.")
