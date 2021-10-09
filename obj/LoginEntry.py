from flask import request, render_template, redirect, url_for


def is_valid_entry(db, base):
    username = request.form["username_input"]
    password = request.form["password_input"]
    user = search_for_user(username, base, db)
    if user is None:
        return error_message_page(5, base, db)
    if user.password_incorrect_entries >= 3:
        return error_message_page(3, base, db)
    if password == user.password:
        if user.activated:
            return user_role(user.role)
        else:
            return error_message_page(4, base, db)
    else:
        num = attempts_tried(user)
        return error_message_page(num, base, db)


def search_for_user(username, base, db):
    UserTable = base.classes.user
    selected = db.session.query(UserTable).filter_by(username=username).first()
    if bool(selected):
        return selected
    else:
        return None


def attempts_tried(user):
    attempts = user.password_incorrect_entries
    # Store attempts
    attempts = attempts + 1
    if attempts <= 2:
        return attempts
    else:
        return 3


def error_message_page(num, base, db):
    Error_message = base.classes.error_message
    error_message = db.session.query(Error_message).filter_by(id=num).first()
    return render_template('login.html', error_message=error_message.message)


def user_role(role):
    if role == "Administrator":
        return redirect(url_for('admin_home_page'))
    if role == "Manager":
        return redirect('')
    if role == "Accountant":
        return redirect('')