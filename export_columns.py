import psycopg2
import pandas as pd
import os

# Database connection details
conn = psycopg2.connect(
    host="powerbi-data-analytics-server.postgres.database.azure.com",
    port="5432",
    database="orders-db",
    user="maya",
    password="AiCore127!"
)

# Directory to save the CSV files
output_dir = 'F:\PowerBI\columns'
os.makedirs(output_dir, exist_ok=True)

# Query to get list of tables
tables_query = "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' ORDER BY table_name;"
tables_df = pd.read_sql(tables_query, conn)
tables_df.to_csv(os.path.join(output_dir, 'tables_list.csv'), index=False)

# Function to get columns of a table
def get_columns(table_name):
    columns_query = f"SELECT column_name FROM information_schema.columns WHERE table_name = '{table_name}' ORDER BY ordinal_position;"
    columns_df = pd.read_sql(columns_query, conn)
    columns_df.to_csv(os.path.join(output_dir, f'{table_name}_columns.csv'), index=False)

# Get columns for each table
for table in tables_df['table_name']:
    get_columns(table)

# Close the connection
conn.close()