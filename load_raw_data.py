"""
load_raw_data.py

Loads the four CSV files from data/raw/
into the PostgreSQL raw schema.

CSV files:
    patients.csv
    providers.csv
    appointments.csv
    payments.csv

PostgreSQL tables:
    raw.patients_file
    raw.providers_file
    raw.appointments_file
    raw.payments_file
"""

from pathlib import Path

import pandas as pd
import psycopg2


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parent

RAW_DIR = BASE_DIR / "data" / "raw"


# PostgreSQL connection details
DB_CONFIG = {
    "host": "localhost",
    "port": 5432,
    "database": "clinic_db",
    "user": "postgres",
    "password": "harivardhan",
}


# ============================================================
# FILE -> TABLE MAPPING
# ============================================================

FILE_TABLE_MAPPING = {
    "patients.csv": "raw.patients_file",
    "providers.csv": "raw.providers_file",
    "appointments.csv": "raw.appointments_file",
    "payments.csv": "raw.payments_file",
}


# ============================================================
# LOAD CSV INTO POSTGRESQL
# ============================================================

def load_csv_to_postgres(
    connection,
    csv_file,
    table_name
):
    """
    Read a CSV file and insert its records
    into the specified PostgreSQL table.
    """

    csv_path = RAW_DIR / csv_file

    print()
    print("-" * 60)
    print(f"Loading: {csv_file}")
    print(f"Target : {table_name}")
    print("-" * 60)

    # Check whether CSV exists
    if not csv_path.exists():

        print(
            f"ERROR: File not found: {csv_path}"
        )

        return False

    try:

        # Read CSV
        df = pd.read_csv(
            csv_path,
            dtype=str
        )

        # Replace NaN with None
        df = df.where(
            pd.notnull(df),
            None
        )

        print(
            f"Records found: {len(df)}"
        )

        # Get column names
        columns = list(df.columns)

        column_string = ", ".join(
            f'"{column}"'
            for column in columns
        )

        # Create placeholders
        placeholders = ", ".join(
            ["%s"] * len(columns)
        )

        insert_sql = f"""
            INSERT INTO {table_name}
            ({column_string})
            VALUES ({placeholders})
        """

        cursor = connection.cursor()

        # Convert DataFrame rows to tuples
        rows = [
            tuple(row)
            for row in df.itertuples(
                index=False,
                name=None
            )
        ]

        # Insert records
        cursor.executemany(
            insert_sql,
            rows
        )

        connection.commit()

        cursor.close()

        print(
            f"SUCCESS: {len(df)} records loaded "
            f"into {table_name}"
        )

        return True

    except Exception as error:

        connection.rollback()

        print(
            f"ERROR loading {csv_file}:"
        )

        print(error)

        return False


# ============================================================
# MAIN
# ============================================================

def main():

    print()
    print("=" * 60)
    print("POSTGRESQL RAW DATA LOAD")
    print("=" * 60)

    connection = None

    try:

        # ----------------------------------------------------
        # Connect to PostgreSQL
        # ----------------------------------------------------

        print()
        print("Connecting to PostgreSQL...")

        connection = psycopg2.connect(
            host=DB_CONFIG["host"],
            port=DB_CONFIG["port"],
            database=DB_CONFIG["database"],
            user=DB_CONFIG["user"],
            password=DB_CONFIG["password"],
        )

        print(
            "SUCCESS: Connected to clinic_db"
        )

        # ----------------------------------------------------
        # Load all four files
        # ----------------------------------------------------

        successful_loads = 0

        for csv_file, table_name in FILE_TABLE_MAPPING.items():

            success = load_csv_to_postgres(
                connection,
                csv_file,
                table_name
            )

            if success:
                successful_loads += 1

        # ----------------------------------------------------
        # Final summary
        # ----------------------------------------------------

        print()
        print("=" * 60)
        print("LOAD SUMMARY")
        print("=" * 60)

        print(
            f"Successfully loaded: "
            f"{successful_loads}/"
            f"{len(FILE_TABLE_MAPPING)} files"
        )

        print("=" * 60)

    except psycopg2.Error as error:

        print()
        print(
            "ERROR: Could not connect to PostgreSQL."
        )

        print(error)

    finally:

        if connection is not None:

            connection.close()

            print()
            print(
                "PostgreSQL connection closed."
            )


# ============================================================
# PROGRAM ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()