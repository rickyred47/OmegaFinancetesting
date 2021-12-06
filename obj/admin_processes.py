from flask import render_template, request, session
from datetime import datetime, timedelta, date
from obj import NewUser, email_manager


def account_form(database):
    category = request.form["category"]
    name = request.form["name"]
    subcategory = request.form["subcategory"]
    initial_num = request.form["initial_num"]
    number = request.form["number"]
    account_num = concat(initial_num, number)
    description = request.form["description"]
    normal_side = request.form["normal_side"]
    balance = request.form["initial_balance"]
    comment = request.form["comment"]
    created = datetime.now()
    statement = get_statement_doc(category)

    AccountsTable = database.get_accounts_table()
    new_account = AccountsTable(number=account_num, name=name, description=description, normal_side=normal_side,
                                balance=balance, date_created=created, statement=statement, comment=comment,
                                category=category, subcategory=subcategory, active=False, created_by=session["username"])
    database.commit_to_database(new_account)

    AccountEventsTable = database.get_account_events_table()
    new_account_event = AccountEventsTable(event_type='Created', username=session['username'], date_made=created,
                                           account_id=new_account.id, account_number_before=None,
                                           account_number_after=account_num, account_name_before=None,
                                           account_name_after=name, account_balance_before=None,
                                           account_balance_after=balance, account_normal_side_before=None,
                                           account_normal_side_after=normal_side, account_active_before=None,
                                           account_active_after=True)
    database.commit_to_database(new_account_event)


def is_valid_name_number(database):
    name = request.form["name"]
    number = request.form["number"]
    accounts = database.get_accounts_info()
    valid_name = True
    valid_number = True
    for account in accounts:
        if name.lower() == account.name.lower():
            valid_number = False
        if number == account.number:
            valid_number = False
    if valid_number & valid_name:
        return True
    else:
        return False


def get_statement_doc(categories):
    if categories == "Asset" or categories == "Liability" or categories == "Equity":
        return "BS"
    else:
        return "IS"


def concat(number1, number2):
    string = str(number1) + str(number2)
    return int(string)


def edit_save_account(account, database):
    initial_num = request.form["initial_num"]
    name = request.form["name"]
    number = int(str(concat(initial_num, request.form["number"])))
    normal_side = request.form["normal_side"]
    balance = request.form["balance"]

    if any([name != account.name, number != account.number, normal_side != account.normal_side,
            str(balance) != str(account.balance)]):
        AccountEventsTable = database.get_account_events_table()
        created = datetime.now()
        new_account_event = AccountEventsTable(event_type='Modified', username=session['username'], date_made=created,
                                               account_id=account.id, account_number_before=account.number,
                                               account_number_after=number, account_name_before=account.name,
                                               account_name_after=name, account_balance_before=account.balance,
                                               account_balance_after=balance,
                                               account_normal_side_before=account.normal_side,
                                               account_normal_side_after=normal_side,
                                               account_active_before=account.active,
                                               account_active_after=account.active)
        database.commit_to_database(new_account_event)

    if name != account.name or number != account.number:
        change_journal(account, name, number, database)
        change_ledger(account, number, database)

    # Edit account
    account.category = request.form["category"]
    account.name = name
    account.subcategory = request.form["subcategory"]
    account.number = number
    account.description = request.form["description"]
    account.normal_side = normal_side
    account.balance = balance
    account.comment = request.form["comment"]
    database.commit_info()


def toggle_active(account, database):
    num = 0
    if account.active:
        if not account.balance:
            account.active = False
            num = 0
        else:
            num = 10
    else:
        account.active = True
        num = 0

    if num == 0:
        AccountEventsTable = database.get_account_events_table()
        created = datetime.now()
        new_account_event = AccountEventsTable(event_type='Modified', username=session['username'], date_made=created,
                                               account_id=account.id, account_number_before=account.number,
                                               account_number_after=account.number, account_name_before=account.name,
                                               account_name_after=account.name, account_balance_before=account.balance,
                                               account_balance_after=account.balance,
                                               account_normal_side_before=account.normal_side,
                                               account_normal_side_after=account.normal_side,
                                               account_active_before=not account.active,
                                               account_active_after=account.active)
        database.commit_to_database(new_account_event)

    database.commit_info()
    return num


