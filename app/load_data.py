import os
import pandas as pd
from sqlalchemy import create_engine

# Koneksi ke PostgreSQL
DB_USER = "user"
DB_PASS = "password"
DB_HOST = "db"
DB_PORT = "5432"
DB_NAME = "mydb"

engine = create_engine(f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}")

# Mapping file with table name
files_tables = {
    "CRMCallCenterLogs.csv": "crm_call_center_logs",
    "CRMEvents.csv": "crm_events",
    "LuxuryLoanPortfolio.csv":"luxury_loan_portfolio"
}

for file_name, table_name in files_tables.items():
    file_path = os.path.join("/app/data", file_name)
    print(f"Loading {file_name} into table {table_name}...")

    # Read CSV
    try:
        df = pd.read_csv(file_path, encoding="utf-8")
    except UnicodeDecodeError:
        df = pd.read_csv(file_path, encoding="latin1")

    # Change columns name
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
        .str.replace("-", "_")
        .str.replace(r"\?", "", regex=True)
    )

    # formatting date
    if "date_received" in df.columns:
        df["date_received"] = pd.to_datetime(df["date_received"], errors="coerce").dt.date

    if "date_received" not in df.columns and "date_received" in [c.lower() for c in df.columns]:
        for col in df.columns:
            if col.lower() == "date_received":
                df[col] = pd.to_datetime(df[col], errors="coerce").dt.date


    # Save to postgresql
    df.to_sql(table_name, engine, if_exists="replace", index=False)

print("Data loaded successfully!")
