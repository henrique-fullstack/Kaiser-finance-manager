from src.database import get_values_by_type

def calculate_income(id_users):
    """ Search the database and calculate the total income for a given user ID. 
    Args:
        id_users: string (the user's unique ID Hex)
    Returns:
        The total income calculated as the sum of all transaction values of type 'ganho' for the given user ID
    """
    income_list = get_values_by_type(id_users, 'ganho')
    return sum(income_list)

def calculate_expense(id_users):
    """ Search the database and calculate the total expense for a given user ID. 
    Args:
        id_users: string (the user's unique ID Hex)
    Returns:
        The total expense calculated as the sum of all transaction values of type 'despesa' for the given user ID
    """
    expense_list = get_values_by_type(id_users, 'despesa')
    return sum(expense_list)

def calculate_balance(id_users):
    """ Search the database and calculate the final balance based on the user ID. 
    Args:
        id_users: string (the user's unique ID Hex)
    Returns:
        The final balance calculated as total income minus total expenses for the given user ID
    """
    total_income = calculate_income(id_users)
    total_expense = calculate_expense(id_users)
    return total_income - total_expense

def get_transaction_input(tipo_transacao):
    """ Get user input for a transaction value and category, with error handling for invalid input. 
    Args:
        tipo_transacao: string (the type of transaction, either 'ganho' or 'despesa')
    Returns:
        A tuple containing the transaction value (float) and category (string), or (None, None) if the input is invalid 
    """
    try:
        valor = float(input(f"Valor do {tipo_transacao}: "))
        categoria = input(f"Categoria do {tipo_transacao}: ")
        return valor, categoria
    except ValueError:
        print("❌ Erro: Digite um número válido!")
        return None, None

