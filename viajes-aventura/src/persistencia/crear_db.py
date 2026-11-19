"""Creación del esquema según el motor seleccionado."""
from pathlib import Path

from .conexion import (
    PROJECT_ROOT, abrir_conexion, abrir_conexion_servidor,
    es_nombre_bd_valido, obtener_configuracion, obtener_motor,
)

PERSISTENCE_DIR = Path(__file__).resolve().parent


def _crear_base_mysql():
    config = obtener_configuracion()
    nombre = config["database"]
    if not es_nombre_bd_valido(nombre):
        raise ValueError("DB_NAME solo puede contener letras, números y guion bajo.")
    conexion = abrir_conexion_servidor()
    cursor = conexion.cursor()
    try:
        cursor.execute(
            f"CREATE DATABASE IF NOT EXISTS `{nombre}` "
            "CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci"
        )
        conexion.commit()
    finally:
        cursor.close()
        conexion.close()


def crear_base_y_tablas():
    motor = obtener_motor()
    if motor == "mysql":
        _crear_base_mysql()
        schema_path = PROJECT_ROOT / "viajes_aventura_mysql.sql"
    else:
        schema_path = PERSISTENCE_DIR / "viajes_aventura_sqlite.sql"

    if not schema_path.is_file():
        raise FileNotFoundError(f"No se encontró el esquema: {schema_path}")

    script = schema_path.read_text(encoding="utf-8")
    conexion = abrir_conexion()
    try:
        # Los dos esquemas contienen sentencias separadas por ';' sin rutinas almacenadas.
        for sentencia in (parte.strip() for parte in script.split(";") if parte.strip()):
            conexion.execute(sentencia)
        conexion.commit()
    except Exception:
        conexion.rollback()
        raise
    finally:
        conexion.close()
