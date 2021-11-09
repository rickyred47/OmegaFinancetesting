from flask import request


def journal_entry_form(user, database):
    debit_accounts_count = request.form["debit_accounts_counter"]
    credit_accounts_count = request.form["credit_accounts_counter"]
    entry_date = request.form["date_entry"]
    journal_type = request.form["journal_type"]
    description = request.form["description"]
    # file = request.form["file"]
    account = request.form["debit_account_select0"]
    debit_accounts = [account]
    account1 = request.form["credit_account_select0"]
    credit_accounts = [account1]
    amount = request.form["debit_amount_input0"]
    debit_accounts_amount = [amount]
    amount1 = request.form["credit_amount_input0"]
    credit_accounts_amount = [amount1]
    if int(debit_accounts_count) > 0:
        for x in range(1, int(debit_accounts_count) + 1):
            account_name = "debit_account_select" + str(x)
            amount_name = "debit_amount_input" + str(x)
            account = request.form[account_name]
            amount = request.form[amount_name]
            debit_accounts.append(account)
            debit_accounts_amount.append(amount)
    if int(credit_accounts_count) > 0:
        for y in range(1, int(credit_accounts_count) + 1):
            account_name = "credit_account_select" + str(y)
            amount_name = "credit_amount_input" + str(y)
            account = request.form[account_name]
            amount = request.form[amount_name]
            credit_accounts.append(account)
            credit_accounts_amount.append(amount)

    journal_entry = database.get_journal_table()
    new_entry = journal_entry(date=entry_date, type=journal_type, created_by=user,
                              debit_accounts=debit_accounts, credit_accounts=credit_accounts,
                              debit_amounts=debit_accounts_amount, credit_amounts=credit_accounts_amount,
                              status="Pending", description=description)
    database.commit_to_database(new_entry)

