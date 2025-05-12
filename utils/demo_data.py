from models.database import Database
from models.student import Student
from models.subject import Subject
import random

def generate_demo_data():
    database = Database()

    # Clear existing data
    database.clear()

    # Create demo students
    demo_students = [
        Student("Alice Johnson", "alice.johnson@university.com", "Password123"),
        Student("Bob Smith", "bob.smith@university.com", "Secure456"),
        Student("Charlie Brown", "charlie.brown@university.com", "Strong789"),
    ]

    # Add random subjects to each student
    for student in demo_students:
        for _ in range(random.randint(1, 4)):  # Each student gets 1-4 subjects
            subject = Subject()
            student.enrol(subject)

    # Save demo students to the database
    for student in demo_students:
        database.add_student(student)

    print("Demo data has been successfully generated!")

if __name__ == "__main__":
    generate_demo_data()
