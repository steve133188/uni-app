import tkinter as tk
from tkinter import messagebox
import random
import pickle
import re
import os
from typing import List

from UniSystemCLI.models.student import Student
from UniSystemCLI.models.subject import Subject


class Enrollment:
    def __init__(self, student_id, subject_id):
        self.id = f"{random.randint(1, 999999):06d}"
        self.student_id = student_id
        self.subject_id = subject_id

class Database:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "../UniSystemCLI/data")
        self.students_file = os.path.join(self.data_dir, "students.data")
        self.subjects_file= os.path.join(self.data_dir, "subjects.data")
        self.enrollments_file = os.path.join(self.data_dir, "enrollments.data")
        self._init_files()

    def _init_files(self):
        if not os.path.exists(self.students_file):
            initial_students = [
                Student("John Smith", "john@student.com", "pass123"),
                Student("Emma Wilson", "emma@student.com", "pass456"),
                Student("Michael Kim", "michael@student.com", "pass789"),
                Student("Sarah Lee", "sarah@student.com", "pass321"),
                Student("David Chen", "david@student.com", "pass654")
            ]
            self._save_data(initial_students, self.students_file)

        if not os.path.exists(self.subjects_file):
            # Create AI-related subjects with predefined IDs
            subjects = []
            subject_names = [
                "Introduction to Artificial Intelligence",
                "Machine Learning Fundamentals",
                "Deep Learning and Neural Networks",
                "Natural Language Processing",
                "Computer Vision",
                "Robotics and AI",
                "AI Ethics and Society",
                "Reinforcement Learning",
                "Expert Systems",
                "Data Mining and AI"
            ]

            for name in subject_names:
                subject = Subject(name=name)
                subjects.append(subject)

            self._save_data(subjects, self.subjects_file)

        if not os.path.exists(self.enrollments_file):
            self._save_data([], self.enrollments_file)

    def _save_data(self, data, filename):
        with open(filename, 'wb') as f:
            pickle.dump(data, f)

    def _load_data(self, filename):
        try:
            with open(filename, 'rb') as f:
                return pickle.load(f)
        except:
            return []

    def get_students(self):
        return self._load_data(self.students_file)

    def get_subjects(self):
        return self._load_data(self.subjects_file)

    def get_enrollments(self):
        return self._load_data(self.enrollments_file)

    def save_student(self, student):
        students = self.get_students()
        students.append(student)
        self._save_data(students, self.students_file)

    def save_enrollment(self, enrollment):
        enrollments = self.get_enrollments()
        enrollments.append(enrollment)
        self._save_data(enrollments, self.enrollments_file)

    def delete_enrollment(self, student_id, subject_id):
        enrollments = self.get_enrollments()
        enrollments = [e for e in enrollments if not (e.student_id == student_id and e.subject_id == subject_id)]
        self._save_data(enrollments, self.enrollments_file)

class LoginWindow:
    def __init__(self, root, db):
        self.root = root
        self.db = db
        self.root.title("University App - Login")
        self.root.geometry("300x200")

        # Create widgets
        tk.Label(root, text="Email:").pack(pady=5)
        self.email_entry = tk.Entry(root)
        self.email_entry.pack(pady=5)

        tk.Label(root, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(root, show="*")
        self.password_entry.pack(pady=5)

        tk.Button(root, text="Login", command=self.login).pack(pady=20)

    def login(self):
        email = self.email_entry.get()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields!")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid email format!")
            return

        students = self.db.get_students()
        student = next((s for s in students if s.email == email and s.password == password), None)

        if student:
            self.root.withdraw()
            enrollment_window = tk.Toplevel()
            EnrollmentWindow(enrollment_window, self.db, student, self.root)
        else:
            messagebox.showerror("Error", "Invalid credentials!")

