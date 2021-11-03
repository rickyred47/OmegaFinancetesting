from flask import request


def journal_entry_form():
    debit_accounts_count = request.form["debit_accounts_counter"]
    credit_accounts_count = request.form["credit_accounts_counter"]
    entry_date = request.form["date_entry"]
    journal_type = request.form["journal_type"]
    description = request.form["description"]
    # file = request.form["file"]
    account = request.form["debit_account_select"]
    debit_accounts = [account]
    account1 = request.form["credit_account_select"]
    credit_accounts = [account1]
    amount = request.form["debit_account_amount"]
    debit_accounts_amount = [amount]
    amount1 = request.form["credit_account_amount"]
    credit_accounts_amount = [amount1]
    if int(debit_accounts_count) > 0:
        for x in range(1, int(debit_accounts_count) + 1):
            account_name = "debit_account_select" + str(x)
            amount_name = "debit_account_amount" + str(x)
            account = request.form[account_name]
            amount = request.form[amount_name]
            debit_accounts.append(account)
            debit_accounts_amount.append(amount)
    if int(credit_accounts_count) > 0:
        for y in range(1, int(credit_accounts_count) + 1):
            account_name = "credit_account_select" + str(y)
            amount_name = "credit_account_amount" + str(y)
            account = request.form[account_name]
            amount = request.form[amount_name]
            credit_accounts.append(account)
            credit_accounts_amount.append(amount)

    print(debit_accounts)
    print(debit_accounts_amount)
    print(credit_accounts)
    print(credit_accounts_amount)
