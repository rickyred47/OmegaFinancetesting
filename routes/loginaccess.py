from flask import render_template


def setup_page_routing(app):
    # set up routes to run

    # the login page route
    @app.route('/')
    def login_page():
        return render_template('login.html')

    @app.route('/fgtpsswrd')
    def forgot_password():
        return render_template('forgot_password.html')

    @app.route('/newuser')
    def new_user():
        return render_template('new_user.html')
