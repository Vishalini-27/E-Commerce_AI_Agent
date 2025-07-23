from db_config import get_connection

def create_tables():
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS product_eligibility (
        eligibility_datetime_utc DATETIME,
        item_id INT,
        eligibility BOOLEAN,
        message TEXT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ad_sales_metrics (
        date DATE,
        item_id INT,
        ad_sales FLOAT,
        impressions INT,
        ad_spend FLOAT,
        clicks INT,
        units_sold INT
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS total_sales_metrics (
        date DATE,
        item_id INT,
        total_sales FLOAT,
        total_units_ordered INT
    )
    """)

    conn.commit()
    conn.close()
    print("Tables created successfully.")

if __name__ == '__main__':
    create_tables()
