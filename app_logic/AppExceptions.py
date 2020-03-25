class AppError(Exception):
    def __init__(self, *args):

        self.message = args[0] if args else None

    def __str__(self):

        if self.message:
            return 'Logical Error ,\n\n Error details :\n {0} '.format(self.message)
        else:
            return 'A logical error has occurred'
