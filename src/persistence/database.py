import os
import sqlite3
from pathlib import Path
from typing import Optional

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass


class DatabaseConnection:
    def __init__(self, engine: Optional[str] = None, sqlite_path: Optional[str] = None) -> None:
        self.engine = (engine or os.getenv("DB_ENGINE", "sqlite")).strip().lower()
        self.sqlite_path = sqlite_path or os.getenv("SQLITE_DB_PATH", "viajes_aventura.db")

    def get_connection(self):
        if self.engine == "sqlite":
            conn = sqlite3.connect(self.sqlite_path)
            conn.row_factory = sqlite3.Row
            conn.execute("PRAGMA foreign_keys = ON;")
            return conn

        if self.engine == "mysql":
            import mysql.connector

            return mysql.connector.connect(
                host=os.getenv("MYSQL_HOST", "localhost"),
                port=int(os.getenv("MYSQL_PORT", "3306")),
                user=os.getenv("MYSQL_USER", "root"),
                password=os.getenv("MYSQL_PASSWORD", ""),
                database=os.getenv("MYSQL_DATABASE", "viajes_aventura"),
                collation="utf8mb4_unicode_ci"
            )

        raise ValueError(f"Unsupported database engine: {self.engine}")

    def get_placeholder(self) -> str:
        return "?" if self.engine == "sqlite" else "%s"

    def initialize_schema(self) -> None:
        schema_dir = Path(__file__).resolve().parent
        conn = self.get_connection()
        try:
            cursor = conn.cursor()
            if self.engine == "sqlite":
                schema_file = schema_dir / "schema_sqlite.sql"
                sql_script = schema_file.read_text(encoding="utf-8")
                cursor.executescript(sql_script)
            else:
                schema_file = schema_dir / "schema_mysql.sql"
                sql_script = schema_file.read_text(encoding="utf-8")
                for statement in sql_script.split(";"):
                    cleaned = statement.strip()
                    if cleaned and not cleaned.upper().startswith(("CREATE DATABASE", "USE ")):
                        cursor.execute(cleaned)
            conn.commit()
        finally:
            conn.close()
