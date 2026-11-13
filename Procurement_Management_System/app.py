
import sqlite3
from pathlib import Path
from datetime import date

from flask import (
    Flask, render_template_string,
    request, redirect, url_for, flash
)

# Flask application
app = Flask(__name__)
app.secret_key = "procurement_management_secret"

# Database location
DB_PATH = Path(__file__).parent / "procurement.db"


# Database connection
def get_db_connection():
    connection = sqlite3.connect(DB_PATH)
    connection.row_factory = sqlite3.Row
    connection.execute("PRAGMA foreign_keys = ON")
    return connection


# Dashboard and main page
@app.route("/")
def dashboard():

    if not DB_PATH.exists():
        return "Database not found. Run python database.py first."

    connection = get_db_connection()

    # Dashboard counts
    departments = connection.execute(
        "SELECT COUNT(*) FROM departments"
    ).fetchone()[0]

    employees = connection.execute(
        "SELECT COUNT(*) FROM employees"
    ).fetchone()[0]

    suppliers = connection.execute(
        "SELECT COUNT(*) FROM suppliers"
    ).fetchone()[0]

    products = connection.execute(
        "SELECT COUNT(*) FROM products"
    ).fetchone()[0]

    requests_count = connection.execute(
        "SELECT COUNT(*) FROM purchase_requests"
    ).fetchone()[0]

    pending = connection.execute(
        "SELECT COUNT(*) FROM purchase_requests WHERE status = 'Pending'"
    ).fetchone()[0]

    approved = connection.execute(
        "SELECT COUNT(*) FROM purchase_requests WHERE status = 'Approved'"
    ).fetchone()[0]

    rejected = connection.execute(
        "SELECT COUNT(*) FROM purchase_requests WHERE status = 'Rejected'"
    ).fetchone()[0]

    total_orders = connection.execute(
        "SELECT COUNT(*) FROM purchase_orders"
    ).fetchone()[0]

    total_amount = connection.execute(
        "SELECT COALESCE(SUM(total_amount), 0) FROM purchase_orders"
    ).fetchone()[0]

    # Recent purchase requests
    recent_requests = connection.execute("""
        SELECT
            pr.request_id,
            e.employee_name,
            d.department_name,
            pr.request_date,
            pr.total_amount,
            pr.status
        FROM purchase_requests pr
        LEFT JOIN employees e
            ON pr.employee_id = e.employee_id
        LEFT JOIN departments d
            ON pr.department_id = d.department_id
        ORDER BY pr.request_id DESC
        LIMIT 10
    """).fetchall()

    connection.close()

    return render_template_string(
        TEMPLATE,
        page="dashboard",
        departments=departments,
        employees=employees,
        suppliers=suppliers,
        products=products,
        requests_count=requests_count,
        pending=pending,
        approved=approved,
        rejected=rejected,
        total_orders=total_orders,
        total_amount=total_amount,
        recent_requests=recent_requests
    )


# Supplier management
@app.route("/suppliers", methods=["GET", "POST"])
def suppliers_page():

    connection = get_db_connection()

    if request.method == "POST":

        name = request.form.get("supplier_name", "").strip()
        contact = request.form.get("contact_person", "").strip()
        email = request.form.get("email", "").strip()
        phone = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()

        if not name:
            flash("Supplier name is required.")
        else:
            connection.execute("""
                INSERT INTO suppliers
                (supplier_name, contact_person, email, phone, address)
                VALUES (?, ?, ?, ?, ?)
            """, (name, contact, email, phone, address))

            connection.commit()
            flash("Supplier added successfully!")

        connection.close()
        return redirect(url_for("suppliers_page"))

    supplier_list = connection.execute("""
        SELECT * FROM suppliers
        ORDER BY supplier_id DESC
    """).fetchall()

    connection.close()

    return render_template_string(
        TEMPLATE,
        page="suppliers",
        supplier_list=supplier_list
    )


# Product management
@app.route("/products", methods=["GET", "POST"])
def products_page():

    connection = get_db_connection()

    if request.method == "POST":

        name = request.form.get("product_name", "").strip()
        description = request.form.get("description", "").strip()

        try:
            price = float(request.form.get("unit_price", 0))
            quantity = int(request.form.get("quantity", 0))

            if not name or price < 0 or quantity < 0:
                raise ValueError

            connection.execute("""
                INSERT INTO products
                (product_name, description, unit_price, quantity)
                VALUES (?, ?, ?, ?)
            """, (name, description, price, quantity))

            connection.commit()
            flash("Product added successfully!")

        except ValueError:
            flash("Enter a valid product name, price and quantity.")

        connection.close()
        return redirect(url_for("products_page"))

    product_list = connection.execute("""
        SELECT * FROM products
        ORDER BY product_id DESC
    """).fetchall()

    connection.close()

    return render_template_string(
        TEMPLATE,
        page="products",
        product_list=product_list
    )


