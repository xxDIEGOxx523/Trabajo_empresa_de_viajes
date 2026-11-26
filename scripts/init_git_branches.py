import subprocess
import sys

SPRINT2_BRANCHES = [
    (
        "docs/va-20-database-model-v2",
        "docs(va-20): add physical database model v2 and 10 validation queries",
        [
            "src/persistence/schema_sqlite.sql",
            "src/persistence/schema_mysql.sql",
            "docs/database_validation_qa.md",
            "docs/requirements.md",
        ],
    ),
    (
        "docs/va-21-bpmn-three-processes",
        "docs(va-21): add 3 BPMN diagrams (PNG, SVG, PUML) for all functional milestones",
        [
            "docs/bpmn",
            "docs/bpmn_processes.md",
        ],
    ),
    (
        "docs/va-22-use-case-diagram",
        "docs(va-22): add integrated UML use case diagram for Admin and Client",
        [
            "docs/use_case_diagram.puml",
        ],
    ),
    (
        "docs/va-23-class-diagram-architecture",
        "docs(va-23): add integrated UML class diagram, AI audit and layered domain models",
        [
            "docs/class_diagram.puml",
            "docs/ai_design_audit.md",
            "src/domain",
        ],
    ),
    (
        "feature/va-24-destinations-crud",
        "feat(va-24): implement layered Destinations CRUD, Spanish UI, seed and tests",
        [
            "src/persistence/base_dao.py",
            "src/persistence/dao_factory.py",
            "src/persistence/destination_dao.py",
            "src/services",
            "src/ui",
            "tests",
            "main.py",
            "seed.py",
        ],
    ),
    (
        "fix/va-25-mysql-wampserver-collation",
        "fix(va-25): enforce utf8mb4_unicode_ci collation and 767-byte index compatibility for WampServer",
        [
            "src/persistence/database.py",
            "src/persistence/schema_mysql.sql",
            ".env.example",
            "docs/git_workflow.md",
            "README.md",
        ],
    ),
]


def run_git(*args: str, check: bool = True) -> subprocess.CompletedProcess:
    return subprocess.run(["git", *args], check=check, capture_output=True, text=True)


def main() -> None:
    try:
        run_git("--version")
    except FileNotFoundError:
        print("[Error] Git no está instalado o no está en el PATH del sistema.")
        sys.exit(1)

    print("1. Inicializando repositorio Git con rama principal 'main'...")
    run_git("init", "-b", "main")
    run_git("add", ".gitignore", ".env.example", "requirements.txt", "README.md")
    run_git("commit", "-m", "chore: initialize sprint 2 base repository structure")

    print("2. Creando ramas del Sprint 2 (una por tarjeta de Jira)...")
    for branch_name, commit_msg, paths in SPRINT2_BRANCHES:
        run_git("switch", "main")
        run_git("switch", "-c", branch_name)
        run_git("add", *paths)
        status = run_git("status", "--porcelain").stdout.strip()
        if status:
            run_git("commit", "-m", commit_msg)
        print(f"   [OK] Rama creada y con commit: {branch_name}")

    run_git("switch", "main")
    # Merge all feature/docs/fix branches cleanly or keep them ready for PRs
    print("\nRamas disponibles en tu repositorio local:")
    branches_out = run_git("branch", "-a").stdout
    print(branches_out)
    print(
        "Listo. Ahora puedes hacer 'git push -u origin <nombre-rama>' para abrir\n"
        "cada Pull Request hacia 'main' y enlazarlos en Jira."
    )


if __name__ == "__main__":
    main()
