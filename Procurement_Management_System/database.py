
import sqlite3
from pathlib import Path

# Database file location
DB_PATH = Path(__file__).parent / "procurement.db"


# Connect to database
def get_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# Create database and tables
def create_database():

    connection = get_connection()
    cursor = connection.cursor()

    cursor.executescript("""

    CREATE TABLE IF NOT EXISTS departments (
        department_id INTEGER PRIMARY KEY AUTOINCREMENT,
        department_name TEXT NOT NULL UNIQUE
    );

    CREATE TABLE IF NOT EXISTS employees (
        employee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_name TEXT NOT NULL,
        email TEXT UNIQUE,
        department_id INTEGER,
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
    );

    CREATE TABLE IF NOT EXISTS suppliers (
        supplier_id INTEGER PRIMARY KEY AUTOINCREMENT,
        supplier_name TEXT NOT NULL,
        contact_person TEXT,
        email TEXT,
        phone TEXT,
        address TEXT
    );

    CREATE TABLE IF NOT EXISTS products (
        product_id INTEGER PRIMARY KEY AUTOINCREMENT,
        product_name TEXT NOT NULL,
        description TEXT,
        unit_price REAL NOT NULL,
        quantity INTEGER DEFAULT 0
    );

    CREATE TABLE IF NOT EXISTS purchase_requests (
        request_id INTEGER PRIMARY KEY AUTOINCREMENT,
        employee_id INTEGER,
        department_id INTEGER,
        request_date TEXT NOT NULL,
        status TEXT DEFAULT 'Pending',
        total_amount REAL DEFAULT 0,
        FOREIGN KEY (employee_id)
        REFERENCES employees(employee_id),
        FOREIGN KEY (department_id)
        REFERENCES departments(department_id)
    );

    CREATE TABLE IF NOT EXISTS purchase_orders (
        order_id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER,
        supplier_id INTEGER,
        order_date TEXT NOT NULL,
        total_amount REAL DEFAULT 0,
        status TEXT DEFAULT 'Created',
        FOREIGN KEY (request_id)
        REFERENCES purchase_requests(request_id),
        FOREIGN KEY (supplier_id)
        REFERENCES suppliers(supplier_id)
    );

    CREATE TABLE IF NOT EXISTS order_items (
        item_id INTEGER PRIMARY KEY AUTOINCREMENT,
        order_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        unit_price REAL NOT NULL,
        FOREIGN KEY (order_id)
        REFERENCES purchase_orders(order_id),
        FOREIGN KEY (product_id)
        REFERENCES products(product_id)
    );

    CREATE TABLE IF NOT EXISTS approvals (
        approval_id INTEGER PRIMARY KEY AUTOINCREMENT,
        request_id INTEGER,
        approved_by INTEGER,
        approval_status TEXT DEFAULT 'Pending',
        approval_date TEXT,
        remarks TEXT,
        FOREIGN KEY (request_id)
        REFERENCES purchase_requests(request_id),
        FOREIGN KEY (approved_by)
        REFERENCES employees(employee_id)
    );

    """)

    connection.commit()
    connection.close()

    print("Database and tables created successfully!")


# Run database
if __name__ == "__main__":
    create_database()
