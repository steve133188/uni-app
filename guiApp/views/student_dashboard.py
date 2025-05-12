from tkinter import Frame, Label, Button, Tk
from tkinter import ttk

class StudentDashboard(Frame):
    def __init__(self, master, student):
        super().__init__(master, bg="white")  # Set background color to white
        self.master = master
        self.student = student
        self.create_widgets()
        self.grid(padx=20, pady=20)  # Add padding around the frame

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", background="white", foreground="#323232", font=("Arial", 12))
        style.configure("TButton", background="#0f4beb", foreground="white", font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("TButton", background=[("active", "#0d3ba8")])  # Darker blue on hover

        # Title label
        Label(self, text=f"Welcome, {self.student.name}!", bg="white", fg="#0f4beb", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Buttons for actions
        ttk.Button(self, text="View Subjects", command=self.view_subjects).grid(row=1, column=0, padx=10, pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Enroll in Subject", command=self.enroll_subject).grid(row=1, column=1, padx=10, pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Change Password", command=self.change_password).grid(row=2, column=0, padx=10, pady=10, ipadx=10, ipady=5)
        ttk.Button(self, text="Logout", command=self.logout).grid(row=2, column=1, padx=10, pady=10, ipadx=10, ipady=5)

    def view_subjects(self):
        # Placeholder for viewing subjects
        print("Viewing subjects...")

    def enroll_subject(self):
        # Placeholder for enrolling in a subject
        print("Enrolling in a subject...")

    def change_password(self):
        # Placeholder for changing password
        print("Changing password...")

    def logout(self):
        self.master.destroy()
        root = Tk()
        root.title("Login")
        root.configure(bg="white")  # Set background color to white
        from guiApp.views.login_window import LoginWindow
        LoginWindow(root)
        root.mainloop()
