import mysql.connector


class UseDatabase:
    def __init__(self, config: dict):
        self.configuration = config

    def __enter__(self):
        try:
            self.conn = mysql.connector.connect(**self.configuration)
            self.cursor = self.conn.cursor()
            return self.cursor
        except mysql.connector.errors.InterfaceError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.ProgrammingError as err:
            raise ConnectionError(err)
        except mysql.connector.errors.DataError as err:
            raise DataError(err)

    def __exit__(self, exc_type, exc_value, exc_trace):
        self.conn.commit()
        self.cursor.close()
        self.conn.close()
        if exc_type is mysql.connector.errors.ProgrammingError:
            raise SQLError(exc_value)
        if exc_type is mysql.connector.errors.DataError:
            raise DataError(exc_value)


class ConnectionError(Exception):
    pass


class SQLError(Exception):
    pass


class DataError(Exception):
    pass
