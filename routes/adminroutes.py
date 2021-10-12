from flask import render_template, redirect, request, url_for
from obj import adminprocesses


def setup_page_routing(app, base, db):
    # set up routes to run

    # The admin pages
    @app.route('/admin_home')
    def admin_home_page():
        accounts = adminprocesses.get_accounts_info(base, db)
        newusers = adminprocesses.get_new_users(base, db)
        users = adminprocesses.get_user_accounts(base, db)
        return render_template('admin.html', accounts=accounts, newusers=newusers, users=users)

    @app.route('/admin_users_accounts')
    def admin_user_accounts():
        return render_template('adminuseraccounts.html')

    @app.route('/admin_chart_accounts')
    def admin_chart_accounts():
        return render_template('chart_accounts_admin.html')

    @app.route('/admin_accounts', methods=['GET', 'POST'])
    def admin_accounts():
        if request.method == "POST":
            idnum = request.form["account_id"]
            account = adminprocesses.get_account_info(base, db, idnum)
            adminprocesses.toggle_active(account, db)
            accounts = adminprocesses.get_accounts_info(base, db)
            return render_template('accounts_admin.html', accounts=accounts)
        else:
            accounts = adminprocesses.get_accounts_info(base, db)
            return render_template('accounts_admin.html', accounts=accounts)

    @app.route('/admin_create_user', methods=['GET', 'POST'])
    def admin_create_user():
        return render_template('admincreateuser.html')

    @app.route('/admin_create_account', methods=['GET', 'POST'])
    def admin_create_account():
        if request.method == "POST":
            adminprocesses.account_form(base, db)
            return redirect('admin_accounts')
        else:
            return render_template('createnewaccount.html')

    @app.route('/admin_add_chart_accounts')
    def admin_add_chart_account():
        return render_template('add_to_chart_of_accounts.html')

    @app.route('/admin_edit_account/<account_id>', methods=['GET', 'POST'])
    def admin_edit_account(account_id):
        username = "rrojo"
        account = adminprocesses.get_account_info(base, db, account_id)
        if request.method == "POST":
            return adminprocesses.edit_save_account(account, db)
        else:
            return adminprocesses.edit_account(username, account)

    @app.route('/admin_ledger/<account_id>')
    def admin_account_ledger(account_id):
        account = adminprocesses.get_account_info(base, db, account_id)
        return render_template('accounts_ledger.html', name=account.name, number=account.number, balance=account.balance)
