#!/usr/bin/env python3
"""
University Management System - GUI Application
A modern, Next.js-inspired GUI for the University Management System
"""

import os
import sys
from GuiAppV2.GUIUniApp import LoginWindow
import tkinter as tk

from UniSystemCLI.models.database import Database

# Add the project root to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))



if __name__ == "__main__":
    # Initialize database
    #
    # # Create a test student if none exists
    # if not db.get_students():
    #     test_student = Student("Test Student", "test@test.com", "password")
    #     db.save_student(test_student)

    # Start the application
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()