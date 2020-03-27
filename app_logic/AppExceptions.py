from datetime import datetime


class AppError(Exception):
    def __init__(self, *args):

        self.message = args[0] if args else None

    def __str__(self):

        if self.message:
            return 'Logical Error :\n {0} '.format(self.message)
        else:
            return 'A logical error has occurred\n'


class DatabaseError(Exception):
    def __init__(self, *args):

        self.message = args[0] if args else None

    def __str__(self):

        if self.message:
            return self.message
        else:
            return 'Application lucks some data to enable processing. Details haven\'t been captured. ' \
                   'Time of error : ' + str(datetime.now())
