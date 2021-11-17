from sqlalchemy import desc, asc
from datetime import datetime
import pytz


class DatabaseHandler:
    def __init__(self):
        self.db = None
        self.base = None
        self.AccountsTable = None
        self.NewUsersTable = None
        self.UserTable = None
        self.ErrorTable = None
        self.AccountEventsTable = None
        self.Journal_Table = None
        self.Ledger_Table = None

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

    def get_account_info_by_number(self, number):
        self.AccountsTable = self.base.classes.accounts
        account = self.db.session.query(self.AccountsTable).filter_by(number=number).first()
        return account

    def get_all_accounts(self):
        self.AccountsTable = self.base.classes.accounts
        accounts = self.db.session.query(self.AccountsTable)
        return accounts

    def get_active_accounts(self):
        self.AccountsTable = self.base.classes.accounts
        accounts = self.db.session.query(self.AccountsTable).filter_by(active=True).order_by(asc(
            self.AccountsTable.order))
        return accounts

    def get_inactive_accounts(self):
        self.AccountsTable = self.base.classes.accounts
        accounts = self.db.session.query(self.AccountsTable).filter_by(active=False)
        return accounts

    def get_accounts_by_category(self, category):
        self.AccountsTable = self.base.classes.accounts
        accounts = self.db.session.query(self.AccountsTable).filter_by(category=category).order_by(asc(
            self.AccountsTable.order))
        return accounts

    # End of Accounts Database Methods

    # Account events database methods
    def get_account_events_table(self):
        self.AccountEventsTable = self.base.classes.account_event
        return self.AccountEventsTable

    def get_all_account_events(self):
        self.AccountEventsTable = self.base.classes.account_event
        account_events = self.db.session.query(self.AccountEventsTable)
        return account_events

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
        self.UserTable = self.base.classes.user
        users = self.db.session.query(self.UserTable).filter_by(is_suspended=True)
        return users

    def get_expired_users(self):
        users = self.get_user_accounts()
        current_time = datetime.today()
        current_time = pytz.utc.localize(current_time)
        userlist = []
        for user in users:
            user.password_expire_date.replace(tzinfo=current_time.tzinfo)
            if user.password_expire_date < current_time:
                print(user.password_expire_date)
                userlist.append(user)
        return userlist

    # End of User Database Methods

    # Journal Database Methods
    def get_journal_table(self):
        self.Journal_Table = self.base.classes.journal
        return self.Journal_Table

    def get_journal_entries(self):
        self.Journal_Table = self.base.classes.journal
        journal_entries = self.db.session.query(self.Journal_Table).order_by(desc(self.Journal_Table.date))
        return journal_entries

    def get_journal_entry(self, id_num):
        self.Journal_Table = self.base.classes.journal
        journal_entry = self.db.session.query(self.Journal_Table).filter_by(id=id_num).first()
        return journal_entry

    def get_journal_contains_account(self, account_name):
        self.Journal_Table = self.base.classes.journal
        account_entries = self.db.session.query(self.Journal_Table).filter(
            self.Journal_Table.debit_accounts.contains([account_name]) |
            self.Journal_Table.credit_accounts.contains([account_name])).filter_by(status="Accepted").order_by(desc(
            self.Journal_Table.date))
        return account_entries

    # End Journal Database Methods

    # Journal Event Database Methods
    def get_journal_event_table(self):
        self.Journal_Event_Table = self.base.classes.journal_event
        return self.Journal_Event_Table

    def get_all_journal_events(self):
        self.JournalEventsTable = self.base.classes.journal_event
        journal_events = self.db.session.query(self.JournalEventsTable)
        return journal_events

    # End Journal Event Database Methods

    # General Ledger Database Methods
    def get_ledger_table_class(self):
        self.Ledger_Table = self.base.classes.general_ledger
        return self.Ledger_Table

    def get_account_ledger_info(self, account_num):
        self.Ledger_Table = self.base.classes.general_ledger
        account_info = self.db.session.query(self.Ledger_Table).filter_by(account_number=account_num).order_by(asc(
            self.Ledger_Table.id))
        return account_info

    # End General Ledger Methods

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
