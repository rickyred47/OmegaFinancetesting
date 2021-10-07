from flask import render_template, request, redirect, url_for
from obj import NewUser


def setup_page_routing(app, base, db):
    # set up routes to run

    # Database accounts
    UserTable = base.classes.user
    Error_MessageTable = base.classes.error_message

    # the login page route
    @app.route('/', methods=['GET', 'POST'])
    def login_page():
        if request.method == "POST":
            username = request.form["username_input"]
            psswrd = request.form["password_input"]
            errormessage = db.session.query(Error_MessageTable).filter_by(id=5).first()
            return render_template('login.html', errormessage=errormessage.message)
        else:
            errormessage = db.session.query(Error_MessageTable).filter_by(id=0).first()
            return render_template('login.html', errormessage=errormessage.message)

    @app.route('/fgtpsswrd')
    def forgot_password():
        return render_template('forgot_password.html')

    # The new user Page
    @app.route('/new_user', methods=['GET', 'POST'])
    def new_user():
        if request.method == "POST":
            print("test")
            # Checks the both passwords are valid
            if NewUser.correct_passwords_input():
                # gathers the information of the form text fields
                print("test")
                NewUser.gatherInfo(db, base)
                print("test")
                return redirect(url_for('signed_up'))
        else:
            return render_template('new_user.html')

    @app.route('/signed_up')
    def signed_up():
        return render_template('signup.html')
