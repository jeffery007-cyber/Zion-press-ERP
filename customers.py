import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database.db import Database
from tkinter import messagebox


class CustomersWindow:

    def __init__(self, parent):

        self.parent = parent

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill="both", expand=True)
        self.db = Database()

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="Customer Management",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=20, pady=20)

        form_frame = ttk.Frame(self.frame)
        form_frame.pack(fill="x", padx=20)

        ttk.Label(form_frame, text="Customer Name").grid(
            row=0,
            column=0,
            sticky="w",
            pady=5
        )

        self.name_entry = ttk.Entry(form_frame, width=40)
        self.name_entry.grid(row=0, column=1, padx=10)

        ttk.Label(form_frame, text="Phone").grid(
            row=1,
            column=0,
            sticky="w",
            pady=5
        )

        self.phone_entry = ttk.Entry(form_frame, width=40)
        self.phone_entry.grid(row=1, column=1, padx=10)

        ttk.Label(form_frame, text="Email").grid(
            row=2,
            column=0,
            sticky="w",
            pady=5
        )

        self.email_entry = ttk.Entry(form_frame, width=40)
        self.email_entry.grid(row=2, column=1, padx=10)

        ttk.Button(
            form_frame,
            text="Save Customer",
            bootstyle=SUCCESS,
            command=self.save_customer
        ).grid(row=3, column=1, pady=20)
    def save_customer(self):

        name = self.name_entry.get().strip()
        phone = self.phone_entry.get().strip()
        email = self.email_entry.get().strip()

        if name == "":
            messagebox.showerror("Error", "Customer name is required.")
            return

        self.db.cursor.execute(
            """
            INSERT INTO customers
            (customer_name, phone, email)
            VALUES (?, ?, ?)
            """,
            (name, phone, email)
        )

        self.db.connection.commit()

        messagebox.showinfo(
            "Success",
            "Customer added successfully!"
        )

        self.name_entry.delete(0, "end")
        self.phone_entry.delete(0, "end")
        self.email_entry.delete(0, "end")