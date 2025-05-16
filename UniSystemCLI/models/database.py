import os
import pickle

from UniSystemCLI.models.student import Student
from UniSystemCLI.utils.console import console


class Database:
    def __init__(self):
        self.data_dir = os.path.join(os.path.dirname(__file__), "../data")
        # Use separate files for each data type
        self.students_filepath = os.path.join(self.data_dir, "students.data")
        self.subjects_filepath = os.path.join(self.data_dir, "subjects.data")
        self.enrollments_filepath = os.path.join(self.data_dir, "enrollments.data")
        # Ensure data directory exists
        if not os.path.exists(self.data_dir):
            os.makedirs(self.data_dir)

    # Student methods
    
    def load_students(self):
        if not os.path.exists(self.students_filepath):
            return []
        try:
            with open(self.students_filepath, "rb") as file:
                students = pickle.load(file)
                return students
        except (EOFError, pickle.UnpicklingError):
            return []

    def save_students(self, students):
        with open(self.students_filepath, "wb") as file:
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
    
    def get_student_by_id(self, student_id):
        students = self.load_students()
        for student in students:
            if student.id == student_id:
                return student
        return None
        
    def remove_student(self, student_id):
        """Remove a student by their ID."""
        students = self.load_students()
        for i, student in enumerate(students):
            if student.id == student_id:
                students.pop(i)
                self.save_students(students)
                return True
        return False
    
    # Subject methods
    def load_subjects(self):
        if not os.path.exists(self.subjects_filepath):
            return []
        try:
            with open(self.subjects_filepath, "rb") as file:
                return pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            return []

    def save_subjects(self, subjects):
        with open(self.subjects_filepath, "wb") as file:
            pickle.dump(subjects, file)

    def add_subject(self, subject):
        subjects = self.load_subjects()
        subjects.append(subject)
        self.save_subjects(subjects)

    def get_subject_by_id(self, subject_id):
        subjects = self.load_subjects()
        for subject in subjects:
            if subject.id == subject_id:
                return subject
        return None
    
    def remove_subject(self, subject_id):
        """Remove a subject by its ID."""
        subjects = self.load_subjects()
        for i, subject in enumerate(subjects):
            if subject.id == subject_id:
                subjects.pop(i)
                self.save_subjects(subjects)
                return True
        return False
    
    # Enrollment methods
    def load_enrollments(self):
        if not os.path.exists(self.enrollments_filepath):
            return []
        try:
            with open(self.enrollments_filepath, "rb") as file:
                return pickle.load(file)
        except (EOFError, pickle.UnpicklingError):
            return []

    def save_enrollments(self, enrollments):
        with open(self.enrollments_filepath, "wb") as file:
            pickle.dump(enrollments, file)

    def add_enrollment(self, enrollment):
        # Check if student already has 4 enrollments
        student_enrollments = self.get_enrollments_by_student_id(enrollment.student_id)
        if len(student_enrollments) >= 4:
            return None, "Maximum of 4 subjects allowed"
            
        # Check if student is already enrolled in this subject
        for enroll in student_enrollments:
            if enroll.subject_id == enrollment.subject_id:
                return None, "Already enrolled in this subject"
                
        enrollments = self.load_enrollments()
        enrollments.append(enrollment)
        self.save_enrollments(enrollments)
        return enrollment, "Enrollment successful"

    def get_enrollments_by_student_id(self, student_id):
        enrollments = self.load_enrollments()
        return [e for e in enrollments if e.student_id == student_id]
        
    def calculate_student_average_mark(self, student_id):
        """Calculate the average mark of all enrollments for a student."""
        enrollments = self.get_enrollments_by_student_id(student_id)
        if not enrollments:
            return 0.0
        return sum(enrollment.mark for enrollment in enrollments) / len(enrollments)
    
    def is_student_passing(self, student_id):
        """Check if the student has passed all enrolled subjects.
        A student is considered passing if they have no F grades and no N/A grades.
        """
        enrollments = self.get_enrollments_by_student_id(student_id)
        if not enrollments:
            return False
        # A student passes if they have no F grades and no N/A grades
        return all(enrollment.grade not in ["F", "N/A"] for enrollment in enrollments)
    
    def get_enrollments_by_subject_id(self, subject_id):
        enrollments = self.load_enrollments()
        return [e for e in enrollments if e.subject_id == subject_id]
    
    def get_enrollment(self, student_id, subject_id):
        enrollments = self.load_enrollments()
        for enrollment in enrollments:
            if enrollment.student_id == student_id and enrollment.subject_id == subject_id:
                return enrollment
        return None
    
    def update_enrollment_mark(self, student_id, subject_id, mark):
        enrollments = self.load_enrollments()
        for enrollment in enrollments:
            if enrollment.student_id == student_id and enrollment.subject_id == subject_id:
                enrollment.set_mark(mark)
                self.save_enrollments(enrollments)
                return True
        return False
    
    def remove_enrollment(self, student_id, subject_id):
        enrollments = self.load_enrollments()
        for i, enrollment in enumerate(enrollments):
            if enrollment.student_id == student_id and enrollment.subject_id == subject_id:
                enrollments.pop(i)
                self.save_enrollments(enrollments)
                return True
        return False
    
    # General methods
    def clear(self):
        """Clear all data from the database."""
        success = False
        for filepath in [self.students_filepath, self.subjects_filepath, self.enrollments_filepath]:
            if os.path.exists(filepath):
                with open(filepath, "wb") as file:
                    pickle.dump([], file)
                success = True
        if success:
            console("Database cleared.")
        return success
