import sqlite3

class DB:
    def __init__(self, path="data.db"):
        self.conn = sqlite3.connect(path)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()

    def run(self, query, params=()):
        self.cur.execute(query, params)
        self.conn.commit()

    def get(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchone()

    def all(self, query, params=()):
        self.cur.execute(query, params)
        return self.cur.fetchall()

    def close(self):
        self.conn.close()


