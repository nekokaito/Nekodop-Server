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


db = DB()

# db.run("UPDATE cats SET is_approved = 1 WHERE id = '1f0582f4-616a-4558-88d9-7fb3baaec121'")
# db.run("UPDATE users SET user_role = 'admin' WHERE id = '5c509f37-fb90-4e1a-9dd5-473e43c0eb26'")