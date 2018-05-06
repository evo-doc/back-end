import re

def validate_email(email):
    """
    Just basic email validation
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_username(username):
    """
    Validate username
    """
    return re.match(r"\w{3,}", username)

def validate_password(password):
    return re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password)
