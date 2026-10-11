import ttkbootstrap as ttk
from ttkbootstrap.constants import *

from database.db import Database

from modules.customers import CustomersWindow
from modules.orders import OrdersWindow
from modules.billing import BillingWindow
from modules.inventory import InventoryWindow
from modules.reports import ReportsWindow
from modules.settings import SettingsWindow


class DashboardWindow:

    def __init__(self, role):

        self.role = role

        self.root = ttk.Window(themename="flatly")
        self.root.title("PressFlow ERP - Zion Press")
        self.root.state("zoomed")

        self.create_layout()

        self.root.mainloop()

    # ==========================================
    # MAIN LAYOUT
    # ==========================================

    def create_layout(self):

        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=BOTH, expand=True)

        self.create_sidebar()

        self.right_frame = ttk.Frame(self.main_frame)
        self.right_frame.pack(
            side=LEFT,
            fill=BOTH,
            expand=True
        )

        self.create_header()

        self.content = ttk.Frame(self.right_frame)
        self.content.pack(
            fill=BOTH,
            expand=True,
            padx=20,
            pady=20
        )

        self.show_dashboard()

    # ==========================================
    # SIDEBAR
    # ==========================================

    def create_sidebar(self):

        self.sidebar = ttk.Frame(
            self.main_frame,
            width=220
        )

        self.sidebar.pack(
            side=LEFT,
            fill=Y
        )

        self.sidebar.pack_propagate(False)

        ttk.Label(
            self.sidebar,
            text="PressFlow ERP",
            font=("Segoe UI", 18, "bold")
        ).pack(
            pady=(30, 5)
        )

        ttk.Label(
            self.sidebar,
            text="Zion Press",
            font=("Segoe UI", 11)
        ).pack(
            pady=(0, 25)
        )

        # Dashboard
        ttk.Button(
            self.sidebar,
            text="Dashboard",
            command=self.show_dashboard
        ).pack(
            fill=X,
            padx=15,
            pady=5
        )

        # Customers
        ttk.Button(
            self.sidebar,
            text="Customers",
            command=self.open_customers
        ).pack(
            fill=X,
            padx=15,
            pady=5
        )

        # Orders
        ttk.Button(
            self.sidebar,
            text="Orders",
            command=self.open_orders
        ).pack(
            fill=X,
            padx=15,
            pady=5
        )

        # Billing
        ttk.Button(
            self.sidebar,
            text="Billing",
            command=self.open_billing
        ).pack(
            fill=X,
            padx=15,
            pady=5
        )

        # Inventory
        ttk.Button(
            self.sidebar,
            text="Inventory",
            command=self.open_inventory
        ).pack(
            fill=X,
            padx=15,
            pady=5
        )

        # Reports
        ttk.Button(
            self.sidebar,
            text="Reports",
            command=self.open_reports
        ).pack(
            fill=X,
            padx=15,
            pady=5
        )

        # Settings
        ttk.Button(
            self.sidebar,
            text="Settings",
            command=self.open_settings
        ).pack(
            fill=X,
            padx=15,
            pady=5
        )

        # Logout
        ttk.Button(
            self.sidebar,
            text="Logout",
            bootstyle=DANGER,
            command=self.logout
        ).pack(
            side=BOTTOM,
            fill=X,
            padx=15,
            pady=20
        )

    # ==========================================
    # HEADER
    # ==========================================

    def create_header(self):

        self.header = ttk.Frame(
            self.right_frame,
            height=60
        )

        self.header.pack(fill=X)

        self.page_title = ttk.Label(
            self.header,
            text="Dashboard",
            font=("Segoe UI", 22, "bold")
        )

        self.page_title.pack(
            side=LEFT,
            padx=20
        )

        ttk.Label(
            self.header,
            text=f"Logged in as : {self.role}",
            font=("Segoe UI", 11)
        ).pack(
            side=RIGHT,
            padx=20
        )

    # ==========================================
    # CLEAR CONTENT
    # ==========================================

    def clear_content(self):

        for widget in self.content.winfo_children():
            widget.destroy()

    # ==========================================
    # DASHBOARD
    # ==========================================

    def show_dashboard(self):

        self.page_title.config(
            text="Dashboard"
        )

        self.clear_content()

        db = Database()

        # --------------------------------------
        # Get Today's Orders
        # --------------------------------------

        db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE DATE(created_at) = DATE('now', 'localtime')
            """
        )

        today_orders = db.cursor.fetchone()[0]

        # --------------------------------------
        # Get Pending Orders
        # --------------------------------------

        db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM orders
            WHERE status = 'Pending'
            """
        )

        pending_orders = db.cursor.fetchone()[0]

        # --------------------------------------
        # Get Revenue
        # --------------------------------------

        db.cursor.execute(
            """
            SELECT IFNULL(SUM(total), 0)
            FROM bills
            """
        )

        revenue = db.cursor.fetchone()[0]

        # --------------------------------------
        # Get Customers
        # --------------------------------------

        db.cursor.execute(
            """
            SELECT COUNT(*)
            FROM customers
            """
        )

        customers = db.cursor.fetchone()[0]

        db.close()

        # --------------------------------------
        # Welcome
        # --------------------------------------

        ttk.Label(
            self.content,
            text="Welcome to Zion Press",
            font=("Segoe UI", 24, "bold")
        ).pack(
            anchor="w"
        )

        ttk.Label(
            self.content,
            text="Today's Overview",
            font=("Segoe UI", 12)
        ).pack(
            anchor="w",
            pady=(0, 20)
        )

        # --------------------------------------
        # Cards
        # --------------------------------------

        cards = ttk.Frame(
            self.content
        )

        cards.pack(
            fill=X
        )

        self.create_card(
            cards,
            "Today's Orders",
            str(today_orders)
        ).pack(
            side=LEFT,
            padx=10
        )

        self.create_card(
            cards,
            "Pending Orders",
            str(pending_orders)
        ).pack(
            side=LEFT,
            padx=10
        )

        self.create_card(
            cards,
            "Revenue",
            f"₹{revenue:.2f}"
        ).pack(
            side=LEFT,
            padx=10
        )

        self.create_card(
            cards,
            "Customers",
            str(customers)
        ).pack(
            side=LEFT,
            padx=10
        )

    # ==========================================
    # CUSTOMERS
    # ==========================================

    def open_customers(self):

        self.page_title.config(
            text="Customers"
        )

        self.clear_content()

        CustomersWindow(
            self.content
        )

    # ==========================================
    # ORDERS
    # ==========================================

    def open_orders(self):

        self.page_title.config(
            text="Orders"
        )

        self.clear_content()

        OrdersWindow(
            self.content
        )

    # ==========================================
    # BILLING
    # ==========================================

    def open_billing(self):

        self.page_title.config(
            text="Billing"
        )

        self.clear_content()

        BillingWindow(
            self.content
        )

    # ==========================================
    # INVENTORY
    # ==========================================

    def open_inventory(self):

        self.page_title.config(
            text="Inventory"
        )

        self.clear_content()

        InventoryWindow(
            self.content
        )

    # ==========================================
    # REPORTS
    # ==========================================

    def open_reports(self):

        self.page_title.config(
            text="Reports"
        )

        self.clear_content()

        ReportsWindow(
            self.content
        )

    # ==========================================
    # SETTINGS
    # ==========================================

    def open_settings(self):

        self.page_title.config(
            text="Settings"
        )

        self.clear_content()

        SettingsWindow(
            self.content,
            self.role
        )

    # ==========================================
    # CARD
    # ==========================================

    def create_card(
        self,
        parent,
        title,
        value
    ):

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
            font=("Segoe UI", 24, "bold")
        ).pack(
            expand=True
        )

        return frame

    # ==========================================
    # LOGOUT
    # ==========================================

    def logout(self):

        self.root.destroy()