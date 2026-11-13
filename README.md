# Procurement_Management_System_

## 1. Project Overview

The **Procurement Management System** is a Python-based application designed to manage and monitor the complete procurement process, starting from purchase requests and supplier quotations to purchase approvals, purchase orders, and supplier deliveries.

The system provides a centralized platform for managing procurement activities, maintaining transaction records, tracking approvals, comparing supplier quotations, monitoring deliveries, and identifying procurement exceptions.

The project uses Python, Flask, SQLite, HTML, CSS, and data analysis libraries.

## 2. Problem Statement

Organizations need an effective procurement process to manage purchasing activities, supplier relationships, budgets, approvals, and deliveries.

Manual procurement processes can result in:
- Delays in purchase approvals.
- Difficulty comparing supplier quotations.
- Budget overruns.
- Unauthorized purchase orders.
- Supplier delivery delays.
- Lack of transaction traceability.
- Errors in procurement records.

This project aims to address these challenges through a centralized procurement management solution.

## 3. Project Objectives

The main objectives are:

1. Manage purchase requests and request details.
2. Maintain department, requester, supplier, and budget information.
3. Generate Request for Quotations (RFQs).
4. Collect and compare supplier quotations.
5. Implement approval workflows.
6. Generate purchase orders from selected quotations.
7. Track supplier deliveries.
8. Identify procurement exceptions and risks.
9. Maintain audit history for important transactions.
10. Generate structured CSV and JSON data exports.
11. Validate procurement data and transaction records.

## 4. Technologies Used

| Technology | Purpose |
|---|---|
| Python | Backend programming |
| Flask | Web application framework |
| SQLite | Database management |
| HTML | Web page structure |
| CSS | User interface styling |
| Bootstrap | Responsive interface components |
| Pandas | Data processing and analysis |
| Matplotlib | Data visualization |
| CSV | Structured data exports |
| JSON | Data exchange and reporting |

## 5. System Modules

### 5.1 Master Data Management

Maintains the basic procurement information:

- Departments
- Requesters
- Budgets
- Suppliers

### 5.2 Purchase Request Management

Allows users to create purchase requests with:

- Request ID
- Requester information
- Department
- Item name
- Item category
- Quantity
- Unit price
- Estimated total
- Business justification

### 5.3 Approval Management

Maintains approval records for different approval levels:

- Department Manager
- Finance
- Procurement Head

Approval requirements depend on purchase value and applicable business rules.

### 5.4 Request for Quotation (RFQ)

Creates RFQs for eligible purchase requests and records supplier quotation information.

### 5.5 Supplier Quote Comparison

Stores and compares supplier quotations based on:

- Supplier
- Quotation amount
- Freight charges
- Tax
- Total landed cost
- Delivery time
- Supplier status
- Supplier risk

### 5.6 Purchase Order Management

Maintains purchase orders generated from selected supplier quotations.

Purchase order records include:

- PO number
- Purchase request ID
- Supplier ID
- Selected quotation
- Order date
- Total amount
- Approval status

### 5.7 Delivery Management

Tracks supplier delivery information, including:

- Delivery ID
- Purchase order ID
- Delivery date
- Quantity received
- Delivery status
- Delivery notes

### 5.8 Exception Management

Identifies procurement issues such as:

- Purchase orders without approval
- Expired supplier quotations
- Inactive suppliers
- Currency mismatches
- Supplier risk concerns
- Budget overruns
- Duplicate purchase requests

The complete exception rules are subject to implementation and validation.

### 5.9 Audit Management

Maintains records of important procurement activities, including entity details, actions, previous values, updated values, actors, and event timestamps.

## 6. Project Folder Structure

```text
Procurement_Management_System/
│
├── app.py
├── database.py
├── generator.py
├── validate.py
├── requirements.txt
├── README.md
├── procurement.db
├── ground_truth.csv
├── validation_summary.jso
│
├── docs/
│   ├── DATA_DICTIONARY.md
│
├── templates/
│   ├── base.html
│   ├── dashboard.html
│   ├── requests.html
│   ├── suppliers.html
│   ├── quotes.html
│   ├── orders.html
│   ├── exceptions.html
│   └── new_request.html
│
├── static/
│   └── style.css
│
└── exports/
    ├── approvals.csv
    ├── departments.csv
    ├── purchase_orders.csv
    ├── purchase_requests.csv
    ├── source_manifest.json
    ├── suppliers.csv
    
```

Note: Generated database, reports, and export files appear after running the corresponding project scripts. Additional documentation files should be created as the project is completed.

## 7. Database Design

The application uses SQLite for storing procurement information.

The database contains the following main tables:

| Table | Description |
|---|---|
| departments | Department information |
| requesters | Employee/requester information |
| budgets | Department budget information |
| suppliers | Supplier details |
| purchase_requests | Purchase request records |
| request_lines | Requested items and quantities |
| rfqs | Request for quotation records |
| supplier_quotes | Supplier quotation details |
| approvals | Approval decisions |
| purchase_orders | Purchase order records |
| purchase_order_lines | Items included in purchase orders |
| deliveries | Supplier delivery records |
| audit_events | Transaction audit history |
| exception_records | Procurement exception records |

