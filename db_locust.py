import logging

import pyodbc
from locust import task, User, TaskSet

count = 0
# SQL Server Connection Details
server = ''
database = 'test'
username = ''
password = ''
driver = 'ODBC Driver 17 for SQL Server'
connection_string = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password}"


class Sampletaskset(TaskSet):

    def on_start(self):
        global count
        count = count + 1
        self.counter = count

    def getConnection(self):
        conn = pyodbc.connect(driver=driver, host=server, Database=database, UID=username,
                              PWD=password, Trusted_Connection='no')
        return conn

    @task
    def executequery(self):
        logging.info("User {} started".format(self.counter))
        query = "select * from SampleTable"
        conn = self.getConnection()
        cursor = conn.cursor()
        try:
            logging.info("User %s Executing Query %s ", self.counter, query)
            cursor.execute(query)
            rows = cursor.fetchall()
            resp_len = len(rows)
            logging.info("User %s completed Query", self.counter)

        finally:
            cursor.close()
            conn.close()


class Testuser(User):
    logging.info("Starting user")
    tasks = [Sampletaskset]
