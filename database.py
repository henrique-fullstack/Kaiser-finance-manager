import sqlite3
import datetime
import hashlib

database = 'database.db'

def id_generator(username):
    """Gera um ID Hexadecimal único baseado no nome e tempo."""
    timestamp = datetime.datetime.now().strftime("%Y%m%d%H%M%S%f")
    semente = f"{username[::-1]}{timestamp}"
    return hashlib.md5(semente.encode()).hexdigest()[:8].upper()

def get_connection():
    conn = sqlite3.connect(database)
    conn.row_factory = sqlite3.Row 
    return conn


def create_database():
    connection = get_connection() 
    cursor = connection.cursor()
    
    cursor.execute("PRAGMA foreign_keys = ON;")

    sql_table_users = """ 
    CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY AUTOINCREMENT,
    username TEXT NOT NULL,
    id_hex TEXT UNIQUE NOT NULL,
    registration_date DATETIME DEFAULT CURRENT_TIMESTAMP, 
    position TEXT NOT NULL DEFAULT 'users'); 
    """

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
        print("--- Sucesso: Tabelas verificadas ---")
    except sqlite3.Error as e:
        print(f"Erro: {e}")
    finally:
        connection.close()

def save_user(username, id_hex, position='users'):
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO users (username, id_hex, registration_date, position) VALUES (?, ?, CURRENT_TIMESTAMP, ?)",
            (username, id_hex, position)
        )
        connection.commit()
        print(f"Usuário {username} salvo com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao salvar usuário: {e}")
    finally:
        connection.close()

def login_system(id_busca):
    """Verifica se o ID Hex existe e retorna os dados do usuário."""
    connection = get_connection()
    cursor = connection.cursor()
    try:
        cursor.execute("SELECT username, position FROM users WHERE id_hex = ?", (id_busca.upper(),))
        user = cursor.fetchone()
        return user if user else None
    finally:
        connection.close()

def save_transaction(id_users, value, type, category=None):
    connection = get_connection() 
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (id_users, value, type, category) VALUES (?, ?, ?, ?)",
            (id_users, value, type, category)
        )
        connection.commit()
        print(f"Transação salva.")
    except sqlite3.Error as e:
        print(f"Erro: {e}")
    finally:
        connection.close()

def open_database(table_name, id_busca=None):
    connection = get_connection() 
    cursor = connection.cursor()
    print(f"--- ACESSANDO O SISTEMA ---")

    if id_busca is None:
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        for record in records:
            print(dict(record))
    else:
        cursor.execute(f"SELECT * FROM {table_name} WHERE id_hex = ?", (id_busca.upper(),))
        record = cursor.fetchone()
        if record:
            print(dict(record))
        else:
            print("Nenhum registro encontrado para o ID fornecido.")
    
    
    connection.close()

def get_values_by_type(id_users, type):
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

if __name__ == "__main__":
    create_database()