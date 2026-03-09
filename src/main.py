# Certifique-se de que todas as importações estão corretas
from src.database import create_database, login_system, save_transaction, open_database, save_user, id_generator
from src.functions import calculate_balance, calculate_income, get_total_expense, get_transaction_input
from src.utils import clear_screen, color_text, format_currency
import os
import sys

def main():
    create_database() 
    id_usuario = None # Inicializamos a variável

    while True:
        clear_screen() # Limpa a tela antes de mostrar o menu de login/registro
        print("\n--- 🟦 KAISER FINANCE MANAGER 🟦 ---", "blue")
        print("1. Login")
        print("2. Register")
        print(color_text("3. Exit", "red"))
        choice = input("Choose an option: ")
        
        if choice == "1":
            id_input = input("Digite seu ID Hex para entrar: ").strip().upper()
            user = login_system(id_input)
            if user:
                id_usuario = id_input # Só define se o login der certo
                print(f"\nBem-vindo, {user['username']}! (Cargo: {user['position']})")
                break # SAI do loop de login e vai para o menu principal
            else:
                print(color_text(f"❌ Usuário não encontrado!", "red"))
                input("Press Enter to try again...") # Pausa para o usuário ler a mensagem de erro
        
        elif choice == "2":
            username = input("Enter your username: ")
            id_hex = id_generator(username)
            position = input("Enter your position: ")
            save_user(username, id_hex, position)
            print(color_text(f"✅ User registered! Your ID Hex is: {id_hex}", "green"))
            input("Press Enter to return to the login menu...") # Pausa para o usuário ler o ID e depois volta para o menu de login
            # Após registrar, ele volta para o menu de login para o usuário entrar com o ID novo
        
        elif choice == "3":
            print("Exiting... Goodbye!")
            sys.exit()
        else:
            print("Invalid option!")

    # SEGUNDO LOOP - SÓ CHEGA AQUI SE TIVER LOGADO (id_usuario preenchido)
    while id_usuario:
        clear_screen() # Limpa a tela antes de mostrar o menu principal
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
                saldo = calculate_balance(id_users=id_usuario)
                print(f"💰 Seu saldo atual é: R$ {saldo:.2f}")
                input("Press Enter to continue...") # Pausa para o usuário ler o saldo
            case "2":
                total_ganho = calculate_income(id_users=id_usuario)
                print(f"📈 Total de Ganhos: R$ {total_ganho:.2f}")
                input("Press Enter to continue...") # Pausa para o usuário ler o total de ganhos
            case "3":
                total_expenses = get_total_expense(id_users=id_usuario)
                print(f"📉 Total de Despesas: R$ {total_expenses:.2f}")
                input("Press Enter to continue...") # Pausa para o usuário ler o total de despesas
            case "4":
                valor_ganho, categoria = get_transaction_input("ganho")
                if valor_ganho is not None:
                    save_transaction(id_usuario, valor_ganho, "ganho", categoria)
                    print(color_text("✅ Ganho adicionado com sucesso!", "green"))
                    input("Press Enter to continue...") # Pausa para o usuário ler a mensagem de sucesso
            case "5":
                valor_despesa, categoria = get_transaction_input("despesa")
                if valor_despesa is not None:
                    save_transaction(id_usuario, valor_despesa, "despesa", categoria)
                    print(color_text("✅ Despesa adicionada com sucesso!", "green"))
                    input("Press Enter to continue...") # Pausa para o usuário ler a mensagem de sucesso
            case "6":
                open_database("transactions", id_usuario)
                input("Press Enter to continue...") # Pausa para o usuário ver o histórico
            case "7":
                print("Saving data and exiting... Goodbye.")
                break 
            case _:
                print(color_text("❌ Invalid Option!", "red"))

        clear_screen() # Limpa a tela antes de mostrar o menu novamente
               


if __name__ == "__main__":
    main()