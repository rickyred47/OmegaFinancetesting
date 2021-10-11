from flask import render_template, request
from datetime import datetime


def get_accounts_info(base, db):
    AccountsTable = base.classes.accounts
    accounts = db.session.query(AccountsTable)
    return accounts


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
    new_account = AccountsTable(number=accountnum, name=name, discription=description, normal_side=normal_side,
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