class DatabaseHandler:
    def __init__(self):
        self.db = None
        self.base = None
        self.AccountsTable = None
        self.NewUsersTable = None
        self.UserTable = None
        self.ErrorTable = None

    # Accounts Database Methods
    def get_accounts_table(self):
        self.AccountsTable = self.base.classes.accounts
        return self.AccountsTable

    def get_accounts_info(self):
        self.AccountsTable = self.base.classes.accounts
        accounts = self.db.session.query(self.AccountsTable)
        return accounts

    def get_account_info(self, id_num):
        self.AccountsTable = self.base.classes.accounts
        account = self.db.session.query(self.AccountsTable).filter_by(id=id_num).first()
        return account

    def get_active_accounts(self):
        self.AccountsTable = self.base.classes.accounts
        accounts = self.db.session.query(self.AccountsTable).filter_by(active=True)
        return accounts

    def get_inactive_accounts(self):
        self.AccountsTable = self.base.classes.accounts
        accounts = self.db.session.query(self.AccountsTable).filter_by(active=False)
        return accounts
    # End of Accounts Database Methods

    # Account events database methods
    def get_account_events_table(self):
        self.account_events_table = self.base.classes.account_event
        return self.account_events_table
    # End of account events database methods

    # New User Database Methods
    def get_new_user_Table(self):
        self.NewUsersTable = self.base.classes.new_user
        return self.NewUsersTable

    def get_new_users(self):
        self.NewUsersTable = self.base.classes.new_user
        new_users = self.db.session.query(self.NewUsersTable)
        return new_users

    def get_new_user(self, username):
        self.NewUsersTable = self.base.classes.new_user
        new_user = self.db.session.query(self.NewUsersTable).filter_by(username=username).first()
        return new_user
    # End of New User Database Methods

    # User Database Methods
    def get_user_table(self):
        self.UserTable = self.base.classes.user
        return self.UserTable

    def get_user_accounts(self):
        self.UserTable = self.base.classes.user
        users = self.db.session.query(self.UserTable)
        return users

    def get_users_by_role(self, role):
        self.UserTable = self.base.classes.user
        users = self.db.session.query(self.UserTable)
        return users

    def get_user_account(self, username):
        self.UserTable = self.base.classes.user
        select_user = self.db.session.query(self.UserTable).filter_by(username=username).first()
        return select_user

    def get_user_role(self, username):
        self.UserTable = self.base.classes.user
        select_user = self.db.session.query(self.UserTable).filter_by(username=username).first()
        return select_user.role

    def get_user_fullname(self, username):
        self.UserTable = self.base.classes.user
        select_user = self.db.session.query(self.UserTable).filter_by(username=username).first()
        return select_user.f_name + " " + select_user.l_name

    def get_suspended_users(self):
        self.UserTable= self.base.classes.user
        users = self.db.session.query(self.UserTable).filter_by(is_suspended=True)
        return users

    # End of User Database Methods

    def get_error_message(self, id_num):
        self.ErrorTable = self.base.classes.error_message
        error = self.db.session.query(self.ErrorTable).filter_by(id=id_num).first()
        return error

    def commit_to_database(self, obj):
        self.db.session.add(obj)
        self.db.session.commit()

    def commit_info(self):
        self.db.session.commit()

    def delete_row(self, obj):
        self.db.session.delete(obj)
        self.db.session.commit()
