from exceptions import Exception

class ModelException(Exception):
    """Exception raised for errors in the input.

    Attributes:
        expr -- input expression in which the error occurred
        msg  -- explanation of the error
    """
    def __init__(self, msg, expr = None):
        self.msg = msg
        self.expr = expr

    def __str__(self):
        return repr(self.msg)