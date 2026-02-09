import sqlite3

database = 'database.db'

# --- 1. A NOVA FUNÇÃO MÁGICA ---
def get_connection():
    """
    Abre a conexão e retorna o objeto connection.
    Centraliza a configuração do banco em um só lugar.
    """
    conn = sqlite3.connect(database)
    # DICA PRO: Isso permite acessar as colunas pelo nome (ex: linha['username'])
    # em vez de só pelo número (linha[1]). É muito mais fácil de ler.
    conn.row_factory = sqlite3.Row 
    return conn

# --- 2. COMO FICAM SUAS FUNÇÕES AGORA ---

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
    
    try:
        cursor.execute(sql_table_users)
        connection.commit()
        print("--- Sucesso: Tabelas verificadas ---")
    except sqlite3.Error as e:
        print(f"Erro: {e}")
    finally:
        connection.close() # Você ainda precisa fechar!

def save_transaction(id_users, value, category=None):
    connection = get_connection() # Limpo e rápido
    cursor = connection.cursor()
    try:
        cursor.execute(
            "INSERT INTO transactions (id_users, value, category) VALUES (?, ?, ?)",
            (id_users, value, category)
        )
        connection.commit()
        print(f"Transação salva.")
    except sqlite3.Error as e:
        print(f"Erro: {e}")
    finally:
        connection.close()

def open_database(table_name, id_busca=None):
    connection = get_connection() # Limpo e rápido
    cursor = connection.cursor()
    print(f"--- ACESSANDO O SISTEMA ---")

    # ... (Sua lógica de if/else continua igual) ...
    
    if id_busca is None:
        cursor.execute(f"SELECT * FROM {table_name}")
        records = cursor.fetchall()
        # COMO USAMOS O row_factory LÁ EM CIMA, AGORA PODEMOS FAZER ISSO:
        for record in records:
            # Converte o objeto Row em um Dicionário Python padrão para ficar bonito no print
            print(dict(record)) 
    
    # ... (Resto do código) ...
    
    connection.close()

if __name__ == "__main__":
    create_database()