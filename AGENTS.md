# AGENTS.md

## Cursor Cloud specific instructions

### Repository layout
This repo contains two unrelated artifacts:
- `Dams-cli` (repo root, Go) — the primary product. A Cobra CLI that queries the status/level/volume of Catalan reservoirs (embassaments) from the public ACA REST API, prints results, optionally saves CSV, and optionally exposes the fetched data over a small embedded HTTP server.
- `ruta-camper-refugio-2026/` — standalone static travel docs (HTML/Markdown/KML) plus a Python 3 generator (`build_guia.py`). No backend; open the HTML in a browser. Not required for the CLI.

There are no automated tests, no Docker, and no databases. The Go module targets Go 1.14 but builds/runs fine on the installed newer Go toolchain.

### Standard commands (Dams-cli)
Run from the repo root. Commands are documented in `Readme.MD`.
- Lint/vet: `go vet ./...`
- Build: `go build ./...`
- Run: `go run ./cmd/dams-cli/main.go <sensor|rio|values> [flags]` (e.g. `sensor -a`, `rio -r ll`, `values -a`)
- Embedded HTTP server: append `-e <endpoint_name>` to any subcommand; it binds hardcoded `:8080` and serves the fetched data as JSON at `http://localhost:8080/<endpoint_name>` (blocks via `log.Fatal`).
- CSV export: append `-s <name>`. Note a pre-existing quirk: `SaveSensorValuesToCSV` appends `.csv` even when the name already ends in `.csv`, so `-s foo.csv` writes `foo.csv.csv`.

### IMPORTANT: upstream API is retired (non-obvious)
The app's hardcoded endpoint `http://aca-web.gencat.cat/sdim2/apirest/...` no longer serves JSON — it now returns a `302` redirect to a "Sentilo domain change" HTML page, so live runs fail with `>> invalid character '<' looking for beginning of value`. This is an external change, not a bug in this repo; do not modify the app's URLs to "fix" it.

To exercise the real end-to-end pipeline without code changes, serve the repo's own bundled sample data over the exact host/path the app calls:
- The repo ships a full sample catalog at `data/package.json` (a JSON array with one object). The app wraps the raw HTTP body in `[ ]` itself, so the mock must return the **bare object** (strip the outer array brackets). The `values` endpoint expects `{"sensors":[{"sensor","observations":[{"value","timestamp"}]}]}` (also bare).
- Add a hosts override `127.0.0.1 aca-web.gencat.cat` and run a local HTTP server on port 80 that serves `data/package.json` (bracket-stripped) at `/sdim2/apirest/catalog` and a values payload at `/sdim2/apirest/data/EMBASSAMENT-EST`. A ready-to-use mock lives at `/tmp/mock_aca/mock_aca.py` during setup (not committed); recreate it if missing. Only the `values` subcommand needs the values endpoint; `sensor` and `rio` need only the catalog endpoint.
