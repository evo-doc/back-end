import re

def validate_email(email):
    """
    Just basic email validation
    """
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)!=None

def validate_username(username):
    """
    Validate username
    """
    return re.match(r"\w{3,}", username)!=None

def validate_password(password):
    return re.match(r"^(?=.*[A-Za-z])(?=.*\d)(?=.*[$@$!%*#?&])[A-Za-z\d$@$!%*#?&]{8,}$", password)!=None
