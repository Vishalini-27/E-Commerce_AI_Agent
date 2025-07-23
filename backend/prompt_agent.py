import sys
import os
from datetime import datetime
import time
import pandas as pd
import matplotlib.pyplot as plt
from tabulate import tabulate

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from backend.query_engine import execute_query

def interpret_prompt(prompt):
    prompt = prompt.lower().strip()

    if any(word in prompt for word in ["total sales", "overall sales"]):
        return "SELECT SUM(total_sales) AS total_sales FROM total_sales_metrics;"

    elif "sales by date" in prompt:
        return "SELECT date, SUM(total_sales) AS total_sales FROM total_sales_metrics GROUP BY date ORDER BY date;"

    elif "sales by item" in prompt:
        return "SELECT item_id, SUM(total_sales) AS total_sales FROM total_sales_metrics GROUP BY item_id ORDER BY total_sales DESC;"

    elif "eligible customers" in prompt:
        return "SELECT COUNT(*) AS eligible_customers FROM customer_eligibility WHERE is_eligible = 1;"

    elif "eligibility breakdown" in prompt or "eligibility by item" in prompt:
        return """
        SELECT item_id,
               SUM(CASE WHEN is_eligible = 1 THEN 1 ELSE 0 END) AS eligible_count,
               SUM(CASE WHEN is_eligible = 0 THEN 1 ELSE 0 END) AS not_eligible_count
        FROM customer_eligibility
        GROUP BY item_id
        ORDER BY eligible_count DESC;
        """

    elif "average cpc" in prompt:
        return "SELECT AVG(ad_spend / NULLIF(clicks, 0)) AS average_cpc FROM ad_sales_metrics;"

    elif "highest cpc" in prompt:
        return """
        SELECT item_id, MAX(ad_spend / NULLIF(clicks, 0)) AS highest_cpc
        FROM ad_sales_metrics
        GROUP BY item_id
        ORDER BY highest_cpc DESC
        LIMIT 1;
        """

    elif "roas" in prompt or "return on ad spend" in prompt:
        return """
        SELECT SUM(ad_sales) / NULLIF(SUM(ad_spend), 0) AS ROAS
        FROM ad_sales_metrics;
        """

    else:
        return None

def simulate_streaming(text, delay=0.03):
    for char in text:
        print(char, end='', flush=True)
        time.sleep(delay)
    print()

def plot_graph(df, prompt):
    if "sales by date" in prompt and 'date' in df.columns:
        df['date'] = pd.to_datetime(df['date'])
        plt.figure(figsize=(10, 5))
        plt.plot(df['date'], df['total_sales'], marker='o')
        plt.title("Total Sales by Date")
        plt.xlabel("Date")
        plt.ylabel("Total Sales")
        plt.grid(True)
        plt.tight_layout()
        plt.xticks(rotation=45)
        plt.show()

    elif "sales by item" in prompt and 'item_id' in df.columns:
        plt.figure(figsize=(10, 5))
        plt.bar(df['item_id'].astype(str), df['total_sales'], color='teal')
        plt.title("Sales by Item")
        plt.xlabel("Item ID")
        plt.ylabel("Total Sales")
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.show()

    elif "eligibility breakdown" in prompt or "eligibility by item" in prompt:
        if 'item_id' in df.columns and 'eligible_count' in df.columns:
            plt.figure(figsize=(10, 5))
            plt.bar(df['item_id'].astype(str), df['eligible_count'], label='Eligible', color='green')
            plt.bar(df['item_id'].astype(str), df['not_eligible_count'], bottom=df['eligible_count'], label='Not Eligible', color='red')
            plt.title("Eligibility Breakdown by Item")
            plt.xlabel("Item ID")
            plt.ylabel("Customer Count")
            plt.legend()
            plt.xticks(rotation=45)
            plt.tight_layout()
            plt.show()

def format_results(df):
    return tabulate(df, headers='keys', tablefmt="fancy_grid", showindex=False)

def main():
    print("E-Commerce Query AI Agent: Ask your question (type 'exit' to quit)\n")

    while True:
        prompt = input("Ask your question (or type 'exit'): ").strip()
        if prompt.lower() == 'exit':
            print("Exiting. Have a great day!")
            break

        query = interpret_prompt(prompt)

        if not query:
            print("Could not determine the dataset (sales, eligibility, or ads). Try rephrasing.\n")
            continue

        simulate_streaming("Processing your request...", delay=0.02)
        print("\nSQL Generated:\n" + query.strip() + "\n")

        try:
            results, columns = execute_query(query)

            if results:
                df = pd.DataFrame(results, columns=columns)
                print(format_results(df))
                print()

                # To show graphs for specific queries
                plot_graph(df, prompt)

                # To simulate streaming for certain types of data
                if "total sales" in prompt or "roas" in prompt:
                    for index, row in df.iterrows():
                        for col in df.columns:
                            simulate_streaming(f"{col}: {row[col]}", delay=0.05)

            else:
                print("No results returned.\n")

        except Exception as e:
            print(f"Error executing query or plotting results: {e}\n")

if __name__ == "__main__":
    main()
