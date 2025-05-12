import os
import pickle
from models.student import Student

class Database:
    def __init__(self):
        self.filepath = os.path.join(os.path.dirname(__file__), "../data/students.data")

    def load_students(self):
        if not os.path.exists(self.filepath):
            return []
        try:
            with open(self.filepath, "rb") as file:
                return pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            return []

    def save_students(self, students):
        with open(self.filepath, "wb") as file:
            pickle.dump(students, file)

    def add_student(self, student):
        students = self.load_students()
        students.append(student)
        self.save_students(students)

    def get_student_by_email(self, email):
        students = self.load_students()
        for student in students:
            if student.email == email:
                return student
        return None
