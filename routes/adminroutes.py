from flask import render_template, redirect, request, url_for, session
from obj import adminprocesses


def setup_page_routing(app, base, db):
    # set up routes to run

    # The admin pages
    @app.route('/admin_home')
    def admin_home_page():
        if "username" in session:
            username = session["username"]
            accounts = adminprocesses.get_accounts_info(base, db)
            newusers = adminprocesses.get_new_users(base, db)
            users = adminprocesses.get_user_accounts(base, db)
            username = session["username"]
            return render_template('admin.html', accounts=accounts, newusers=newusers, users=users, username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_users_accounts')
    def admin_user_accounts():
        if "username" in session:
            username = session["username"]
            users = adminprocesses.get_user_accounts(base, db)
            return render_template('adminuseraccounts.html', username=username, useraccounts=users)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_chart_accounts')
    def admin_chart_accounts():
        if "username" in session:
            username = session["username"]
            return render_template('chart_accounts_admin.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_accounts', methods=['GET', 'POST'])
    def admin_accounts():
        if "username" in session:
            username = session["username"]
            if request.method == "POST":
                idnum = request.form["account_id"]
                account = adminprocesses.get_account_info(base, db, idnum)
                adminprocesses.toggle_active(account, db)
                accounts = adminprocesses.get_accounts_info(base, db)
                return render_template('accounts_admin.html', accounts=accounts, username=username)
            else:
                accounts = adminprocesses.get_accounts_info(base, db)
                return render_template('accounts_admin.html', accounts=accounts, username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_create_user', methods=['GET', 'POST'])
    def admin_create_user():
        if "username" in session:
            if request.method == "POST":
                if adminprocesses.new_use_admin(base, db):
                    return redirect(url_for('admin_user_accounts'))
            else:
                username = session["username"]
                return render_template('admincreateuser.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_create_account', methods=['GET', 'POST'])
    def admin_create_account():
        if "username" in session:
            username = session["username"]
            if request.method == "POST":
                adminprocesses.account_form(base, db)
                return redirect('admin_accounts')
            else:
                return render_template('createnewaccount.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_add_chart_accounts')
    def admin_add_chart_account():
        if "username" in session:
            username = session["username"]
            return render_template('add_to_chart_of_accounts.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_edit_account/<account_id>', methods=['GET', 'POST'])
    def admin_edit_account(account_id):
        if "username" in session:
            username = session["username"]
            account = adminprocesses.get_account_info(base, db, account_id)
            if request.method == "POST":
                return adminprocesses.edit_save_account(account, db)
            else:
                return adminprocesses.edit_account(account)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_ledger/<account_id>')
    def admin_account_ledger(account_id):
        if "username" in session:
            account = adminprocesses.get_account_info(base, db, account_id)
            return render_template('accounts_ledger.html', name=account.name, number=account.number,
                                   balance=account.balance)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_about')
    def admin_about():
        if "username" in session:
            username = session["username"]
            return render_template('admin_about.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin/new_user')
    def admin_new_user_accounts():
        new_users = NewUser.get_new_users_info(base, db)
        return render_template('admin_new_user_accounts.html', newusers=new_users)
