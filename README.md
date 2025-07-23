cat > README.md << 'EOF'
# EchoCommerce AI Agent

EchoCommerce is a command-line, AI-powered assistant that interprets natural language queries, generates SQL, executes them on a MySQL database, and displays both tabular and visual outputs. It is designed to help users interact with e-commerce data through plain English queries.

---

## Features

- Ask natural-language queries about:
  - Total sales
  - Sales trends by item or date
  - Customer eligibility
  - Ad spend, CPC, ROAS
- Visualizes results using matplotlib charts
- Real-time simulated typing response
- Connects to a live MySQL database
- Modular and clean Python codebase

---

## Project Structure

\`\`\`
EchoCommerce/
├── backend/
│   ├── db_config.py         # MySQL connection setup
│   ├── create_tables.py     # Creates required tables
│   ├── load_data.py         # Loads CSVs into DB
│   ├── query_engine.py      # Executes SQL queries
│   └── prompt_agent.py      # Main AI assistant
├── datasets/
│   ├── Ad Sales and Metrics.csv
│   ├── Sales and Metrics.csv
│   └── Eligibility.csv
├── requirements.txt         # Python dependencies
└── README.md
\`\`\`

---

## Setup Instructions

### Step 1: Clone the Repository

\`\`\`bash
git clone https://github.com/your-username/EchoCommerce.git
cd EchoCommerce
\`\`\`

### Step 2: Set Up Virtual Environment

\`\`\`bash
python -m venv venv
source venv/bin/activate        # On Linux or macOS
venv\Scripts\activate           # On Windows
\`\`\`

### Step 3: Install Python Dependencies

\`\`\`bash
pip install -r requirements.txt
\`\`\`

### Step 4: Configure the Database

Edit the following file with your MySQL connection details:

\`\`\`python
# backend/db_config.py
host = "your-mysql-host"
user = "your-username"
password = "your-password"
database = "your-database-name"
port = 3306
\`\`\`

### Step 5: Create Tables

\`\`\`bash
python backend/create_tables.py
\`\`\`

### Step 6: Load Dataset

Make sure the \`datasets/\` folder contains the following files:

- Eligibility.csv
- Ad Sales and Metrics.csv
- Sales and Metrics.csv

Then run:

\`\`\`bash
python backend/load_data.py
\`\`\`

---

## Running the AI Agent

\`\`\`bash
python backend/prompt_agent.py
\`\`\`

You will be prompted to type a natural language question.

### Example Prompts

\`\`\`text
What is my total sales
Calculate the RoAS (Return on Ad Spend)
Which product had the highest CPC (Cost Per Click)
Show sales by item
Show sales by date
Show average CPC
\`\`\`

---

## Real-Time Output and Visuals

- If your query relates to date or item-based sales, the agent will plot a bar/line chart using matplotlib.
- For summary metrics (e.g., total sales, ROAS), it streams the answer as if an AI assistant is typing it in real-time.

---

## Dataset Information

### Eligibility.csv

| eligibility_datetime_utc | item_id | eligibility | message        |
|--------------------------|---------|-------------|----------------|
| 2024-06-01 10:00:00      | 101     | 1           | Eligible item  |

### Ad Sales and Metrics.csv

| date       | item_id | ad_sales | impressions | ad_spend | clicks | units_sold |
|------------|---------|----------|-------------|----------|--------|------------|

### Sales and Metrics.csv

| date       | item_id | total_sales | total_units_ordered |
|------------|---------|-------------|----------------------|

---

## Dependencies

All dependencies are included in \`requirements.txt\`. Install them with:

\`\`\`bash
pip install -r requirements.txt
\`\`\`

Key libraries:

- pandas
- matplotlib
- openai
- mysql-connector-python
- tabulate

---
