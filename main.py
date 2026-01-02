import os.path
import random
import sqlite3

from fastmcp import FastMCP
import sqlite3
import os

connection_string = os.path.join(os.path.dirname(__file__), "expenses.db")

def init_db_connection(connection_string: str):
    try:
        with sqlite3.connect(connection_string) as conn:
            conn.execute(
            """CREATE TABLE IF NOT EXISTS expenses_table(
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            amount REAL NOT NULL,
            category TEXT NOT NULL,
            subcategory TEXT DEFAULT '',
            note TEXT DEFAULT '');""")
            print("Database initialized successfully.")
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")


init_db_connection(connection_string)

# creating a FastMCP server
mcp = FastMCP(name="my_first_mcp_server")

@mcp.tool
def add_expense(date, amount, category, subcategory, note):
    """Adds an expense to the database."""
    with sqlite3.connect(connection_string) as conn:
        cursor = conn.execute(
            "INSERT INTO expenses_table (date, amount, category, subcategory, note) VALUES (?, ?, ?, ?, ?)",
            (date, amount, category, subcategory, note),
        )
        return {"status": "success", "id": cursor.lastrowid}

@mcp.tool
def list_expenses():
    """Lists all expenses in the database."""
    with sqlite3.connect(connection_string) as conn:
        curr =  conn.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses_table ORDER BY id ASC")
        cols = [d[0] for d in curr.description ]
        return [dict(zip(cols, r)) for r in  curr.fetchall()]


@mcp.tool
def list_expenses_on_category(category):
    with sqlite3.connect(connection_string) as conn:
        curr = conn.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses_table WHERE category = ? ORDER BY id ASC",
            (category,))
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, r)) for r in curr.fetchall()]


@mcp.tool
def list_expense_between_dates(start_date, end_date):
    with sqlite3.connect(connection_string) as conn:
        curr = conn.execute(
            "SELECT id, date, amount, category, subcategory, note FROM expenses_table WHERE date BETWEEN ? AND ? ORDER BY id ASC",
            (start_date, end_date))
        cols = [d[0] for d in curr.description]
        return [dict(zip(cols, r)) for r in curr.fetchall()]

if __name__ == "__main__":
    mcp.run()

