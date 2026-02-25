import sys
# Certifique-se de que todas as importações estão corretas
from database import create_database, login_system, save_transaction, open_database, save_user, id_generator
from functions import calculate_balance, calculate_income, get_total_expense

def main():
    create_database() 
    id_usuario = None # Inicializamos a variável

    while True:
        print("\n--- 🟦 KAISER FINANCE MANAGER 🟦 ---")
        print("1. Login")
        print("2. Register")
        print("3. Exit")
        choice = input("Choose an option: ")
        
        if choice == "1":
            id_input = input("Digite seu ID Hex para entrar: ").strip().upper()
            user = login_system(id_input)
            if user:
                id_usuario = id_input # Só define se o login der certo
                print(f"\nBem-vindo, {user['username']}! (Cargo: {user['position']})")
                break # SAI do loop de login e vai para o menu principal
            else:
                print("❌ Usuário não encontrado!")
        
        elif choice == "2":
            username = input("Enter your username: ")
            id_hex = id_generator(username)
            position = input("Enter your position: ")
            save_user(username, id_hex, position)
            print(f"✅ User registered! Your ID Hex is: {id_hex}")
            # Após registrar, ele volta para o menu de login para o usuário entrar com o ID novo
        
        elif choice == "3":
            print("Exiting... Goodbye!")
            sys.exit()
        else:
            print("Invalid option!")

    # SEGUNDO LOOP - SÓ CHEGA AQUI SE TIVER LOGADO (id_usuario preenchido)
    while id_usuario:
        print("\n--- MENU ---")
        print("1. Ver Saldo Atual")
        print("2. Ver Total de Ganhos")
        print("3. Ver Total de Despesas")
        print("4. Adicionar Ganho")
        print("5. Adicionar Despesa")
        print("6. Ver Histórico")
        print("7. Sair")
        
        opcao = input("\nEscolha uma opção: ")

        match opcao:
            case "1":
                # Certifique-se de que a função calculate_balance aceita o parâmetro id_users
                saldo = calculate_balance(id_users=id_usuario)
                print(f"💰 Seu saldo atual é: R$ {saldo:.2f}")
            case "2":
                total_ganho = calculate_income(id_users=id_usuario)
                print(f"📈 Total de Ganhos: R$ {total_ganho:.2f}")
            case "3":
                expensive = get_total_expense(id_users=id_usuario)
                print(f"📉 Total de Despesas: R$ {expensive:.2f}")
            case "4":
                try:
                    valor = float(input("Valor do ganho: "))
                    categoria = input("Categoria do ganho: ")
                    save_transaction(id_usuario, valor, "ganho", categoria)
                    print("✅ Ganho adicionado com sucesso!")
                except ValueError:
                    print("❌ Erro: Digite um número válido!")
            case "5":
                try:
                    valor_despesa = float(input("Valor da despesa: "))
                    categoria = input("Categoria da despesa: ")
                    save_transaction(id_usuario, valor_despesa, "despesa", categoria)
                    print("✅ Despesa adicionada com sucesso!")
                except ValueError:
                    print("❌ Erro: Digite um número válido!")
            case "6":
                # Verifique se open_database realmente imprime algo ou retorna dados
                open_database("transactions", id_usuario)
            case "7":
                print("Saving data and exiting... Goodbye, Kaiser.")
                break 
            case _:
                print("❌ Invalid Option!")

if __name__ == "__main__":
    main()