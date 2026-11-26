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
    def __init__(
        self, engine: Optional[str] = None, sqlite_path: Optional[str] = None
    ) -> None:
        self.engine = (engine or os.getenv("DB_ENGINE", "sqlite")).strip().lower()
        self.sqlite_path = sqlite_path or os.getenv(
            "SQLITE_DB_PATH", "viajes_aventura.db"
        )
        self.mysql_charset = os.getenv("MYSQL_CHARSET", "utf8mb4").strip()
        self.mysql_collation = os.getenv(
            "MYSQL_COLLATION", "utf8mb4_unicode_ci"
        ).strip()

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
                charset=self.mysql_charset,
                collation=self.mysql_collation,
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
                raw_lines = [
                    line
                    for line in schema_file.read_text(encoding="utf-8").splitlines()
                    if not line.strip().startswith("--")
                ]
                sql_script = "\n".join(raw_lines)
                for statement in sql_script.split(";"):
                    cleaned = statement.strip()
                    if not cleaned:
                        continue
                    upper_stmt = cleaned.upper()
                    if upper_stmt.startswith(("CREATE DATABASE", "USE ", "SET NAMES")):
                        continue
                    cursor.execute(cleaned)
            conn.commit()
        finally:
            conn.close()
