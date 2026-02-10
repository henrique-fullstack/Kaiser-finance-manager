import database

def iniciar_programa():
    print("=== SISTEMA DE FINANÇAS PESSOAIS ===")
    
    # 1. Garante que o banco e as tabelas existam
    database.criar_base_de_dados()
    
    # 2. Aqui entrará o seu loop de menu futuramente
    print("Sistema pronto para uso.")

if __name__ == "__main__":
    iniciar_programa()


# 2. O FLUXO: Interação com o usuário
print("--- SISTEMA DE CADASTRO PYTHON ---")
name_input = input("Digite o nome completo: ")
age_input = input("Digite a idade: ")