def new_user_admin(database):
    if NewUser.correct_passwords_input():
        user = NewUser.get_new_user_info()
        role = request.form["role"]
        username = NewUser.set_username(user[0], user[1], user[9])
        UserTable = database.get_user_table()
        UserEventsTable = database.get_user_event_table()
        created = datetime.now()
        password_exp = created + timedelta(days=90)
        pre_passwords = [user[3]]

        # Create new user
        new_user = UserTable(username=username, password=user[3], role=role, activated=True, profile_picture=" ",
                             f_name=user[0], l_name=user[1], email=user[2], address=user[4], dob=user[9],
                             account_creation_date=created, password_expire_date=password_exp,
                             password_incorrect_entries=0, previous_passwords=pre_passwords, security_questions=None,
                             security_answers=None, city=None, apt_number=user[7], zip=user[8], state_province=user[5],
                             country=user[6], suspension_start=None, suspension_end=None, is_suspended=False)
        database.commit_to_database(new_user)

        # Create new user event
        new_user_event = UserEventsTable(username_before=None, username_after=username, role_before=None,
                                         role_after=role, f_name_before=None, f_name_after=user[0], l_name_before=None,
                                         l_name_after=user[1], address_before=None, address_after=user[4],
                                         city_before=None, city_after=None, apt_number_before=None,
                                         apt_number_after=user[7], zip_before=None, zip_after=user[8],
                                         state_province_before=None, state_province_after=user[5], country_before=None,
                                         country_after=user[6], activated_before=False, activated_after=False,
                                         is_suspended_before=False, is_suspended_after=False, date_made=datetime.now(),
                                         event_type='Created', username=session['username'], user_id=new_user.id)
        database.commit_to_database(new_user_event)
        return True

    else:
        return False


def get_answers():
    answers = ["", "", ""]
    answers[0] = request.form["answer1"]
    answers[1] = request.form["answer2"]
    answers[2] = request.form["answer3"]
    return answers


def verify_answers(answers):
    input_answers = get_answers()
    correct = [False, False, False]
    for x in range(0, 3):
        if answers[x] == input_answers[x]:
            correct[x] = True
    return correct


def transfer_User_info(username, role, database):
    new_user = database.get_new_user(username)
    UserTable = database.get_user_table()
    UserEventsTable = database.get_user_event_table()
    transfer = datetime.now()
    passwordExpire = transfer + timedelta(days=90)
    passwords = ["", new_user.password]

    # Create new user
    user = UserTable(username=new_user.username, password=new_user.password, role=role, activated=True,
                     profile_picture="", f_name=new_user.firstname, l_name=new_user.lastname, email=new_user.email,
                     address=new_user.street, dob=new_user.dob, account_creation_date=transfer,
                     password_expire_date=passwordExpire, password_incorrect_entries=0, previous_passwords=passwords,
                     security_questions=new_user.security_questions, security_answers=new_user.security_answers,
                     city=None, apt_number=new_user.aptnum, zip=new_user.zipcode, state_province=new_user.state,
                     country=new_user.country, suspension_start=None, suspension_end=None, is_suspended=False)
    database.commit_to_database(user)

    # Create new user event
    new_user_event = UserEventsTable(username_before=new_user.username, username_after=new_user.username,
                                     role_before=role, role_after=role, f_name_before=new_user.firstname,
                                     f_name_after=new_user.firstname, l_name_before=new_user.lastname,
                                     l_name_after=new_user.lastname, address_before=new_user.street,
                                     address_after=new_user.street, city_before=None, city_after=None,
                                     apt_number_before=new_user.aptnum, apt_number_after=new_user.aptnum,
                                     zip_before=new_user.zipcode, zip_after=new_user.zipcode,
                                     state_province_before=new_user.state, state_province_after=new_user.state,
                                     country_before=new_user.country, country_after=new_user.country,
                                     activated_before=False, activated_after=True, is_suspended_before=False,
                                     is_suspended_after=False, date_made=datetime.now(),
                                     event_type='Modified', username=session['username'], user_id=new_user.id)
    database.commit_to_database(new_user_event)

    # Delete the entry in the new user table
    database.delete_row(new_user)


def send_acceptance_email(user):
    username = user.username
    user_email = user.email
    name = user.f_name + " " + user.l_name
    body = "" + name + "\nYour account has been activated.\nYour username is : " + username
    body.format(name, username)
    subject = "Account Accepted"
    email_manager.send_email(user_email, subject, body)


def email(database):
    email_manager.send_email([request.form['to_input']], request.form['subject_input'], request.form['body_input'])
    username = session["username"]
    users = database.get_user_accounts()
    return render_template('admin_email.html', username=username, users=users)


