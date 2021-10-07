from flask import render_template, request


def gatherInfo(db, base):
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    password = request.form["password2"]
    address = request.form["street"]
    state = request.form["state"]
    country = request.form["country"]
    aptnum = request.form["aptnum"]
    zipcode = request.form["zipcode"]
    dob = request.form["dob"]
    print("test1")
    NewUserTable = base.classes.new_user
    newuser = NewUserTable(status="Pending", firstname=firstname, lastname=lastname, email=email, password=password,
                           street=address, aptnum=aptnum, state=state, country=country, dob=dob, zipcode=zipcode)
    print("test1")
    commit_to_database(db, newuser)


def correct_passwords_input():
    password = request.form["password"]
    if is_valid_password(password):
        password2 = request.form["password2"]
        if do_passwords_match(password, password2):
            return True
        else:
            return False
    else:
        return False


# code imported form Jade's user class
def is_valid_password(password):
    """
        Checks whether or not the supplied password is valid.
        In order for a password to be valid, it must:
            - be 8 to 64 characters in length
            - start with a letter
            - have at least one number
            - have at least one special character (!, @, #, $, etc.)

        Arguments:
            password (str) : Raw password string.

        Returns:
            bool : Whether or not this password is valid.
        """
    # Check for length.
    if len(password) < 8 or len(password) > 64:
        return False

    # Check for beginning with a letter.
    if password.lower()[0] not in 'abcdefghijklmnopqrstuvwxyz':
        return False

    # Check for having a number.
    has_num = False
    for c in password[1:]:
        if c in '123456789':
            has_num = True
            break
    if not has_num:
        return False

    # Check for having a special character.
    has_special_char = False
    for c in password[1:]:
        if c in '!@#$%^&*()-=_+{}[]:;"|,.<>/?\\\'`~':
            has_special_char = True
            break
    if not has_special_char:
        return False

    # All tests passed, return True
    return True


# Check that the passwords match
def do_passwords_match(password, password2):
    if password == password2:
        return True
    else:
        return False


# Sends the information to the database
def commit_to_database(db, obj):
    db.session.add(obj)
    db.session.commit()
    print("test2")
