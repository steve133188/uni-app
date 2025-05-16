import random
import re

from UniSystemCLI.models.enrollment import Enrollment


class Student:
    def __init__(self, name, email, password, enrolled_subjects=None):
        if enrolled_subjects is None:
            enrolled_subjects = []
            self.enrolled_subjects = [Enrollment]
        self.id = str(random.randint(100000, 999999))  # Generate a random 6-digit ID
        self.name = name
        self.email = email
        self.password = password
        self.enrolled_subjects:[Enrollment]= enrolled_subjects

    def change_password(self, new_password):
        """Change the student's password."""
        self.password = new_password
        print("Password changed successfully.")

    def __str__(self):
        """Return a string representation of the student."""
        return f"{self.id} {self.name} ({self.email})"

    def enroll_subject(self, enrollment:Enrollment):
        if len(self.enrolled_subjects) >= 4:
            print("You can only enroll in 4 subjects.")
            return
        self.enrolled_subjects.append(enrollment)
        print(f"Enrolled in {enrollment.subject_id} with Mark {enrollment.mark} and Grade {enrollment.grade}")

    def remove_subject(self, subject_id):
        for subject in self.enrolled_subjects:
            if subject.id == subject_id:
                self.enrolled_subjects.remove(subject)
                print(f"Removed subject {subject.name}")
                return
        print("Subject ID not found.")

    def average_mark(self):
        if not self.enrolled_subjects:
            return 0

        marks = [sub for sub in self.enrolled_subjects]
        print(marks)
        total_marks = sum(sub.mark for sub in self.enrolled_subjects)
        return sum(total_marks) / len(self.enrolled_subjects)

    def is_passed(self):
        return self.average_mark() >= 50

    def show_enrollments(self):
        if not self.enrolled_subjects:
            print("No enrolled subjects.")
            return
        for sub in self.enrolled_subjects:
            print(sub)

    @staticmethod
    def validate_email(email):
        return re.match(r"^[a-zA-Z0-9_.+-]+@[uU]niversity\.com$", email)

    @staticmethod
    def validate_password(password):
        return re.match(r"^[A-Z][a-zA-Z]{5,}\d{3,}$", password)