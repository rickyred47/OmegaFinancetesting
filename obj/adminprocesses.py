from flask import render_template, request, session
from datetime import datetime


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
    accountnum = concat(initial_num, number)

    AccountsTable = base.classes.accounts
    new_account = AccountsTable(number=accountnum, name=name, description=description, normal_side=normal_side,
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
    numstring = str(account.number)
    initial = int(numstring[0])
    number = int(numstring[1:])
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
