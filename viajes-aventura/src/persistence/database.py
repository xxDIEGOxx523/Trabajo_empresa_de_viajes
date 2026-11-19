"""Conexión configurable para SQLite o MySQL."""
from __future__ import annotations

import os
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]
SQLITE_SCHEMA_PATH = Path(__file__).with_name("schema.sql")
MYSQL_SCHEMA_PATH = Path(__file__).with_name("schema_mysql.sql")


class MySQLConnectionAdapter:
    """Adaptador pequeño para mantener una API similar a sqlite3."""
    def __init__(self, connection):
        self.connection = connection

    def execute(self, sql, params=()):
        cursor = self.connection.cursor()
        cursor.execute(sql.replace("?", "%s"), params)
        return cursor

    def executemany(self, sql, params):
        cursor = self.connection.cursor()
        cursor.executemany(sql.replace("?", "%s"), params)
        return cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()


class Database:
    """Administra conexiones y creación de esquema según DB_BACKEND."""
    def __init__(self, db_path: str | None = None):
        self.backend = os.getenv("DB_BACKEND", "sqlite").strip().lower()
        if self.backend not in {"sqlite", "mysql"}:
            raise ValueError("DB_BACKEND debe ser 'sqlite' o 'mysql'.")
        configured_path = db_path or os.getenv("DB_PATH", "./data/viajes_aventura.db")
        path = Path(configured_path)
        self.db_path = path if path.is_absolute() or configured_path == ":memory:" else PROJECT_ROOT / path

    def connect(self):
        if self.backend == "sqlite":
            if str(self.db_path) != ":memory:":
                self.db_path.parent.mkdir(parents=True, exist_ok=True)
            connection = sqlite3.connect(str(self.db_path))
            connection.row_factory = sqlite3.Row
            connection.execute("PRAGMA foreign_keys = ON")
            return connection

        try:
            import mysql.connector
        except ImportError as error:
            raise RuntimeError("Falta mysql-connector-python. Instale las dependencias con pip install -r requirements.txt") from error

        connection = mysql.connector.connect(
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER", "root"),
            password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_NAME", "viajes_aventura"),
            charset="utf8mb4",
        )
        return MySQLConnectionAdapter(connection)

    def create_schema(self):
        schema_path = MYSQL_SCHEMA_PATH if self.backend == "mysql" else SQLITE_SCHEMA_PATH
        if not schema_path.is_file():
            raise FileNotFoundError(f"No se encontró el esquema SQL: {schema_path}")
        sql_script = schema_path.read_text(encoding="utf-8")
        connection = self.connect()
        try:
            if self.backend == "sqlite":
                connection.executescript(sql_script)
            else:
                cursor = connection.connection.cursor()
                for statement in (part.strip() for part in sql_script.split(";") if part.strip()):
                    cursor.execute(statement)
            connection.commit()
        finally:
            connection.close()
