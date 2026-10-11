import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.db import Database


class BillingWindow:

    def __init__(self, parent):

        self.parent = parent
        self.db = Database()

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="Billing Management",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=20, pady=20)

        form = ttk.Frame(self.frame)
        form.pack(fill=X, padx=20)

        # Customer
        ttk.Label(
            form,
            text="Customer Name"
        ).grid(row=0, column=0, padx=10, pady=8, sticky="w")

        self.customer_entry = ttk.Entry(form, width=40)
        self.customer_entry.grid(row=0, column=1, padx=10)

        # Order
        ttk.Label(
            form,
            text="Order / Job Name"
        ).grid(row=1, column=0, padx=10, pady=8, sticky="w")

        self.order_entry = ttk.Entry(form, width=40)
        self.order_entry.grid(row=1, column=1, padx=10)

        # Amount
        ttk.Label(
            form,
            text="Amount"
        ).grid(row=2, column=0, padx=10, pady=8, sticky="w")

        self.amount_entry = ttk.Entry(form, width=40)
        self.amount_entry.grid(row=2, column=1, padx=10)

        # GST
        ttk.Label(
            form,
            text="GST (%)"
        ).grid(row=3, column=0, padx=10, pady=8, sticky="w")

        self.gst_entry = ttk.Entry(form, width=40)
        self.gst_entry.insert(0, "18")
        self.gst_entry.grid(row=3, column=1, padx=10)

        ttk.Button(
            form,
            text="Generate Bill",
            bootstyle=SUCCESS,
            command=self.generate_bill
        ).grid(row=4, column=1, pady=15)

        # Table
        columns = (
            "ID",
            "Customer",
            "Order",
            "Amount",
            "GST",
            "Total",
            "Date"
        )

        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings",
            height=12
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=10
        )

        self.load_bills()

    def generate_bill(self):

        customer = self.customer_entry.get().strip()
        order = self.order_entry.get().strip()
        amount = self.amount_entry.get().strip()
        gst = self.gst_entry.get().strip()

        if not customer or not order or not amount:
            messagebox.showerror(
                "Error",
                "Please fill all required fields."
            )
            return

        try:
            amount = float(amount)
            gst = float(gst)

            gst_amount = amount * gst / 100
            total = amount + gst_amount

        except ValueError:
            messagebox.showerror(
                "Error",
                "Amount and GST must be numbers."
            )
            return

        self.db.cursor.execute(
            """
            INSERT INTO bills
            (customer_name, order_name, amount, gst, total)
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                customer,
                order,
                amount,
                gst,
                total
            )
        )

        self.db.connection.commit()

        messagebox.showinfo(
            "Success",
            f"Bill Generated Successfully!\n\nTotal: ₹{total:.2f}"
        )

        self.customer_entry.delete(0, END)
        self.order_entry.delete(0, END)
        self.amount_entry.delete(0, END)

        self.load_bills()

    def load_bills(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        self.db.cursor.execute(
            """
            SELECT
                id,
                customer_name,
                order_name,
                amount,
                gst,
                total,
                created_at
            FROM bills
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