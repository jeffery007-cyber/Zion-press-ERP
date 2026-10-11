import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import messagebox
from database.db import Database


class InventoryWindow:

    def __init__(self, parent):

        self.db = Database()

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)

        self.create_widgets()

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="Inventory Management",
            font=("Segoe UI", 22, "bold")
        ).pack(anchor="w", padx=20, pady=15)

        form = ttk.LabelFrame(
            self.frame,
            text="Add Inventory Item"
        )
        form.pack(fill=X, padx=20, pady=10)

        ttk.Label(form, text="Item Name").grid(
            row=0, column=0, padx=10, pady=10
        )

        self.item_entry = ttk.Entry(form, width=30)
        self.item_entry.grid(row=0, column=1, padx=10)

        ttk.Label(form, text="Quantity").grid(
            row=1, column=0, padx=10, pady=10
        )

        self.qty_entry = ttk.Entry(form, width=30)
        self.qty_entry.grid(row=1, column=1, padx=10)

        ttk.Label(form, text="Unit Price").grid(
            row=2, column=0, padx=10, pady=10
        )

        self.price_entry = ttk.Entry(form, width=30)
        self.price_entry.grid(row=2, column=1, padx=10)

        ttk.Button(
            form,
            text="Add Item",
            bootstyle=SUCCESS,
            command=self.add_item
        ).grid(row=3, column=1, pady=15)

        columns = (
            "ID",
            "Item",
            "Quantity",
            "Unit Price",
            "Date"
        )

        self.tree = ttk.Treeview(
            self.frame,
            columns=columns,
            show="headings"
        )

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        self.tree.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=15
        )

        self.load_items()

    def add_item(self):

        item = self.item_entry.get().strip()
        qty = self.qty_entry.get().strip()
        price = self.price_entry.get().strip()

        if not item or not qty or not price:
            messagebox.showerror(
                "Error",
                "Please fill all fields."
            )
            return

        try:
            qty = int(qty)
            price = float(price)
        except ValueError:
            messagebox.showerror(
                "Error",
                "Quantity must be integer and price must be a number."
            )
            return

        self.db.cursor.execute(
            """
            INSERT INTO inventory
            (item_name, quantity, unit_price)
            VALUES (?, ?, ?)
            """,
            (item, qty, price)
        )

        self.db.connection.commit()

        messagebox.showinfo(
            "Success",
            "Inventory item added."
        )

        self.item_entry.delete(0, END)
        self.qty_entry.delete(0, END)
        self.price_entry.delete(0, END)

        self.load_items()

    def load_items(self):

        for row in self.tree.get_children():
            self.tree.delete(row)

        self.db.cursor.execute(
            """
            SELECT
                id,
                item_name,
                quantity,
                unit_price,
                created_at
            FROM inventory
            ORDER BY id DESC
            """
        )

        for row in self.db.cursor.fetchall():
            self.tree.insert(
                "",
                END,
                values=row
            )