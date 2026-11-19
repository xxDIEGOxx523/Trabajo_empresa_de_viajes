"""Configuración y conexiones para SQLite o MySQL."""
from __future__ import annotations

import os
import re
import sqlite3
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[2]

try:
    from dotenv import load_dotenv
    load_dotenv(PROJECT_ROOT / ".env")
except ImportError:
    pass


def obtener_motor() -> str:
    motor = os.getenv("DB_BACKEND", "sqlite").strip().lower()
    if motor not in {"sqlite", "mysql"}:
        raise ValueError("DB_BACKEND debe ser 'sqlite' o 'mysql'.")
    return motor


def obtener_configuracion() -> dict:
    return {
        "backend": obtener_motor(),
        "path": os.getenv("DB_PATH", "./data/viajes_aventura.db"),
        "host": os.getenv("DB_HOST", "localhost"),
        "port": int(os.getenv("DB_PORT", "3306")),
        "user": os.getenv("DB_USER", "root"),
        "password": os.getenv("DB_PASSWORD", ""),
        "database": os.getenv("DB_NAME", "viajes_aventura"),
    }


def _mysql_connector():
    try:
        import mysql.connector
        return mysql.connector
    except ImportError as error:
        raise RuntimeError(
            "Falta mysql-connector-python. Ejecute: python -m pip install -r requirements.txt"
        ) from error


class MySQLConnectionAdapter:
    """Expone placeholders '?' para compartir consultas con SQLite."""
    def __init__(self, connection):
        self.connection = connection

    @staticmethod
    def _adapt(sql: str) -> str:
        return sql.replace("?", "%s")

    def execute(self, sql, params=()):
        cursor = self.connection.cursor()
        cursor.execute(self._adapt(sql), params)
        return cursor

    def executemany(self, sql, params):
        cursor = self.connection.cursor()
        cursor.executemany(self._adapt(sql), params)
        return cursor

    def commit(self):
        self.connection.commit()

    def rollback(self):
        self.connection.rollback()

    def close(self):
        self.connection.close()


def abrir_conexion_servidor():
    """Conecta al servidor MySQL sin seleccionar una base de datos."""
    config = obtener_configuracion()
    if config["backend"] != "mysql":
        raise RuntimeError("La conexión al servidor solo está disponible para MySQL.")
    connector = _mysql_connector()
    return connector.connect(
        host=config["host"], port=config["port"], user=config["user"],
        password=config["password"], charset="utf8mb4",
    )


def abrir_conexion():
    config = obtener_configuracion()
    if config["backend"] == "sqlite":
        configured_path = config["path"]
        path = Path(configured_path)
        if not path.is_absolute() and configured_path != ":memory:":
            path = PROJECT_ROOT / path
        if str(path) != ":memory:":
            path.parent.mkdir(parents=True, exist_ok=True)
        connection = sqlite3.connect(str(path))
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        return connection

    connector = _mysql_connector()
    return MySQLConnectionAdapter(connector.connect(
        host=config["host"], port=config["port"], user=config["user"],
        password=config["password"], database=config["database"], charset="utf8mb4",
    ))


def es_nombre_bd_valido(nombre: str) -> bool:
    return bool(re.fullmatch(r"[A-Za-z0-9_]+", nombre or ""))
