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
                                category=category, subcategory=subcategory, created_by=1234, active=True)
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
    for account in accounts:
        if name.lower() == account.name.lower():
            return False
        if number == account.number:
            return False
        else:
            return True
    return True


def get_statement_doc(categories):
    if categories == "Asset" or categories == "Liability" or categories == "Equity":
        return "BS"
    else:
        return "IS"


def concat(number1, number2):
    string = str(number1) + str(number2)
    return int(string)


def edit_account(account):
    username = session["username"]
    num_string = str(account.number)
    initial = int(num_string[0])
    number = num_string[1:]
    return render_template('editaccount.html', accountcat=account.category, name=account.name,
                           subcategory=account.subcategory, initial_number=initial, number=number,
                           description=account.description, normal_side=account.normal_side,
                           balance=account.balance, comment=account.comment, username=username)


def edit_save_account(account, database):
    username = session["username"]
    initial_num = request.form["initial_num"]
    name = request.form["name"]
    number = int(str(concat(initial_num, request.form["number"]))[1:])
    normal_side = request.form["normal_side"]
    balance = request.form["initial_balance"]

    if any([name != account.name, number != account.number, normal_side != account.normal_side, str(balance) != str(account.balance)]):
        AccountEventsTable = database.get_account_events_table()
        created = datetime.now()
        new_account_event = AccountEventsTable(event_type='Modified', username=session['username'], date_made=created,
                                               account_id=account.id, account_number_before=account.number,
                                               account_number_after=number, account_name_before=account.name,
                                               account_name_after=name, account_balance_before=account.balance,
                                               account_balance_after=balance, account_normal_side_before=account.normal_side,
                                               account_normal_side_after=normal_side, account_active_before=account.active,
                                               account_active_after=account.active)
        database.commit_to_database(new_account_event)

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
    return render_template('editaccount.html', accountcat=account.category, name=account.name,
                           subcategory=account.subcategory, initial_number=initial_num, number=number,
                           description=account.description, normal_side=account.normal_side,
                           balance=account.balance, comment=account.comment, saved="-SAVED", username=username)


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
                                               account_balance_after=account.balance, account_normal_side_before=account.normal_side,
                                               account_normal_side_after=account.normal_side, account_active_before=not account.active,
                                               account_active_after=account.active)
        database.commit_to_database(new_account_event)

    database.commit_info()
    return num


def new_use_admin(database):
    if NewUser.correct_passwords_input():
        user = NewUser.get_new_user_info()
        role = request.form["role"]
        username = NewUser.set_username(user[0], user[1], user[9])
        UserTable = database.get_user_table()
        created = datetime.now()
        password_exp = created + timedelta(days=90)
        pre_passwords = [user[3]]
        new_user = UserTable(username=username, password=user[3], role=role, activated=True, profile_picture=" ",
                             f_name=user[0], l_name=user[1], email=user[2], address=user[4], dob=user[9],
                             account_creation_date=created, password_expire_date=password_exp,
                             password_incorrect_entries=0, previous_passwords=pre_passwords, security_questions=None,
                             security_answers=None, city=None, apt_number=user[7], zip=user[8], state_province=user[5],
                             country=user[6], suspension_start=None, suspension_end=None, is_suspended=False)
        database.commit_to_database(new_user)
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
    transfer = datetime.now()
    passwordExpire = transfer + timedelta(days=90)
    passwords = ["", new_user.password]
    user = UserTable(username=new_user.username, password=new_user.password, role=role, activated=True,
                     profile_picture="", f_name=new_user.firstname, l_name=new_user.lastname, email=new_user.email,
                     address=new_user.street, dob=new_user.dob, account_creation_date=transfer,
                     password_expire_date=passwordExpire, password_incorrect_entries=0, previous_passwords=passwords,
                     security_questions=new_user.security_questions, security_answers=new_user.security_answers,
                     city=None, apt_number=new_user.aptnum, zip=new_user.zipcode, state_province=new_user.state,
                     country=new_user.country, suspension_start=None, suspension_end=None, is_suspended=False)
    database.commit_to_database(user)
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
