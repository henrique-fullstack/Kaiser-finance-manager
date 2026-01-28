import sqlite3

# Configuração do banco de dados SQLite
def create_database():
    connection = sqlite3.connect('database.db')
    cursor = connection.cursor()

    # O comando SQL (usando Docstrings do Python para ficar legível)
    sql_table_users = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT NOT NULL,
        id_hex TEXT UNIQUE NOT NULL,
        registration_date DATETIME DEFAULT CURRENT_TIMESTAMP,
        position TEXT NOT NULL DEFAULT 'users'
    );
    """

    sql_table_transactions = """
    CREATE TABLE IF NOT EXISTS transactions (
        id_transactions INTEGER PRIMARY KEY AUTOINCREMENT,
        id_users TEXT NOT NULL,
        value REAL NOT NULL,
        category TEXT,
        date_transaction DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_users) REFERENCES users(id_hex)
    );
        """
    try:
        cursor.execute(sql_table_users)
        # O commit é o "botão de salvar" do SQL
        connection.commit()
        print("--- Sucesso: Tabela 'usuarios' criada ou já existente ---")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
    
    
    try:
        cursor.execute(sql_table_transactions)
        connection.commit()
        print("--- Sucesso: Tabela 'transacoes' criada ou já existente ---")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        connection.close()

if __name__ == "__main__":
    create_database()