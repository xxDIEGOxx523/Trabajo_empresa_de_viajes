# Viajes Aventura — Sprint 2 (Diseño Integrado, 3 BPMN, Ramas Git y CRUD de Destinos)

Solución completa de **Viajes Aventura** correspondiente al Sprint 2:
- **Tres diagramas BPMN visuales** (`.png` y `.svg`) + fuentes editables `.puml` en `docs/bpmn/`.
- **Ramas Git organizadas por tarjeta Jira** (`docs/git_workflow.md` y script automático `scripts/init_git_branches.py` / `init_git_branches.bat`).
- **Arquitectura por capas** con código 100% en inglés, interfaz navegable en español y compatibilidad verificada con **SQLite** y **MySQL / WampServer**.

## Estructura del Proyecto
```text
viajes_aventura_sprint2_v3/
├── docs/
│   ├── bpmn/
│   │   ├── bpmn_1_gestion_destinos.png (.svg / .puml)
│   │   ├── bpmn_2_preparacion_paquetes.png (.svg / .puml)
│   │   └── bpmn_3_reservas_seguimiento.png (.svg / .puml)
│   ├── ai_design_audit.md
│   ├── bpmn_processes.md
│   ├── class_diagram.puml
│   ├── database_validation_qa.md
│   ├── git_workflow.md
│   ├── requirements.md
│   └── use_case_diagram.puml
├── scripts/
│   └── init_git_branches.py
├── src/
│   ├── domain/
│   ├── persistence/
│   ├── services/
│   └── ui/
├── tests/
├── .env.example
├── .gitignore
├── init_git_branches.bat
├── main.py
├── requirements.txt
└── seed.py
```

## 1. Inicializar las Ramas Git del Sprint 2
Ejecuta una sola vez en la raíz del proyecto (o haz doble clic en `init_git_branches.bat` en Windows):
```bash
python scripts/init_git_branches.py
```
Esto crea `main` y las 6 ramas correspondientes a las tarjetas de Jira (`docs/va-20-database-model-v2`, `docs/va-21-bpmn-three-processes`, `docs/va-22-use-case-diagram`, `docs/va-23-class-diagram-architecture`, `feature/va-24-destinations-crud`, `fix/va-25-mysql-wampserver-collation`).

## 2. Preparación del Entorno y Ejecución
```bash
pip install -r requirements.txt
cp .env.example .env
python seed.py
python -m unittest discover -s tests -v
python main.py
```
