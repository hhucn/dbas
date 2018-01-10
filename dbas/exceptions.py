# coding=utf-8


class UserNotInDatabase(Exception):
    pass


class StatementToShort(Exception):
    def __init__(self, text=None, min_length=None):
        self.min_length = min_length
        self.text = text

        if self.text:
            msg = "%s is %d symbols long."

            if self.min_length:
                msg += "At least %d symbols are expected!".format(min_length)
            else:
                msg += "This is too short."

            super(self).__init__(msg)
