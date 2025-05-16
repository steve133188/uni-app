import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from UniSystemCLI.models.database import Database
from UniSystemCLI.models.subject import Subject
from UniSystemCLI.models.enrollment import Enrollment

class SubjectEnrollmentView(ttk.Frame):
    """A view for managing subjects and enrollments"""
    
    def __init__(self, parent, student=None, colors=None):
        super().__init__(parent)
        self.parent = parent
        self.student = student
        self.database = Database()
        
        # Use default colors if none provided
        self.colors = colors or {
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
        
        self.configure(style="Card.TFrame")
        self.create_widgets()
    
    def create_widgets(self):
        """Create the subject enrollment widgets"""
        # Main container
        main_frame = ttk.Frame(self, style="Card.TFrame")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Header
        header_label = ttk.Label(
            main_frame, 
            text="Subject Management",
            font=("Helvetica", 24, "bold"),
            foreground=self.colors['secondary']
        )
        header_label.pack(anchor="w", pady=(0, 20))
        
        # Create tabs for different views
        tab_control = ttk.Notebook(main_frame)
        
        # Available Subjects Tab
        available_tab = ttk.Frame(tab_control, style="Card.TFrame")
        tab_control.add(available_tab, text="Available Subjects")
        
        # My Enrollments Tab
        if self.student:
            enrollments_tab = ttk.Frame(tab_control, style="Card.TFrame")
            tab_control.add(enrollments_tab, text="My Enrollments")
        
        tab_control.pack(expand=True, fill="both")
        
        # Available Subjects Content
        self.setup_available_subjects_tab(available_tab)
        
        # My Enrollments Content (if student is logged in)
        if self.student:
            self.setup_enrollments_tab(enrollments_tab)
    
    def setup_available_subjects_tab(self, parent):
        """Setup the available subjects tab"""
        # Create frame for subject list
        subjects_frame = ttk.Frame(parent, style="Card.TFrame")
        subjects_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load and display subjects directly in the parent frame
        # The scrollbar is now handled in the load_subjects method
        self.load_subjects(subjects_frame)
    
    def setup_enrollments_tab(self, parent):
        """Setup the student enrollments tab"""
        # Create frame for enrollment list
        enrollments_frame = ttk.Frame(parent, style="Card.TFrame")
        enrollments_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Load and display enrollments directly in the parent frame
        # The scrollbar is now handled in the load_enrollments method
        self.load_enrollments(enrollments_frame)
    
    def load_subjects(self, parent):
        """Load and display all available subjects"""
        subjects = self.database.load_subjects()
        
        if not subjects:
            no_subjects_label = ttk.Label(
                parent,
                text="No subjects available",
                font=("Helvetica", 14),
                foreground=self.colors['text_secondary']
            )
            no_subjects_label.pack(pady=20)
            return
        
        # Create a treeview for better alignment and display
        columns = ("code", "name", "description", "actions")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # Configure column widths and headings
        tree.column("code", width=100, anchor="w")
        tree.column("name", width=200, anchor="w")
        tree.column("description", width=300, anchor="w")
        tree.column("actions", width=150, anchor="center")
        
        # Configure headings
        tree.heading("code", text="Code", anchor="w")
        tree.heading("name", text="Name", anchor="w")
        tree.heading("description", text="Description", anchor="w")
        tree.heading("actions", text="Actions", anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Store action buttons references
        self.action_buttons = {}
        
        # Display each subject
        for i, subject in enumerate(subjects):
            # Insert subject data
            item_id = tree.insert("", "end", values=(subject.code, subject.name, subject.description, ""))
            
            # Create a frame for action buttons that will be displayed in a separate window
            self.action_buttons[item_id] = (subject, self.create_action_buttons_for_subject(subject))
        
        # Bind click event to show action buttons
        tree.bind("<ButtonRelease-1>", lambda event: self.show_action_buttons(event, tree))
        
        # Add subject button (for admin only) - moved from setup_available_subjects_tab
        if not self.student:
            add_subject_btn = ttk.Button(
                parent,
                text="Add New Subject",
                style="Primary.TButton",
                command=self.show_add_subject_dialog
            )
            add_subject_btn.pack(pady=10, padx=10, anchor="e")
    
    def create_action_buttons_for_subject(self, subject):
        """Create action buttons for a subject"""
        # This function creates the buttons but doesn't display them yet
        buttons = []
        
        if self.student:
            # Check if student is already enrolled
            enrollment = self.database.get_enrollment(self.student.id, subject.id)
            if enrollment:
                buttons.append(("Enrolled", self.colors['success'], None))
                buttons.append(("Unenroll", "Secondary.TButton", lambda s=subject: self.unenroll_subject(s)))
            else:
                # Check if student has reached the maximum number of enrollments
                # Use database to get enrollments count instead of student.enrollments
                student_enrollments = self.database.get_enrollments_by_student_id(self.student.id)
                if len(student_enrollments) >= 4:
                    buttons.append(("Max Subjects", self.colors['error'], None))
                else:
                    buttons.append(("Enroll", "Primary.TButton", lambda s=subject: self.enroll_subject(s)))
        else:
            # Admin actions
            buttons.append(("Edit", "Secondary.TButton", lambda s=subject: self.show_edit_subject_dialog(s)))
            buttons.append(("Delete", "Secondary.TButton", lambda s=subject: self.delete_subject(s)))
        
        return buttons
    
    def show_action_buttons(self, event, tree):
        """Show action buttons when a row is clicked"""
        # Get the clicked item
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
        
        # Get the subject and buttons for this item
        subject, buttons = self.action_buttons.get(item_id, (None, []))
        if not subject:
            return
        
        # Create a popup window for the action buttons
        popup = tk.Toplevel(self)
        popup.title("Actions")
        popup.geometry("200x100")
        popup.transient(self)  # Make the window transient to the main window
        popup.grab_set()  # Make the window modal
        
        # Create a frame for the buttons
        button_frame = ttk.Frame(popup, style="Card.TFrame")
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add a label with the subject name
        ttk.Label(
            button_frame,
            text=f"Actions for {subject.code}",
            font=("Helvetica", 12, "bold"),
            foreground=self.colors['secondary']
        ).pack(pady=(0, 10))
        
        # Add the buttons
        for text, style, command in buttons:
            if command:  # It's a button
                btn = ttk.Button(button_frame, text=text, style=style, command=command)
                btn.pack(fill="x", pady=2)
                # Also add a command to close the popup when the button is clicked
                btn.configure(command=lambda cmd=command, p=popup: self.execute_and_close(cmd, p))
            else:  # It's a label
                ttk.Label(
                    button_frame,
                    text=text,
                    foreground=style  # style is actually a color in this case
                ).pack(fill="x", pady=2)
    
    def execute_and_close(self, command, popup):
        """Execute a command and close the popup"""
        command()
        popup.destroy()
            
        if self.student:
                # Check if student is already enrolled
                enrollment = self.database.get_enrollment(self.student.id, subject.id)
                if enrollment:
                    ttk.Label(
                        action_frame, 
                        text="Enrolled", 
                        foreground=self.colors['success']
                    ).pack(side="left", padx=5)
                    
                    unenroll_btn = ttk.Button(
                        action_frame,
                        text="Unenroll",
                        style="Secondary.TButton",
                        command=lambda s=subject: self.unenroll_subject(s)
                    )
                    unenroll_btn.pack(side="left", padx=5)
                else:
                    # Check if student has reached the maximum number of enrollments
                    if len(self.student.enrollments) >= 4:
                        ttk.Label(
                            action_frame, 
                            text="Max Subjects", 
                            foreground=self.colors['error']
                        ).pack(side="left", padx=5)
                    else:
                        enroll_btn = ttk.Button(
                            action_frame,
                            text="Enroll",
                            style="Primary.TButton",
                            command=lambda s=subject: self.enroll_subject(s)
                        )
                        enroll_btn.pack(side="left", padx=5)
        else:
                # Admin actions
                edit_btn = ttk.Button(
                    action_frame,
                    text="Edit",
                    style="Secondary.TButton",
                    command=lambda s=subject: self.edit_subject(s)
                )
                edit_btn.pack(side="left", padx=5)
                
                delete_btn = ttk.Button(
                    action_frame,
                    text="Delete",
                    style="Secondary.TButton",
                    command=lambda s=subject: self.delete_subject(s)
                )
                delete_btn.pack(side="left", padx=5)
            
            # Add separator after each subject except the last one
        if i < len(subjects) - 1:
                separator = ttk.Separator(parent, orient="horizontal")
                separator.pack(fill="x", padx=10, pady=5)
    
    def load_enrollments(self, parent):
        """Load and display student enrollments"""
        if not self.student:
            return
        
        enrollments = self.database.get_enrollments_by_student_id(self.student.id)
        
        if not enrollments:
            no_enrollments_label = ttk.Label(
                parent,
                text="You are not enrolled in any subjects",
                font=("Helvetica", 14),
                foreground=self.colors['text_secondary']
            )
            no_enrollments_label.pack(pady=20)
            return
        
        # Create a treeview for better alignment and display
        columns = ("code", "name", "status", "actions")
        tree = ttk.Treeview(parent, columns=columns, show="headings", height=15)
        
        # Configure column widths and headings
        tree.column("code", width=100, anchor="w")
        tree.column("name", width=200, anchor="w")
        tree.column("status", width=100, anchor="center")
        tree.column("actions", width=150, anchor="center")
        
        # Configure headings
        tree.heading("code", text="Code", anchor="w")
        tree.heading("name", text="Name", anchor="w")
        tree.heading("status", text="Status", anchor="center")
        tree.heading("actions", text="Actions", anchor="center")
        
        # Add scrollbar
        scrollbar = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=scrollbar.set)
        
        # Pack the treeview and scrollbar
        tree.pack(side="left", fill="both", expand=True, padx=10, pady=10)
        scrollbar.pack(side="right", fill="y", pady=10)
        
        # Store action buttons references
        self.enrollment_buttons = {}
        
        # Display each enrollment
        for i, enrollment in enumerate(enrollments):
            # Get the subject
            subject = self.database.get_subject(enrollment.subject_id)
            if not subject:
                continue
            
            # Insert enrollment data
            item_id = tree.insert("", "end", values=(subject.code, subject.name, "Enrolled", ""))
            
            # Create a reference to the subject for the action buttons
            self.enrollment_buttons[item_id] = subject
        
        # Bind click event to show action buttons
        tree.bind("<ButtonRelease-1>", lambda event: self.show_enrollment_actions(event, tree))
    
    def show_enrollment_actions(self, event, tree):
        """Show action buttons when an enrollment row is clicked"""
        # Get the clicked item
        item_id = tree.identify_row(event.y)
        if not item_id:
            return
        
        # Get the subject for this enrollment
        subject = self.enrollment_buttons.get(item_id)
        if not subject:
            return
        
        # Create a popup window for the action buttons
        popup = tk.Toplevel(self)
        popup.title("Enrollment Actions")
        popup.geometry("200x100")
        popup.transient(self)  # Make the window transient to the main window
        popup.grab_set()  # Make the window modal
        
        # Create a frame for the buttons
        button_frame = ttk.Frame(popup, style="Card.TFrame")
        button_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Add a label with the subject name
        ttk.Label(
            button_frame,
            text=f"Actions for {subject.code}",
            font=("Helvetica", 12, "bold"),
            foreground=self.colors['secondary']
        ).pack(pady=(0, 10))
        
        # Add the unenroll button
        unenroll_btn = ttk.Button(
            button_frame,
            text="Unenroll",
            style="Secondary.TButton"
        )
        unenroll_btn.pack(fill="x", pady=2)
        # Configure command to unenroll and close popup
        unenroll_btn.configure(command=lambda s=subject, p=popup: self.execute_unenroll_and_close(s, p))
    
    def execute_unenroll_and_close(self, subject, popup):
        """Unenroll from a subject and close the popup"""
        self.unenroll_subject(subject)
        popup.destroy()
    
    def show_add_subject_dialog(self):
        """Show dialog to add a new subject"""
        dialog = tk.Toplevel(self)
        dialog.title("Add New Subject")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self)  # Set to be on top of the parent window
        dialog.grab_set()  # Modal
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Dialog content
        content_frame = ttk.Frame(dialog, padding=20, style="Card.TFrame")
        content_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            content_frame, 
            text="Add New Subject", 
            font=("Helvetica", 16, "bold"),
            foreground=self.colors['secondary']
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Subject Code
        code_label = ttk.Label(content_frame, text="Subject Code:", foreground=self.colors['text_secondary'])
        code_label.pack(anchor="w", pady=(0, 5))
        
        code_entry = ttk.Entry(content_frame, width=30)
        code_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Subject Name
        name_label = ttk.Label(content_frame, text="Subject Name:", foreground=self.colors['text_secondary'])
        name_label.pack(anchor="w", pady=(0, 5))
        
        name_entry = ttk.Entry(content_frame, width=30)
        name_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Subject Description
        desc_label = ttk.Label(content_frame, text="Description:", foreground=self.colors['text_secondary'])
        desc_label.pack(anchor="w", pady=(0, 5))
        
        desc_entry = tk.Text(content_frame, width=30, height=4)
        desc_entry.pack(fill="x", pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(content_frame, style="Card.TFrame")
        button_frame.pack(fill="x", pady=(10, 0))
        
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            style="Secondary.TButton",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = ttk.Button(
            button_frame,
            text="Save",
            style="Primary.TButton",
            command=lambda: self.save_subject(code_entry.get(), name_entry.get(), desc_entry.get("1.0", "end-1c"), dialog)
        )
        save_btn.pack(side="right", padx=5)
    
    def save_subject(self, code, name, description, dialog):
        """Save a new subject"""
        if not code or not name:
            messagebox.showerror("Error", "Subject code and name are required")
            return
        
        # Create and save the new subject
        subject = Subject(name, code, description)
        self.database.add_subject(subject)
        
        # Close the dialog
        dialog.destroy()
        
        # Refresh the subject list
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
    
    def edit_subject(self, subject):
        """Edit an existing subject"""
        dialog = tk.Toplevel(self)
        dialog.title("Edit Subject")
        dialog.geometry("400x300")
        dialog.resizable(False, False)
        dialog.transient(self)  # Set to be on top of the parent window
        dialog.grab_set()  # Modal
        
        # Center the dialog
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")
        
        # Dialog content
        content_frame = ttk.Frame(dialog, padding=20, style="Card.TFrame")
        content_frame.pack(fill="both", expand=True)
        
        # Title
        title_label = ttk.Label(
            content_frame, 
            text="Edit Subject", 
            font=("Helvetica", 16, "bold"),
            foreground=self.colors['secondary']
        )
        title_label.pack(anchor="w", pady=(0, 20))
        
        # Subject Code
        code_label = ttk.Label(content_frame, text="Subject Code:", foreground=self.colors['text_secondary'])
        code_label.pack(anchor="w", pady=(0, 5))
        
        code_entry = ttk.Entry(content_frame, width=30)
        code_entry.insert(0, subject.code)
        code_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Subject Name
        name_label = ttk.Label(content_frame, text="Subject Name:", foreground=self.colors['text_secondary'])
        name_label.pack(anchor="w", pady=(0, 5))
        
        name_entry = ttk.Entry(content_frame, width=30)
        name_entry.insert(0, subject.name)
        name_entry.pack(fill="x", pady=(0, 15), ipady=5)
        
        # Subject Description
        desc_label = ttk.Label(content_frame, text="Description:", foreground=self.colors['text_secondary'])
        desc_label.pack(anchor="w", pady=(0, 5))
        
        desc_entry = tk.Text(content_frame, width=30, height=4)
        desc_entry.insert("1.0", subject.description)
        desc_entry.pack(fill="x", pady=(0, 15))
        
        # Buttons
        button_frame = ttk.Frame(content_frame, style="Card.TFrame")
        button_frame.pack(fill="x", pady=(10, 0))
        
        cancel_btn = ttk.Button(
            button_frame,
            text="Cancel",
            style="Secondary.TButton",
            command=dialog.destroy
        )
        cancel_btn.pack(side="right", padx=5)
        
        save_btn = ttk.Button(
            button_frame,
            text="Save",
            style="Primary.TButton",
            command=lambda: self.update_subject(subject, code_entry.get(), name_entry.get(), desc_entry.get("1.0", "end-1c"), dialog)
        )
        save_btn.pack(side="right", padx=5)
    
    def update_subject(self, subject, code, name, description, dialog):
        """Update an existing subject"""
        if not code or not name:
            messagebox.showerror("Error", "Subject code and name are required")
            return
        
        # Update the subject
        subject.code = code
        subject.name = name
        subject.description = description
        
        # Save all subjects
        subjects = self.database.load_subjects()
        for i, s in enumerate(subjects):
            if s.id == subject.id:
                subjects[i] = subject
                break
        self.database.save_subjects(subjects)
        
        # Close the dialog
        dialog.destroy()
        
        # Refresh the subject list
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
    
    def delete_subject(self, subject):
        """Delete a subject"""
        # Check if there are enrollments for this subject
        enrollments = self.database.get_enrollments_by_subject_id(subject.id)
        if enrollments:
            messagebox.showerror("Error", "Cannot delete subject with active enrollments")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", f"Are you sure you want to delete {subject.code}: {subject.name}?"):
            return
        
        # Delete the subject
        self.database.remove_subject(subject.id)
        
        # Refresh the subject list
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
    
    def enroll_subject(self, subject):
        """Enroll student in a subject"""
        if not self.student:
            return
        
        # Create a new enrollment
        enrollment = Enrollment(self.student.id, subject.id)
        
        # Add to student's enrollments
        success, message = self.student.enroll(enrollment)
        if not success:
            messagebox.showerror("Error", message)
            return
        
        # Save the enrollment to the database
        self.database.add_enrollment(enrollment)
        
        # Update the student in the database
        students = self.database.load_students()
        for i, s in enumerate(students):
            if s.id == self.student.id:
                students[i] = self.student
                break
        self.database.save_students(students)
        
        # Show success message
        messagebox.showinfo("Success", f"Successfully enrolled in {subject.code}: {subject.name}")
        
        # Refresh the view
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()
    
    def unenroll_subject(self, subject):
        """Unenroll a student from a subject"""
        if not self.student:
            return
        
        # Confirm unenrollment
        if not messagebox.askyesno("Confirm", f"Are you sure you want to unenroll from {subject.code}: {subject.name}?"):
            return
        
        # Remove from student's enrollments
        if not self.student.remove_enrollment(subject.id):
            messagebox.showerror("Error", "You are not enrolled in this subject")
            return
        
        # Remove the enrollment from the database
        self.database.remove_enrollment(self.student.id, subject.id)
        
        # Update the student in the database
        students = self.database.load_students()
        for i, s in enumerate(students):
            if s.id == self.student.id:
                students[i] = self.student
                break
        self.database.save_students(students)
        
        # Show success message
        messagebox.showinfo("Success", f"Successfully unenrolled from {subject.code}: {subject.name}")
        
        # Refresh the view - recreate all widgets to show updated data
        for widget in self.winfo_children():
            widget.destroy()
        self.create_widgets()