from django.db import connection


def log_error(exception_args, exception_details):
    print(exception_args, exception_details)


class Database:
    cursor = ""

    #   def __init__(self):
    #        self.cursor = connection.cursor()

    def connect(self):
        db_connection = False
        try:
            self.cursor = connection.cursor()
            db_connection = True
        except Exception as exception:
            log_error(exception.args, exception)
            db_connection = False
        finally:
            return db_connection

    def disconnect(self):
        try:
            self.cursor.close()
        except Exception as exception:
            log_error(exception.args, exception)

    def get_data(self, procedure):

        try:
            if self.connect():
                self.cursor.callproc(procedure)
                columns = [col[0] for col in self.cursor.description]
                return [
                    dict(zip(columns, row))
                    for row in self.cursor.fetchall()
                ]
                # results = self.cursor.fetchall()
                # return results

        except Exception as exception:
            log_error(exception.args, exception)

        finally:
            self.disconnect()
