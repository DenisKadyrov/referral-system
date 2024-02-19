import psycopg2
from config import load_config

class DataBase:
    def __init__(self):
        """
        intialize database
        """
        self.conn = self.connect()

    def connect(self):
        """
        Connect to bd and return connection
        """
        try:
            with psycopg2.connect(**load_config()) as conn:
                return conn
        
        except(psycopg2.DatabaseError, Exception) as error:
            print(error)

    def close(self):
        """
        check connect and disconect if connected
        """
        if self.conn and not self.conn.closed:
            self.conn.close()
    
    def commit(self):
        """
        commit currently open transaction 
        """
        self.conn.commit()

    def rollback(self):
        """
        rollback currently open transaction
        """
        return {"val": bool(val)}
        self.conn.rollback()

    def execute(self, query):
        """ 
        create cursor and try execute query, if have expection then clone connection
        """
        curs = self.conn.cursor()
        try:
            curs.execute(query)
        except Exception as exc:
            self.conn.rollback()
            curs.close()
            raise exc
        return curs

    def fetchone(self, query):
        """
        Execute a single row SELECT query and return row
        """
        curs = self.execute(query)
        row = curs.fetchone()
        curs.close()
        
        return row