class EnrollmentWindow:
    def __init__(self, root, db, student, login_window):
        self.root = root
        self.db = db
        self.student = student
        self.login_window = login_window
        
        self.root.title(f"Enrollment - {student.name}")
        self.root.geometry("800x500")

        # Create main frame
        main_frame = tk.Frame(root)
        main_frame.pack(expand=True, fill='both', padx=10, pady=10)

        # Top frame for navigation buttons
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, pady=5)
        
        tk.Button(top_frame, text="View My Subjects", command=self.open_subject_window).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Logout", command=self.logout).pack(side=tk.LEFT, padx=5)

        # Left frame for available subjects
        left_frame = tk.LabelFrame(main_frame, text="Available Subjects")
        left_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=5)

        self.subjects_listbox = tk.Listbox(left_frame, width=40, height=15)
        self.subjects_listbox.pack(expand=True, fill='both', padx=5, pady=5)

        # Middle frame for enrollment buttons
        middle_frame = tk.Frame(main_frame)
        middle_frame.pack(side=tk.LEFT, padx=10)

        enroll_button = tk.Button(middle_frame, text="→", command=self.enroll, font=('Arial', 20))
        enroll_button.pack(pady=10)
        
        unenroll_button = tk.Button(middle_frame, text="←", command=self.unenroll, font=('Arial', 20))
        unenroll_button.pack(pady=10)

        # Right frame for enrolled subjects
        right_frame = tk.LabelFrame(main_frame, text="My Subjects")
        right_frame.pack(side=tk.LEFT, expand=True, fill='both', padx=5)

        self.enrolled_subjects_listbox = tk.Listbox(right_frame, width=40, height=15)
        self.enrolled_subjects_listbox.pack(expand=True, fill='both', padx=5, pady=5)

        # Load initial data
        self.load_available_subjects()
        self.load_enrolled_subjects()

    def open_subject_window(self):
        self.root.withdraw()  # Hide enrollment window
        subject_window = tk.Toplevel()
        SubjectWindow(subject_window, self.db, self.student, self.root)

    def logout(self):
        self.root.destroy()
        self.login_window.deiconify()

    def load_available_subjects(self):
        self.subjects_listbox.delete(0, tk.END)
        all_subjects = self.db.get_subjects()
        enrollments = self.db.get_enrollments()
        
        # Filter out subjects student is already enrolled in
        student_enrollments = [e.subject_id for e in enrollments if e.student_id == self.student.id]
        available_subjects = [s for s in all_subjects if s.id not in student_enrollments]
        
        for subject in available_subjects:
            self.subjects_listbox.insert(tk.END, f"{subject.name} (ID: {subject.id})")

    def load_enrolled_subjects(self):
        self.enrolled_subjects_listbox.delete(0, tk.END)
        enrollments = self.db.get_enrollments()
        subjects = self.db.get_subjects()

        student_enrollments = [e for e in enrollments if e.student_id == self.student.id]
        
        for enrollment in student_enrollments:
            subject = next((s for s in subjects if s.id == enrollment.subject_id), None)
            if subject:
                self.enrolled_subjects_listbox.insert(tk.END, 
                    f"{subject.name} (ID: {subject.id}) - Mark: {subject.mark}, Grade: {subject.grade}")

    def enroll(self):
        selection = self.subjects_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a subject!")
            return

        enrollments = self.db.get_enrollments()
        student_enrollments = [e for e in enrollments if e.student_id == self.student.id]
        
        if len(student_enrollments) >= 4:
            messagebox.showerror("Error", "Maximum enrollment (4 subjects) reached!")
            return

        all_subjects = self.db.get_subjects()
        available_subjects = [s for s in all_subjects if s.id not in [e.subject_id for e in student_enrollments]]
        selected_subject = available_subjects[selection[0]]
        
        new_enrollment = Enrollment(self.student.id, selected_subject.id)
        self.db.save_enrollment(new_enrollment)
        
        # Refresh both listboxes first
        self.load_available_subjects()
        self.load_enrolled_subjects()
        
        # Show success message after update
        messagebox.showinfo("Success", "Successfully enrolled in subject!")

    def unenroll(self):
        selection = self.enrolled_subjects_listbox.curselection()
        if not selection:
            messagebox.showerror("Error", "Please select a subject to unenroll!")
            return

        enrollments = self.db.get_enrollments()
        student_enrollments = [e for e in enrollments if e.student_id == self.student.id]
        
        if not student_enrollments:
            return
            
        selected_enrollment = student_enrollments[selection[0]]
        self.db.delete_enrollment(self.student.id, selected_enrollment.subject_id)
        
        # Refresh both listboxes first
        self.load_available_subjects()
        self.load_enrolled_subjects()
        
        # Show success message after update
        messagebox.showinfo("Success", "Successfully unenrolled from subject!")

class SubjectWindow:
    def __init__(self, root, db, student, enrollment_window):
        self.root = root
        self.db = db
        self.student = student
        self.enrollment_window = enrollment_window
        
        self.root.title(f"My Subjects - {student.name}")
        self.root.geometry("600x500")

        # Top frame for navigation buttons
        top_frame = tk.Frame(root)
        top_frame.pack(side=tk.TOP, pady=5)
        
        tk.Button(top_frame, text="Back to Enrollment", command=self.back_to_enrollment).pack(side=tk.LEFT, padx=5)
        tk.Button(top_frame, text="Logout", command=self.logout).pack(side=tk.LEFT, padx=5)

        # Main content
        main_frame = tk.LabelFrame(root, text="My Enrolled Subjects")
        main_frame.pack(expand=True, fill='both', padx=10, pady=5)

        self.subjects_text = tk.Text(main_frame, width=50, height=20)
        self.subjects_text.pack(expand=True, fill='both', padx=5, pady=5)

        self.load_subjects()

    def back_to_enrollment(self):
        self.enrollment_window.deiconify()  # Show enrollment window
        self.root.destroy()  # Close subject window

    def logout(self):
        self.enrollment_window.destroy()  # Close enrollment window
        self.root.destroy()  # Close subject window
        # Find and show login window
        for widget in tk.Tk.winfo_all(self.root):
            if isinstance(widget, tk.Tk):
                widget.deiconify()
                break

    def load_subjects(self):
        self.subjects_text.delete(1.0, tk.END)
        enrollments = self.db.get_enrollments()
        subjects = self.db.get_subjects()

        student_enrollments = [e for e in enrollments if e.student_id == self.student.id]
        
        if not student_enrollments:
            self.subjects_text.insert(tk.END, "You are not enrolled in any subjects yet.")
            return
            
        for enrollment in student_enrollments:
            subject = next((s for s in subjects if s.id == enrollment.subject_id), None)
            if subject:
                self.subjects_text.insert(tk.END, 
                    f"\nSubject: {subject.name}\n"
                    f"ID: {subject.id}\n"
                    f"Mark: {subject.mark}\n"
                    f"Grade: {subject.grade}\n"
                    f"------------------------\n")


