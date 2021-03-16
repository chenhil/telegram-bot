import logging
import psycopg2
import os


class Database:
    def __init__(self, dbKey):
        self.dbKey = dbKey
        connection = psycopg2.connect(dbKey,sslmode='require')
        cursor = connection.cursor()

        logging.info("PostgreSQL server information")
        logging.info(connection.get_dsn_parameters())

        # Create tables if not exist
        cursor.execute(self.get_sql("assetTable"))
        cursor.execute(self.get_sql("commandTable"))

        cursor.close()
        connection.commit()
        connection.close()

        self.getCoinStat = self.get_sql("getasset")
        self.deleteCoinStat = self.get_sql("deleteasset")
        self.insertCoinStat = self.get_sql("insertasset")
        self.insertCommand = self.get_sql("insertcommand")


    # Get string with SQL statement from file
    def get_sql(self, filename):
        filename = f"{filename}.sql"
        with open(os.path.join("sql", filename)) as f:
            return f.read()

    
    # Save issued commands to database
    def save_data(self, user_id, chat_id, command):
        try:
            self.execute_query(self.insertCommand, user_id, chat_id, command)
        except Exception as e:
            logging.error(e)

    def execute_query(self, sql, *args):
        result = {"result": None, "error": None}
        connection = psycopg2.connect(self.dbKey,sslmode='require')
        cursor = connection.cursor()

        try:
            cursor.execute(sql, args)
            connection.commit()
            result["result"] = cursor.fetchall()
        except Exception as e:
            logging.error(e)
            result["error"] = e
        
        connection.close()
        return result  