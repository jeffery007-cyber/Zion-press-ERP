import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.db import Database


class OrdersWindow:

    def __init__(self, parent):

        self.db = Database()

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):

        # Title
        ttk.Label(
            self.frame,
            text="Orders Management",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=20, pady=15)

        # ==============================
        # FORM
        # ==============================

        form = ttk.Labelframe(
            self.frame,
            text="Add New Order"
        )

        form.pack(
            fill=X,
            padx=20,
            pady=10
        )

        # Customer
        ttk.Label(
            form,
            text="Customer Name"
        ).grid(
            row=0,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.customer_entry = ttk.Entry(
            form,
            width=35
        )

        self.customer_entry.grid(
            row=0,
            column=1,
            padx=10,
            pady=10
        )

        # Job
        ttk.Label(
            form,
            text="Job Name"
        ).grid(
            row=0,
            column=2,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.job_entry = ttk.Entry(
            form,
            width=35
        )

        self.job_entry.grid(
            row=0,
            column=3,
            padx=10,
            pady=10
        )

        # Quantity
        ttk.Label(
            form,
            text="Quantity"
        ).grid(
            row=1,
            column=0,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.qty_entry = ttk.Entry(
            form,
            width=35
        )

        self.qty_entry.grid(
            row=1,
            column=1,
            padx=10,
            pady=10
        )

        # Amount
        ttk.Label(
            form,
            text="Amount"
        ).grid(
            row=1,
            column=2,
            padx=10,
            pady=10,
            sticky="w"
        )

        self.amount_entry = ttk.Entry(
            form,
            width=35
        )

        self.amount_entry.grid(
            row=1,
            column=3,
            padx=10,
            pady=10
        )

        # Save button
        ttk.Button(
            form,
            text="Save Order",
            bootstyle=SUCCESS,
            command=self.save_order
        ).grid(
            row=2,
            column=1,
            columnspan=2,
            pady=15
        )

        # ==============================
        # ORDERS TABLE
        # ==============================

        table_frame = ttk.Frame(self.frame)

        table_frame.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        columns = (
            "ID",
            "Customer",
            "Job",
            "Quantity",
            "Amount",
            "Status",
            "Date"
        )

        self.tree = ttk.Treeview(
            table_frame,
            columns=columns,
            show="headings"
        )

        for col in columns:

            self.tree.heading(
                col,
                text=col
            )

            self.tree.column(
                col,
                width=130,
                anchor="center"
            )

        self.tree.pack(
            fill=BOTH,
            expand=True
        )

        self.load_orders()

    # ==============================
    # SAVE ORDER
    # ==============================

    def save_order(self):

        customer = self.customer_entry.get().strip()
        job = self.job_entry.get().strip()
        quantity = self.qty_entry.get().strip()
        amount = self.amount_entry.get().strip()

        if not customer or not job or not quantity or not amount:

            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )

            return

        try:
            quantity = int(quantity)
            amount = float(amount)

        except ValueError:

            messagebox.showerror(
                "Error",
                "Quantity must be a number and Amount must be numeric."
            )

            return

        if quantity <= 0:

            messagebox.showerror(
                "Error",
                "Quantity must be greater than 0."
            )

            return

        self.db.cursor.execute(
            """
            INSERT INTO orders
            (
                customer_name,
                job_name,
                quantity,
                amount,
                status
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                customer,
                job,
                quantity,
                amount,
                "Pending"
            )
        )

        self.db.connection.commit()

        messagebox.showinfo(
            "Success",
            "Order added successfully!"
        )

        self.customer_entry.delete(0, END)
        self.job_entry.delete(0, END)
        self.qty_entry.delete(0, END)
        self.amount_entry.delete(0, END)

        self.load_orders()

    # ==============================
    # LOAD ORDERS
    # ==============================

    def load_orders(self):

        for item in self.tree.get_children():
            self.tree.delete(item)

        self.db.cursor.execute(
            """
            SELECT
                id,
                customer_name,
                job_name,
                quantity,
                amount,
                status,
                created_at
            FROM orders
            ORDER BY id DESC
            """
        )

        rows = self.db.cursor.fetchall()

        for row in rows:

            self.tree.insert(
                "",
                END,
                values=row
            )