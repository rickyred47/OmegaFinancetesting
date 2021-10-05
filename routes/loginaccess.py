from flask import render_template, request


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
            print(errormessage.message)
            return render_template('login.html', errormessage=errormessage.message)
        else:
            errormessage = db.session.query(Error_MessageTable).filter_by(id=0).first()
            return render_template('login.html', errormessage=errormessage.message)

    @app.route('/fgtpsswrd')
    def forgot_password():
        return render_template('forgot_password.html')

    @app.route('/new_user')
    def new_user():
        return render_template('new_user.html')
