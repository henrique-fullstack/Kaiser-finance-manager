"""
Database Module for Kaiser Finance Manager.

This module handles all SQLite interactions, including connection,
table creation, and CRUD operations for incomes and expenses.

Author: Henrique
Date: March 2026
"""
import sqlite3
import datetime
import hashlib
import os

# Handle file paths for the SQLite database in a way that works across different operating systems and environments.
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
# Return the parent directory (ex: source folder)
BASE_DIR = os.path.dirname(CURRENT_DIR)
# Create 'data' directory path (where the SQLite database will be stored)
DATA_DIR = os.path.join(BASE_DIR, 'data')

# If the folder doesn't exist, create it
if not os.path.exists(DATA_DIR):
    os.makedirs(DATA_DIR)

# Define the complete path to the .db file (ex: data/database.db)
DATABASE_PATH = os.path.join(DATA_DIR, 'database.db')

def id_generator(username):
    """
    Generates a unique ID Hex for a user based on their username and the current timestamp.
    Args:
        username: string
    Returns:        id_hex: string (8-character hexadecimal ID)
    """
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    #reserve the first 8 characters of the MD5 hash of the reversed username + timestamp as the ID Hex
    seed = f"{username[::-1]}{timestamp}"
    id_hex = hashlib.md5(seed.encode()).hexdigest()[:8].upper()
    return id_hex
    

def get_connection():
    """ 
    creates a connection to the SQLite database and sets the row factory to sqlite3.Row for dict-like access.
     Returns:
        conn: sqlite3.Connection object 
     """
    conn = sqlite3.connect(DATABASE_PATH)
    conn.row_factory = sqlite3.Row 
    return conn


def create_database():
    """ 
    Initializes the 'users' and 'transactions' tables in the SQLite database if they do not already exist.
    Returns:
        None
    """
    connection = get_connection() 
    cursor = connection.cursor()
    #Enable foreign key support in SQLite
    cursor.execute("PRAGMA foreign_keys = ON;")

    #Create 'users' table
    sql_table_users = """ 
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        id_hex TEXT UNIQUE NOT NULL,
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
        position TEXT NOT NULL DEFAULT 'users'
    ); 
    """
    
    #Create 'transactions' table (Corrigido o FOREIGN KEY para 'id_users')
    sql_table_transactions = """
    CREATE TABLE IF NOT EXISTS transactions (
        id_transactions INTEGER PRIMARY KEY AUTOINCREMENT,
        id_users TEXT NOT NULL,
        value REAL NOT NULL,
        type TEXT NOT NULL,  -- NOVO: 'ganho' ou 'despesa'
        category TEXT,
        date_transaction DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_users) REFERENCES users(id_hex)
    );
    """
    
    try:
        cursor.execute(sql_table_users)
        cursor.execute(sql_table_transactions)
        connection.commit()
        print("--- Success: Tables created and verified ---")
    except sqlite3.Error as e:
        print(f"Erro: {e}")
    finally:
        connection.close()


def save_user(username, id_hex, position='users'):
    """ 
    Saves a new user to the 'users' table in the SQLite database with the provided username, id_hex, and position.
    Args:        username: string (the user's name)
        id_hex: string (the unique ID Hex generated for the user)
        position: string (the user's role/position, default is 'users')
    Returns:        None 
    """

    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, id_hex, registration_date, position) VALUES (?, ?, CURRENT_TIMESTAMP, ?)",
            (username, id_hex, position)
        )
        connection.commit()
        print(f"User saved {username} with success.")
    except sqlite3.Error as e:
        print(f"Error saving user: {e}")
    finally:
        connection.close()

def login_system(id_busca):
    """
    Verifies if the Hex ID exists and returns the user's data.
    Arg:       id_busca: string (the ID Hex entered by the user during login)
    Returns:   The user's data if found, otherwise None
    """
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT username, position FROM users WHERE id_hex = ?", (id_busca.upper(),))
        user = cursor.fetchone()
        return user if user else None
    finally:
        connection.close()

def save_transaction(id_hex, value, type, category=None):
    """ 
    Saves a new transaction to the 'transactions' table in the SQLite database.
    Args:
        id_hex: string (the user's unique ID Hex)
        value: float (the transaction value)
        type: string (the type of transaction, either 'ganho' or 'despesa')
        category: string (the category of the transaction, optional)
    Returns:
        None
    """

    connection = get_connection() 
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (id_users, value, type, category) VALUES (?, ?, ?, ?)",
            (id_hex, value, type, category)
        )
        connection.commit()
        print(f"Transação salva.")
    except sqlite3.Error as e:
        print(f"Erro: {e}")
    finally:
        connection.close()

def open_database(table_name, id_busca=None):
    """ 
    Opens the specified table in the SQLite database and prints its contents. 
    Includes Allowlist validation to prevent SQL Injection.
    Args:
        table_name: string (the name of the table to open, must be 'users' or 'transactions')
        id_busca: string (optional, the ID Hex to filter the results by)
    Returns: 
        None 
    """
    # Allowlist validation for table names to prevent SQL Injection
    valid_tables = ['users', 'transactions']
    if table_name not in valid_tables:
        print(f"Error: Access denied. Table '{table_name}' is not a valid table.")
        return

    connection = get_connection() 
    cursor = connection.cursor()
    print(f"--- ACCESSING SYSTEM: {table_name.upper()} ---")

    try:
        if id_busca is None:
            cursor.execute(f"SELECT * FROM {table_name}")
            records = cursor.fetchall()
            for record in records:
                # Use the get method with default values to avoid KeyError if a column is missing
                print(f"ID: {record.get('id_users', 'N/A')} | Value: R$ {record.get('value', 0):.2f} | Type: {record.get('type', 'N/A')} | Category: {record.get('category', 'N/A')}")
        else:
            cursor.execute(f"SELECT * FROM {table_name} WHERE id_users = ?", (id_busca.upper(),))
            records = cursor.fetchall()
            if records:
                for r in records:
                    print(f"ID: {r.get('id_users', 'N/A')} | Value: R$ {r.get('value', 0):.2f} | Type: {r.get('type', 'N/A')} | Category: {r.get('category', 'N/A')}")
            else:
                print("No records found for the provided ID.")
    except sqlite3.Error as e:
        print(f"Database error: {e}")
    finally:
        connection.close()

def get_values_by_type(id_users, type):
    """ 
    Gets a list of transaction values from the 'transactions' table in the SQLite database for a specific user and transaction type.
    Args:        id_users: string (the user's unique ID Hex)
        type: string (the type of transaction to filter by, either 'ganho' or 'despesa')
    Returns:        A list of transaction values that match the specified user and type 
     """

    connection = get_connection() 
    cursor = connection.cursor()
    try:
        cursor.execute(
            "SELECT value FROM transactions WHERE id_users = ? AND type = ?",
            (id_users, type)
        )
        records = cursor.fetchall()
        values_list = [record['value'] for record in records]
        return values_list
    finally:
        connection.close()

# Create database on startup if it doesn't exist
if __name__ == "__main__":
    create_database()
