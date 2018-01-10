# coding=utf-8


class UserNotInDatabase(Exception):
    pass


class StatementToShort(Exception):
    def __init__(self, text=None, min_length=None):
        self.min_length = min_length
        self.text = text

        if self.text:
            msg = "{} is {} symbols long. ".format(self.text, len(self.text))

            if self.min_length:
                msg += "At least {} symbols are expected!".format(self.min_length)
            else:
                msg += "This is too short."

            Exception.__init__(self, msg)
