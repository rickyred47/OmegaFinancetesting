from flask import request, session


def gatherInfo_and_commit(db, base):
    """
        This will all the information of the form and commit
        it to the database

        Arguments
            db: will get the database
            base: gets the auto_map class to create user tables
        Returns:
            None
    """
    # Gather User's Information
    user = get_new_user_info()
    username = set_username(user[0], user[1], user[9])
    new_user = find_new_user(username, base, db)
    if not bool(new_user):
        # Creates a NewUser class based on the new_user table
        NewUserTable = base.classes.new_user
        # Creates a new user object
        newuser = NewUserTable(status="Pending", firstname=user[0], lastname=user[1], email=user[2], password=user[3],
                               street=user[4], aptnum=user[7], state=user[5], country=user[6], dob=user[9],
                               zipcode=user[8],
                               security_questions=None, security_answers=None, username=username)
        # Adds the Information to the database and commits it
        commit_to_database(db, newuser)
    # Creates a session to complete Questions
    session["New_user"] = username


# Makes sure that all constraints are being fallowed
def correct_passwords_input():
    """
        The method will first check if the code is valid
        Then it will check if both password match with each other

        Return:
            bool: whether the passwords pass both or fail at least once
    """
    # Get teh string password from the form
    password = request.form["password"]
    # Checks if the password is valid
    if is_valid_password(password):
        # Once teh test is passed it will compare both passwords
        # Gets the retyped password form the form
        password2 = request.form["password2"]
        # Checks if the passwords match
        if do_passwords_match(password, password2):
            # Since it passed both validations it returns true
            return True
        else:
            # The password did not match, so it will return false
            return False
    else:
        # The password was not valid, so it will return false
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
    """
    Arguments:
        password (str): Raw password string
        password2 (str): Second password string to compare
    Returns:
        bool : Whether both password str matched
    """

    # Checks both password match
    if password == password2:
        return True
    else:
        return False


# Sends the information to the database
def commit_to_database(db, obj):
    db.session.add(obj)
    db.session.commit()


def get_new_user_info():
    """
    Gather the basic info of a user

    Returns: [array positions]
    firstname [0]
    lastname  [1]
    email     [2]
    password  [3]
    address   [4]
    state     [5]
    country   [6]
    apt_num   [7]
    zipcode   [8]
    dob       [9]
    """
    firstname = request.form["firstname"]
    lastname = request.form["lastname"]
    email = request.form["email"]
    password = request.form["password2"]
    address = request.form["street"]
    state = request.form["state"]
    country = request.form["country"]
    apt_num = request.form["aptnum"]
    zipcode = request.form["zipcode"]
    dob = request.form["dob"]
    return firstname, lastname, email, password, address, state, country, apt_num, zipcode, dob


def gather_security_info():
    questions = ["", "", ""]
    answers = ["", "", ""]
    questions[0] = request.form["question1"]
    answers[0] = request.form["answer1"]
    questions[1] = request.form["question2"]
    answers[1] = request.form["answer2"]
    questions[2] = request.form["question3"]
    answers[2] = request.form["answer3"]
    return questions, answers


def get_new_users_info(base, db):
    New_UserTable = base.classes.new_user
    new_users = db.session.query(New_UserTable)
    return new_users


def find_new_user(username, base, db):
    New_UserTable = base.classes.new_user
    new_user = db.session.query(New_UserTable).filter_by(username=username).first()
    return new_user


def set_username(f_name, l_name, dob):
    username = f_name[0].lower() + l_name.lower() + dob[5:7] + dob[2:4]
    return username


def get_error_message(id_num, base, db):
    Errors = base.classes.error_message
    error = db.session.query(Errors).filter_by(id=id_num).first()
    return error.message