# Purchase request management
@app.route("/requests", methods=["GET", "POST"])
def requests_page():

    connection = get_db_connection()

    if request.method == "POST":

        try:
            employee_id = int(request.form.get("employee_id"))
            amount = float(request.form.get("total_amount"))

            employee = connection.execute("""
                SELECT department_id
                FROM employees
                WHERE employee_id = ?
            """, (employee_id,)).fetchone()

            if employee is None or amount <= 0:
                raise ValueError

            connection.execute("""
                INSERT INTO purchase_requests
                (employee_id, department_id, request_date,
                 status, total_amount)
                VALUES (?, ?, ?, ?, ?)
            """, (
                employee_id,
                employee["department_id"],
                date.today().isoformat(),
                "Pending",
                amount
            ))

            connection.commit()
            flash("Purchase request submitted successfully!")

        except (ValueError, TypeError):
            flash("Please enter valid request details.")

        connection.close()
        return redirect(url_for("requests_page"))

    employee_list = connection.execute("""
        SELECT employee_id, employee_name
        FROM employees
        ORDER BY employee_name
    """).fetchall()

    request_list = connection.execute("""
        SELECT
            pr.*,
            e.employee_name,
            d.department_name
        FROM purchase_requests pr
        LEFT JOIN employees e
            ON pr.employee_id = e.employee_id
        LEFT JOIN departments d
            ON pr.department_id = d.department_id
        ORDER BY pr.request_id DESC
    """).fetchall()

    connection.close()

    return render_template_string(
        TEMPLATE,
        page="requests",
        employee_list=employee_list,
        request_list=request_list
    )


# Approve or reject purchase requests
@app.route("/update_request/<int:request_id>/<status>")
def update_request(request_id, status):

    if status not in ["Approved", "Rejected"]:
        flash("Invalid request status.")
        return redirect(url_for("requests_page"))

    connection = get_db_connection()

    existing = connection.execute("""
        SELECT status FROM purchase_requests
        WHERE request_id = ?
    """, (request_id,)).fetchone()

    if existing is None:
        flash("Purchase request not found.")

    elif existing["status"] != "Pending":
        flash("This request has already been processed.")

    else:
        connection.execute("""
            UPDATE purchase_requests
            SET status = ?
            WHERE request_id = ?
        """, (status, request_id))

        connection.execute("""
            UPDATE approvals
            SET approval_status = ?,
                approval_date = ?,
                remarks = ?
            WHERE request_id = ?
        """, (
            status,
            date.today().isoformat(),
            "Request " + status.lower(),
            request_id
        ))

        connection.commit()
        flash("Purchase request " + status.lower() + "!")

    connection.close()

    return redirect(url_for("requests_page"))


# All purchase orders
@app.route("/orders")
def orders_page():

    connection = get_db_connection()

    order_list = connection.execute("""
        SELECT
            po.*,
            s.supplier_name
        FROM purchase_orders po
        LEFT JOIN suppliers s
            ON po.supplier_id = s.supplier_id
        ORDER BY po.order_id DESC
    """).fetchall()

    connection.close()

    return render_template_string(
        TEMPLATE,
        page="orders",
        order_list=order_list
    )


