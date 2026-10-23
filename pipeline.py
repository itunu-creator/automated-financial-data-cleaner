"""
Automated Financial Ingestion & Transformation Pipeline (ETL)
Simulates extracting raw batch transaction data, cleaning/validating records,
and preparing transformed datasets for cloud object storage ingestion.
"""

import csv
import os
from datetime import datetime

# Sample raw transactional data simulating a daily batch drop
SAMPLE_RAW_DATA = """txn_id,account_number,txn_amount,txn_date,txn_type
TXN_101,ACC_4401,1500.50,2026-10-01,DEPOSIT
TXN_102,ACC_4402,,2026-10-01,WITHDRAWAL
TXN_103,ACC_4403,-250.00,2026-10-02,WITHDRAWAL
TXN_104,ACC_4401,3400.00,2026-10-02,DEPOSIT
TXN_105,ACC_4404,500.00,2026/10/03,DEPOSIT
"""

RAW_FILENAME = "raw_transactions.csv"
CLEAN_FILENAME = "transformed_transactions.csv"
REJECTS_FILENAME = "rejected_records.csv"


def extract_raw_file():
    """Simulates receiving raw batch CSV data from transactional branches."""
    with open(RAW_FILENAME, "w", encoding="utf-8") as f:
        f.write(SAMPLE_RAW_DATA)
    print(f"[EXTRACT] Raw transaction batch written to {RAW_FILENAME}")


def transform_and_validate():
    """
    Parses raw transactional records, enforces data schema rules:
    - Verifies amount is not null and is positive
    - Standardizes date formats to ISO YYYY-MM-DD
    - Normalizes transaction types to uppercase
    Separates clean records from corrupted/rejected records.
    """
    clean_records = []
    rejected_records = []

    with open(RAW_FILENAME, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            txn_id = row.get("txn_id")
            account = row.get("account_number")
            raw_amount = row.get("txn_amount")
            raw_date = row.get("txn_date")
            txn_type = row.get("txn_type", "").upper()

            # Validation 1: Check for missing or invalid numerical amount
            try:
                amount = float(raw_amount)
                if amount <= 0:
                    rejected_records.append({**row, "rejection_reason": "Non-positive transaction amount"})
                    continue
            except (ValueError, TypeError):
                rejected_records.append({**row, "rejection_reason": "Missing or non-numeric amount"})
                continue

            # Validation 2: Standardize date format to YYYY-MM-DD
            standardized_date = raw_date.replace("/", "-")

            clean_records.append({
                "txn_id": txn_id,
                "account_number": account,
                "amount": f"{amount:.2f}",
                "transaction_date": standardized_date,
                "transaction_type": txn_type,
                "processed_at_utc": datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
            })

    # Write Clean Data
    if clean_records:
        keys = clean_records[0].keys()
        with open(CLEAN_FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(clean_records)
        print(f"[TRANSFORM] {len(clean_records)} clean records written to {CLEAN_FILENAME}")

    # Write Rejection Log (For audit/compliance)
    if rejected_records:
        keys = rejected_records[0].keys()
        with open(REJECTS_FILENAME, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=keys)
            writer.writeheader()
            writer.writerows(rejected_records)
        print(f"[AUDIT] {len(rejected_records)} invalid records routed to {REJECTS_FILENAME}")


def simulate_cloud_upload():
    """
    Simulates staging clean files to cloud storage (e.g., AWS S3 / Azure Blob Storage).
    Concepts aligned with cloud storage fundamentals (datAFRIK).
    """
    target_bucket = "s3://corporate-banking-lakehouse/curated/transactions/"
    print(f"[LOAD/CLOUD] Staging {CLEAN_FILENAME} for ingestion into: {target_bucket}")
    print("[SUCCESS] Pipeline cycle executed cleanly.")


if __name__ == "__main__":
    extract_raw_file()
    transform_and_validate()
    simulate_cloud_upload()