def deactivated_user(user, database):
    user.activated = False
    database.commit_info()

    # Create new user event
    UserEventsTable = database.get_user_event_table()
    new_user_event = UserEventsTable(username_before=user.username, username_after=user.username,
                                     role_before=user.role, role_after=user.role, f_name_before=user.f_name,
                                     f_name_after=user.f_name, l_name_before=user.l_name,
                                     l_name_after=user.l_name, address_before=user.address,
                                     address_after=user.address, city_before=None, city_after=None,
                                     apt_number_before=user.apt_number, apt_number_after=user.apt_number,
                                     zip_before=user.zip, zip_after=user.zip,
                                     state_province_before=user.state_province,
                                     state_province_after=user.state_province,
                                     country_before=user.country, country_after=user.country,
                                     activated_before=True, activated_after=False,
                                     is_suspended_before=user.is_suspended, is_suspended_after=user.is_suspended,
                                     date_made=datetime.now(), event_type='Modified', username=session['username'],
                                     user_id=user.id)
    database.commit_to_database(new_user_event)


def set_suspension(user, database):
    start_date = request.form["start_date"]
    end_date = request.form["end_date"]
    now = date.today()
    if now.strftime("%Y-%m-%d") == start_date:
        deactivated_user(user, database)
    user.suspension_start = start_date
    user.suspension_end = end_date
    user.is_suspended = True
    database.commit_info()

    # Create new user event
    UserEventsTable = database.get_user_event_table()
    new_user_event = UserEventsTable(username_before=user.username, username_after=user.username,
                                     role_before=user.role, role_after=user.role, f_name_before=user.f_name,
                                     f_name_after=user.f_name, l_name_before=user.l_name,
                                     l_name_after=user.l_name, address_before=user.adr,
                                     address_after=None, city_before=None, city_after=None,
                                     apt_number_before=user.apt_number, apt_number_after=user.apt_number,
                                     zip_before=user.zip, zip_after=user.zip,
                                     state_province_before=user.state_province,
                                     state_province_after=user.state_province,
                                     country_before=user.country, country_after=user.country,
                                     activated_before=True, activated_after=True,
                                     is_suspended_before=False, is_suspended_after=True,
                                     date_made=datetime.now(), event_type='Modified', username=session['username'],
                                     user_id=user.id)
    database.commit_to_database(new_user_event)


def change_journal(account, name, number, database):
    entries = database.get_journal_contains_account(account.name)
    for entry in entries:
        journal_entry = database.get_journal_entry(entry.id)
        accounts = journal_entry.debit_accounts
        numbers = journal_entry.debit_accounts_numbers
        if account.name in accounts:
            x = accounts.index(account.name)
            accounts[x] = name
            numbers[x] = number
            database.commit_info()
            journal_entry.debit_accounts = accounts
            database.commit_info()
            journal_entry.debit_accounts_numbers = numbers
            database.commit_info()

        accounts = journal_entry.credit_accounts
        numbers = journal_entry.credit_accounts_numbers
        if account.name in accounts:
            x = accounts.index(account.name)
            accounts[x] = name
            numbers[x] = number
            database.commit_info()
            journal_entry.credit_accounts = accounts
            database.commit_info()
            journal_entry.credit_accounts_numbers = numbers
            database.commit_info()


def change_ledger(account, number, database):
    ledger_entries = database.get_account_ledger_info(account.number)
    for ledger_entry in ledger_entries:
        ledger = database.get_ledger_entry(ledger_entry.id)
        if ledger.account_number == account.number:
            database.commit_info()
            ledger.account_number = number
            database.commit_info()


def subcategory_accounts(accounts):
    subcategories = []
    for account in accounts:
        in_subcategories = False
        subcategory = account.subcategory
        if len(subcategories) == 0:
            subcategories.append(subcategory)
        else:
            for sub_cat in subcategories:
                if sub_cat == subcategory:
                    in_subcategories = True
            if not in_subcategories:
                subcategories.append(subcategory)
    return subcategories


def max_order_num(accounts):
    num = 0
    for account in accounts:
        if num < account.order:
            num = account.order
    return num


def add_account_to_chart(account, database):
    account.order = request.form["select_order"]
    balance = request.form["initial_balance"]
    account.balance = balance
    account.initial_balance = balance
    account.active = True
    database.commit_info()


def change_order(accounts, database):
    start = False
    order = request.form["select_order"]
    order_num = int(order)
    print(order_num)
    for account in accounts:
        print(account.order)
        if int(account.order) == order_num:
            order_num += 1
            account.order = order_num
            print(account.order)
            database.commit_info()
            start = True
        else:
            if start:
                break


