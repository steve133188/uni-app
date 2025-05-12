import random
from models.subject import Subject

class Student:
    def __init__(self, name, email, password):
        self.id = str(random.randint(100000, 999999))  # Generate a random 6-digit ID
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []  # List of enrolled subjects

    def enrol(self, subject):
        """Enroll the student in a new subject."""
        self.subjects.append(subject)

    def remove_subject(self, subject_id):
        """Remove a subject by its ID."""
        for subject in self.subjects:
            if subject.id == subject_id:
                self.subjects.remove(subject)
                return True
        return False

    def list_subjects(self):
        """List all enrolled subjects with marks and grades."""
        for subject in self.subjects:
            print(f"Subject ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}")

    def change_password(self, new_password):
        """Change the student's password."""
        self.password = new_password

    def average_mark(self):
        """Calculate the average mark of all enrolled subjects."""
        if not self.subjects:
            return 0.0
        return sum(subject.mark for subject in self.subjects) / len(self.subjects)

    def is_pass(self):
        """Check if the student has passed based on their average mark."""
        return all(subject.grade != "F" for subject in self.subjects)
