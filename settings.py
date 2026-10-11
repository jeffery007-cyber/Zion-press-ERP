import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox


class SettingsWindow:

    def __init__(self, parent, role):

        self.parent = parent
        self.role = role

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="Settings",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=20, pady=20)

        # Application Settings
        app_frame = ttk.Labelframe(
            self.frame,
            text="Application Settings"
        )
        app_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(
            app_frame,
            text="Application Name"
        ).grid(row=0, column=0, padx=20, pady=15, sticky="w")

        ttk.Label(
            app_frame,
            text="PressFlow ERP"
        ).grid(row=0, column=1, padx=20, pady=15, sticky="w")

        ttk.Label(
            app_frame,
            text="Printing Press"
        ).grid(row=1, column=0, padx=20, pady=15, sticky="w")

        ttk.Label(
            app_frame,
            text="Zion Press"
        ).grid(row=1, column=1, padx=20, pady=15, sticky="w")

        ttk.Label(
            app_frame,
            text="Logged-in Role"
        ).grid(row=2, column=0, padx=20, pady=15, sticky="w")

        ttk.Label(
            app_frame,
            text=self.role
        ).grid(row=2, column=1, padx=20, pady=15, sticky="w")

        # About
        about_frame = ttk.Labelframe(
            self.frame,
            text="About PressFlow ERP"
        )
        about_frame.pack(fill=X, padx=20, pady=10)

        ttk.Label(
            about_frame,
            text="PressFlow ERP - Printing Press Management System",
            font=("Segoe UI", 14, "bold")
        ).pack(anchor="w", padx=20, pady=(15, 5))

        ttk.Label(
            about_frame,
            text="Developed for Zion Press"
        ).pack(anchor="w", padx=20, pady=5)

        ttk.Label(
            about_frame,
            text="Version 1.0"
        ).pack(anchor="w", padx=20, pady=(5, 15))

        ttk.Button(
            self.frame,
            text="Show System Information",
            bootstyle=INFO,
            command=self.show_info
        ).pack(anchor="w", padx=20, pady=20)

    def show_info(self):

        messagebox.showinfo(
            "System Information",
            "PressFlow ERP\n\n"
            "Printing Press Management System\n"
            "Zion Press\n\n"
            "Version: 1.0"
        )