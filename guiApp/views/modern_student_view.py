import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from guiApp.views.base_view import BaseView

class ModernStudentView(BaseView):
    """A modern, Next.js inspired view for student information"""
    
    def __init__(self, parent, student, colors=None):
        super().__init__(parent, colors)
        self.student = student
        self.create_widgets()
    
    def create_widgets(self):
        """Create the student view widgets"""
        # Student profile section
        profile_frame = ttk.Frame(self)
        profile_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Student name and ID
        self.create_header(profile_frame, self.student.name, padding=(0, 5))
        
        self.create_label(
            profile_frame, 
            f"Student ID: {self.student.id}",
            font_size=14,
            color_key='text_secondary',
            anchor="w"
        ).pack(pady=(0, 20))
        
        # Student details in a card
        details_frame = self.create_card_frame(profile_frame)
        details_frame.pack(fill="both", expand=True, pady=10)
        
        # Email
        email_container = ttk.Frame(details_frame)
        email_container.pack(fill="x", pady=5)
        
        email_label = ttk.Label(
            email_container, 
            text="Email:",
            font=("Arial", 12, "bold"),
            foreground=self.colors['text_secondary']
        )
        email_label.pack(side="left", padx=(0, 10))
        
        email_value = ttk.Label(
            email_container, 
            text=self.student.email,
            font=("Arial", 12),
            foreground=self.colors['text']
        )
        email_value.pack(side="left")
        
        # Enrolled subjects
        self.create_subheader(details_frame, "Enrolled Subjects", padding=(20, 10))
        
        # Check if student has subjects
        if hasattr(self.student, 'subjects') and self.student.subjects:
            # Create a scrollable frame for subjects
            subjects_container = ttk.Frame(details_frame)
            subjects_container.pack(fill="both", expand=True)
            
            # Create a canvas for scrolling
            canvas = tk.Canvas(subjects_container, highlightthickness=0)
            scrollbar = ttk.Scrollbar(subjects_container, orient="vertical", command=canvas.yview)
            
            # Configure the canvas
            canvas.configure(yscrollcommand=scrollbar.set)
            canvas.pack(side="left", fill="both", expand=True)
            scrollbar.pack(side="right", fill="y")
            
            # Create a frame inside the canvas
            subjects_frame = ttk.Frame(canvas)
            canvas.create_window((0, 0), window=subjects_frame, anchor="nw")
            
            # Add subject cards
            for i, subject in enumerate(self.student.subjects):
                self.create_subject_card(subjects_frame, subject, i)
            
            # Update the canvas scroll region
            subjects_frame.bind(
                "<Configure>",
                lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
            )
        else:
            # No subjects message
            self.create_label(
                details_frame, 
                "Not enrolled in any subjects",
                color_key='text_secondary'
            ).pack(anchor="w", pady=10)
    
    # Using create_card_frame from BaseView
    
    def create_subject_card(self, parent, subject, index):
        """Create a card for a subject"""
        # Create a card frame
        card = self.create_card_frame(parent, padding=(15, 15))
        card.pack(fill="x", pady=5)
        
        # Subject code and name
        subject_header = ttk.Frame(card)
        subject_header.pack(fill="x")
        
        # Subject code with primary color
        self.create_label(
            subject_header, 
            subject.code,
            font_size=12,
            is_bold=True,
            color_key='primary'
        ).pack(side="left")
        
        # Subject name with secondary color
        self.create_label(
            subject_header, 
            subject.name,
            font_size=14,
            is_bold=True,
            color_key='secondary'
        ).pack(side="left", padx=(10, 0))
        
        # Subject description
        if hasattr(subject, 'description') and subject.description:
            self.create_label(
                card, 
                subject.description,
                font_size=12,
                color_key='text'
            ).configure(wraplength=500)
            # Add some padding after description
            ttk.Frame(card).pack(pady=(10, 0))
        
        # Subject details
        details_frame = ttk.Frame(card)
        details_frame.pack(fill="x", pady=(10, 0))
        
        # Credits
        if hasattr(subject, 'credits'):
            self.create_label(
                details_frame, 
                f"Credits: {subject.credits}",
                font_size=12,
                color_key='text_secondary'
            ).pack(side="left", padx=(0, 20))
        
        # Instructor
        if hasattr(subject, 'instructor') and subject.instructor:
            self.create_label(
                details_frame, 
                f"Instructor: {subject.instructor}",
                font_size=12,
                color_key='text_secondary'
            ).pack(side="left")
        
        # Action buttons
        actions_frame = ttk.Frame(card)
        actions_frame.pack(fill="x", pady=(15, 0))
        
        self.create_button(
            actions_frame, 
            "View Details",
            lambda: self.view_subject_details(subject),
            "Primary.TButton"
        )
        
        self.create_button(
            actions_frame, 
            "Unenroll",
            lambda: self.unenroll_subject(subject),
            "Secondary.TButton"
        )
    
    def view_subject_details(self, subject):
        """View details of a subject"""
        # This would be implemented to show a detailed view of the subject
        print(f"Viewing details for {subject.name}")
    
    def unenroll_subject(self, subject):
        """Unenroll from a subject"""
        # This would be implemented to unenroll the student from the subject
        print(f"Unenrolling from {subject.name}")