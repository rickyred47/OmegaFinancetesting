from flask import request, session
from datetime import datetime


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
    account = account_name_number[(a + 1):]
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
            account = account_name_number[(split + 1):]
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

    journal_event = database.get_journal_event_table()
    new_entry2 = journal_event(journal_type_before=None, journal_type_after=journal_type,
                               journal_debit_accounts_before=None, journal_debit_accounts_after=debit_accounts,
                               journal_debit_amounts_before=None, journal_debit_amounts_after=debit_accounts_amount,
                               journal_credit_accounts_before=None, journal_credit_accounts_after=credit_accounts,
                               journal_credit_amounts_before=None, journal_credit_amounts_after=credit_accounts_amount,
                               journal_status_before=None, journal_status_after='Pending',
                               date_made=datetime.now(), event_type='Created', username=session['username'],
                               journal_id=new_entry.id)
    database.commit_to_database(new_entry2)


def post_info(entry, database):
    Ledger = database.get_ledger_table_class()
    for x in range(0, len(entry.debit_accounts)):
        account = database.get_account_info_by_number(entry.debit_accounts_numbers[x])
        new_balance = calculate_balance(account.balance, account.normal_side, entry.debit_amounts[x], True)
        new_ledger_entry = Ledger(pr_number=entry.id, date=entry.date, description=entry.description,
                                  debit_amount=entry.debit_amounts[x], credit_amount=None, old_balance=account.balance,
                                  new_balance=new_balance, account_number=account.number)
        database.commit_to_database(new_ledger_entry)
        account.balance = new_balance
        database.commit_info()
    for y in range(0, len(entry.credit_accounts)):
        account = database.get_account_info_by_number(entry.credit_accounts_numbers[y], False)
        new_balance = calculate_balance(account.balance, account.normal_side, entry.credit_amounts[y])
        new_ledger_entry = Ledger(pr_number=entry.id, date=entry.date, description=entry.description,
                                  debit_amount=None, credit_amount=entry.credit_amounts[y], old_balance=account.balance,
                                  new_balance=new_balance, account_number=account.number)
        database.commit_to_database(new_ledger_entry)
        account.balance = new_balance
        database.commit_info()


def calculate_balance(balance, side, amount, is_debit):
    new_balance = 0
    if is_debit:
        if side == "Left":
            new_balance = balance + amount
        elif side == "Right":
            new_balance = balance - amount
    else:
        if side == "Left":
            new_balance = balance - amount
        elif side == "Right":
            new_balance = balance + amount
    return new_balance


