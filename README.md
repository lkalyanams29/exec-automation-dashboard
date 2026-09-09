# QEI Knowledge Intelligence

An enterprise Quality Engineering knowledge-assistant POC that correlates authorized evidence from Jira, Confluence, SharePoint, Bitbucket, Slack, Katalon assets, and TestOps. The working surface demonstrates project-aware Ask QE and Mentor modes, evidence-level citations, authority and freshness signals, traceability, confidence, safe fallback, and a Week 2 evaluation suite.

The included corpus is representative demo evidence. Production connectors, identity mapping, permission synchronization, embeddings/vector storage, and live LLM generation remain deployment integrations; the UI never presents the Week 2 quality targets as measured results.

## Week 2 architecture

1. Query intelligence identifies project, ticket, intent, and access scope.
2. Hybrid retrieval combines semantic, keyword/BM25, exact identifier, and metadata filters.
3. Graph lookup follows requirement → implementation → automation → execution.
4. Reranking considers project fit, authority, freshness, and graph relationships.
5. Evidence validation checks permissions, conflicts, missing sources, and stale context.
6. Response generation returns a status, confidence, citations, and an explicit evidence boundary.

## Evidence authority

- Level 5: approved requirements, specifications, designs, and QE standards.
- Level 4: current merged source, Katalon automation, and contracts.
- Level 3: TestOps results, build execution, and review findings.
- Level 2: comments, Slack discussions, and supporting project notes.
- Level 1: old or superseded information.
- Level 0: AI inference, which can explain evidence but never becomes evidence.

## Previous dashboard foundation

The repository also retains the Katalon TestOps automation-management data pipeline and CSV corpus assets developed in Week 1.

An executive-first automation portfolio dashboard with a React/Vinext frontend and reusable Python ingestion and metrics layers. The UI uses representative data so it is immediately reviewable; connect credentials and validate TestOps response shapes before enabling live synchronization.

The initial dashboard dataset is `sources/katalon_testops_sample_dataset.csv`. Its 2,063 rows are summarized in `app/sample-data.ts`, and the dashboard defaults to the latest 30-day execution window ending on the maximum date in that file.

## Included

- Executive KPIs, period comparisons, automation growth, execution trends, result distribution, project performance, stability indicators and management summary
- Project drill-down interaction, responsive and print/PDF-friendly layout, date presets and manual refresh
- Config-driven projects and configurable health/flakiness/growth thresholds in `config/projects.yaml`
- Defensive TestOps client with pagination, retry/backoff, rate-limit handling and response-shape discovery
- Normalized SQLite schema with daily snapshots, duplicate-safe keys, failure categorization and a PostgreSQL-friendly repository boundary
- Equivalent hosted D1 schema plus unit tests for core metric definitions
- Monthly CSV import with required-column validation, automatic metric recalculation, durable import history and latest-import loading

## Setup

1. Copy `.env.example` to `.env`; add `KATALON_API_KEY`, `KATALON_ACCOUNT_ID` and `KATALON_ORG_ID`. Never commit `.env`.
2. Replace placeholder IDs in `config/projects.yaml`.
3. Run `npm install`, then `npm run dev`.
4. Create a Python environment, run `pip install -r requirements.txt`, then `pytest`.

## Monthly CSV import

Choose **Import CSV** in the dashboard and upload the next Katalon export. A file may contain only the new month or cumulative history, although cumulative history produces the most complete growth and comparison trends. Imports accept files up to 5 MB and require: `execution_id`, `run_id`, `project_name`, `test_case_id`, `test_case_created_at`, `execution_started_at`, `status`, and `duration_seconds`. Optional fields such as `is_flaky`, `repeat_failure_flag`, `failure_category`, `execution_week_start`, and `creation_week_start` enrich stability and failure reporting.

Successful imports are stored in the `csv_imports` analytics table with the original CSV and calculated summary. The most recent import becomes the dashboard source on subsequent visits; invalid files do not replace the active dataset.

## Phase 1 — connectivity and field discovery

Do not assume endpoint paths or envelopes. With the endpoint paths from your tenant's current Katalon API documentation, call `backend.katalon.discover.probe`. It prints field names and types—not credentials or full records. Confirm projects, test cases, executions and execution results before implementing tenant-specific field mapping.

## Metric rules

- Pass rate: `passed / (passed + failed) × 100`; skipped, incomplete and errors are excluded.
- Failure rate: `failed / (passed + failed) × 100`.
- Growth: tests created in the period; daily snapshot deltas are the fallback when creation dates are unavailable.
- Growth percent: `new tests / tests at start of period × 100`.
- POC flakiness: failed / pass+fail in the recent configured window, only when both outcomes occur and minimum executions are met.

Daily snapshots are the source for weekly/monthly comparisons. Execution IDs and `(execution_id, test_case_id)` result keys make repeated incremental syncs idempotent. Synchronization should overlap its watermark by the configured lookback to capture late updates.

## Architecture

`Katalon TestOps → Python client/collector → SQLite → metrics/API → React dashboard`

The integration, repository, calculations and UI are separate. Replace the repository to move from SQLite to PostgreSQL without changing collection or metric logic.

## Production checklist

- Complete response discovery and add fixture-based mapping tests for your tenant.
- Add a scheduled collector, structured JSON log configuration and sync health alerting.
- Store credentials in the deployment secret store, restrict dashboard access and configure backups.
- Wire analytics queries and server-side CSV/XLSX generation. The current Export action provides print-to-PDF and screenshot-ready output.
