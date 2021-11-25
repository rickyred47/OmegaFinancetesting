def get_total_amounts(accounts):
    total_debit = 0
    total_credit = 0
    for account in accounts:
        if account.normal_side == "Left":
            total_debit += account.balance
        elif account.normal_side == "Right":
            total_credit += account.balance
    return total_debit, total_credit


def get_total_amount(accounts):
    amount = 0
    for account in accounts:
        amount += account.balance
    return amount