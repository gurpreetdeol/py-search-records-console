import pymssql
from ticket import config


class Database:
    ERROR_MESSAGE: str = None
    IS_CONNECTED: bool = False

    def __init__(self):
        __credentials = config.DBConfiguration()
        if __credentials.IS_FOUND:
            try:
                self.__connection = pymssql.connect(
                    server=__credentials.SERVER,
                    user=__credentials.USERNAME,
                    password=__credentials.PASSWORD,
                    database=__credentials.DATABASE)
                self.__cursor = self.__connection.cursor()
                self.IS_CONNECTED = True
            except Exception as ex:
                self.ERROR_MESSAGE = str(ex)
        else:
            self.ERROR_MESSAGE = __credentials.ERROR_MESSAGE

    def search(self, ticket_number: int):
        if self.IS_CONNECTED:
            try:
                __ticket_num = int(ticket_number)
                __query = f"EXEC ticket_search {__ticket_num}"
                self.__cursor.execute(__query)
                return self.__cursor.fetchall()
            except ValueError:
                print("Invalid Ticker Number.")
        elif len(self.ERROR_MESSAGE) == 0:
            self.ERROR_MESSAGE = "DB Server not connected"

        return None
