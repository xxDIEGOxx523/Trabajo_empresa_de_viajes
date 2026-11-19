"""Operaciones SQL comunes para los DAO del proyecto."""
from .conexion import abrir_conexion, obtener_motor
from .interfaces_dao import IBaseDAO


def _filas_a_diccionarios(cursor, filas):
    columnas = [columna[0] for columna in (cursor.description or [])]
    resultado = []
    for fila in filas:
        if hasattr(fila, "keys"):
            resultado.append(dict(fila))
        else:
            resultado.append(dict(zip(columnas, fila)))
    return resultado


class BaseDAO(IBaseDAO):
    TABLE = ""
    COLUMNS = ()

    def insertar_lote(self, registros):
        if not registros:
            return 0
        prefijo = "INSERT OR IGNORE" if obtener_motor() == "sqlite" else "INSERT IGNORE"
        columnas = ", ".join(self.COLUMNS)
        placeholders = ", ".join("?" for _ in self.COLUMNS)
        sql = f"{prefijo} INTO {self.TABLE} ({columnas}) VALUES ({placeholders})"
        conexion = abrir_conexion()
        try:
            cursor = conexion.executemany(sql, registros)
            conexion.commit()
            return cursor.rowcount
        except Exception:
            conexion.rollback()
            raise
        finally:
            conexion.close()

    def obtener_todos(self):
        conexion = abrir_conexion()
        try:
            cursor = conexion.execute(f"SELECT * FROM {self.TABLE} ORDER BY 1")
            return _filas_a_diccionarios(cursor, cursor.fetchall())
        finally:
            conexion.close()

    def contar(self):
        conexion = abrir_conexion()
        try:
            return conexion.execute(f"SELECT COUNT(*) FROM {self.TABLE}").fetchone()[0]
        finally:
            conexion.close()
