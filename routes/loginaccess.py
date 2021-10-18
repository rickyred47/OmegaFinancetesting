from flask import render_template, request, redirect, url_for, session
from obj import NewUser, LoginEntry, adminprocesses


def setup_page_routing(app, base, db):
    # set up routes to run

    # the login page route
    @app.route('/', methods=['GET', 'POST'])
    def login_page():
        if request.method == "POST":
            return LoginEntry.is_valid_entry(db, base)
        else:
            return LoginEntry.error_message_page(0, base, db)

    @app.route('/forgot_password', methods=['GET', 'POST'])
    def forgot_password():
        if request.method == "POST":
            email = request.form["email"]
            username = request.form["username"]
            user = adminprocesses.get_user_account(username, base, db)
            if bool(user):
                if user.email == email:
                    session["user"] = user.username
                    return redirect(url_for('security_questions_fp'))
                else:
                    return LoginEntry.error_message_page_fp(6, base, db)
            else:
                return LoginEntry.error_message_page_fp(5, base, db)
        else:
            return render_template('forgot_password.html')

    # The new user Page
    @app.route('/new_user', methods=['GET', 'POST'])
    def new_user():
        if request.method == "POST":
            # Checks the both passwords are valid
            if NewUser.correct_passwords_input():
                # gathers the information of the form text fields
                NewUser.gatherInfo_and_commit(db, base)
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
        if "New_user" in session:
            username = session["New_user"]
            if request.method == "POST":
                user = NewUser.find_new_user(username, base, db)
                security_info = NewUser.gather_security_info()
                user.security_questions = security_info[0]
                user.security_answers = security_info[1]
                db.session.commit()
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
            user = adminprocesses.get_user_account(username, base, db)
            questions = user.security_questions
            if request.method == "POST":
                answers = user.security_answers
                correct_answers = adminprocesses.verify_answers(answers)
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
            user = adminprocesses.get_user_account(username, base, db)
            passwords = user.previous_passwords
            if request.method == "POST":
                used = False
                password_input = request.form["password1"]
                password2 = request.form["password2"]
                if NewUser.is_valid_password(password_input) and NewUser.do_passwords_match(password_input, password2):
                    for password in passwords:
                        if password == password_input:
                            used = True
                    if not used:
                        user.password = password_input
                        db.session.commit()
                        passwords.append(password_input)
                        user.previous_passwords = passwords
                        db.session.commit()
                        return redirect(url_for('login_page'))
                    else:
                        message = NewUser.get_error_message(7, base, db)
                        return render_template('new_password.html', error_message=message)
                return render_template('new_password.html')
            else:
                return render_template('new_password.html')
        else:
            redirect(url_for('login_page'))
