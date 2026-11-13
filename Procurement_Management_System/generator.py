
import random
import sqlite3
from pathlib import Path
from datetime import date, timedelta

DB_PATH = Path(__file__).parent / "procurement.db"


def generate_data():

    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    # Enable foreign keys
    cursor.execute("PRAGMA foreign_keys = ON")

    # Departments
    departments = [
        ("IT",),
        ("HR",),
        ("Finance",),
        ("Marketing",),
        ("Operations",)
    ]

    cursor.executemany("""
        INSERT OR IGNORE INTO departments (department_name)
        VALUES (?)
    """, departments)

    # Employees
    employees = [
        ("Aditi", "aditi@gmail.com", 1),
        ("Rahul", "rahul@gmail.com", 2),
        ("Priya", "priya@gmail.com", 3),
        ("Kiran", "kiran@gmail.com", 4),
        ("Sneha", "sneha@gmail.com", 5)
    ]

    for name, email, dept_id in employees:
        cursor.execute("""
            INSERT OR IGNORE INTO employees
            (employee_name, email, department_id)
            VALUES (?, ?, ?)
        """, (name, email, dept_id))

    # Suppliers
    suppliers = [
        ("Tech Solutions", "Ramesh", "tech@gmail.com",
         "9876543210", "Hyderabad"),
        ("Global Electronics", "Suresh", "global@gmail.com",
         "9876543211", "Bangalore"),
        ("Office World", "Mahesh", "office@gmail.com",
         "9876543212", "Chennai"),
        ("Smart Supplies", "Rajesh", "smart@gmail.com",
         "9876543213", "Mumbai"),
        ("Digital Systems", "Arun", "digital@gmail.com",
         "9876543214", "Delhi")
    ]

    cursor.executemany("""
        INSERT INTO suppliers
        (supplier_name, contact_person, email, phone, address)
        VALUES (?, ?, ?, ?, ?)
    """, suppliers)

    # Products
    products = [
        ("Laptop", "Business Laptop", 55000, 20),
        ("Desktop", "Office Desktop", 45000, 15),
        ("Printer", "Laser Printer", 12000, 10),
        ("Keyboard", "Wireless Keyboard", 1500, 50),
        ("Mouse", "Wireless Mouse", 800, 50),
        ("Monitor", "LED Monitor", 15000, 25),
        ("Office Chair", "Ergonomic Chair", 7000, 30),
        ("Projector", "HD Projector", 35000, 5)
    ]

    cursor.executemany("""
        INSERT INTO products
        (product_name, description, unit_price, quantity)
        VALUES (?, ?, ?, ?)
    """, products)

    connection.commit()

    # Get employee and department IDs
    cursor.execute("SELECT employee_id, department_id FROM employees")
    employee_records = cursor.fetchall()

    # Purchase Requests
    request_ids = []

    statuses = ["Pending", "Approved", "Rejected"]

    for i in range(10):

        employee_id, department_id = random.choice(employee_records)

        request_date = (
            date.today() - timedelta(days=random.randint(1, 30))
        ).isoformat()

        status = random.choice(statuses)
        total_amount = round(random.uniform(5000, 100000), 2)

        cursor.execute("""
            INSERT INTO purchase_requests
            (employee_id, department_id, request_date,
             status, total_amount)
            VALUES (?, ?, ?, ?, ?)
        """, (
            employee_id,
            department_id,
            request_date,
            status,
            total_amount
        ))

        request_ids.append((cursor.lastrowid, employee_id, status))

    # Purchase Orders
    cursor.execute("SELECT supplier_id FROM suppliers")
    supplier_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT product_id, unit_price FROM products")
    product_records = cursor.fetchall()

    for request_id, employee_id, status in request_ids:

        if status != "Approved":
            continue

        supplier_id = random.choice(supplier_ids)

        order_date = date.today().isoformat()

        cursor.execute("""
            INSERT INTO purchase_orders
            (request_id, supplier_id, order_date,
             total_amount, status)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request_id,
            supplier_id,
            order_date,
            0,
            "Created"
        ))

        order_id = cursor.lastrowid
        order_total = 0

        # Order Items
        for _ in range(random.randint(1, 3)):

            product_id, unit_price = random.choice(product_records)
            quantity = random.randint(1, 5)

            cursor.execute("""
                INSERT INTO order_items
                (order_id, product_id, quantity, unit_price)
                VALUES (?, ?, ?, ?)
            """, (
                order_id,
                product_id,
                quantity,
                unit_price
            ))

            order_total += quantity * unit_price

        cursor.execute("""
            UPDATE purchase_orders
            SET total_amount = ?
            WHERE order_id = ?
        """, (order_total, order_id))

    # Approvals
    for request_id, employee_id, status in request_ids:

        approval_status = (
            status if status in ["Approved", "Rejected"]
            else "Pending"
        )

        approval_date = (
            date.today().isoformat()
            if approval_status != "Pending"
            else None
        )

        cursor.execute("""
            INSERT INTO approvals
            (request_id, approved_by, approval_status,
             approval_date, remarks)
            VALUES (?, ?, ?, ?, ?)
        """, (
            request_id,
            employee_id,
            approval_status,
            approval_date,
            "Sample approval record"
        ))

    connection.commit()
    connection.close()

    print("Sample procurement data generated successfully!")


if __name__ == "__main__":
    generate_data()
