
class DbException(Exception):
    def __init__(self, errorCode, message):
        self.errorCode=errorCode
        self.message=message
