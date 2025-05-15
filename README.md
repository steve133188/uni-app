# University Management System - Modern GUI V2

A modern, Next.js-inspired GUI application for the University Management System. This application provides a clean, intuitive interface for students and administrators to interact with the university system.

## Features

- **Modern UI Design**: Clean, card-based interface inspired by Next.js website
- **Student Dashboard**: View enrolled subjects, personal information, and manage account
- **Admin Dashboard**: Manage students, courses, and system settings
- **Responsive Layout**: Adapts to different window sizes
- **Consistent Styling**: Blue accent colors, clean typography, and card-based UI elements

## Getting Started

### Prerequisites

- Python 3.6 or higher
- Tkinter (usually comes with Python installation)

### Running the Application

To run the GUI application, execute the following command from the project root:

```bash
python3 gui_main.py
```

### Login Credentials

#### Student Login
Use any student email and password from the database.

#### Admin Login
- Email: admin@university.edu
- Password: admin

## Project Structure

- `gui_main.py`: Entry point for the GUI application
- `guiApp/`: Contains all GUI-related code
  - `nextjs_style_app.py`: Main application with Next.js-inspired styling
  - `views/`: UI components for different views
    - `modern_student_view.py`: Student dashboard view
    - `modern_admin_view.py`: Admin dashboard view
    - `login_window.py`: Login screen

## Design Choices

- **Color Scheme**: Primary blue (#0070f3) inspired by Next.js website
- **Card-Based UI**: Content organized in clean, bordered cards
- **Typography**: Clear hierarchy with different font sizes and weights
- **Consistent Styling**: Uniform button and input styles throughout the application

## Future Enhancements

- Implement all placeholder functionality
- Add more detailed student and course management
- Enhance reporting capabilities
- Add user profile management
- Implement dark mode