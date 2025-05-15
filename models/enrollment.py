import random

class Enrollment:
    def __init__(self, student_id, subject_id):
        self.id = str(random.randint(10000, 99999))  # Generate a random 5-digit ID
        self.student_id = student_id
        self.subject_id = subject_id
        self.mark = 0  # Default mark is 0
        self.grade = 'N/A'  # Default grade is N/A
    
    def set_mark(self, mark):
        """Set the mark for this enrollment and calculate the grade."""
        self.mark = mark
        self.calculate_grade()
    
    def calculate_grade(self):
        """Calculate the grade based on the mark."""
        if self.mark >= 85:
            self.grade = "A"
        elif self.mark >= 70:
            self.grade = "B"
        elif self.mark >= 55:
            self.grade = "C"
        elif self.mark >= 40:
            self.grade = "D"
        else:
            self.grade = "F"
        return self.grade