from flask import render_template, request, session, redirect, url_for
from obj import journal


def setup_page_routing(app, database):
    """

    :param database:
    :param app:
    :return: None
    """

    # The accountant pages
    @app.route('/accountant_home')
    def accountant_home_page():
        if "Accountant" in session:
            username = session["Accountant"]
            return render_template('accountant_home_page.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/chart_accounts')
    def accountant_chart_accounts():
        if "Accountant" in session:
            username = session["Accountant"]
            accounts = database.get_accounts_info()
            return render_template('accountant_char_accounts.html', username=username, accounts=accounts)
        else:
            return redirect(url_for('login_Page'))

    @app.route('/accountant/<account_id>_ledger')
    def accountant_account_ledger(account_id):
        if "Accountant" in session:
            username = session["Accountant"]
            account = database.get_account_info(account_id)
            ledger_entries = database.get_account_ledger_info(account.number)
            return render_template('accountant_account_ledger.html', username=username, account=account,
                                   Omaledger_entries=ledger_entries)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/journal')
    def accountant_journal():
        if "Accountant" in session:
            username = session["Accountant"]
            accounts = database.get_active_accounts()
            entries = database.get_journal_entries()
            return render_template('accountant_journal.html', username=username, accounts=accounts, entries=entries)
        else:
            return redirect(url_for('login_page'))

    @app.route('/accountant/journal/submit_entry', methods=['GET', 'POST'])
    def accountant_entry():
        if "Accountant" in session:
            user = session["Accountant"]
            if request.method == "POST":
                journal.journal_entry_form(user, database)
                return redirect(url_for('accountant_journal'))
            else:
                return '', 204
        else:
            return redirect(url_for('login_page'))
