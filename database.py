import sqlite3
database = 'database.db'

# Configuração do banco de dados SQLite
def create_database():
    connection = sqlite3.connect(database)
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

def save_user(username, id_hex, position='users'):
    connection = sqlite3.connect(database)
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

def save_transaction(id_users, value, category=None):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (id_users, value, category) VALUES (?, ?, ?,)",
            (id_users, value, category)
        )
        connection.commit()
        print(f"Transação para o usuário {id_users} salva com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao salvar transação: {e}")
    finally:
        connection.close()


def open_database(table_name, id_hex=None):
    connection = sqlite3.connect(database)
    cursor = connection.cursor()
    print(f"--- ACESSANDO O SISTEMA ---")

    if id_hex is None:
        print(f"Exibindo todos os registros da tabela '{table_name}':")
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        for record in records:
            print(record)
    else:
        print(f"Exibindo registros para o id_hex '{id_hex}' na tabela '{table_name}':")
        cursor.execute(f"SELECT * FROM {table_name} WHERE id_hex = ?", (id_hex,))
        records = cursor.fetchall()
        for record in records:
            print(record)
    print("---------------------------")
    connection.close()
