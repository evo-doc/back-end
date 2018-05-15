import re

def validate_email(email):
    """
    Just basic email validation
        :param email:
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)!=None

def validate_username(username):
    """
    Validate username, username has to be at least 3 chars long
        :param username:
    """
    return re.match(r"\w{3,}", username)!=None

def validate_password(password):
    """
    Validate password, password has to be at least 8 chars long with one upper and one lower case, one number and one special character
        :param password:
    """
    return re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password)!=None
