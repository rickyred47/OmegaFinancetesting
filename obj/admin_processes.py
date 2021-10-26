from flask import render_template, request, session
from datetime import datetime, timedelta
from obj import NewUser, email_manager


def account_form(database):
    category = request.form["category"]
    name = request.form["name"]
    subcategory = request.form["subcategory"]
    initial_num = request.form["initial_num"]
    number = request.form["number"]
    description = request.form["description"]
    normal_side = request.form["normal_side"]
    balance = request.form["initial_balance"]
    comment = request.form["comment"]
    created = datetime.now()
    statement = get_statement_doc(category)
    account_num = concat(initial_num, number)

    AccountsTable = database.get_accounts_table()
    new_account = AccountsTable(number=account_num, name=name, description=description, normal_side=normal_side,
                                balance=balance, date_created=created, statement=statement, comment=comment,
                                category=category, subcategory=subcategory, created_by=1234, active=True)
    database.commit_to_database(new_account)


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
    number = int(num_string[1:])
    return render_template('editaccount.html', accountcat=account.category, name=account.name,
                           subcategory=account.subcategory, initial_number=initial, number=number,
                           description=account.description, normal_side=account.normal_side,
                           balance=account.balance, comment=account.comment, username=username)


def edit_save_account(account, database):
    username = session["username"]
    account.category = request.form["category"]
    account.name = request.form["name"]
    account.subcategory = request.form["subcategory"]
    initial_num = request.form["initial_num"]
    number = request.form["number"]
    account.number = concat(initial_num, number)
    account.description = request.form["description"]
    account.normal_side = request.form["normal_side"]
    account.balance = request.form["initial_balance"]
    account.comment = request.form["comment"]
    database.commit_info()
    return render_template('editaccount.html', accountcat=account.category, name=account.name,
                           subcategory=account.subcategory, initial_number=initial_num, number=number,
                           description=account.description, normal_side=account.normal_side,
                           balance=account.balance, comment=account.comment, saved="-SAVED", username=username)


def toggle_active(account, database):
    if account.active:
        account.active = False
    else:
        account.active = True
    database.commit_info()


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
                             country=user[6])
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
                     country=new_user.country)
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
