import sys
from database import create_database, login_system, save_transaction, open_database
from functions import calculate_balance, calculate_income, get_total_expense

def main():
    create_database() # Garante que as tabelas existem
    
    print("--- 🟦 KAISER FINANCE MANAGER 🟦 ---")
    id_usuario = input("Digite seu ID Hex para entrar: ").strip().upper()
    
    user = login_system(id_usuario)
    
    if not user:
        print("Usuário não encontrado. Saindo...")
        sys.exit()

    print(f"\nBem-vindo, {user['username']}! (Cargo: {user['position']})")

    while True:
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
                saldo = calculate_balance(id_usuario)
                print(f"💰 Seu saldo atual é: R$ {saldo:.2f}")
                # Aqui você chamaria uma função do seu functions.py
            case "2":
                total_ganho = calculate_income(id_usuario)
                print(f"📈 Total de Ganhos: R$ {total_ganho:.2f}")
            case "3":
                expensive = get_total_expense(id_usuario)
                print(f"💰 Seu saldo total de despesas é: R$ {expensive:.2f}")
            case "4":
                valor = float(input("Valor do ganho: "))
                categoria = input("Categoria do ganho: ")
                save_transaction(id_usuario, valor, "ganho", categoria)
                print("✅ Ganho adicionado com sucesso!")
            case "5":
                expensive = float(input("Valor da despesa: "))
                categoria = input("Categoria da despesa: ")
                save_transaction(id_usuario, expensive, "despesa", categoria)
                print("✅ Despesa adicionada com sucesso!")
            case "6":
                    open_database("transactions", id_usuario)
                    print("📄 Histórico de transações aberto.")
            case "7":
                print("Saving data and exiting... Goodbye, Kaiser.")
                break # Quebra o loop e encerra o programa
            case _:
                print("❌ Invalid Option! Please choose between 1 and 7.")


if __name__ == "__main__":
    main()