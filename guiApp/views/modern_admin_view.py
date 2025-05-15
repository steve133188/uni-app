import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from models.database import Database
from guiApp.views.base_view import BaseView

class ModernAdminView(BaseView):
    """A modern, Next.js inspired view for admin dashboard"""
    
    def __init__(self, parent, colors=None):
        super().__init__(parent, colors)
        self.database = Database()
        self.create_widgets()
    
    def create_widgets(self):
        """Create the admin dashboard widgets"""
        # Admin dashboard main container
        main_frame = ttk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Dashboard header
        self.create_header(main_frame, "Admin Dashboard")
        
        # Stats overview section
        stats_frame = self.create_card_frame(main_frame)
        stats_frame.pack(fill="x", pady=(0, 20))
        
        self.create_subheader(stats_frame, "System Overview")
        
        # Stats grid
        stats_grid = ttk.Frame(stats_frame)
        stats_grid.pack(fill="x")
        
        # Get actual stats
        students = self.database.load_students()
        student_count = len(students)
        
        # Create stat cards
        self.create_stat_card(stats_grid, "Total Students", str(student_count), 0, 0)
        self.create_stat_card(stats_grid, "Active Courses", "12", 0, 1)  # Placeholder value
        self.create_stat_card(stats_grid, "Enrollments", "45", 0, 2)  # Placeholder value
        
        # Configure grid columns
        stats_grid.columnconfigure(0, weight=1)
        stats_grid.columnconfigure(1, weight=1)
        stats_grid.columnconfigure(2, weight=1)
        
        # Admin actions section
        self.create_subheader(main_frame, "Administrative Actions")
        
        # Actions grid
        actions_grid = ttk.Frame(main_frame)
        actions_grid.pack(fill="both", expand=True)
        
        # Create action cards
        self.create_action_card(
            actions_grid,
            "Manage Students",
            "Add, edit, or remove student accounts",
            "manage_students_icon.png",  # Placeholder for icon
            self.manage_students,
            0, 0
        )
        
        self.create_action_card(
            actions_grid,
            "Manage Courses",
            "Create and manage course offerings",
            "manage_courses_icon.png",  # Placeholder for icon
            self.manage_courses,
            0, 1
        )
        
        self.create_action_card(
            actions_grid,
            "System Reports",
            "Generate and view system reports",
            "reports_icon.png",  # Placeholder for icon
            self.view_reports,
            1, 0
        )
        
        self.create_action_card(
            actions_grid,
            "Database Management",
            "Backup, restore, or clear database",
            "database_icon.png",  # Placeholder for icon
            self.manage_database,
            1, 1
        )
        
        # Configure grid columns
        actions_grid.columnconfigure(0, weight=1)
        actions_grid.columnconfigure(1, weight=1)
    
    # Using create_card_frame from BaseView
    
    def create_stat_card(self, parent, title, value, row, col):
        """Create a statistics card"""
        card = self.create_card_frame(parent, padding=(15, 15))
        card.grid(row=row, column=col, padx=10, pady=10, sticky="ew")
        
        # Stat title
        self.create_label(
            card, 
            title,
            font_size=14,
            color_key='text_secondary',
            anchor="w"
        )
        
        # Stat value
        self.create_label(
            card, 
            value,
            font_size=24,
            is_bold=True,
            color_key='primary',
            anchor="w"
        ).pack(pady=(5, 0))
    
    def create_action_card(self, parent, title, description, icon_path, command, row, col):
        """Create an action card"""
        card = self.create_card_frame(parent, padding=(20, 20))
        card.grid(row=row, column=col, padx=10, pady=10, sticky="nsew")
        
        # Card content frame
        content = ttk.Frame(card)
        content.pack(fill="both", expand=True)
        
        # Card title
        self.create_subheader(content, title, padding=(0, 0))
        
        # Card description
        self.create_label(
            content, 
            description,
            color_key='text_secondary'
        ).configure(wraplength=250)
        self.create_label(content, "").pack(pady=(5, 15))
        
        # Action button
        self.create_button(
            content,
            "Open",
            command,
            "Primary.TButton"
        ).pack(anchor="w", side=None)
    
    def manage_students(self):
        """Open the student management interface"""
        # This would be implemented to show student management
        print("Opening student management")
        
        # Get students from database
        students = self.database.load_students()
        
        # Create a new window to display students
        student_window = tk.Toplevel(self.parent)
        student_window.title("Student Management")
        student_window.geometry("800x600")
        student_window.configure(bg=self.colors['background'])
        
        # Create a frame for the student list
        frame = ttk.Frame(student_window, padding=(20, 20))
        frame.pack(fill="both", expand=True)
        
        # Header
        header = ttk.Label(
            frame, 
            text="Student Management",
            font=("Arial", 20, "bold"),
            foreground=self.colors['secondary']
        )
        header.pack(anchor="w", pady=(0, 20))
        
        # Create a treeview for students
        columns = ("id", "name", "email")
        tree = ttk.Treeview(frame, columns=columns, show="headings")
        
        # Define headings
        tree.heading("id", text="ID")
        tree.heading("name", text="Name")
        tree.heading("email", text="Email")
        
        # Define column widths
        tree.column("id", width=100)
        tree.column("name", width=200)
        tree.column("email", width=300)
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        tree.pack(fill="both", expand=True)
        
        # Add students to the treeview
        for student in students:
            tree.insert("", "end", values=(student.id, student.name, student.email))
        
        # Add buttons for actions
        button_frame = ttk.Frame(frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        add_btn = ttk.Button(
            button_frame,
            text="Add Student",
            style="Primary.TButton",
            command=self.add_student
        )
        add_btn.pack(side="left", padx=(0, 10))
        
        edit_btn = ttk.Button(
            button_frame,
            text="Edit Selected",
            style="Secondary.TButton",
            command=lambda: self.edit_student(tree)
        )
        edit_btn.pack(side="left", padx=(0, 10))
        
        delete_btn = ttk.Button(
            button_frame,
            text="Delete Selected",
            style="Secondary.TButton",
            command=lambda: self.delete_student(tree)
        )
        delete_btn.pack(side="left")
    
    def add_student(self):
        """Add a new student"""
        print("Adding a new student")
    
    def edit_student(self, tree):
        """Edit the selected student"""
        selected = tree.selection()
        if selected:
            student_id = tree.item(selected[0], "values")[0]
            print(f"Editing student with ID: {student_id}")
    
    def delete_student(self, tree):
        """Delete the selected student"""
        selected = tree.selection()
        if selected:
            student_id = tree.item(selected[0], "values")[0]
            print(f"Deleting student with ID: {student_id}")
    
    def manage_courses(self):
        """Open the course management interface"""
        print("Opening course management")
    
    def view_reports(self):
        """Open the reports interface"""
        print("Opening reports")
    
    def manage_database(self):
        """Open the database management interface"""
        print("Opening database management")
        
        # Create a new window for database management
        db_window = tk.Toplevel(self.parent)
        db_window.title("Database Management")
        db_window.geometry("600x400")
        db_window.configure(bg=self.colors['background'])
        
        # Create a frame for the database options
        frame = ttk.Frame(db_window, padding=(20, 20))
        frame.pack(fill="both", expand=True)
        
        # Header
        header = ttk.Label(
            frame, 
            text="Database Management",
            font=("Arial", 20, "bold"),
            foreground=self.colors['secondary']
        )
        header.pack(anchor="w", pady=(0, 20))
        
        # Warning message
        warning = ttk.Label(
            frame, 
            text="Warning: These operations can result in data loss. Please proceed with caution.",
            font=("Arial", 12),
            foreground=self.colors['error'],
            wraplength=500
        )
        warning.pack(anchor="w", pady=(0, 20))
        
        # Buttons for database actions
        backup_btn = ttk.Button(
            frame,
            text="Backup Database",
            style="Primary.TButton",
            command=self.backup_database
        )
        backup_btn.pack(anchor="w", pady=(0, 10), fill="x")
        
        restore_btn = ttk.Button(
            frame,
            text="Restore Database",
            style="Secondary.TButton",
            command=self.restore_database
        )
        restore_btn.pack(anchor="w", pady=(0, 10), fill="x")
        
        clear_btn = ttk.Button(
            frame,
            text="Clear Database",
            style="Secondary.TButton",
            command=self.clear_database
        )
        clear_btn.pack(anchor="w", fill="x")
    
    def backup_database(self):
        """Backup the database"""
        print("Backing up database")
    
    def restore_database(self):
        """Restore the database from backup"""
        print("Restoring database")
    
    def clear_database(self):
        """Clear the database"""
        result = self.database.clear()
        if result:
            print("Database cleared successfully")
        else:
            print("Failed to clear database")