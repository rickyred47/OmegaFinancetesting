from flask import render_template, request, session, redirect, url_for


def setup_page_routing(app, database):
    """

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
            return render_template('manager_account_ledger.html', username=username, name=account.name,
                                   number=account.number, balance=account.balance)
        else:
            return redirect(url_for('login_page'))

    @app.route('/manager/journal')
    def manager_journal():
        if "Manager" in session:
            username = session["Manager"]
            accounts = database.get_active_accounts()
            return render_template('manager_journal.html', username=username, accounts=accounts)
        else:
            return redirect(url_for('login_page'))
