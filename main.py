import datetime
import secrets
import database

def iniciar_programa():
    print("=== SISTEMA DE FINANÇAS PESSOAIS ===")
    
    # 1. Garante que o banco e as tabelas existam
    database.criar_base_de_dados()
    
    # 2. Aqui entrará o seu loop de menu futuramente
    print("Sistema pronto para uso.")

if __name__ == "__main__":
    iniciar_programa()

# 1. A FUNÇÃO: Nossa 'máquina' de gerar IDs e validar usuários
def criar_usuario(name, age):
    # Gerando o ID com a sua lógica criativa de ontem
    key = datetime.datetime.now().hour
    data = datetime.date.today().day
    id_gerado = len(name) + int(age) * data + key
    
    # Criando um dicionário (um objeto) para organizar os dados
    usuario = {
        "id": id_gerado,
        "nome": name.strip().title(), # Limpa espaços e deixa a primeira letra maiúscula
        "idade": int(age),
        "data_cadastro": datetime.date.today(),
        "status": "Ativo" if int(age) >= 18 else "Pendente (Menor de idade)"
    }
    
    return usuario

# 2. O FLUXO: Interação com o usuário
print("--- SISTEMA DE CADASTRO PYTHON ---")
nome_input = input("Digite o nome completo: ")
idade_input = input("Digite a idade: ")

# Chamando a função e guardando o resultado
novo_usuario = criar_usuario(nome_input, idade_input)

# 3. O RESULTADO: Exibindo os dados organizados
print("\n--- USUÁRIO CRIADO COM SUCESSO ---")
for chave, valor in novo_usuario.items():
    print(f"{chave.upper()}: {valor}")

if novo_usuario["status"] == "Ativo":
    print(f"\nBem-vindo ao sistema, {novo_usuario['nome']}!")
else:
    print("\nAcesso restrito: Necessário supervisão.")