from flask import render_template


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
