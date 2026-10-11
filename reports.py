import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from database.db import Database


class ReportsWindow:

    def __init__(self, parent):

        self.parent = parent
        self.db = Database()

        self.frame = ttk.Frame(parent)
        self.frame.pack(fill=BOTH, expand=True)

        self.create_widgets()

    # ==========================================
    # CREATE WIDGETS
    # ==========================================

    def create_widgets(self):

        ttk.Label(
            self.frame,
            text="Reports & Statistics",
            font=("Segoe UI", 22, "bold")
        ).pack(
            anchor="w",
            padx=20,
            pady=20
        )

        # Get statistics
        customers = self.get_customer_count()
        orders = self.get_order_count()
        pending = self.get_pending_orders()
        revenue = self.get_revenue()

        cards = ttk.Frame(self.frame)
        cards.pack(fill=X, padx=20)

        self.create_card(
            cards,
            "Customers",
            str(customers)
        ).pack(side=LEFT, padx=10)

        self.create_card(
            cards,
            "Total Orders",
            str(orders)
        ).pack(side=LEFT, padx=10)

        self.create_card(
            cards,
            "Pending Orders",
            str(pending)
        ).pack(side=LEFT, padx=10)

        self.create_card(
            cards,
            "Total Revenue",
            f"₹{revenue:.2f}"
        ).pack(side=LEFT, padx=10)

        # Refresh button
        ttk.Button(
            self.frame,
            text="Refresh Reports",
            bootstyle="info",
            command=self.refresh
        ).pack(
            anchor="w",
            padx=30,
            pady=30
        )

    # ==========================================
    # CARD
    # ==========================================

    def create_card(self, parent, title, value):

        frame = ttk.Labelframe(
            parent,
            text=title,
            width=220,
            height=120
        )

        frame.pack_propagate(False)

        ttk.Label(
            frame,
            text=value,
            font=("Segoe UI", 22, "bold")
        ).pack(expand=True)

        return frame

    # ==========================================
    # DATABASE
    # ==========================================

    def get_customer_count(self):

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM customers"
        )

        return self.db.cursor.fetchone()[0]

    def get_order_count(self):

        self.db.cursor.execute(
            "SELECT COUNT(*) FROM orders"
        )

        return self.db.cursor.fetchone()[0]

    def get_pending_orders(self):

        self.db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'Pending'
            """
        )

        return self.db.cursor.fetchone()[0]

    def get_revenue(self):

        self.db.cursor.execute(
            """
            SELECT IFNULL(SUM(total), 0)
            FROM bills
            """
        )

        return self.db.cursor.fetchone()[0]

    # ==========================================
    # REFRESH
    # ==========================================

    def refresh(self):

        self.frame.destroy()

        self.frame = ttk.Frame(self.parent)
        self.frame.pack(fill=BOTH, expand=True)

        self.create_widgets()