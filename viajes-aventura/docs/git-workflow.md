# Flujo de ramas y Pull Requests

## Regla
No hacer push directo a `main`. Todo cambio debe integrarse mediante Pull Request revisado y aprobado.

## Convención
`<prefix>/<jira-key>-<description>`

Ejemplos:
- `docs/VA-12-requirements`
- `feature/VA-18-create-reservation`
- `fix/VA-21-validate-dates`

## Flujo
1. Crear una rama desde `main`.
2. Realizar cambios y commits.
3. Publicar la rama.
4. Abrir PR hacia `main`.
5. Solicitar revisión a un compañero.
6. Corregir observaciones.
7. Integrar PR aprobado.
8. Enlazar evidencia y PR en Jira.
