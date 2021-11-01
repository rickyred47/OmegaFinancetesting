from flask import render_template, request, session, redirect, url_for


def setup_page_routing(app, database):
    """

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
            return render_template('accountant_account_ledger.html', username=username, name=account.name,
                                   number=account.number, balance=account.balance)
        else:
            return redirect(url_for('login_page'))
