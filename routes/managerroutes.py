from flask import render_template, request, session, redirect, url_for
from obj import journal


def setup_page_routing(app, database):
    """

    :param database:
    :param app:
    :return:

    Set Up routes to run for the manager

    Manager pages
    """
    @app.route('/manager_home')
    def manager_home_page():
        if "Manager" in session:
            return render_template('manager_home_page.html', username="Ricardo Rojo")
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/chart_accounts')
    def manager_chart_accounts():
        if "Manager" in session:
            username = session["Manager"]
            accounts = database.get_accounts_info()
            return render_template('manager_char_accounts.html', username=username, accounts=accounts)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/<account_id>_ledger')
    def manager_account_ledger(account_id):
        if "Manager" in session:
            username = session["Manager"]
            account = database.get_account_info(account_id)
            entries = database.get_journal_contains_account(account.name)
            return render_template('manager_account_ledger.html', username=username, name=account.name,
                                   number=account.number, balance=account.balance, entries=entries)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/<account_number>_to_id')
    def manager_number_id(account_number):
        if"Manager" in session:
            account = database.get_account_info_by_number(account_number)
            return redirect(url_for('manager_account_ledger', account_id=account.id))
        else:
            return '', 204

    @app.route('/manager/journal')
    def manager_journal():
        if "Manager" in session:
            username = session["Manager"]
            accounts = database.get_active_accounts()
            entries = database.get_journal_entries()
            error = database.get_error_message(11)
            return render_template('manager_journal.html', username=username, accounts=accounts, entries=entries,
                                   error_message=error.message)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/journal/submit_entry', methods=['GET', 'POST'])
    def manager_entry():
        if "Manager" in session:
            user = session["Manager"]
            if request.method == "POST":
                journal.journal_entry_form(user, database)
                return redirect(url_for('manager_journal'))
            else:
                return '', 204
        else:
            return redirect(url_for('login_page'))

    @app.route('/back_ground_accept_reject_entry', methods=['GET', 'POST'])
    def manager_accept_reject_entry():
        if "Manager" in session:
            if request.method == "POST":
                entry_id = request.form["entry_id"]
                entry = database.get_journal_entry(entry_id)
                if request.form['accept_reject'] == 'Accept':
                    entry.status = "Accepted"
                    database.commit_info()
                elif request.form['accept_reject'] == 'Reject':
                    entry.status = "Rejected"
                    database.commit_info()
                return redirect(url_for('manager_journal'))
            else:
                return '', 204
        else:
            return redirect(url_for('login_page'))
