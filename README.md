# Cloud-Ready Financial Data Ingestion & Transformation Pipeline

## Overview
This repository contains an end-to-end Python-based ETL pipeline designed to ingest raw, batch financial data, execute automated schema validation, segregate corrupted records for auditing, and stage validated analytical files for cloud object storage (e.g., AWS S3 / Azure Blob).

## Core Features
1. **Automated Extraction:** Ingests raw batch CSV files simulating banking transaction feeds.
2. **Schema & Business Validation:**
   * Rejects missing values and non-positive transactional amounts.
   * Standardizes heterogeneous date formats (`YYYY/MM/DD` $\to$ `YYYY-MM-DD`).
   * Normalizes category casing for reliable downstream analytics.
3. **Data Quality & Audit Segregation:** Clean records and rejected anomalies are routed to separate files to maintain downstream database reliability.
4. **Cloud-Ready Staging:** Simulates staging curated datasets for cloud storage consumption (aligning with cloud computing paradigms).

## How to Run (Using Python standard library - No external packages required)
```bash
python pipeline.py
