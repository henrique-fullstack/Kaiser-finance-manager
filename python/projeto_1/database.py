import sqlite3

# Configuração do banco de dados SQLite
def criar_base_de_dados():
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()

    # O comando SQL (usando Docstrings do Python para ficar legível)
    sql_tabela_usuarios = """
    CREATE TABLE IF NOT EXISTS usuarios (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        id_hex TEXT UNIQUE NOT NULL,
        data_registro DATETIME DEFAULT CURRENT_TIMESTAMP,
        cargo TEXT NOT NULL DEFAULT 'usuario'
    );
    """
    
    sql_tabela_transacoes = """
    CREATE TABLE IF NOT EXISTS transacoes (
        id_transacao INTEGER PRIMARY KEY AUTOINCREMENT,
        id_usuario TEXT NOT NULL,
        valor REAL NOT NULL,
        categoria TEXT,
        data_transacao DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id_hex)
    );
        """
    try:
        cursor.execute(sql_tabela_usuarios)
        # O commit é o "botão de salvar" do SQL
        conexao.commit()
        print("--- Sucesso: Tabela 'usuarios' criada ou já existente ---")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
    
    
    try:
        cursor.execute(sql_tabela_transacoes)
        conexao.commit()
        print("--- Sucesso: Tabela 'transacoes' criada ou já existente ---")
    except sqlite3.Error as e:
        print(f"Erro ao criar tabela: {e}")
    finally:
        conexao.close()

if __name__ == "__main__":
    criar_base_de_dados()

def salvar_usuario(usuario):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()

    sql_inserir = """
    INSERT INTO usuarios (id, nome, id_hex, data_registro, cargo)

        VALUES (?, ?, ?, ?, ?);
    """
    dados = (
        usuario['id'],
        usuario['nome'],
        usuario['id_hex'],
        usuario['data_registro'],
        usuario['cargo']
    )
    cursor.execute(sql_inserir, dados)
    conexao.commit()
    conexao.close()

    print(f"--- Sucesso: Usuário {usuario['nome']} salvo no banco de dados ---")

def buscar_usuarios():
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()
    
    try:
        cursor.execute("SELECT * FROM usuarios")
        usuarios = cursor.fetchall()
        return usuarios
    except sqlite3.Error as e:
        print(f"Erro ao buscar: {e}")
        return []
    finally:
        conexao.close()

def salvar_transacao(id_usuario, valor, categoria):
    conexao = sqlite3.connect('database.db')
    cursor = conexao.cursor()

    try:
        sql = """
        INSERT INTO transacoes (id_usuario, valor, categoria)
        VALUES (?, ?, ?)
        """
        # Aqui passamos os valores que vieram do seu sistema
        cursor.execute(sql, (id_usuario, valor, categoria))
        conexao.commit()
        print(f"--- Sucesso: Gasto de R${valor} registrado! ---")
    except sqlite3.Error as e:
        print(f"Erro ao salvar transação: {e}")
    finally:
        conexao.close()