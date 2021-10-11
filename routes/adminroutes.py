from flask import render_template, redirect, request
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

    @app.route('/admin_accounts')
    def admin_accounts():
        return render_template('accounts_admin.html')

    @app.route('/admin_create_user')
    def admin_create_user():
        return render_template('admincreateuser.html')

    @app.route('/admin_create_account')
    def admin_create_account():
        return render_template('createnewaccount.html')

    @app.route('/admin_add_chart_accounts')
    def admin_add_chart_account():
        return render_template('add_to_chart_of_accounts.html')
