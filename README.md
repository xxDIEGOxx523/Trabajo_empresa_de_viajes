▒▒▒▒▒▒▒▓
▒▒▒▒▒▒▒▓▓▓
▒▓▓▓▓▓▓░░░▓
▒▓░░░░▓░░░░▓
▓░░░░░░▓░▓░▓
▓░░░░░░▓░░░▓
▓░░▓░░░▓▓▓▓
▒▓░░░░▓▒▒▒▒▓
▒▒▓▓▓▓▒▒▒▒▒▓
▒▒▒▒▒▒▒▒▓▓▓▓
▒▒▒▒▒▓▓▓▒▒▒▒▓
▒▒▒▒▓▒▒▒▒▒▒▒▒▓
▒▒▒▓▒▒▒▒▒▒▒▒▒▓
▒▒▓▒▒▒▒▒▒▒▒▒▒▒▓
▒▓▒▓▒▒▒▒▒▒▒▒▒▓
▒▓▒▓▓▓▓▓▓▓▓▓▓
▒▓▒▒▒▒▒▒▒▓
▒▒▓▒▒▒▒▒▓

# Viajes Aventura — Sprint 2 (Diseño Integrado y CRUD de Destinos)

Proyecto desarrollado con arquitectura por capas, código Python y SQL **100% en inglés** e interfaz de usuario interactiva **en español**, compatible con **SQLite** y **MySQL**.

## Estructura del Proyecto
```text
viajes_aventura_sprint2/
├── docs/
│   ├── bpmn_processes.md
│   ├── class_diagram.puml
│   ├── database_validation_qa.md
│   └── use_case_diagram.puml
├── src/
│   ├── domain/
│   │   ├── destination.py
│   │   └── models.py
│   ├── persistence/
│   │   ├── database.py
│   │   ├── destination_dao.py
│   │   ├── schema_mysql.sql
│   │   └── schema_sqlite.sql
│   ├── services/
│   │   └── destination_service.py
│   └── ui/
│       └── console_ui.py
├── tests/
│   └── test_destination_crud.py
├── .env.example
├── .gitignore
├── main.py
├── requirements.txt
└── seed.py
```

## Preparación del Entorno
1. Crear entorno virtual e instalar dependencias:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate
   # Linux/Mac: source .venv/bin/activate
   pip install -r requirements.txt
   ```
2. Crear el archivo `.env` local a partir de `.env.example`:
   ```bash
   cp .env.example .env
   ```

## Ejecución con SQLite (por defecto)
1. Asegúrate de tener `DB_ENGINE=sqlite` en `.env`.
2. Carga los 3 destinos de ejemplo (Santiago, Buenos Aires, Mendoza):
   ```bash
   python seed.py
   ```
3. Inicia la interfaz interactiva:
   ```bash
   python main.py
   ```

## Ejecución con MySQL
1. Ejecuta `src/persistence/schema_mysql.sql` en tu servidor MySQL (o crea la base `viajes_aventura`).
2. Cambia en tu `.env` local:
   ```env
   DB_ENGINE=mysql
   MYSQL_HOST=localhost
   MYSQL_PORT=3306
   MYSQL_USER=tu_usuario
   MYSQL_PASSWORD=tu_clave
   MYSQL_DATABASE=viajes_aventura
   ```
3. Ejecuta `python seed.py` y luego `python main.py`.

## Pruebas Automatizadas
```bash
python -m unittest discover -s tests -v
```
