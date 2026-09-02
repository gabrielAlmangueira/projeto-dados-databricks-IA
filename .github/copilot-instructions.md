# Copilot instructions for this repository

## Project scope

This repository is centered on a Databricks Declarative Automation Bundles (DABs) project under `rotaperfume/`.

The important structure is:

- `rotaperfume/databricks.yml`: bundle root; defines the Databricks workspace host, targets (`dev`, `prod`), and bundle variables.
- `rotaperfume/resources/`: declarative Databricks jobs/pipelines/resources loaded by the bundle.
- `rotaperfume/src/`: Python modules for project logic. The package entry point is configured in `pyproject.toml` as `main = "rotaperfume.main:main"`.
- `rotaperfume/tests/`: pytest suite, which initializes Databricks Connect and Spark fixtures.
- `rotaperfume/fixtures/`: CSV/JSON fixture datasets used by tests.

## Build, test, and lint

Use the project root inside `rotaperfume/` for all local commands:

- Install/update dev dependencies:
  - `cd rotaperfume && uv sync --dev`
- Run the full test suite:
  - `cd rotaperfume && uv run pytest`
- Run a single file:
  - `cd rotaperfume && uv run pytest tests/test_file.py`
- Run one test by name:
  - `cd rotaperfume && uv run pytest tests/test_file.py -k "test_name"`
- Lint the project:
  - `cd rotaperfume && uv run ruff check .`

For deployment and Databricks bundle tasks:

- Deploy the dev bundle:
  - `cd rotaperfume && databricks bundle deploy --target dev`
- Deploy the prod bundle:
  - `cd rotaperfume && databricks bundle deploy --target prod`
- Run a configured job or pipeline from the bundle:
  - `cd rotaperfume && databricks bundle run`

## High-level architecture

This project is intentionally bundle-first, not ad-hoc script-first:

- The Databricks bundle is the source of truth for project deployment and environment configuration.
- `databricks.yml` defines workspace targets and variables that resources use.
- Resource definitions in `resources/*.yml` are the deployment layer for jobs and pipelines; keep resource names and target variables consistent when editing these files.
- Python code in `src/` is expected to be job/pipeline code and should stay modular, testable, and environment-agnostic.
- Tests are not plain unit tests; `tests/conftest.py` bootstraps Databricks Connect, creates a Spark session, and provides a fixture loader for JSON/CSV files under `fixtures/`.

## Key conventions and repo-specific patterns

- Prefer Databricks bundle workflows over manual workspace changes. This repo is designed for bundle-based deploys and target-aware environments.
- Use `uv` for package setup and test execution; project dependencies are declared in `pyproject.toml` and the dev environment is installed with `uv sync --dev`.
- Treat Databricks Connect as part of the local test setup. Local pytest runs may connect to Databricks and automatically fall back to serverless compute if no explicit cluster is configured.
- Keep code and bundle configuration aligned with the project naming already defined in `databricks.yml` (`rotaperfume`, `dev`, `prod`, and the catalog/schema variables).
- Keep tests under `tests/` and fixture data under `fixtures/`; they are expected to be consumed by the Spark fixture loader defined in `tests/conftest.py`.

## AI agent guidance already captured by project docs

The repository’s existing agent guidance (`rotaperfume/AGENTS.md` and `rotaperfume/CLAUDE.md`) points to Databricks AI tooling for reliable bundle work:

- Read the Databricks `databricks-core` skill before making project-specific changes when available.
- If needed, install Databricks AI tooling with:
  - `databricks aitools install`
- Keep authentication and bundle target selection aligned with the Databricks CLI setup for this project.

## When making changes

- Update bundle resource definitions and Python code together when a workflow change spans both layers.
- Preserve target naming and variable contracts in `databricks.yml`.
- Favor small, focused edits around the bundle or job logic being changed; this repo is lightweight and does not define a broad service architecture beyond the Databricks bundle structure.
