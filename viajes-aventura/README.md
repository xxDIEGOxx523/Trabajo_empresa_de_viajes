# Viajes Aventura

Proyecto académico TI3021 - Programación Orientada a Objeto Seguro.

## Estructura

- `docs/`: documentación, requerimientos y modelos.
- `src/presentation/`: interfaz con el usuario.
- `src/business/`: lógica de negocio y modelos.
- `src/persistence/`: conexión, esquema SQL y datos de prueba.
- `tests/`: pruebas.

## Preparación

1. Instalar Python 3.
2. Crear un entorno virtual: `python -m venv .venv`
3. Activar el entorno virtual.
4. Instalar dependencias: `python -m pip install -r requirements.txt` (la semilla usa la biblioteca estándar de Python, por lo que no requiere paquetes externos).

## Crear la base de datos y cargar datos ficticios

Desde la carpeta raíz del proyecto, ejecutar:

```bash
python -m src.persistence.seed
```

El programa crea `data/viajes_aventura.db`, genera las tablas y carga los datos relacionados. La semilla contiene:

| Tabla | Datos insertados |
|---|---:|
| `CUSTOMERS` | 10 clientes |
| `DESTINATIONS` | 10 destinos |
| `PACKAGES` | 10 paquetes |
| `PACKAGE_DESTINATIONS` | 20 relaciones entre paquetes y destinos |
| `RESERVATIONS` | 10 reservas |

La operación se puede repetir sin duplicar los registros iniciales. Para probar el acceso de los clientes, la clave compartida es `Demo1234!`; se almacena como hash PBKDF2-SHA256 con sal aleatoria. Estas credenciales son exclusivamente para pruebas locales y deben reemplazarse antes de cualquier uso real.

La base de datos se guarda dentro de `data/` y está excluida de Git. Para cambiar su ubicación, se puede definir la variable de entorno `DB_PATH`.

## Ejecución

```bash
python src/main.py
```

La implementación inicial de persistencia usa SQLite. MySQL se incorporará posteriormente.

## Flujo Git

No realizar push directo a `main`. Trabajar en ramas y abrir Pull Requests para revisión.


## Configuración de base de datos

El proyecto permite seleccionar SQLite o MySQL mediante `DB_BACKEND` en el archivo `.env`.

### SQLite (predeterminado)

```env
DB_BACKEND=sqlite
DB_PATH=./data/viajes_aventura.db
```

### MySQL

1. Crear la base de datos en MySQL:

```sql
CREATE DATABASE viajes_aventura CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

2. En `.env`, configurar:

```env
DB_BACKEND=mysql
DB_HOST=localhost
DB_PORT=3306
DB_USER=root
DB_PASSWORD=tu_clave
DB_NAME=viajes_aventura
```

3. Instalar dependencias:

```bash
pip install -r requirements.txt
```

4. Ejecutar la semilla (el esquema se crea automáticamente):

```bash
python -m src.persistence.seed
```

La misma semilla funciona con ambos motores. En SQLite utiliza `INSERT OR IGNORE` y en MySQL `INSERT IGNORE`, por lo que puede ejecutarse nuevamente sin duplicar los registros de IDs existentes.
