#!/usr/bin/env python3
"""
University Management System - GUI Application
A modern, Next.js-inspired GUI for the University Management System
"""

import os
import sys

# Add the project root to the path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import the Next.js style application
from guiApp.nextjs_style_app import NextJSStyleApp

if __name__ == "__main__":
    # Launch the Next.js style application
    app = NextJSStyleApp()
    app.mainloop()