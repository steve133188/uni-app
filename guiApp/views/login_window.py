from tkinter import Frame, Label, Entry, Button, messagebox, Tk
from tkinter import ttk
from models.database import Database
from guiApp.views.student_dashboard import StudentDashboard

class LoginWindow(Frame):
    def __init__(self, master):
        super().__init__(master, bg="white")  # Set background color to white
        self.master = master
        self.database = Database()
        self.create_widgets()
        self.place(relx=0.5, rely=0.5, anchor="center")  # Center the frame in the window

    def create_widgets(self):
        style = ttk.Style()
        style.configure("TLabel", background="white", foreground="#323232", font=("Arial",16 ,"bold"))
        style.configure("TButton", foreground="white", background="white", font=("Arial", 16, "bold"), borderwidth=0, relief="flat", padding=0)
        style.configure("TEntry", foreground="white", background="white" ,font=("Arial", 16), borderwidth=1, relief="outline")  # No background color

        # Title label
        Label(self, text="Login to Your Account", bg="white", fg="#0f4beb", font=("Arial", 24, "bold")).grid(row=0, column=0, columnspan=2, pady=(0, 20))

        # Email label and entry
        Label(self, text="Email:", bg="white", fg="#323232", font=("Arial",16 ,"bold")).grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = ttk.Entry(self, style="TEntry")
        self.email_entry.grid(row=1, column=1, padx=10,  sticky="w")

        # Password label and entry
        Label(self, text="Password:", bg="white", fg="#323232", font=("Arial",16 ,"bold")).grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ttk.Entry(self, style="TEntry", show="*")
        self.password_entry.grid(row=2, column=1, padx=10, sticky="w")

        # Login button
        login_button = ttk.Button(self, text="Login", command=self.login, style="TButton", width=24, padding=0)
        login_button.grid(row=3, column=0, columnspan=2, pady=0, padx=0, ipadx=0, ipady=0)

    def login(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        student = self.database.get_student_by_email(email)
        if student and student.password == password:
            messagebox.showinfo("Login Successful", f"Welcome, {student.name}!")
            self.master.destroy()
            root = Tk()
            root.title("Student Dashboard")
            root.configure(bg="white")  # Set background color to white
            StudentDashboard(root, student)
            root.mainloop()
        else:
            messagebox.showerror("Login Failed", "Invalid email or password.")
