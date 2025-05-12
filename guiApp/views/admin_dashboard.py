from tkinter import Frame, Label, Button, messagebox

class AdminDashboard(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(padx=20, pady=20)  # Ensure the frame is displayed properly
        self.create_widgets()

    def create_widgets(self):
        Label(self, text="Welcome to the Admin Dashboard", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        Button(self, text="Clear Database", command=self.clear_database, font=("Helvetica", 12)).grid(row=1, column=0, padx=10, pady=10)
        Button(self, text="Show All Students", command=self.show_students, font=("Helvetica", 12)).grid(row=1, column=1, padx=10, pady=10)

    def clear_database(self):
        messagebox.showinfo("Clear Database", "Clear database functionality not implemented yet.")

    def show_students(self):
        messagebox.showinfo("Show Students", "Show students functionality not implemented yet.")
