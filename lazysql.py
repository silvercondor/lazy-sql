class ConnectionNotFoundException(Exception):
    pass


class LazySql:
    def __init__(self, connector, uri, logger=None):
        self.connector = connector  # DB connector i.e psycopg2, sqlite3
        self.uri = uri
        self.conn = None
        if logger:
            self.logger = logger
        else:
            self.logger = None

    def query(self, query, data=None, commit=False):
        """
        Used for ephemeral operations
        Connection is closed after executing query
        """
        try:
            with self.connector.connect(self.uri) as conn:
                cur = conn.cursor()
                if not data:
                    cur.execute(f"{query}")
                else:
                    cur.execute(f"{query}", data)
                if not commit:
                    rows = cur.fetchall()
                    if not rows:
                        return rows
                    col_names = [c[0] for c in cur.description]
                    return [dict(zip(col_names, r)) for r in rows]
                else:
                    conn.commit()
                return True
        except Exception as e:
            logmsg = 'LazySql query Exception'
            print(f'{logmsg} {e}')
            if self.logger:
                self.logger.exception(f'{logmsg}')
            return False

    def batch(self, query, data=None, commit=False, close=False):
        """
        Used for write operations

        Db connection is manually handled
        commit will commit and close the connection
        close will close without committing
        """
        try:
            if all([close, commit]):
                raise ValueError('Choose commit or close')
            else:
                if not self.conn:
                    # Opens connection if not exist
                    self.conn = self.connector.connect(self.uri)
                    self.cur = self.conn.cursor()
                if query:
                    if not data:
                        self.cur.execute(f"{query}")
                    else:
                        self.cur.execute(f"{query}", data)
                if commit:
                    self.conn.commit()
                    close = True
                if close:
                    self.conn.close()
                    self.conn = None
                    self.cur = None
                return True
        except Exception as e:
            logmsg = 'LazySql batch Exception'
            print(f'{logmsg} {e}')
            if self.logger:
                self.logger.exception(f'{logmsg}')
            return False

    def commit(self):
        if self.conn:
            self.conn.commit()
            self.conn.close()
            return True
        raise ConnectionNotFoundException('DB connection not found')

    def close(self):
        if self.conn:
            self.conn.close()
            return True
        raise ConnectionNotFoundException('DB connection not found')

    def rollback(self):
        if self.conn:
            self.conn.rollback()
        raise ConnectionNotFoundException('DB connection not found')
