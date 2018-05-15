
class DbException(Exception):
    """
    This exception is raised in entity module
    """
    def __init__(self, errorCode, message):
        self.errorCode=errorCode
        self.message=message

class ApiException(Exception):
    """
    This exception is raised in api module
    """
    def __init__(self, errorCode, message):
        self.errorCode=errorCode
        self.message=message
