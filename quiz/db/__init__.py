import inspect
import sqlite3
import os


class DatabasePathNotDefined(Exception):
    pass


class DatabaseMigrationPathNotFound(Exception):
    pass


class DatabaseTableObjectDoesNotSubclass(Exception):
    pass


class DatabaseTableWasNotInitedProperly(Exception):
    pass


class Database:
    def __init__(self, app=None, path="", debug=False):
        if app:
            self.path = app.config.get("DATABASE_PATH", None)
            if self.path is None:
                raise DatabasePathNotDefined("`DATABASE_PATH` was not found.")

            self.debug = app.config.get("DEBUG", False)

        else:
            if not path:
                raise DatabasePathNotDefined(
                    "`path` was not passed as an argument to the function.")

            self.debug = debug
            self.path = path

        self.objects = {}

    @property
    def conn(self):
        return sqlite3.connect(self.path, isolation_level=None)

    def run_migrations(self, schema):
        if not os.path.exists(schema):
            raise DatabaseMigrationPathNotFound(
                f"`{schema}` was not found in your filesystem.")

        with open(schema, "r") as f:
            sql = f.read()

        self.conn.executescript(sql)

    def register(self, _class):
        if not inspect.isclass(_class) or not issubclass(_class, Table):
            raise DatabaseTableObjectDoesNotSubclass(
                "The specified object does not subclass from `Table`.")

        default_args = [
            None for _ in range(_class.__init__.__code__.co_argcount - 2)
        ].__add__([self])

        self.objects[_class.__name__.lower()] = _class(*default_args)

    def get(self, object_name):
        return self.objects.get(object_name.lower(), None)


class Table:
    def __init__(self, db):
        self.db = db

    @property
    def debug(self):
        return self.db.debug

    def query(self, q, args=None):
        if not self.db:
            raise DatabaseTableWasNotInitedProperly(
                "Please register the Table before trying to use it.")

        if self.debug:
            print(f"[DB] Running query: `{q=}` with `{args=}`.")

        if args:
            return self.db.conn.execute(q, args)

        else:
            return self.db.conn.execute(q)
