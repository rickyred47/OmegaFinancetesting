from flask import render_template, request, redirect, url_for, session
from obj import NewUser, login_entry, admin_processes


def setup_page_routing(app, database):
    # set up routes to run

    # the login page route
    @app.route('/', methods=['GET', 'POST'])
    def login_page():
        if request.method == "POST":
            return login_entry.is_valid_entry(database)
        else:
            return login_entry.error_message_page(0, database)

    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        if request.method == "POST":
            email = request.form["email"]
            username = request.form["username"]
            user = database.get_user_account(username)
            if bool(user):
                if user.email == email:
                    session["user"] = user.username
                    return redirect(url_for('security_questions_fp'))
                else:
                    return login_entry.error_message_page_fp(6, database)
            else:
                return login_entry.error_message_page_fp(5, database)
        else:
            return render_template('forgot_password.html')

    # The new user Page
    @app.route('/new_user', methods=['GET', 'POST'])
    def new_user():
        if request.method == "POST":
            # Checks the both passwords are valid
            if NewUser.correct_passwords_input():
                # gathers the information of the form text fields
                NewUser.gatherInfo_and_commit(database)
                # Sends to Security questions
                return redirect(url_for('security_question_new_user'))
        else:
            return render_template('new_user.html')

    @app.route('/logged_off')
    def logged_off_page():
        if "username" in session:
            session.pop("username", None)
            return render_template('Logoff.html')
        else:
            return redirect('login_page')

    @app.route('/security_questions', methods=['GET', 'POST'])
    def security_question_new_user():
        if "user" in session:
            username = session["user"]
            if request.method == "POST":
                login_entry.gather_security_questions(username, database)
                role = database.get_user_role(username)
                session.pop("user", None)
                session["username"] = database.get_user_fullname(username)
                return login_entry.user_role(role)
            else:
                return render_template('security_questions.html')
        if "New_user" in session:
            username = session["New_user"]
            if request.method == "POST":
                login_entry.gather_security_questions(username, database)
                return redirect('signed_up')
            else:
                return render_template('security_questions.html')
        else:
            return redirect('login_page')

    @app.route('/signed_up')
    def signed_up():
        if "New_user" in session:
            session.pop("New_user", None)
            return render_template('signedup.html')
        else:
            return redirect('login_page')

    @app.route('/forgot_password/security_questions', methods=['GET', 'POST'])
    def security_questions_fp():
        if "user" in session:
            username = session["user"]
            user = database.get_user_account(username)
            questions = user.security_questions
            if request.method == "POST":
                answers = user.security_answers
                correct_answers = admin_processes.verify_answers(answers)
                if correct_answers[0] and correct_answers[1] and correct_answers[2]:
                    return redirect(url_for('create_new_password'))
                else:
                    return render_template('security_questions_fp.html', question1=questions[0], question2=questions[1],
                                           question3=questions[2], correct=correct_answers)
            else:
                return render_template('security_questions_fp.html', question1=questions[0], question2=questions[1],
                                       question3=questions[2], correct=[True, True, True])
        else:
            return redirect('login_page')

    @app.route('/forgot_password/new_password', methods=['GET', 'POST'])
    def create_new_password():
        if "user" in session:
            username = session["user"]
            user = database.get_user_account(username)
            passwords = user.previous_passwords
            if request.method == "POST":
                used = False
                password_in = request.form["password1"]
                password2 = request.form["password2"]
                if new_user.is_valid_password(password_in) and new_user.do_passwords_match(password_in, password2):
                    for password in passwords:
                        if password == password_in:
                            used = True
                    if not used:
                        user.password = password_in
                        database.commit_info()
                        passwords.append(password_in)
                        user.previous_passwords = passwords
                        database.commit_info()
                        return redirect(url_for('login_page'))
                    else:
                        error = database.get_error_message(7)
                        return render_template('new_password.html', error_message=error.message)
                return render_template('new_password.html')
            else:
                return render_template('new_password.html')
        else:
            redirect(url_for('login_page'))
