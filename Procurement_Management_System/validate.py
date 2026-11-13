
import sqlite3
from pathlib import Path

DB_PATH = Path(__file__).parent / "procurement.db"


def validate_database():

    print("\n========== PROCUREMENT DATABASE VALIDATION ==========\n")

    if not DB_PATH.exists():
        print("ERROR: Database file does not exist!")
        print("Please run: python database.py")
        return

    try:
        connection = sqlite3.connect(DB_PATH)
        connection.row_factory = sqlite3.Row

        cursor = connection.cursor()

        # Check database integrity
        cursor.execute("PRAGMA integrity_check")
        result = cursor.fetchone()[0]

        print("Database Integrity:", result)

        if result != "ok":
            print("ERROR: Database integrity check failed!")
            connection.close()
            return

        # Check required tables
        required_tables = [
            "departments",
            "employees",
            "suppliers",
            "products",
            "purchase_requests",
            "purchase_orders",
            "order_items",
            "approvals"
        ]

        cursor.execute("""
            SELECT name FROM sqlite_master
            WHERE type = 'table'
        """)

        existing_tables = [
            row["name"] for row in cursor.fetchall()
        ]

        print("\nTable Validation:")

        for table in required_tables:
            if table in existing_tables:
                print(f"PASS: {table} table exists")
            else:
                print(f"FAIL: {table} table is missing")

        # Check records in each table
        print("\nRecord Count:")

        for table in required_tables:
            if table in existing_tables:
                cursor.execute(
                    f"SELECT COUNT(*) FROM {table}"
                )
                count = cursor.fetchone()[0]
                print(f"{table}: {count} records")

        # Check foreign key relationships
        cursor.execute("PRAGMA foreign_key_check")
        foreign_key_errors = cursor.fetchall()

        print("\nForeign Key Validation:")

        if len(foreign_key_errors) == 0:
            print("PASS: No foreign key errors")
        else:
            print("FAIL: Foreign key errors found")

            for error in foreign_key_errors:
                print(tuple(error))

        # Final result
        if all(table in existing_tables for table in required_tables):
            print("\nSUCCESS: All required tables are available!")
        else:
            print("\nWARNING: Some required tables are missing.")

        connection.close()

        print("\n========== VALIDATION COMPLETED ==========\n")

    except sqlite3.DatabaseError as error:
        print("Database Error:", error)

    except Exception as error:
        print("Unexpected Error:", error)


if __name__ == "__main__":
    validate_database()