## 8. Installation and Setup

### Prerequisites

Install the following:

- Python 3.10 or later
- Visual Studio Code
- Python extension for VS Code

### Step 1: Open the project folder

Open the `Procurement_Management_System` folder in Visual Studio Code.

### Step 2: Open the terminal

Select:

Terminal → New Terminal

Make sure the terminal is inside the project folder.

### Step 3: Create a virtual environment

```bash
py -m venv venv
```

### Step 4: Activate the virtual environment

For Windows PowerShell:

```powershell
.\venv\Scripts\Activate.ps1
```

### Step 5: Install dependencies

```bash
py -m pip install -r requirements.txt
```

The requirements file contains:

```text
Flask==3.1.0
pandas==2.2.3
matplotlib==3.10.0
```

## 9. Running the Application

Run the following commands from the main project directory.

### Step 1: Initialize the database

```bash
py database.py
```

### Step 2: Generate starter dataset

```bash
py generator.py --scale starter
```

### Step 3: Validate the generated dataset

```bash
py validate.py
```

### Step 4: Start the Flask application

```bash
py app.py
```

### Step 5: Open the application

Open your browser and visit:

http://127.0.0.1:5000

## 10. Dataset Generation

The project supports two dataset configurations.

### Starter Dataset

```bash
py generator.py --scale starter
```

Expected configuration:

| Entity | Target count |
|---|---:|
| Requesters | 30 |
| Suppliers | 15 |
| Purchase Requests | 60 |
| RFQs | 25 |
| Supplier Quotes | 75 |
| Purchase Orders | 40 |

### Full Dataset

```bash
py generator.py --scale full
```

Target configuration:

| Entity | Target count |
|---|---:|
| Requesters | 300 |
| Suppliers | 120 |
| Purchase Requests | 1,200 |
| RFQs | 500 |
| Supplier Quotes | 1,500 |
| Purchase Orders | 900 |

**Random Seed:** `20261022`

The generator uses a fixed random seed to support repeatable synthetic data generation. Actual generated counts must be checked in the database and validation report.

## 11. Data Export

The system supports exporting procurement records in:

- CSV format
- JSON format

The generated exports are stored in the `exports/` directory.

The source manifest records the dataset seed, scale, and generated table row counts.

The `ground_truth.csv` file stores expected decisions for selected procurement exception scenarios.

## 12. Data Validation

The `validate.py` module is used to check the quality and consistency of generated procurement records.

Important validation checks include:

- Duplicate primary keys
- Foreign key integrity
- Missing required records
- Purchase request calculations
- Supplier quotation calculations
- Purchase order calculations
- Invalid quotation dates
- Relationship consistency

The validation report is saved as:

```text
validation_summary.json
```

Additional acceptance checks should verify lifecycle transitions, delivery reconciliation, budget calculations, exception coverage, exact dataset sizes, and reproducibility checksums.

## 13. Expected Project Outcomes

The intended outcomes are:

1. Centralized procurement record management.
2. Better visibility into purchase requests.
3. Improved supplier quotation comparison.
4. Structured approval tracking.
5. Better monitoring of purchase orders and deliveries.
6. Identification of procurement risks and exceptions.
7. Improved data traceability.
8. Structured procurement data exports.
9. Consistent procurement reporting.

## 14. Limitations and Future Enhancements

The current implementation is a prototype and requires additional development and testing before all business requirements can be considered complete.

Future enhancements include:

- Complete multi-level approval enforcement.
- Automated budget reservation and reconciliation.
- Prevention of unauthorized purchase orders.
- Duplicate purchase request detection.
- Complete single-source purchasing workflow.
- Advanced supplier performance evaluation.
- Complete exception detection and ground-truth coverage.
- Reproducibility checksums.
- Advanced procurement analytics and charts.
- User authentication and role-based access control.
- Improved reporting and downloadable reports.

## 15. Data Privacy and Provenance

This project uses synthetically generated procurement data for demonstration and testing.

Names, email addresses, supplier records, transaction amounts, and other generated information are fictional.

No real supplier quotations, company procurement transactions, or confidential business records are represented.

## 16. Conclusion

The Procurement Management System provides a structured approach to managing the procurement lifecycle, including purchase requests, supplier quotations, approvals, purchase orders, and deliveries.

By combining Python, Flask, and SQLite, the project establishes a foundation for improving procurement visibility, transaction tracking, and exception management.

The system can be extended with additional business rules, validation mechanisms, and analytics to support a more complete end-to-end procurement solution.

---

**Project Name:** Procurement Management System

**Primary Language:** Python

**Database:** SQLite

**Framework:** Flask

**Data Type:** Synthetic Procurement Data
