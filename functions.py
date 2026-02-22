from database import get_values_by_type

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