# Persistence Layer

Esta capa administra la conexión SQLite y la persistencia inicial. MySQL se incorporará en una etapa posterior.

## Archivos

- `database.py`: abre conexiones SQLite, activa claves foráneas y crea el esquema.
- `schema.sql`: define las tablas `CUSTOMERS`, `DESTINATIONS`, `PACKAGES`, `PACKAGE_DESTINATIONS` y `RESERVATIONS`.
- `seed.py`: inserta datos ficticios de demostración relacionados entre sí.

## Crear la base de datos y cargar la semilla

Desde la raíz del proyecto, ejecutar:

```bash
python -m src.persistence.seed
```

El comando crea automáticamente la carpeta `data/`, la base `viajes_aventura.db`, las tablas y los datos. Se puede ejecutar varias veces: `INSERT OR IGNORE` evita duplicar los registros de demostración.

La semilla incluye 10 clientes, 10 destinos, 10 paquetes, 20 relaciones entre paquetes y destinos, y 10 reservas. Las contraseñas de demostración se guardan como hashes PBKDF2-SHA256 con sal aleatoria, no como texto plano. La clave compartida para pruebas locales es `Demo1234!`.

Para usar otra ruta, definir la variable de entorno `DB_PATH` antes de ejecutar el comando. La base de datos local no debe subirse al repositorio.