# HTML and CSS template
TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>Procurement Management System</title>

    <meta name="viewport" content="width=device-width, initial-scale=1">

    <style>
        * {
            box-sizing: border-box;
        }

        body {
            margin: 0;
            font-family: Arial, sans-serif;
            background: #f3f5f9;
            color: #263238;
        }

        header {
            background: #172554;
            color: white;
            padding: 22px 30px;
        }

        header h1 {
            margin: 0;
            font-size: 25px;
        }

        nav {
            background: #1e3a8a;
            padding: 14px 25px;
        }

        nav a {
            color: white;
            text-decoration: none;
            margin-right: 22px;
            font-weight: bold;
        }

        nav a:hover {
            text-decoration: underline;
        }

        .container {
            padding: 25px;
            max-width: 1250px;
            margin: auto;
        }

        .cards {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 18px;
            margin-bottom: 25px;
        }

        .card {
            background: white;
            padding: 22px;
            border-radius: 10px;
            box-shadow: 0 2px 8px #00000010;
        }

        .card h3 {
            margin: 0 0 12px;
            color: #64748b;
            font-size: 15px;
        }

        .card h2 {
            margin: 0;
            color: #1e3a8a;
            font-size: 27px;
        }

        .panel {
            background: white;
            padding: 22px;
            border-radius: 10px;
            margin-bottom: 25px;
            overflow-x: auto;
        }

        table {
            width: 100%;
            border-collapse: collapse;
            min-width: 600px;
        }

        th, td {
            padding: 13px;
            text-align: left;
            border-bottom: 1px solid #e5e7eb;
        }

        th {
            background: #eff6ff;
        }

        form {
            margin-bottom: 15px;
        }

        input, select {
            width: 100%;
            padding: 11px;
            margin: 7px 0 14px;
            border: 1px solid #cbd5e1;
            border-radius: 5px;
        }

        button, .btn {
            background: #1e40af;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 5px;
            cursor: pointer;
            text-decoration: none;
            display: inline-block;
            margin: 3px;
        }

        button:hover, .btn:hover {
            background: #172554;
        }

        .reject {
            background: #dc2626;
        }

        .success {
            background: #dcfce7;
            color: #166534;
            padding: 12px;
            margin-bottom: 15px;
            border-radius: 5px;
        }

        .status {
            font-weight: bold;
        }

        .pending {
            color: #d97706;
        }

        .approved {
            color: #15803d;
        }

        .rejected {
            color: #dc2626;
        }

        @media(max-width: 600px) {
            .container {
                padding: 12px;
            }

            nav a {
                display: inline-block;
                margin: 6px;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>Procurement Management System</h1>
    <p>Manage purchasing, suppliers, products and approvals</p>
</header>

<nav>
    <a href="/">Dashboard</a>
    <a href="/suppliers">Suppliers</a>
    <a href="/products">Products</a>
    <a href="/requests">Purchase Requests</a>
    <a href="/orders">Purchase Orders</a>
</nav>

<div class="container">

    {% with messages = get_flashed_messages() %}
        {% for message in messages %}
            <div class="success">{{ message }}</div>
        {% endfor %}
    {% endwith %}

    {% if page == "dashboard" %}

        <h2>Dashboard Overview</h2>

        <div class="cards">

            <div class="card">
                <h3>Departments</h3>
                <h2>{{ departments }}</h2>
            </div>

            <div class="card">
                <h3>Employees</h3>
                <h2>{{ employees }}</h2>
            </div>

            <div class="card">
                <h3>Suppliers</h3>
                <h2>{{ suppliers }}</h2>
            </div>

            <div class="card">
                <h3>Products</h3>
                <h2>{{ products }}</h2>
            </div>

            <div class="card">
                <h3>Total Requests</h3>
                <h2>{{ requests_count }}</h2>
            </div>

            <div class="card">
                <h3>Pending Requests</h3>
                <h2>{{ pending }}</h2>
            </div>

            <div class="card">
                <h3>Approved Requests</h3>
                <h2>{{ approved }}</h2>
            </div>

            <div class="card">
                <h3>Rejected Requests</h3>
                <h2>{{ rejected }}</h2>
            </div>

            <div class="card">
                <h3>Purchase Orders</h3>
                <h2>{{ total_orders }}</h2>
            </div>

            <div class="card">
                <h3>Order Value</h3>
                <h2>₹{{ "%.2f"|format(total_amount) }}</h2>
            </div>

        </div>

        <div class="panel">
            <h2>Recent Purchase Requests</h2>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Employee</th>
                    <th>Department</th>
                    <th>Date</th>
                    <th>Amount</th>
                    <th>Status</th>
                </tr>

                {% for item in recent_requests %}
                <tr>
                    <td>{{ item.request_id }}</td>
                    <td>{{ item.employee_name or 'N/A' }}</td>
                    <td>{{ item.department_name or 'N/A' }}</td>
                    <td>{{ item.request_date }}</td>
                    <td>₹{{ "%.2f"|format(item.total_amount) }}</td>
                    <td class="status {{ item.status|lower }}">
                        {{ item.status }}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>

    {% elif page == "suppliers" %}

        <h2>Supplier Management</h2>

        <div class="panel">
            <h3>Add New Supplier</h3>

            <form method="POST">
                <label>Supplier Name</label>
                <input type="text" name="supplier_name" required>

                <label>Contact Person</label>
                <input type="text" name="contact_person">

                <label>Email</label>
                <input type="email" name="email">

                <label>Phone</label>
                <input type="text" name="phone">

                <label>Address</label>
                <input type="text" name="address">

                <button type="submit">Add Supplier</button>
            </form>
        </div>

        <div class="panel">
            <h3>Supplier List</h3>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Contact</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Address</th>
                </tr>

                {% for s in supplier_list %}
                <tr>
                    <td>{{ s.supplier_id }}</td>
                    <td>{{ s.supplier_name }}</td>
                    <td>{{ s.contact_person }}</td>
                    <td>{{ s.email }}</td>
                    <td>{{ s.phone }}</td>
                    <td>{{ s.address }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

    {% elif page == "products" %}

        <h2>Product Management</h2>

        <div class="panel">
            <h3>Add New Product</h3>

            <form method="POST">
                <label>Product Name</label>
                <input type="text" name="product_name" required>

                <label>Description</label>
                <input type="text" name="description">

                <label>Unit Price</label>
                <input type="number" name="unit_price"
                       min="0" step="0.01" required>

                <label>Quantity</label>
                <input type="number" name="quantity"
                       min="0" required>

                <button type="submit">Add Product</button>
            </form>
        </div>

        <div class="panel">
            <h3>Product List</h3>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Product</th>
                    <th>Description</th>
                    <th>Unit Price</th>
                    <th>Quantity</th>
                </tr>

                {% for p in product_list %}
                <tr>
                    <td>{{ p.product_id }}</td>
                    <td>{{ p.product_name }}</td>
                    <td>{{ p.description }}</td>
                    <td>₹{{ "%.2f"|format(p.unit_price) }}</td>
                    <td>{{ p.quantity }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

    {% elif page == "requests" %}

        <h2>Purchase Request Management</h2>

        <div class="panel">
            <h3>Create Purchase Request</h3>

            <form method="POST">

                <label>Select Employee</label>

                <select name="employee_id" required>
                    <option value="">Select Employee</option>

                    {% for e in employee_list %}
                    <option value="{{ e.employee_id }}">
                        {{ e.employee_name }}
                    </option>
                    {% endfor %}
                </select>

                <label>Total Amount</label>

                <input type="number"
                       name="total_amount"
                       min="0.01"
                       step="0.01"
                       required>

                <button type="submit">
                    Submit Request
                </button>

            </form>
        </div>

        <div class="panel">
            <h3>All Purchase Requests</h3>

            <table>
                <tr>
                    <th>ID</th>
                    <th>Employee</th>
                    <th>Department</th>
                    <th>Date</th>
                    <th>Amount</th>
                    <th>Status</th>
                    <th>Action</th>
                </tr>

                {% for r in request_list %}
                <tr>
                    <td>{{ r.request_id }}</td>
                    <td>{{ r.employee_name or 'N/A' }}</td>
                    <td>{{ r.department_name or 'N/A' }}</td>
                    <td>{{ r.request_date }}</td>
                    <td>₹{{ "%.2f"|format(r.total_amount) }}</td>

                    <td class="status {{ r.status|lower }}">
                        {{ r.status }}
                    </td>

                    <td>
                        {% if r.status == "Pending" %}

                        <a class="btn"
                           href="/update_request/{{ r.request_id }}/Approved">
                           Approve
                        </a>

                        <a class="btn reject"
                           href="/update_request/{{ r.request_id }}/Rejected">
                           Reject
                        </a>

                        {% else %}
                            Completed
                        {% endif %}
                    </td>
                </tr>
                {% endfor %}
            </table>
        </div>

    {% elif page == "orders" %}

        <h2>Purchase Order Management</h2>

        <div class="panel">
            <h3>Purchase Orders</h3>

            <table>
                <tr>
                    <th>Order ID</th>
                    <th>Request ID</th>
                    <th>Supplier</th>
                    <th>Order Date</th>
                    <th>Total Amount</th>
                    <th>Status</th>
                </tr>

                {% for o in order_list %}
                <tr>
                    <td>{{ o.order_id }}</td>
                    <td>{{ o.request_id }}</td>
                    <td>{{ o.supplier_name or 'N/A' }}</td>
                    <td>{{ o.order_date }}</td>
                    <td>₹{{ "%.2f"|format(o.total_amount) }}</td>
                    <td>{{ o.status }}</td>
                </tr>
                {% endfor %}
            </table>
        </div>

    {% endif %}

</div>

</body>
</html>
"""


# Start Flask application
if __name__ == "__main__":

    if not DB_PATH.exists():
        print("Database not found. Run python database.py first.")
    else:
        print("Starting Procurement Management System...")
        print("Open http://127.0.0.1:5000 in your browser")

        app.run(debug=True)
