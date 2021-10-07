from flask import render_template, request, redirect, url_for
from obj import NewUser, LoginEntry


def setup_page_routing(app, base, db):
    # set up routes to run

    # Database accounts
    Error_MessageTable = base.classes.error_message

    # the login page route
    @app.route('/', methods=['GET', 'POST'])
    def login_page():
        if request.method == "POST":
            return LoginEntry.is_valid_entry(db, base)
        else:
            return LoginEntry.error_message_page(0, base, db)

    @app.route('/fgtpsswrd')
    def forgot_password():
        return render_template('forgot_password.html')

    # The new user Page
    @app.route('/new_user', methods=['GET', 'POST'])
    def new_user():
        if request.method == "POST":
            # Checks the both passwords are valid
            if NewUser.correct_passwords_input():
                # gathers the information of the form text fields
                NewUser.gatherInfo_and_commit(db, base)
                # Send to signed_up Page
                return render_template('signup.html')
        else:
            return render_template('new_user.html')

