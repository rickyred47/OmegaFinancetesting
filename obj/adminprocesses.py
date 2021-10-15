from flask import render_template, request, session
from datetime import datetime
from datetime import datetime, timedelta
from obj import NewUser


def get_accounts_info(base, db):
    AccountsTable = base.classes.accounts
    accounts = db.session.query(AccountsTable)
    return accounts


def get_account_info(base, db, idnum):
    AccountsTable = base.classes.accounts
    account = db.session.query(AccountsTable).filter_by(id=idnum).first()
    return account


def get_new_users(base, db):
    NewUsersTable = base.classes.new_user
    newusers = db.session.query(NewUsersTable)
    return newusers


def get_user_accounts(base, db):
    UserTable = base.classes.user
    users = db.session.query(UserTable)
    return users


def account_form(base, db):
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

    AccountsTable = base.classes.accounts
    new_account = AccountsTable(number=account_num, name=name, description=description, normal_side=normal_side,
                                balance=balance, date_created=created, statement=statement, comment=comment,
                                category=category, subcategory=subcategory, created_by=1234, active=True)
    commit_to_database(new_account, db)


def get_statement_doc(categorys):
    if categorys == "Asset" or categorys == "Liability" or categorys == "Equity":
        return "BS"
    else:
        return "IS"


def commit_to_database(obj, db):
    db.session.add(obj)
    db.session.commit()


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


def edit_save_account(account, db):
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
    db.session.commit()
    return render_template('editaccount.html', accountcat=account.category, name=account.name,
                           subcategory=account.subcategory, initial_number=initial_num, number=number,
                           description=account.description, normal_side=account.normal_side,
                           balance=account.balance, comment=account.comment, saved="-SAVED", username=username)


def toggle_active(account, db):
    if account.active:
        account.active = False
    else:
        account.active = True
    db.session.commit()


def new_use_admin(base, db):
    if NewUser.correct_passwords_input():
        user = NewUser.get_new_user_info()
        role = request.form["role"]
        username = set_username(user[0], user[1], user[9])
        UserTable = base.classes.user
        created = datetime.now()
        password_exp = created + timedelta(days=90)
        new_user = UserTable(username=username, password=user[3], role=role, activated=True, profile_picture=" ",
                             f_name=user[0], l_name=user[1], email=user[2], address=user[4], dob=user[9],
                             account_creation_date=created, password_expire_date=password_exp,
                             password_incorrect_entries=0, previous_passwords=None, security_questions=None,
                             security_answers=None, city=None, apt_number=user[7], zip=user[8], state_province=user[5],
                             country=user[6])
        NewUser.commit_to_database(db, new_user)
        return True

    else:
        return False


def set_username(f_name, l_name, dob):
    username = f_name[0].lower() + l_name.lower() + dob[5:7] + dob[2:4]
    return username
