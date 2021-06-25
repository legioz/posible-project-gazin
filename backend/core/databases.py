import mariadb
from core.config import config


class Connection:
    def __init__(self, name='database'):
        try:
            if name == 'database':
                self._conn = mariadb.connect(
                    host=config.get('MARIADB_HOST', None),
                    user=config.get('MARIADB_USER', None),
                    passwd=config.get('MARIADB_PASS', None),
                    db=config.get('MARIADB_DB', None),
                )
                self._cursor = self._conn.cursor()
            else:
                raise Exception()
        except Exception as e:
            print('\nDatabase connection error!\n')

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection(self):
        return self._conn

    @property
    def cursor(self):
        return self._cursor

    def commit(self):
        self.connection.commit()

    def close(self, commit=True):
        if commit:
            self.commit()
        self.connection.close()

    def execute(self, sql, params=None):
        self.cursor.execute(sql, params or ())

    def executemany(self, sql, params=None):
        self.cursor.executemany(sql, params or ())

    def fetchall(self):
        return self.cursor.fetchall()

    def fetchone(self):
        return self.cursor.fetchone()

    def dictfetchall(self):
        columns = [col[0] for col in self.cursor.description]
        return [
            dict(zip(columns, row))
            for row in self.cursor.fetchall()
        ]

    def query_list(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.fetchall()

    def query_dict(self, sql, params=None):
        self.cursor.execute(sql, params or ())
        return self.dictfetchall()
