from flask import render_template, redirect, request


def setup_page_routing(app, base, db):
    # set up routes to run

    # The admin pages
    @app.route('/admin')
    def admin_home_page():
        return render_template('admin.html')

    @app.route('/admin_users_accounts')
    def admin_user_accounts():
        return render_template('adminuseraccounts.html')
