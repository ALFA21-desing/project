"""
Database - Simple MySQL helper for the project

Provides a thin wrapper around ``mysql.connector`` that makes it easy
for automation scripts or the backend to grab a connection and execute
queries. Credentials default to common local settings but may be
overridden via environment variables.
"""

import os
import mysql.connector
from mysql.connector import Error


class Database:
    """Helper class that manages a MySQL connection.

    The constructor will open a connection immediately; call ``close()``
    when finished. A cursor configured with ``dictionary=True`` is
    available as ``self.cursor`` so rows behave like Python dicts.
    """

    def __init__(
        self,
        host: str | None = None,
        port: int | None = None,
        user: str | None = None,
        password: str | None = None,
        database: str | None = None,
    ):
        # read environment variables as fallback
        host = host or os.getenv("DB_HOST", "localhost")
        port = port or int(os.getenv("DB_PORT", "3306"))
        user = user or os.getenv("DB_USER", "root")
        password = password or os.getenv("DB_PASSWORD", "")
        database = database or os.getenv("DB_NAME", "jewelry_store_db")

        try:
            self.conn = mysql.connector.connect(
                host=host,
                port=port,
                user=user,
                password=password,
                database=database,
                autocommit=False,
            )
            self.cursor = self.conn.cursor(dictionary=True)
        except Error as e:
            raise RuntimeError(f"Failed to connect to database: {e}")

    def execute(self, query: str, params: tuple | list | None = None):
        """Execute a statement and return the cursor.

        ``params`` may be a sequence of values to bind to the query
        (parameterized style uses ``%s`` placeholders).
        """
        self.cursor.execute(query, params or ())
        return self.cursor

    def fetchall(self):
        """Convenience wrapper around ``cursor.fetchall()``."""
        return self.cursor.fetchall()

    def fetchone(self):
        """Convenience wrapper for ``cursor.fetchone()``."""
        return self.cursor.fetchone()

    def commit(self):
        """Commit the current transaction."""
        self.conn.commit()

    def rollback(self):
        """Rollback the current transaction."""
        self.conn.rollback()

    def close(self):
        """Close cursor and connection cleanly."""
        try:
            self.cursor.close()
        except Exception:
            pass
        try:
            self.conn.close()
        except Exception:
            pass


# module convenience function

def get_db(**kwargs) -> Database:
    """Return a new :class:`Database` instance using defaults or overrides."""
    return Database(**kwargs)
