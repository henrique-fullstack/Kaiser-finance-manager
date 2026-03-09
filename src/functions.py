from src.database import get_values_by_type

def calculate_income(id_users):
    """Busca no banco e calcula o total de ganhos."""
    income_list = get_values_by_type(id_users, 'ganho')
    return sum(income_list)

def get_total_expense(id_users):
    """Busca no banco e calcula o total de despesas."""
    expense_list = get_values_by_type(id_users, 'despesa')
    return sum(expense_list)

def calculate_balance(id_users):
    """Calcula o saldo final baseado no ID do usuário."""
    total_income = calculate_income(id_users)
    total_expense = get_total_expense(id_users)
    return total_income - total_expense

def get_transaction_input(tipo_transacao):
    """Lida com a entrada de dados para evitar repetição no menu"""
    try:
        valor = float(input(f"Valor do {tipo_transacao}: "))
        categoria = input(f"Categoria do {tipo_transacao}: ")
        return valor, categoria
    except ValueError:
        print("❌ Erro: Digite um número válido!")
        return None, None

