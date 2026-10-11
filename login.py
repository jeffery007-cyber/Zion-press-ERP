import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from modules.dashboard import DashboardWindow
from database.db import Database


class LoginWindow:

    def __init__(self):

        self.database = Database()

        self.root = ttk.Window(themename="darkly")

        self.root.title("PressFlow ERP - Zion Press")
        self.root.geometry("500x450")
        self.root.resizable(False, False)

        self.center_window()

        self.create_widgets()

        self.root.mainloop()

    def center_window(self):

        self.root.update_idletasks()

        width = 500
        height = 450

        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)

        self.root.geometry(f"{width}x{height}+{x}+{y}")

    def create_widgets(self):

        ttk.Label(
            self.root,
            text="PressFlow ERP",
            font=("Segoe UI", 24, "bold")
        ).pack(pady=(40, 5))

        ttk.Label(
            self.root,
            text="Installed for Zion Press",
            font=("Segoe UI", 11)
        ).pack()

        ttk.Separator(self.root).pack(fill="x", padx=30, pady=25)

        ttk.Label(
            self.root,
            text="Username"
        ).pack(anchor="w", padx=50)

        self.username_entry = ttk.Entry(
            self.root,
            width=35
        )

        self.username_entry.pack(pady=5)

        ttk.Label(
            self.root,
            text="Password"
        ).pack(anchor="w", padx=50)

        self.password_entry = ttk.Entry(
            self.root,
            show="*",
            width=35
        )

        self.password_entry.pack(pady=5)

        ttk.Button(
            self.root,
            text="Login",
            bootstyle="success",
            command=self.login
        ).pack(pady=30)

        ttk.Button(
            self.root,
            text="Exit",
            bootstyle="danger",
            command=self.root.destroy
        ).pack()

    def login(self):

        username = self.username_entry.get()
        password = self.password_entry.get()

        role = self.database.validate_login(username, password)

        if role:
            print("LOGIN SUCCESS")
            self.root.withdraw()
            DashboardWindow(role)
            

        else:

            messagebox.showerror(
                "Login Failed",
                "Invalid Username or Password."
            )