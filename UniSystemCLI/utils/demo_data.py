import os
import sys
import random

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from UniSystemCLI.models.student import Student
from UniSystemCLI.models.subject import Subject
from UniSystemCLI.models.enrollment import Enrollment
from UniSystemCLI.models.database import Database

def generate_demo_data():
    """Generate demo data for the university management system"""
    db = Database()
    
    # Clear existing data
    db.clear()
    
    # Create demo subjects
    subjects = [
        Subject("Introduction to Computer Science", "CS101", "An introductory course to computer science and programming concepts."),
        Subject("Data Structures and Algorithms", "CS201", "Study of fundamental data structures and algorithms used in computing."),
        Subject("Database Systems", "CS301", "Introduction to database design, implementation, and management."),
        Subject("Web Development", "CS401", "Learn to build dynamic web applications using modern frameworks."),
        Subject("Artificial Intelligence", "CS501", "Introduction to AI concepts, algorithms, and applications."),
        Subject("Software Engineering", "SE101", "Principles and practices of software development and project management."),
        Subject("Mathematics for Computing", "MA101", "Essential mathematical concepts for computer science."),
        Subject("Network Security", "NS201", "Understanding network vulnerabilities and security measures.")
    ]
    
    # Save subjects to database
    for subject in subjects:
        db.add_subject(subject)
    
    # Create demo students
    students = [
        Student("John Doe", "john@university.com", "password"),
        Student("Jane Smith", "jane@university.com", "password"),
        Student("Bob Johnson", "bob@university.com", "password"),
        Student("Alice Brown", "alice@university.com", "password")
    ]
    
    # Save students to database
    for student in students:
        db.add_student(student)
    
    # Create enrollments (each student enrolls in 2-4 subjects)
    for student in students:
        # Randomly select 2-4 subjects for each student
        num_subjects = random.randint(2, 4)
        selected_subjects = random.sample(subjects, num_subjects)
        
        for subject in selected_subjects:
            # Create enrollment
            enrollment = Enrollment(student.id, subject.id)
            
            # Randomly assign a mark (40-100)
            enrollment.set_mark(random.randint(40, 100))
            
            # Add enrollment to student and database
            student.enroll_subject(enrollment)
            db.add_enrollment(enrollment)
        
        # Update student in database with enrollments
        all_students = db.load_students()
        for i, s in enumerate(all_students):
            if s.id == student.id:
                all_students[i] = student
                break
        db.save_students(all_students)
    
    print("Demo data generated successfully!")
    print(f"Created {len(subjects)} subjects and {len(students)} students")

if __name__ == "__main__":
    generate_demo_data()
