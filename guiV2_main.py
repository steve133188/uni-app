#!/usr/bin/env python3
"""
University Management System - GUI Application
A modern, Next.js-inspired GUI for the University Management System
"""

import os
import sys
from GuiAppV2.GUIUniApp import Database, Student, LoginWindow
import tkinter as tk

# Add the project root to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



if __name__ == "__main__":
    # Initialize database
    db = Database()

    # Create a test student if none exists
    if not db.get_students():
        test_student = Student("Test Student", "test@test.com", "password")
        db.save_student(test_student)

    # Start the application
    root = tk.Tk()
    app = LoginWindow(root, db)
    root.mainloop()