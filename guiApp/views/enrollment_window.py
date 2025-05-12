from tkinter import Frame, Label, Button, Listbox, messagebox

class EnrollmentWindow(Frame):
    def __init__(self, master):
        super().__init__(master)
        self.grid(padx=20, pady=20)  # Ensure the frame is displayed properly
        self.create_widgets()

    def create_widgets(self):
        Label(self, text="Subject Enrollment", font=("Helvetica", 16)).grid(row=0, column=0, columnspan=2, pady=10)

        Label(self, text="Available Subjects:", font=("Helvetica", 14)).grid(row=1, column=0, columnspan=2, pady=10)
        self.subject_listbox = Listbox(self, width=50, font=("Helvetica", 12))
        self.subject_listbox.grid(row=2, column=0, columnspan=2, pady=10)

        Button(self, text="Enroll", command=self.enroll, font=("Helvetica", 12)).grid(row=3, column=0, columnspan=2, pady=10)

    def enroll(self):
        messagebox.showinfo("Enroll", "Enroll functionality not implemented yet.")
