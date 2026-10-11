import sqlite3
import os

from utils.security import Security


class Database:

    def __init__(self):
        db_path = os.path.join(
            os.path.dirname(__file__),
            "printing_press.db"
        )

        self.connection = sqlite3.connect(db_path)
        self.cursor = self.connection.cursor()

    # ============================================
    # Create Tables
    # ============================================

    def create_tables(self):

        # Users Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS users(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL,
                role TEXT NOT NULL
            )
        """)

        # Customers Table
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS customers(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_name TEXT NOT NULL,
                phone TEXT,
                email TEXT,
                address TEXT,
                gst TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS orders(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            job_name TEXT,
            quantity INTEGER,
            amount REAL,
            status TEXT DEFAULT 'Pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS bills(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            customer_name TEXT,
            order_name TEXT,
            amount REAL,
            gst REAL,
            total REAL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)
        self.cursor.execute("""
        CREATE TABLE IF NOT EXISTS inventory(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            item_name TEXT NOT NULL,
            quantity INTEGER NOT NULL,
            unit_price REAL NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        """)

        self.connection.commit()

        self.create_default_admin()

    # ============================================
    # Default Admin
    # ============================================

    def create_default_admin(self):

        self.cursor.execute(
            "SELECT * FROM users WHERE username=?",
            ("admin",)
        )

        if self.cursor.fetchone() is None:

            hashed = Security.hash_password("admin123")

            self.cursor.execute("""
                INSERT INTO users(
                    username,
                    password,
                    role
                )
                VALUES(?,?,?)
            """, (
                "admin",
                hashed,
                "Administrator"
            ))

        self.connection.commit()

    # ============================================
    # Login Validation
    # ============================================

    def validate_login(self, username, password):

        self.cursor.execute(
            "SELECT password, role FROM users WHERE username=?",
            (username,)
        )

        result = self.cursor.fetchone()

        if result:

            hashed_password, role = result

            if Security.verify_password(password, hashed_password):
                return role

        return None

    # ============================================
    # Customer Operations
    # ============================================

    def add_customer(self, name, phone, email, address, gst):

        self.cursor.execute("""
            INSERT INTO customers(
                customer_name,
                phone,
                email,
                address,
                gst
            )
            VALUES(?,?,?,?,?)
        """, (
            name,
            phone,
            email,
            address,
            gst
        ))

        self.connection.commit()

    def get_customers(self):

        self.cursor.execute("""
            SELECT
                id,
                customer_name,
                phone,
                email,
                gst
            FROM customers
            ORDER BY customer_name
        """)

        return self.cursor.fetchall()

    def update_customer(
        self,
        customer_id,
        name,
        phone,
        email,
        address,
        gst
    ):

        self.cursor.execute("""
            UPDATE customers
            SET
                customer_name=?,
                phone=?,
                email=?,
                address=?,
                gst=?
            WHERE id=?
        """, (
            name,
            phone,
            email,
            address,
            gst,
            customer_id
        ))

        self.connection.commit()

    def delete_customer(self, customer_id):

        self.cursor.execute(
            "DELETE FROM customers WHERE id=?",
            (customer_id,)
        )

        self.connection.commit()

    # ============================================
    # Close Database
    # ============================================

    def close(self):
        self.connection.close()