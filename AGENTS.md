# Repository Guidelines

## Project Structure
```
src/<feature>/
tests/<feature>/test_<unit>.py
assets/
docs/
```

## Build Commands
No build tooling configured yet. When added, use one entrypoint:
- `make setup` / `npm install`
- `make test` / `npm test`
- `make lint` / `npm run lint`
- `make dev`

## Coding Style
- Indentation: 4 spaces (Python) or 2 spaces (JS/TS)
- Naming: `snake_case` (Python), `camelCase` (JS/TS), `PascalCase` (classes)

## Testing
- Mirror `tests/` paths to `src/`
- Name tests as `test_<behavior>`

## Commit Format
`type(scope): short summary` (e.g., `feat(auth): add token refresh`)

## Security
Never commit secrets. Use `.env` and commit only `.env.example`.