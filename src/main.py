from src.database import create_database, login_system, save_transaction, open_database, save_user, id_generator
from src.functions import calculate_balance, calculate_income, calculate_expense, get_transaction_input
from src.utils import clear_screen, color_text, format_currency
import os
import sys

def main():
    """ 
    Main function that runs the Kaiser Finance Manager application. It handles user registration, login, and the main menu for managing finances.
    Args:        
        None
    Returns:      
        None
    """
    create_database() 
    id_usuario = None # Variable for storing the logged-in user's ID, starts as None until login is successful

    while True:
        clear_screen()
        print(color_text("\n--- 🟦 KAISER FINANCE MANAGER 🟦 ---", "blue"))
        print("1. Login")
        print("2. Register")
        print(color_text("3. Exit", "red"))
        choice = input("Choose an option: ")
        
        if choice == "1":
            id_input = input("Enter your ID Hex: ").strip().upper()
            user = login_system(id_input)
            if user:
                id_usuario = id_input
                print(f"\nWelcome, {user['username']}! (Position: {user['position']})")
                input("Press Enter to continue...") # Pause for read message before going to the main menu
                break 
            else:
                print(color_text(f"❌ User not found!", "red"))
                input("Press Enter to try again...")
        
        elif choice == "2":
            username = input("Enter your username: ")
            id_hex = id_generator(username)
            position = input("Enter your position: ")
            save_user(username, id_hex, position)
            print(color_text(f"✅ User registered! Your ID Hex is: {id_hex}", "green"))
            input("Press Enter to return to the login menu...") # Pause for user to read the registration success message and the generated ID before returning to the login menu
            # After registration, the user is prompted to press Enter to return to the login menu, where they can use their new ID Hex to log in.
        
        elif choice == "3":
            print("Exiting... Goodbye!")
            sys.exit()
        else:
            print("Invalid option!")

    # SECOND MENU - MAIN FINANCE MANAGEMENT 
    while id_usuario:
        clear_screen() # Clear the screen before showing the main menu to keep the interface clean and focused on the current options
        print("\n--- MENU ---")
        print("1. See all balance")
        print("2. See Total Income")
        print("3. See Total Expenses")
        print("4. Add Income")
        print("5. Add Expense")
        print("6. View History")
        print("7. Exit")
        
        opcao = input("\nChoose an option: ")

        match opcao:
            case "1":
                saldo = calculate_balance(id_users=id_usuario)
                print(f"💰 Your current balance is: {format_currency(saldo)}")
                input("Press Enter to continue...") # Pause for user to read the balance
            case "2":
                total_ganho = calculate_income(id_users=id_usuario)
                print(f"📈 Total Income: {format_currency(total_ganho)}")
                input("Press Enter to continue...") # Pause for user to read the total income
            case "3":
                total_expenses = calculate_expense(id_users=id_usuario)
                print(f"📉 Total Expenses: {format_currency(total_expenses)}")
                input("Press Enter to continue...") # Pause for user to read the total expenses
            case "4":
                valor_ganho, categoria = get_transaction_input("ganho")
                if valor_ganho is not None:
                    save_transaction(id_usuario, valor_ganho, "ganho", categoria)
                    print(color_text("✅ Income added successfully!", "green"))
                    input("Press Enter to continue...") # Pause for user to read the success message
            case "5":
                valor_despesa, categoria = get_transaction_input("despesa")
                if valor_despesa is not None:
                    save_transaction(id_usuario, valor_despesa, "despesa", categoria)
                    print(color_text("✅ Expense added successfully!", "green"))
                    input("Press Enter to continue...") # Pause for user to read the success message
            case "6":
                open_database("transactions", id_usuario)
                input("Press Enter to continue...") # Pause for user to view the history
            case "7":
                print("Saving data and exiting... Goodbye.")
                break 
            case _:
                print(color_text("❌ Invalid Option!", "red"))

        clear_screen() # Clear the screen after each action to keep the interface clean and focused on the current options
               


if __name__ == "__main__":
    main()