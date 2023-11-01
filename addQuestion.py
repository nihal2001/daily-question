import os
import pyodbc
import csv
from datetime import datetime

def get_today_question(filename):
    # Assuming the csv has a column "date" in format YYYY-MM-DD and a column "question"
    today = datetime.now().date()
    with open(filename, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if datetime.strptime(row['date'], "%Y-%m-%d").date() == today:
                return row['question']
    return None

global conn

# Connection string
# Use environment variables or Azure Key Vault to secure your credentials
conn_str = ("Driver={ODBC Driver 17 for SQL Server};"
            "Server=tcp:qotd.database.windows.net,1433;"
            "Database=qotddb;"
            "UID=nihal;"
            "PWD=Pokem0n10!;"
            "Encrypt=yes;"
            "TrustServerCertificate=yes;")

try:
    conn = pyodbc.connect(conn_str)
except pyodbc.Error as e:
    print(f"Error: {e}")
    conn = None

if conn:
    # Get today's question from CSV
    question_for_today = get_today_question('questions.csv')
    
    if question_for_today:
        cursor = conn.cursor()
        # Assuming you have a table "questions" with columns "date" and "question"
        cursor.execute("INSERT INTO Questions(Date, Content) VALUES (?, ?)", datetime.now().date(), question_for_today)
        conn.commit()

        print(f"Inserted question for {datetime.now().date()}: {question_for_today}")
    else:
        print(f"No question for {datetime.now().date()}")

    cursor.close()
    conn.close()
