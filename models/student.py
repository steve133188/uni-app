import random

class Student:
    def __init__(self, name, email, password):
        self.id = str(random.randint(100000, 999999))  # Generate a random 6-digit ID
        self.name = name
        self.email = email
        self.password = password

    def change_password(self, new_password):
        """Change the student's password."""
        self.password = new_password

    def __str__(self):
        """Return a string representation of the student."""
        return f"{self.name} ({self.email})"
