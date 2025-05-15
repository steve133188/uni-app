import tkinter as tk
from tkinter import ttk
import sys
import os

# Add parent directory to path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

class BaseView(ttk.Frame):
    """A base view class with common styling and utility methods for all views"""
    
    def __init__(self, parent, colors=None):
        super().__init__(parent)
        self.parent = parent
        
        # Use default colors if none provided
        self.colors = colors or {
            'primary': '#0070f3',      # Next.js blue
            'secondary': '#000000',    # Black
            'background': '#ffffff',   # White
            'light_gray': '#ffffff',   # White background
            'border': '#eaeaea',       # Border color
            'success': '#0070f3',      # Success color
            'error': '#ff0000',        # Error color
            'text': '#000000',         # Text color
            'text_secondary': '#666666' # Secondary text color
        }
        
        self.configure(style="Card.TFrame")
    
    def create_card_frame(self, parent, padding=(20, 20)):
        """Create a card-style frame with shadow effect"""
        # Create frame with border
        frame = ttk.Frame(
            parent,
            borderwidth=1,
            relief="solid"
        )
        
        # Style the frame
        frame.configure(padding=padding)
        
        return frame
    
    def create_header(self, parent, text, font_size=24, padding=(0, 20)):
        """Create a standard header with consistent styling"""
        header = ttk.Label(
            parent, 
            text=text,
            font=("Arial", font_size, "bold"),
            foreground=self.colors['secondary']
        )
        header.pack(anchor="w", pady=padding)
        return header
    
    def create_subheader(self, parent, text, font_size=16, padding=(0, 10)):
        """Create a standard subheader with consistent styling"""
        subheader = ttk.Label(
            parent, 
            text=text,
            font=("Arial", font_size, "bold"),
            foreground=self.colors['secondary']
        )
        subheader.pack(anchor="w", pady=padding)
        return subheader
    
    def create_label(self, parent, text, font_size=12, is_bold=False, color_key='text', anchor="w"):
        """Create a standard label with consistent styling"""
        font_weight = "bold" if is_bold else ""
        label = ttk.Label(
            parent, 
            text=text,
            font=("Arial", font_size, font_weight),
            foreground=self.colors[color_key]
        )
        label.pack(anchor=anchor)
        return label
    
    def create_button(self, parent, text, command, style="Primary.TButton", side="left", padx=(0, 10)):
        """Create a standard button with consistent styling"""
        button = ttk.Button(
            parent, 
            text=text,
            style=style,
            command=command
        )
        button.pack(side=side, padx=padx)
        return button