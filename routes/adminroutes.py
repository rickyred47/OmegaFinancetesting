from flask import render_template, redirect, request, url_for, session
from obj import admin_processes


def setup_page_routing(app, database):
    # set up routes to run

    # The admin pages
    @app.route('/admin_home')
    def admin_home_page():
        if "username" in session:
            username = session["username"]
            accounts = database.get_accounts_info()
            newusers = database.get_new_users()
            users = database.get_user_accounts()
            return render_template('admin_home_page.html', accounts=accounts[-6:], newusers=newusers[-6:], users=users[-6:],
                                   username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_users_accounts')
    def admin_user_accounts():
        if "username" in session:
            username = session["username"]
            users = database.get_user_accounts()
            return render_template('adminuseraccounts.html', username=username, useraccounts=users)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_chart_accounts')
    def admin_journalize():
        if "username" in session:
            username = session["username"]
            return render_template('journalize_admin.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_accounts', methods=['GET', 'POST'])
    def admin_chart_accounts():
        if "username" in session:
            username = session["username"]
            if request.method == "POST":
                idnum = request.form["account_id"]
                account = database.get_account_info(idnum)
                admin_processes.toggle_active(account, database)
                accounts = database.get_accounts_info()
                return render_template('admin_char_accounts.html', accounts=accounts, username=username)
            else:
                accounts = database.get_accounts_info()
                return render_template('admin_char_accounts.html', accounts=accounts, username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_create_user', methods=['GET', 'POST'])
    def admin_create_user():
        if "username" in session:
            if request.method == "POST":
                if admin_processes.new_use_admin(database):
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
                admin_processes.account_form(database)
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
            account = database.get_account_info(account_id)
            if request.method == "POST":
                return admin_processes.edit_save_account(account, database)
            else:
                return admin_processes.edit_account(account)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_ledger/<account_id>')
    def admin_account_ledger(account_id):
        if "username" in session:
            account = database.get_account_info(account_id)
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

    @app.route('/admin/new_users')
    def admin_new_user_accounts():
        new_users = database.get_new_users()
        return render_template('admin_new_user_accounts.html', newusers=new_users)

    @app.route('/admin_password_report')
    def admin_password_report():
        if "username" in session:
            username = session["username"]
            return render_template('admin_password_report.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/admin_email', methods=['GET', 'POST'])
    def admin_email():
        if "username" in session:
            if request.method == "POST":
                print(request.form)
                return admin_processes.email(database)
            else:
                username = session["username"]
                users = database.get_user_accounts()
                return render_template('admin_email.html', username=username, users=users)
        else:
            return redirect(url_for('login_page'))

    @app.route('/eventlog')
    def eventlog():
        if "username" in session:
            username = session["username"]
            return render_template('eventlog.html', username=username)
        else:
            return redirect(url_for('login_page'))

    @app.route('/background_accept_user', methods=['POST'])
    def admin_accept_user():
        if request.method == "POST":
            username = request.form["username_input"]
            role = request.form["role"]
            admin_processes.transfer_User_info(username, role, database)
            user = database.get_user_account(username)
            admin_processes.send_acceptance_email(user)
            return redirect(url_for('admin_new_user_accounts'))

    @app.route('/background_reject_user/<username>')
    def admin_reject_user(username):
        new_user = database.get_new_user(username)
        database.delete_row(new_user)
        return redirect(url_for('admin_new_user_accounts'))
