from tkinter import Tk
from views.login_window import LoginWindow

if __name__ == "__main__":
    root = Tk()
    root.title("University System - Login")
    root.geometry("720x480")
    root.configure(background="white")  # Set the background color of the main window to white
    app = LoginWindow(root)
    root.mainloop()
