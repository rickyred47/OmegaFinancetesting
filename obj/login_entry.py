from flask import request, render_template, redirect, url_for, session
from obj import NewUser


def is_valid_entry(database):
    username = request.form["username_input"]
    password = request.form["password_input"]
    user = database.get_user_account(username)
    if user is None:
        return error_message_page(5, database)
    if user.password_incorrect_entries >= 3:
        return error_message_page(3, database)
    if password == user.password:
        if user.activated:
            if user.security_questions is None:
                session["user"] = user.username
                return redirect(url_for('security_question_new_user'))
            user.password_incorrect_entries = 0
            database.commit_info()
            return user_role(user)
        else:
            return error_message_page(4, database)
    else:
        num = attempts_tried(database, user)
        return error_message_page(num, database)


def attempts_tried(database, user):
    attempts = user.password_incorrect_entries
    attempts = attempts + 1
    # Store attempts
    user.password_incorrect_entries = attempts
    database.commit_info()
    if attempts <= 2:
        return attempts
    else:
        return 3


def error_message_page(num, database):
    error_message = database.get_error_message(num)
    return render_template('login.html', error_message=error_message.message)


def user_role(user):
    role = user.role
    if role == "Administrator":
        session["Administrator"] = user.f_name + " " + user.l_name
        return redirect(url_for('admin_home_page'))
    if role == "Manager":
        session["Manager"] = user.f_name + " " + user.l_name
        return redirect(url_for('manager_home_page'))
    if role == "Accountant":
        session["Accountant"] = user.f_name + " " + user.l_name
        return redirect(url_for('accountant_home_page'))


def error_message_page_fp(num, database):
    error_message = database.get_error_message(num)
    return render_template('forgot_password.html', error_message=error_message.message)


def gather_security_questions_commit(user, database):
    security_info = NewUser.gather_security_info()
    user.security_questions = security_info[0]
    user.security_answers = security_info[1]
    database.commit_info()
