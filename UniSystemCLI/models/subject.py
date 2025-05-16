import random

class Subject:
    def __init__(self, name="", code="", description=""):
        self.id = str(random.randint(100, 999))
        self.name = name
        self.code = code
        self.description = description
        
    def __str__(self):
        return f"{self.id} {self.code}: {self.name}"
