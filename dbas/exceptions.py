# coding=utf-8


class UserNotInDatabase(Exception):
    pass


class StatementToShort(Exception):
    def __init__(self, text=None, min_length=None):
        if text:
            msg = "%s is %d symbols long."

            if min_length:
                msg += "At least %d symbols are expected!".format(min_length)
            else:
                msg += "This is too short."

            super(self).__init__(msg)
