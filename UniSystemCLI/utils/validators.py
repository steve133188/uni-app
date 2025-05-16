import re

def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9._%+-]+@university\.com$", email))

def validate_password(password):
    return bool(re.match(r"^[A-Z][a-zA-Z]{4,}\d{3,}$", password))
