from tabulate import tabulate
from datetime import datetime
from db_config import get_connection
import pandas as pd

def execute_query(query, return_df=False):
    try:
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        columns = [desc[0] for desc in cursor.description]

        if return_df:
            df = pd.DataFrame(results, columns=columns)
            return df

        return results, columns

    except Exception as e:
        print(f"Database error: {e}")
        return (pd.DataFrame() if return_df else ([], []))

    finally:
        if 'cursor' in locals():
            cursor.close()
        if 'conn' in locals() and conn.is_connected():
            conn.close()

def format_results(df):
    if isinstance(df, pd.DataFrame):
        return tabulate(df, headers='keys', tablefmt='fancy_grid', showindex=False)
    return ""

def get_dataset(prompt):
    prompt = prompt.lower()
    if "eligibility" in prompt:
        return "customer_eligibility"
    elif "ad" in prompt or "spend" in prompt or "roas" in prompt:
        return "ad_sales_metrics"
    elif "sale" in prompt or "revenue" in prompt:
        return "total_sales_metrics"
    return None
