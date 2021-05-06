import sqlite3
import os


class DatabasePathNotDefined(Exception):
    pass


class DatabasePathNotFound(Exception):
    pass


class MigrationPathNotFound(Exception):
    pass


class Database:
    def __init__(self, app=None, db_path=None):
        if app and not db_path:
            path = app.config.get("DATABASE_PATH", None)
            if path is None:
                raise DatabasePathNotFound("`DATABASE_PATH` was not found.")
        else:
            if db_path:
                path = db_path
            else:
                raise DatabasePathNotDefined(
                    "`db_path` was not passed as an argument to the function.")

        self.app = app
        self.conn = sqlite3.connect(
            path,
            isolation_level=None,
        )

    def run_migrations(self, schema):
        if not os.path.exists(schema):
            raise MigrationPathNotFound(
                f"`{schema}` was not found in your filesystem.")

        with open(schema, 'r') as f:
            sql = f.read()

        self.conn.executescript(sql)


class Table:
    def __init__(self, db):
        self.db = db

    def query(self, q, args=None):
        if self.db.app:
            if self.db.app.config.get("DEBUG"):
                print(f"[DB] Running query: `{q=}` with `{args=}`.")

        if args:
            return self.db.conn.execute(q, args)
        else:
            return self.db.conn.execute(q)
