# Procurement Management System

## Project Description

An end-to-end procurement management application that
manages purchase requests, approvals, supplier quotations,
purchase orders, deliveries and procurement exceptions.

## Technologies

- Python
- Flask
- SQLite
- Pandas
- Matplotlib
- HTML
- CSS
- Bootstrap

## Main Modules

1. Master Data Management
2. Purchase Request Management
3. Approval Management
4. RFQ Management
5. Supplier Quote Comparison
6. Purchase Order Management
7. Delivery Management
8. Exception Management
9. Audit Tracking
10. Synthetic Data Generation
11. Data Validation

## Setup

Install dependencies:

    py -m pip install -r requirements.txt

Initialize the database:

    py database.py

Generate starter data:

    py generator.py --scale starter

Validate data:

    py validate.py

Start the application:

    py app.py

Open:

    http://127.0.0.1:5000

## Full Dataset

    py generator.py --scale full

## Reproducibility

Random seed: 20261022

All generated records are synthetic.
No confidential supplier or personal information is used.

## Database

SQLite database: procurement.db

## Exports

CSV and JSON exports are stored in exports/.

Ground-truth labels are stored separately
in ground_truth.csv.

## Future Enhancements

- Complete RFQ workflow interface
- Budget reservation and reconciliation
- Delivery quantity validation
- Advanced exception detection
- Procurement analytics
- Supplier performance scoring
- Role-based authentication
