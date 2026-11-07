from contextlib import contextmanager
from pathlib import Path
import sqlite3


class SQLiteConnector:
    def __init__(self, db_path=None):
        self.db_path = Path(db_path) if db_path else (
            Path(__file__).resolve().parents[2] / "wendo.db"
        )

    @contextmanager
    def connection(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        try:
            yield conn
            conn.commit()
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def fetch_all(self, query, params=()):
        with self.connection() as conn:
            return conn.execute(query, params).fetchall()

    def execute(self, query, params=()):
        with self.connection() as conn:
            cursor = conn.execute(query, params)
            return cursor.lastrowid