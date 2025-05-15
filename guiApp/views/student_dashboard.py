from tkinter import Frame, Label, Button, Tk, StringVar
from tkinter import ttk
import sys
import os

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models.database import Database

class StudentDashboard(Frame):
    def __init__(self, master, student):
        super().__init__(master, bg="white")  # Set background color to white
        self.master = master
        self.student = student
        self.database = Database()
        self.create_widgets()
        self.grid(padx=20, pady=20)  # Add padding around the frame

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", background="white", foreground="#323232", font=("Arial", 12))
        style.configure("TButton", background="#0f4beb", foreground="white", font=("Arial", 12, "bold"), borderwidth=0, relief="flat")
        style.map("TButton", background=[("active", "#0d3ba8")])  # Darker blue on hover
        style.configure("Treeview", background="white", foreground="#323232", rowheight=25)
        style.configure("Treeview.Heading", background="#f0f0f0", foreground="#323232", font=("Arial", 10, "bold"))

        # Title label
        Label(self, text=f"Welcome, {self.student.name}!", bg="white", fg="#0f4beb", font=("Arial", 16, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))
        
        # Student stats
        avg_mark = self.database.calculate_student_average_mark(self.student.id)
        is_passing = self.database.is_student_passing(self.student.id)
        
        stats_frame = Frame(self, bg="white", bd=1, relief="solid")
        stats_frame.grid(row=1, column=0, columnspan=2, sticky="ew", padx=10, pady=10)
        
        Label(stats_frame, text=f"Average Mark: {avg_mark:.1f}", bg="white", fg="#323232", font=("Arial", 12)).pack(side="left", padx=20, pady=10)
        Label(stats_frame, text=f"Overall Status: {'Passing' if is_passing else 'Failing'}", 
              bg="white", fg="#34C759" if is_passing else "#FF3B30", font=("Arial", 12, "bold")).pack(side="right", padx=20, pady=10)
        
        # Enrollments section
        Label(self, text="My Enrolled Subjects", bg="white", fg="#323232", font=("Arial", 14, "bold")).grid(row=2, column=0, columnspan=2, sticky="w", padx=10, pady=(20, 10))
        
        # Create treeview for enrollments
        enrollments_frame = Frame(self, bg="white")
        enrollments_frame.grid(row=3, column=0, columnspan=2, sticky="nsew", padx=10, pady=10)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(enrollments_frame)
        scrollbar.pack(side="right", fill="y")
        
        # Treeview
        self.enrollments_tree = ttk.Treeview(enrollments_frame, columns=("code", "name", "mark", "grade"), show="headings", yscrollcommand=scrollbar.set)
        self.enrollments_tree.heading("code", text="Code")
        self.enrollments_tree.heading("name", text="Subject")
        self.enrollments_tree.heading("mark", text="Mark")
        self.enrollments_tree.heading("grade", text="Grade")
        
        self.enrollments_tree.column("code", width=100)
        self.enrollments_tree.column("name", width=200)
        self.enrollments_tree.column("mark", width=100)
        self.enrollments_tree.column("grade", width=100)
        
        self.enrollments_tree.pack(fill="both", expand=True)
        scrollbar.config(command=self.enrollments_tree.yview)
        
        # Load enrollments
        self.load_enrollments()
        
        # Buttons for actions
        ttk.Button(self, text="Enroll in Subject", command=self.enroll_subject).grid(row=4, column=0, padx=10, pady=20, ipadx=10, ipady=5)
        ttk.Button(self, text="Change Password", command=self.change_password).grid(row=4, column=1, padx=10, pady=20, ipadx=10, ipady=5)
        ttk.Button(self, text="Logout", command=self.logout).grid(row=5, column=0, columnspan=2, padx=10, pady=10, ipadx=10, ipady=5)

    def load_enrollments(self):
        # Clear existing items
        for item in self.enrollments_tree.get_children():
            self.enrollments_tree.delete(item)
            
        # Get enrollments from database
        enrollments = self.database.get_enrollments_by_student_id(self.student.id)
        
        if not enrollments:
            self.enrollments_tree.insert("", "end", values=("No subjects", "You are not enrolled in any subjects", "", ""))
            return
            
        # Add enrollments to treeview
        for enrollment in enrollments:
            subject = self.database.get_subject_by_id(enrollment.subject_id)
            if subject:
                self.enrollments_tree.insert("", "end", values=(
                    subject.code,
                    subject.name,
                    enrollment.mark,
                    enrollment.grade
                ))

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
