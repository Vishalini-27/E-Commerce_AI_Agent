import pandas as pd
import os
from db_config import get_connection

def clean_row(row):
    """Replaces NaN with None to prevent SQL errors."""
    return [None if pd.isna(x) else x for x in row]

def load_csv_to_db():
    base_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'datasets'))

    eligibility_path = os.path.join(base_path, 'Eligibility.csv')
    ad_sales_path = os.path.join(base_path, 'Ad Sales and Metrics.csv')
    total_sales_path = os.path.join(base_path, 'Sales and Metrics.csv')

    # Load CSVs
    eligibility = pd.read_csv(eligibility_path)
    ad_sales = pd.read_csv(ad_sales_path)
    total_sales = pd.read_csv(total_sales_path)

    # Connect to MySQL
    conn = get_connection()
    cursor = conn.cursor()

    print("Uploading product_eligibility data...")
    eligibility_clean = [clean_row(row) for _, row in eligibility.iterrows()]
    cursor.executemany("""
        INSERT INTO product_eligibility VALUES (%s, %s, %s, %s)
    """, eligibility_clean)
    conn.commit()
    print(f"Inserted {len(eligibility_clean)} rows into product_eligibility.")

    print("Uploading ad_sales_metrics data...")
    ad_sales_clean = [clean_row(row) for _, row in ad_sales.iterrows()]
    cursor.executemany("""
        INSERT INTO ad_sales_metrics VALUES (%s, %s, %s, %s, %s, %s, %s)
    """, ad_sales_clean)
    conn.commit()
    print(f"Inserted {len(ad_sales_clean)} rows into ad_sales_metrics.")

    print("Uploading total_sales_metrics data...")
    total_sales_clean = [clean_row(row) for _, row in total_sales.iterrows()]
    cursor.executemany("""
        INSERT INTO total_sales_metrics VALUES (%s, %s, %s, %s)
    """, total_sales_clean)
    conn.commit()
    print(f"Inserted {len(total_sales_clean)} rows into total_sales_metrics.")

    cursor.close()
    conn.close()
    print("All data uploaded successfully.")

if __name__ == '__main__':
    load_csv_to_db()
