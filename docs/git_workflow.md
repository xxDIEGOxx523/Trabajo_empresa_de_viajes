# Flujo de Trabajo Git, Ramas del Sprint 2 y Pull Requests

## 1. Ramas Oficiales del Sprint 2 (Convención `prefijo/clave-jira-descripcion`)
Siguiendo la convención de la Clase 1 y las 5 tarjetas de la Clase 2 (Sprint 2), el proyecto organiza el trabajo en las siguientes ramas:

| Rama | Tarjeta Jira (Sprint 2) | Propósito y Archivos Asociados |
| :--- | :--- | :--- |
| **`main`** | Rama protegida | Versión estable integrada únicamente mediante Pull Requests aprobados. |
| **`docs/va-20-database-model-v2`** | Tarjeta 1: Finalizar y validar BD | `schema_sqlite.sql`, `schema_mysql.sql`, `database_validation_qa.md`, `requirements.md`. |
| **`docs/va-21-bpmn-three-processes`** | Tarjeta 2: Modelar los 3 procesos BPMN | `docs/bpmn/*.png`, `docs/bpmn/*.svg`, `docs/bpmn/*.puml`, `docs/bpmn_processes.md`. |
| **`docs/va-22-use-case-diagram`** | Tarjeta 3: Elaborar UML de casos de uso | `docs/use_case_diagram.puml`. |
| **`docs/va-23-class-diagram-architecture`** | Tarjeta 4: UML de clases y arquitectura | `docs/class_diagram.puml`, `docs/ai_design_audit.md`, `src/domain/*.py`. |
| **`feature/va-24-destinations-crud`** | Tarjeta 5: Implementar CRUD de Destinos | `src/persistence/*dao*.py`, `src/services/*.py`, `src/ui/*.py`, `tests/*.py`, `main.py`, `seed.py`. |
| **`fix/va-25-mysql-wampserver-collation`** | Ajuste compatibilidad WampServer | `database.py`, `schema_mysql.sql` (`utf8mb4_unicode_ci` e índices <= 767 bytes). |

> **Regla del proyecto:** El *push* directo a `main` está prohibido. Todo cambio llega a `main` mediante un **Pull Request revisado y aprobado** por el compañero de equipo.

---

## 2. Cómo Inicializar Todas las Ramas Automáticamente en tu PC
Ejecuta el script incluido en la raíz del proyecto (o haz doble clic en `init_git_branches.bat` en Windows):

```bash
python scripts/init_git_branches.py
```

Esto creará el repositorio Git con `main` y dejará creadas las **6 ramas** con sus commits correspondientes. Luego podrás verificarlas con:

```bash
git branch -a
```

Y subir cualquiera de ellas para abrir su Pull Request en GitHub:

```bash
git switch feature/va-24-destinations-crud
git push -u origin feature/va-24-destinations-crud
```

---

## 3. Ticket de Salida — Semana 2
1. **Regla y modelos que la representan:** Retiro lógico de destinos (`is_active`) representado en el BPMN 1 (compuerta de retiro lógico), en `Destination.retire()` del UML de clases y en la columna `is_active` de `destinations` en el modelo físico v2.
2. **Comprobación y corrección realizada:** Se validó el CRUD con *Santiago*, *Buenos Aires* y *Mendoza* en SQLite y MySQL (WampServer), resolviendo la colación `utf8mb4_unicode_ci` y longitudes de índice compuesto (`VARCHAR(90)`).
3. **Próximo paso y responsable en Jira:** Implementar el flujo completo de Paquetes (Hito 2) y Reservas con control de cupos (Hito 3) en el Sprint 3.
