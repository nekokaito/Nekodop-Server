import os
import sqlite3

class DB:
    def __init__(self, path=None):
        if path is None:
            base_dir = os.path.dirname(os.path.abspath(__file__))
            path = os.path.join(base_dir, "data.db")
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        
    # run a query
    def run(self, query, params=()):
        self.cur.execute(query, params)
        self.conn.commit()

    # get a single row
    def get(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchone()
    
     # get all rows
    def all(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchall()
