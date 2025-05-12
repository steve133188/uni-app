import random

class Subject:
    def __init__(self):
        self.id = str(random.randint(100, 999))
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.mark >= 85:
            return "A"
        elif self.mark >= 70:
            return "B"
        elif self.mark >= 55:
            return "C"
        elif self.mark >= 40:
            return "D"
        else:
            return "F"
