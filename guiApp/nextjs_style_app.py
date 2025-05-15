import tkinter as tk
from tkinter import ttk, font
import os
import sys

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from models.database import Database
from models.admin_database import AdminDatabase

class NextJSStyleApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("University Management")
        self.geometry("1024x768")
        self.configure(bg="#FFFFFF")
        self.minsize(800, 600)
        
        # Set window appearance to be more minimal
        if os.name == 'nt':  # Windows
            self.iconbitmap(default="")
        self.option_add("*Font", "Helvetica 14")
        
        # Configure fonts and styles
        self.configure_styles()
        
        # Initialize databases
        self.student_db = Database()
        self.admin_db = AdminDatabase()
        
        # Show login screen
        self.show_login()
    
    def configure_styles(self):
        """Configure the application styles to match Apple's minimal design aesthetics"""
        # Configure default font - Apple uses SF Pro but we'll use system fonts
        default_font = font.nametofont("TkDefaultFont")
        default_font.configure(family="Helvetica", size=12)
        
        # Configure styles
        style = ttk.Style(self)
        
        # Configure colors - Apple's minimal color palette
        # This color palette will be used across all views
        self.colors = {
            'primary': '#007AFF',      # Apple blue
            'secondary': '#1D1D1F',    # Apple dark gray (almost black)
            'background': '#FFFFFF',   # Pure white background
            'light_gray': '#F5F5F7',   # Very light gray for subtle backgrounds
            'border': '#D2D2D7',       # Light border color
            'success': '#34C759',      # Apple green
            'error': '#FF3B30',        # Apple red
            'text': '#1D1D1F',         # Main text color (almost black)
            'text_secondary': '#86868B' # Secondary text color (medium gray)
        }
        
        # Configure button styles - Apple style
        style.configure(
            "Primary.TButton",
            font=("Helvetica", 12),
            background=self.colors['primary'],
            foreground=self.colors['primary'],
            borderwidth=0,
            focusthickness=0,
            padding=(12, 12),
            focuscolor=self.colors['primary']
        )
        style.map(
            "Primary.TButton",
            background=[("active", "#0069D9")],  # Slightly darker when pressed
            relief=[("pressed", "flat")]
        )
        
        # Configure secondary button style - Apple style
        style.configure(
            "Secondary.TButton",
            font=("Helvetica", 12),
            background=self.colors['light_gray'],
            foreground=self.colors['primary'],
            borderwidth=0,
            padding=(12, 6),
            relief="flat"
        )
        style.map(
            "Secondary.TButton",
            background=[("active", "#E5E5EA")],  # Slightly darker when pressed
            relief=[("pressed", "flat")]
        )
        
        # Configure label styles - Apple style
        style.configure(
            "Title.TLabel",
            font=("Helvetica", 32, "bold"),
            background=self.colors['background'],
            foreground=self.colors['secondary']
        )

        style.map("Title.TLabel", foreground=[("active", self.colors['secondary'])])

        style.configure(
            "Subtitle.TLabel",
            font=("Helvetica", 20,"bold"),
            background=self.colors['background'],
            foreground=self.colors['secondary']
        )

        style.configure(
            "Body.TLabel",
            font=("Helvetica", 20,"bold"),
            background=self.colors['background'],
            foreground=self.colors['text']
        )
        
        style.configure(
            "Subtitle.TLabel",
            font=("Helvetica", 20,"bold"),
            background=self.colors['background'],
            foreground=self.colors['secondary']
        )
        
        style.configure(
            "Body.TLabel",
            font=("Helvetica", 20,"bold"),
            background=self.colors['background'],
            foreground=self.colors['text']
        )
        
        # Configure entry style - Apple style
        style.configure(
            "Custom.TEntry",
            fieldbackground=self.colors['background'],
            bordercolor=self.colors['border'],
            lightcolor=self.colors['border'],
            darkcolor=self.colors['border'],
            borderwidth=0,
            font=("Helvetica", 14)
        )
        
        # Configure frame styles - Apple style (minimal borders)
        style.configure(
            "Card.TFrame",
            background=self.colors['background'],
            borderwidth=0,
            relief="flat"
        )
    
    def create_card_frame(self, parent, padding=(16, 16)):
        """Create a card-style frame with Apple's minimal design"""
        # Import BaseView here to avoid circular imports
        from guiApp.views.base_view import BaseView
        
        # Create outer frame with minimal styling
        outer_frame = ttk.Frame(parent, style="Card.TFrame")
        
        # Create inner frame with padding
        inner_frame = ttk.Frame(outer_frame, style="Card.TFrame")
        inner_frame.pack(padx=padding[0], pady=padding[1], fill="both", expand=True)
        
        return outer_frame, inner_frame
    
    def show_login(self):
        """Show the login screen with Apple-inspired minimal design"""
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create main frame with clean white background
        main_frame = ttk.Frame(self, style="Card.TFrame")
        main_frame.pack(fill="both", expand=True)
        
        # Create login form with centered, minimal design
        login_frame = ttk.Frame(main_frame, style="Card.TFrame")
        login_frame.place(relx=0.5, rely=0.5, anchor="center")
        
        # Title - larger, cleaner font
        title_label = ttk.Label(login_frame, text="University Management", style="Title.TLabel", font=("Helvetica", 24, "bold") )
        title_label.grid(row=0, column=0, columnspan=2, pady=(0, 40), sticky="n")
        
        # Subtitle - lighter weight
        subtitle_label = ttk.Label(login_frame, text="Sign In", style="Subtitle.TLabel",font=("Helvetica", 18, "bold"))
        subtitle_label.grid(row=1, column=0, columnspan=2, pady=(0, 30), sticky="n")
        
        # Email field - minimal styling
        email_label = ttk.Label(login_frame, text="Email", style="Body.TLabel", foreground=self.colors['text_secondary'])
        email_label.grid(row=2, column=0, columnspan=2, sticky="w", pady=(0, 8))
        
        self.email_entry = ttk.Entry(login_frame, width=36, style="Custom.TEntry")
        self.email_entry.grid(row=3, column=0, columnspan=2, pady=(0, 24), ipady=8)
        
        # Password field - minimal styling
        password_label = ttk.Label(login_frame, text="Password", style="Body.TLabel", foreground=self.colors['text_secondary'])
        password_label.grid(row=4, column=0, columnspan=2, sticky="w", pady=(0, 8))
        
        self.password_entry = ttk.Entry(login_frame, width=36, style="Custom.TEntry", show="•")
        self.password_entry.grid(row=5, column=0, columnspan=2, pady=(0, 32), ipady=8)
        
        # Login buttons - Apple-style buttons
        student_login_btn = ttk.Button(
            login_frame, 
            text="Student Sign In", 
            style="Secondary.TButton",
            command=self.student_login
        )
        student_login_btn.grid(row=6, column=0, columnspan=2, pady=(0, 16), sticky="ew")
        
        # admin_login_btn = ttk.Button(
        #     login_frame, 
        #     text="Admin Sign In", 
        #     style="Secondary.TButton",
        #     command=self.admin_login
        # )
        # admin_login_btn.grid(row=7, column=0, columnspan=2, pady=(0, 0), sticky="ew")
    
    def student_login(self):
        """Handle student login"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        student = self.student_db.get_student_by_email(email)
        if student and student.password == password:
            self.show_student_dashboard(student)
        else:
            self.show_error("Invalid email or password")
    
    def admin_login(self):
        """Handle admin login"""
        # This is a placeholder - would need to implement admin authentication
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        
        # For demo purposes, allow login with admin/admin
        if email == "admin@university.edu" and password == "admin":
            self.show_admin_dashboard()
        else:
            self.show_error("Invalid admin credentials")
    
    def show_error(self, message):
        """Show error message with Apple-style minimal design"""
        # Create a frame with subtle background
        error_frame = ttk.Frame(self)
        error_frame.configure(padding=(16, 8))
        error_frame.place(relx=0.5, rely=0.7, anchor="center")
        
        # Error message with Apple-style typography
        error_label = ttk.Label(
            error_frame, 
            text=message, 
            foreground=self.colors['error'],
            background=self.colors['background'],
            font=("Helvetica", 14)
        )
        error_label.pack()
        
        # Remove after 3 seconds
        self.after(3000, error_frame.destroy)
    
    def show_student_dashboard(self, student):
        """Show the student dashboard"""
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create main container
        container = ttk.Frame(self, style="Card.TFrame")
        container.pack(fill="both", expand=True)
        
        # Create header with Apple-style minimal design
        header = ttk.Frame(container, style="Card.TFrame")
        header.pack(fill="x", padx=0, pady=0)
        
        # Header content - clean typography
        logo_label = ttk.Label(header, text="University", style="Title.TLabel")
        logo_label.pack(side="left", padx=24, pady=16)
        
        # User info and logout - Apple-style minimal design
        user_frame = ttk.Frame(header, style="Card.TFrame")
        user_frame.pack(side="right", padx=24, pady=16)
        
        user_label = ttk.Label(user_frame, text=f"{student.name}", style="Body.TLabel")
        user_label.pack(side="left", padx=(0, 16))
        
        logout_btn = ttk.Button(
            user_frame, 
            text="Sign Out", 
            style="Secondary.TButton",
            command=self.show_login
        )
        logout_btn.pack(side="right")
        
        # Main content area with cards - Apple-style minimal design
        content = ttk.Frame(container, style="Card.TFrame")
        content.pack(fill="both", expand=True, padx=32, pady=32)
        
        # Dashboard title - clean typography
        dashboard_title = ttk.Label(content, text="Dashboard", style="Subtitle.TLabel")
        dashboard_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 32))
        
        # Create feature cards
        self.create_feature_card(
            content, 
            0, 0, 
            "View Subjects", 
            "Browse all available subjects and your enrollments",
            lambda: self.show_subject_enrollment_view(student)
        )
        
        self.create_feature_card(
            content, 
            0, 1, 
            "Enroll in Subject", 
            "Register for new subjects and courses",
            lambda: self.show_subject_enrollment_view(student)
        )
        
        self.create_feature_card(
            content, 
            0, 2, 
            "View Grades", 
            "Check your academic performance and grades",
            lambda: self.show_subject_enrollment_view(student)
        )
        
        self.create_feature_card(
            content, 
            1, 0, 
            "Update Profile", 
            "Update your personal information and settings",
            lambda: self.show_message("Update Profile clicked")
        )
        
        self.create_feature_card(
            content, 
            1, 1, 
            "Change Password", 
            "Update your account password",
            lambda: self.show_message("Change Password clicked")
        )
        
        self.create_feature_card(
            content, 
            1, 2, 
            "Contact Support", 
            "Get help with any issues or questions",
            lambda: self.show_message("Contact Support clicked")
        )
        
        # Configure grid
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)
    
    def create_feature_card(self, parent, row, col, title, description, command):
        """Create a feature card with Apple's minimal design"""
        # Create a clean, minimal card with subtle styling
        card_outer, card = self.create_card_frame(parent)
        card_outer.grid(row=row+1, column=col, padx=16, pady=16, sticky="nsew")
        
        # Card title - clean typography
        card_title = ttk.Label(card, text=title, style="Subtitle.TLabel")
        card_title.pack(anchor="w", pady=(0, 12))
        
        # Card description - lighter weight text
        card_desc = ttk.Label(
            card, 
            text=description, 
            style="Body.TLabel",
            foreground=self.colors['text_secondary'],
            wraplength=220
        )
        card_desc.pack(anchor="w", pady=(0, 20))
        
        # Card button - Apple-style minimal button
        card_btn = ttk.Button(
            card, 
            text="Open", 
            style="Primary.TButton",
            command=command
        )
        card_btn.pack(anchor="w")
    
    def show_admin_dashboard(self):
        """Show the admin dashboard"""
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create main container
        container = ttk.Frame(self, style="Card.TFrame")
        container.pack(fill="both", expand=True)
        
        # Create header
        header = ttk.Frame(container, style="Card.TFrame")
        header.pack(fill="x", padx=0, pady=0)
        
        # Header content
        logo_label = ttk.Label(header, text="University System - Admin", style="Title.TLabel")
        logo_label.pack(side="left", padx=20, pady=10)
        
        # User info and logout
        user_frame = ttk.Frame(header, style="Card.TFrame")
        user_frame.pack(side="right", padx=20, pady=10)
        
        user_label = ttk.Label(user_frame, text="Administrator", style="Body.TLabel")
        user_label.pack(side="left", padx=(0, 10))
        
        logout_btn = ttk.Button(
            user_frame, 
            text="Logout", 
            style="Secondary.TButton",
            command=self.show_login
        )
        logout_btn.pack(side="right")
        
        # Main content area with cards
        content = ttk.Frame(container, style="Card.TFrame")
        content.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Dashboard title
        dashboard_title = ttk.Label(content, text="Admin Dashboard", style="Subtitle.TLabel")
        dashboard_title.grid(row=0, column=0, columnspan=3, sticky="w", pady=(0, 20))
        
        # Create feature cards
        self.create_feature_card(
            content, 
            0, 0, 
            "Manage Students", 
            "Add, edit, or remove student accounts",
            lambda: self.show_message("Manage Students clicked")
        )
        
        self.create_feature_card(
            content, 
            0, 1, 
            "Manage Subjects", 
            "Create and manage course offerings",
            lambda: self.show_subject_enrollment_view(None)  # None indicates admin mode
        )
        
        self.create_feature_card(
            content, 
            0, 2, 
            "View Reports", 
            "Generate and view system reports",
            lambda: self.show_message("View Reports clicked")
        )
        
        self.create_feature_card(
            content, 
            1, 0, 
            "System Settings", 
            "Configure system parameters and options",
            lambda: self.show_message("System Settings clicked")
        )
        
        self.create_feature_card(
            content, 
            1, 1, 
            "Clear Database", 
            "Reset the system database",
            lambda: self.clear_database()
        )
        
        self.create_feature_card(
            content, 
            1, 2, 
            "Backup Data", 
            "Create system backups and restore points",
            lambda: self.show_message("Backup Data clicked")
        )
        
        # Configure grid
        content.grid_columnconfigure(0, weight=1)
        content.grid_columnconfigure(1, weight=1)
        content.grid_columnconfigure(2, weight=1)
    
    def show_message(self, message, error=False):
        """Show a temporary message"""
        # This is a placeholder for actual functionality
        message_label = ttk.Label(
            self, 
            text=message, 
            foreground=self.colors['error'] if error else self.colors['primary'],
            background=self.colors['background'],
            font=("Helvetica", 12),
            padding=10
        )
        message_label.place(relx=0.5, rely=0.9, anchor="center")
        self.after(2000, message_label.destroy)  # Remove after 2 seconds

    def show_subject_enrollment_view(self, student):
        """Show the subject enrollment view"""
        # Import here to avoid circular imports
        from guiApp.views.subject_enrollment_view import SubjectEnrollmentView
        
        # Clear any existing widgets
        for widget in self.winfo_children():
            widget.destroy()
        
        # Create main container
        container = ttk.Frame(self, style="Card.TFrame")
        container.pack(fill="both", expand=True)
        
        # Create header
        header = ttk.Frame(container, style="Card.TFrame")
        header.pack(fill="x", padx=0, pady=0)
        
        # Header content
        if student:
            logo_label = ttk.Label(header, text="University - Subjects", style="Title.TLabel")
        else:
            logo_label = ttk.Label(header, text="University System - Subject Management", style="Title.TLabel")
        logo_label.pack(side="left", padx=20, pady=10)
        
        # User info and back button
        user_frame = ttk.Frame(header, style="Card.TFrame")
        user_frame.pack(side="right", padx=20, pady=10)
        
        if student:
            user_label = ttk.Label(user_frame, text=f"{student.name}", style="Body.TLabel")
            user_label.pack(side="left", padx=(0, 10))
            
            back_btn = ttk.Button(
                user_frame, 
                text="Back to Dashboard", 
                style="Secondary.TButton",
                command=lambda: self.show_student_dashboard(student)
            )
        else:
            user_label = ttk.Label(user_frame, text="Administrator", style="Body.TLabel")
            user_label.pack(side="left", padx=(0, 10))
            
            back_btn = ttk.Button(
                user_frame, 
                text="Back to Dashboard", 
                style="Secondary.TButton",
                command=self.show_admin_dashboard
            )
        back_btn.pack(side="right")
        
        # Create and pack the subject enrollment view
        subject_view = SubjectEnrollmentView(container, student, self.colors)
        subject_view.pack(fill="both", expand=True)
    
    def clear_database(self):
        """Clear the database and show confirmation"""
        if self.student_db.clear():
            self.show_message("Database cleared successfully")
        else:
            self.show_message("Error clearing database", error=True)

if __name__ == "__main__":
    app = NextJSStyleApp()
    app.mainloop()