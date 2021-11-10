from flask import request


def journal_entry_form(user, database):
    debit_accounts_count = request.form["debit_accounts_counter"]
    credit_accounts_count = request.form["credit_accounts_counter"]
    entry_date = request.form["date_entry"]
    journal_type = request.form["journal_type"]
    description = request.form["description"]
    # file = request.form["file"]
    account_name_number = request.form["debit_account_select0"]
    a = account_name_number.index("-")
    id_num = account_name_number[:a]
    debit_account_ids = [id_num]
    account = account_name_number[(a+1):]
    debit_accounts = [account]
    account_name_number1 = request.form["credit_account_select0"]
    b = account_name_number1.index("-")
    id_num1 = account_name_number1[:b]
    account1 = account_name_number1[(b + 1):]
    credit_accounts = [account1]
    credit_accounts_ids = [id_num1]
    amount = request.form["debit_amount_input0"]
    debit_accounts_amount = [amount]
    amount1 = request.form["credit_amount_input0"]
    credit_accounts_amount = [amount1]
    if int(debit_accounts_count) > 0:
        for x in range(1, int(debit_accounts_count) + 1):
            account_name = "debit_account_select" + str(x)
            amount_name = "debit_amount_input" + str(x)
            account_name_number = request.form[account_name]
            split = account_name_number.index("-")
            id_num = account_name_number[:split]
            account = account_name_number[(split+1):]
            amount = request.form[amount_name]
            debit_accounts.append(account)
            debit_account_ids.append(id_num)
            debit_accounts_amount.append(amount)
    if int(credit_accounts_count) > 0:
        for y in range(1, int(credit_accounts_count) + 1):
            account_name = "credit_account_select" + str(y)
            amount_name = "credit_amount_input" + str(y)
            account_name_number1 = request.form[account_name]
            split = account_name_number1.index("-")
            id_num = account_name_number1[:split]
            account = account_name_number1[(split + 1):]
            amount = request.form[amount_name]
            credit_accounts.append(account)
            credit_accounts_ids.append(id_num)
            credit_accounts_amount.append(amount)

    journal_entry = database.get_journal_table()
    new_entry = journal_entry(date=entry_date, type=journal_type, created_by=user,
                              debit_accounts=debit_accounts, credit_accounts=credit_accounts,
                              debit_amounts=debit_accounts_amount, credit_amounts=credit_accounts_amount,
                              status="Pending", description=description, debit_accounts_numbers=debit_account_ids,
                              credit_accounts_numbers=credit_accounts_ids)
    database.commit_to_database(new_entry)

