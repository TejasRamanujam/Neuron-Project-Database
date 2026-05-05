from database import SessionLocal, engine, Base
from models import Project

Base.metadata.create_all(bind=engine)

P = []

def a(title, subtitle, desc, problem, stack, archs, libs, diff, build, uis, repos, gap, features, outcomes, tags):
    P.append(dict(title=title, subtitle=subtitle, description=desc, problem_statement=problem,
                  tech_stack=stack, architectures_used=archs, libraries_used=libs, difficulty=diff,
                  build_plan=build, ui_components=uis, repo_inspiration=repos, resume_gap_filled=gap,
                  key_features=features, learning_outcomes=outcomes, tags=tags))

# ============================================================
# BUILD PLANS (each is a detailed markdown string)
# ============================================================

BP = {}

BP["AI Code Review Pipeline"] = """\
## Phase 1: Project Foundation
**Step 1: Scaffold the monorepo.** Create a project root with `backend/` (Python 3.11+, FastAPI) and `frontend/` (React 18 + TypeScript + Vite). Initialize Git, set up `.env`, `docker-compose.yml` with PostgreSQL 16 and Redis 7 services, and a `Makefile` with common commands.

**Step 2: Build the database layer.** Define SQLAlchemy models: `Repository` (id, owner, name, webhook_secret), `PullRequest` (id, repo_id, pr_number, title, status, diff_text), `ReviewResult` (pr_id, risk_score, issues JSON). Use Alembic for migrations. Seed with sample PR data from public repos.

**Step 3: Set up Celery + Redis.** Configure Celery with Redis as broker. Create `tasks.py` with a base `ReviewTask` class that accepts a PR diff, runs analysis, and stores results. Set result backend to PostgreSQL.

## Phase 2: ML-Powered Code Analysis
**Step 4: Train XGBoost risk classifier.** Collect labeled bug-introducing commit data from public datasets (e.g., BugsJS, Defects4J). Extract features: lines changed, file types, cyclomatic complexity delta, author experience, time-of-day, keywords in commit message. Train an XGBoost classifier (precision-recall optimized). Serialize with `joblib` and bundle as `models/risk_model.pkl`.

**Step 5: Build the static analysis pipeline.** Create modular analyzers in `analyzers/`: `SecurityAnalyzer` (regex patterns for SQL injection, XSS, credential leaks), `StyleAnalyzer` (wraps ESLint/PyLint output), `PerformanceAnalyzer` (detects N+1 queries, O(n²) loops). Each analyzer yields `Issue` objects with severity, file, line, message.

**Step 6: Implement GitHub App webhooks.** Use FastAPI to receive `pull_request.opened` and `pull_request.synchronize` events. Verify HMAC signature. Dispatch the diff to Celery task `analyze_pr`. Return a pending status to GitHub immediately (commit status "pending").

## Phase 3: Frontend — Dashboard & Review UI
**Step 7: Build the diff viewer component.** Install `react-diff-view` and `react-syntax-highlighter`. Create `DiffViewer.tsx` that takes unified diff text, renders split or unified view, and highlights added/removed lines. Overlay annotation markers where issues were found.

**Step 8: Create the dashboard.** Use Recharts for trend charts: risk score over time, issue breakdown by category, PR volume per developer. Build filterable `PRTable` with columns: PR title, repo, risk score (color-coded), status, date. Clicking a row opens the detail view.

**Step 9: Build the rule configuration UI.** Create `RuleEditor.tsx` with a form to enable/disable specific analyzers, set severity thresholds, and define custom regex patterns. Store config as JSON in the backend and sync on save.

## Phase 4: Integration & Deployment
**Step 10: Wire up the pipeline.** Webhook → FastAPI → Celery → analyze → store → notify. Create a polling endpoint `/api/pr/{id}/status` that the frontend uses to check analysis progress. Use React Query for auto-refetch.

**Step 11: Add GitHub commit status updates.** After analysis completes, update the PR commit status: "success" (risk < threshold) or "failure" (risk > threshold) with a link to the detailed report. Use Octokit REST API.

**Step 12: Dockerize everything.** Write multi-stage Dockerfile for the backend. Use `docker-compose.yml` to wire up PostgreSQL, Redis, Celery worker, FastAPI app, and Nginx reverse proxy for the frontend build output.

**Step 13: Add CI/CD.** Create GitHub Actions workflow: lint, type-check, test (pytest with coverage), build Docker images, deploy to a single VM (or fly.io/render) using docker-compose."""

BP["Real-Time Collaborative Whiteboard"] = """\
## Phase 1: Foundation
**Step 1: Set up the project.** Create a FastAPI backend with WebSocket support and a React + TypeScript + Vite frontend. Use `docker-compose.yml` with PostgreSQL 16 and Redis 7. Set up SQLAlchemy models for `Board`, `Session`, `Stroke`, `User`.

**Step 2: Design the CRDT data model.** Implement a Conflict-Free Replicated Data Type for vector strokes. Each stroke is a sequence of points with an ID, user_id, timestamp, and a "deleted" tombstone flag. Use a Last-Writer-Wins register for stroke properties (color, width, tool). The CRDT ensures concurrent edits converge without conflicts.

**Step 3: Build the WebSocket server.** Use FastAPI's `WebSocket` endpoint at `/ws/{board_id}`. On connect, load the full board state from PostgreSQL and send it as an initial snapshot. Maintain a dict of connected clients per board. On disconnect, clean up and broadcast user leave.

## Phase 2: Real-Time Drawing Engine
**Step 4: Implement canvas rendering.** Use HTML5 Canvas with a React ref. On `mousedown` / `touchstart`, begin a stroke. On `mousemove`, buffer points. On `mouseup`, finalize the stroke and broadcast via WebSocket. Use `requestAnimationFrame` for smooth rendering. Implement `perfect-freehand` for realistic brush strokes.

**Step 5: Implement the state synchronization protocol.** When a stroke is created, send a JSON message `{type: "stroke_add", stroke: {...}}`. Remote peers apply the stroke to their local CRDT and re-render. Support `stroke_update` (for freehand editing), `stroke_delete` (tombstone), and `board_clear`. Handle reconnection by sending the full snapshot from the server.

**Step 6: Build the UI toolbar.** Create a floating toolbar with tool buttons: pen, highlighter, text, rectangle, ellipse, line, arrow, eraser. Add color picker (custom palette + hex input) and stroke width slider. Style with CSS modules and Framer Motion for smooth transitions.

## Phase 3: Advanced Features
**Step 7: Implement presence and cursors.** Broadcast cursor position on `mousemove` (throttled to 50ms). Render other users' cursors as colored dots with name labels. Show user avatars in a sidebar presence list using the WebSocket `presence` channel.

**Step 8: Build session recording and replay.** On the server, append every operation to an append-only `events` table. Implement a replay endpoint that returns the event log. Build a timeline scrubber UI (`SessionTimeline.tsx`) with play/pause and speed control. Replay by re-applying events at the original cadence to a fresh canvas.

**Step 9: Add export functionality.** Implement server-side rendering of the board state to SVG and PNG using `canvas.toDataURL()` on the client (for PNG) and a hand-written SVG serializer (for vector). For PDF, use `pdfkit` on the server to compose a PDF with the rendered SVG.

## Phase 4: Polish
**Step 10: Add undo/redo with branching.** Store each operation in a history stack. Undo = apply inverse operation. Support branching: if the user undoes and then draws, the undone operations become a separate branch (stored but hidden). Show a branch explorer UI.

**Step 11: Dockerize and deploy.** Multi-stage Dockerfiles for frontend (Nginx) and backend (uvicorn). Use Caddy as a reverse proxy with automatic HTTPS. Deploy with `docker compose up -d` on a VPS.

**Step 12: Add image import.** Let users paste or drag-drop images onto the canvas. The frontend uploads the image to the backend via `/api/board/{id}/image` (multipart). The backend stores it, returns a URL, and broadcasts the image placement to other clients."""

BP["ML Model Registry & A/B Testing Platform"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** Create FastAPI backend with SQLAlchemy + PostgreSQL, and React + TypeScript + Vite frontend. Dockerize with docker-compose. Set up Alembic for migrations. Create MLflow tracking server as a separate docker-compose service.

**Step 2: Design the data model.** Define SQLAlchemy models: `Model` (id, name, version, mlflow_run_id, status, tags JSON, created_at), `Deployment` (id, model_id, environment, deployment_type [shadow/canary/prod], config JSON), `ABTest` (id, name, control_model_id, treatment_model_id, traffic_split, start_date, end_date, status, metrics JSON), `MetricEvent` (id, model_id, timestamp, metric_name, metric_value, labels JSON).

**Step 3: Build the MLflow integration.** Create `mlflow_service.py` that wraps the MLflow Tracking API. Implement functions: `log_model(model, run_id)`, `load_model(model_uri)`, `list_models()`, `get_model_version(run_id)`. Store the MLflow run URI in the Model record.

## Phase 2: Core API
**Step 4: Build the Model Registry API.** Full CRUD for models. POST `/api/models` (register with metadata), GET `/api/models` (list with filter/sort), GET `/api/models/{id}` (detail with version history), POST `/api/models/{id}/promote` (promote staging→prod). Each route validates status transitions.

**Step 5: Build the Deployment API.** POST `/api/deployments` creates a deployment. Implement `deployment_service.py` that spawns a FastAPI sub-application for each active deployment (using FastAPI mounted apps pattern) or uses a model server pattern. Support three modes: `shadow` (deploy alongside current, log comparisons), `canary` (x% traffic), `prod` (100%).

**Step 6: Build the A/B Test Engine.** POST `/api/ab-tests` creates a test. Implement `ab_test_service.py` that: (1) assigns users to control/treatment via deterministic hashing, (2) routes inference requests accordingly, (3) collects metrics (latency, accuracy, business KPIs), (4) computes statistical significance using chi-squared or t-test. End a test automatically when significance is reached.

## Phase 3: Frontend
**Step 7: Build the model registry browser.** Create `ModelRegistry.tsx` with a table view (name, version, status badge, date). Click to expand detail: tags, MLflow link, deployment history. Add a "Register New Model" form with file upload and metadata inputs.

**Step 8: Build the A/B test configurator.** Create `ABTestWizard.tsx` as a multi-step form: Step 1 (select control + treatment models), Step 2 (set traffic split % and metrics to track), Step 3 (review and launch). Use React Hook Form for validation.

**Step 9: Build the metrics dashboard.** Use Recharts for real-time metric comparison charts: latency percentile comparison, accuracy over time, error rate. Build `MetricCard.tsx` components with sparklines. Show statistical significance badges (p-value).

## Phase 4: Advanced Features
**Step 10: Implement automated rollback.** Create a `HealthMonitor` background task (runs every 30s) that checks key metrics for canary deployments. If any metric degrades beyond threshold (e.g., error rate > 5% increase), auto-rollback: revert traffic to control model and send Slack/email alert.

**Step 11: Add the inference proxy.** Build `/api/inference/{model_id}` endpoint that loads the model, runs prediction, and returns results. For shadow deployments, run both models and log comparison without affecting the response. Cache models in memory (LRU cache) and reload when deployments change.

**Step 12: Dockerize everything.** docker-compose with: FastAPI app, Celery worker for async training, MLflow server (with PostgreSQL backend + S3 artifact store), PostgreSQL, Redis, and the frontend (Nginx). Add health checks."""

BP["Distributed Task Orchestrator & Monitor"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend, React + TypeScript + Vite frontend, docker-compose with PostgreSQL 16, Redis 7. Python 3.11+. Set up Celery 5.3 with Redis as broker and PostgreSQL as result backend using `django-celery-results`-style custom backend (SQLAlchemy-based).

**Step 2: Design the data model.** `Workflow` (id, name, definition JSON, version), `Task` (id, workflow_id, parent_id, name, status, queue, args JSON, kwargs JSON, result JSON, started_at, completed_at, retry_count, max_retries), `WorkerHeartbeat` (worker_id, hostname, last_heartbeat, active_tasks, queue_names), `TaskEvent` (id, task_id, event_type, timestamp, metadata JSON).

**Step 3: Implement the DAG parser.** Build `dag_parser.py` that reads a YAML workflow definition and resolves the DAG structure. Each node has: id, depends_on (list), task_type, args, retry_policy. Validate no cycles using topological sort. Serialize as a directed graph using NetworkX for analysis.

## Phase 2: Core Task Engine
**Step 4: Build the Celery integration layer.** Create `celery_app.py` with custom task base class that: (1) records start/end timestamps, (2) captures exceptions with full tracebacks, (3) sends real-time events via Redis pub/sub. Register tasks dynamically from YAML definitions using `@app.task(bind=True)`.

**Step 5: Implement the DAG executor.** Build `dag_executor.py`. When a workflow is triggered, the executor: (1) finds all ready nodes (no uncompleted dependencies), (2) dispatches them as Celery tasks in parallel, (3) listens for completion events, (4) when a task completes, checks if downstream tasks are now ready, (5) dispatches those. Use a state machine with states: PENDING, RUNNING, COMPLETED, FAILED, RETRYING, SKIPPED, TIMEOUT.

**Step 6: Implement retry policies.** Each task can define retry_policy: `max_retries`, `min_delay`, `max_delay`, `backoff_multiplier`, `retry_on` (list of exception types). Build `retry_service.py` that schedules retries with exponential backoff + jitter. Use Celery's `retry()` mechanism.

## Phase 3: Real-Time Monitoring
**Step 7: Build the WebSocket monitoring layer.** Use FastAPI WebSocket at `/ws/monitor`. The server subscribes to Redis pub/sub channel `task_events` and forwards all events to connected admin clients. Events: `task_started`, `task_completed`, `task_failed`, `task_retrying`, `worker_heartbeat`, `queue_depth_changed`.

**Step 8: Build the live task stream UI.** Create `TaskStream.tsx` using a virtualized list (react-window) that renders task events in real-time with color-coded status badges. Add filters: by workflow, by status, by worker. Click a task to expand inline detail (args, result, traceback).

**Step 9: Build the DAG visual editor.** Use React Flow to create an interactive DAG editor (`DAGEditor.tsx`). Nodes are draggable task boxes. Edges represent dependencies. Side panel shows task configuration (type, args, retry policy). Export as YAML.

**Step 10: Build the worker pool dashboard.** Create `WorkerDashboard.tsx` with cards for each worker showing: hostname, active tasks, queue membership, last heartbeat (with "alive" indicator). Use Recharts for queue depth time-series graphs.

## Phase 4: Integration
**Step 11: Add notifications.** Implement `notification_service.py` with channels: Slack (webhook), email (SMTP), webhook (POST to URL). Configurable per workflow. Trigger on: task failure, retry exceeded, workflow completion.

**Step 12: Dockerize.** docker-compose with: FastAPI, Celery worker (multiple replicas with different queue names), Celery beat (scheduler), Redis, PostgreSQL, frontend."""

BP["Personal Finance Intelligence Engine"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend. Use docker-compose for PostgreSQL and Redis. Set up Plaid API credentials (sandbox environment).

**Step 2: Design the data model.** `Account` (id, plaid_access_token, plaid_item_id, name, type, balance_available, balance_current), `Transaction` (id, account_id, plaid_transaction_id, amount, date, merchant_name, category, predicted_category, is_anomaly), `Budget` (id, name, category, amount, period, spent), `Goal` (id, name, target_amount, current_amount, deadline), `Forecast` (id, date, predicted_balance, confidence_interval_low, confidence_interval_high).

**Step 3: Integrate Plaid.** Build `plaid_service.py` using `plaid-python`. Implement: `create_link_token()` (generates a Plaid Link token for frontend), `exchange_public_token(public_token)` (exchanges for access token, stores in Account), `sync_transactions(account)` (uses Plaid's `/transactions/sync` endpoint for incremental updates), `get_accounts(item_id)`.

## Phase 2: ML Pipeline
**Step 4: Build the transaction categorizer.** Collect labeled transaction data (use Plaid's category field as ground truth, or use public datasets like the Bank Account Fraud dataset). Extract features: merchant name (TF-IDF), amount, day-of-week, merchant category code. Train a LightGBM classifier with 30+ categories. Achieve >85% accuracy. Serialize with `joblib`.

**Step 5: Build the spending forecaster.** Use XGBoost for time-series forecasting on daily spending aggregates. Features: day-of-week, day-of-month, month, previous 7-day rolling average, previous 30-day rolling average. Forecast 30 days ahead with prediction intervals (use quantile regression or bootstrap). Store forecasts in the Forecast table.

**Step 6: Implement anomaly detection.** Build `anomaly_detector.py` using Isolation Forest from scikit-learn. Features per transaction: amount (z-score relative to merchant history), frequency (transactions with same merchant in last 7 days), time-of-day, location distance from home. Flag transactions with anomaly score > threshold. Show in UI with explanation.

## Phase 3: Frontend
**Step 7: Build the main dashboard.** `Dashboard.tsx` with: (1) balance cards (checking, savings, total net worth) using Framer Motion for number animations, (2) spending breakdown pie chart (Recharts `PieChart` with interactive legend), (3) recent transactions feed with ML-predicted category icons, (4) budget progress rings for top 4 categories.

**Step 8: Build the transaction feed.** `TransactionList.tsx` with infinite scroll (react-query + pagination API). Each row shows: merchant logo (generated from name), amount (red/green for debit/credit), category badge, anomaly indicator. Pull-to-refresh for mobile. Search by merchant name and filter by category, date range, amount range.

**Step 9: Build the budget and goal trackers.** `BudgetManager.tsx`: add budgets by category, set period (weekly/monthly), track progress with ring charts. `GoalTracker.tsx`: create goals with name, target, deadline; show progress bar and projected completion date based on ML forecast.

## Phase 4: Integration & Polish
**Step 10: Build the Plaid Link flow.** Use Plaid Link (CDN script) in the frontend. User clicks "Connect Account" → Link opens → user authenticates at their bank → Link returns a public_token → frontend sends to backend → backend exchanges for access_token.

**Step 11: Add real-time updates.** Use Celery beat to run `sync_all_accounts` every 6 hours. After sync, re-run categorization and anomaly detection. If anomaly found, push notification to the frontend via WebSocket.

**Step 12: Dockerize and deploy.** docker-compose with FastAPI, Celery beat, Celery worker, PostgreSQL, Redis, and frontend."""

BP["Semantic Document Search & QA Platform"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL (with pgvector extension), React + TypeScript + Vite frontend. Dockerize with docker-compose. Use `pgvector` for vector storage.

**Step 2: Design the data model.** `Document` (id, title, file_type, file_size, upload_date, status, user_id), `DocumentChunk` (id, document_id, chunk_index, content TEXT, embedding vector(1536)), `Collection` (id, name, description, user_id), `CollectionDocument` (collection_id, document_id), `Conversation` (id, document_id, user_id, created_at), `Message` (id, conversation_id, role, content, citations JSON).

**Step 3: Build the document parsing pipeline.** Create `parsers/` directory with modular parsers: `PDFParser` (using `unstructured` library for PDF, falls back to `PyMuPDF`), `DOCXParser` (using `python-docx`), `HTMLParser` (using `trafilatura` or `beautifulsoup4`). Each parser extracts text with page/section metadata. Use Celery for async parsing with progress tracking.

## Phase 2: RAG Engine
**Step 4: Build the chunking and embedding pipeline.** After parsing, split text into chunks (512 tokens with 64 token overlap) using LangChain's `RecursiveCharacterTextSplitter`. Generate embeddings using OpenAI's `text-embedding-3-small` model (or Gemini embedding API). Store chunks with embeddings in the Chunks table. Batch process with Celery.

**Step 5: Build the vector search endpoint.** POST `/api/search` accepts a query and optional collection/filter params. Generate query embedding using the same model. Perform hybrid search: vector similarity (cosine distance via pgvector `<=>` operator) + keyword search (PostgreSQL `ts_vector`). Combine results using Reciprocal Rank Fusion (RRF). Return top 10 chunks with scores.

**Step 6: Build the QA endpoint.** POST `/api/ask` takes a query and conversation history. Perform search (Step 5), format results as context, call OpenAI Chat Completions (or Gemini) with a system prompt that instructs the model to answer based ONLY on the provided context, with inline citations `[1]`, `[2]`, etc. Return answer + citations + source chunks.

## Phase 3: Frontend
**Step 7: Build the document management UI.** `DocumentManager.tsx`: upload area (drag-and-drop with `react-dropzone`), document list (table with name, type, date, status badge), batch actions (delete, move to collection). Upload progress bar using axios `onUploadProgress`.

**Step 8: Build the chat interface.** `ChatInterface.tsx` with: message list (user and assistant bubbles), input area with send button and file attachment, streaming responses using Server-Sent Events (SSE). Each assistant message shows citation cards: clickable source snippets that open the document preview at the relevant section.

**Step 9: Build the search results UI.** `SearchResults.tsx`: relevance-highlighted snippets (using `react-highlight-words`), filter sidebar (by collection, date range, file type), sort by relevance/date. Preview panel on the right: embedded document viewer (PDF.js for PDFs, markdown renderer for text).

## Phase 4: Advanced Features
**Step 10: Add access control.** Implement user-based access control: only the document owner can search/query against their documents. Use SQLAlchemy relationship filters. Add sharing: users can share documents or collections with view/comment/edit permissions.

**Step 11: Add LLM provider abstraction.** Build `llm_service.py` with an abstract base class `LLMProvider`. Implement `OpenAIProvider` and `GeminiProvider`. Allow the user to select their preferred provider in settings. Store API keys encrypted using `cryptography.fernet`.

**Step 12: Dockerize.** docker-compose with: FastAPI (with Celery worker), PostgreSQL (with pgvector extension pre-installed), Redis, and frontend. Add health checks and volume mounts for uploads."""

BP["IoT Sensor Data Lake & Alerting System"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend, React + TypeScript + Vite frontend, docker-compose with TimescaleDB (PostgreSQL 16 + TimescaleDB 2.x), Redis 7, and Mosquitto MQTT broker.

**Step 2: Design the data model.** Use TimescaleDB hypertables for time-series data. `Sensor` (id, name, location, sensor_type, metadata JSON), `SensorReading` (time TIMESTAMPTZ, sensor_id INT, value FLOAT, unit VARCHAR - hypertable partitioned by time), `Device` (id, name, mqtt_topic, sensor_ids JSON, last_heartbeat), `Alert` (id, sensor_id, rule_id, triggered_at, resolved_at, severity, message), `AlertRule` (id, name, sensor_id, condition_type [threshold/anomaly], config JSON, enabled).

**Step 3: Set up MQTT ingestion.** Use `paho-mqtt` to create an MQTT client service that subscribes to sensor topics (`sensors/{device_id}/+/reading`). On message received, parse JSON payload, batch insert into TimescaleDB using `psycopg2.extras.execute_values`. Use Redis as a buffer queue during high throughput.

## Phase 2: Real-Time Processing
**Step 4: Build the streaming analytics engine.** Use a Celery-based consumer that reads from Redis stream in batches. Apply windowed aggregations: 5-minute moving average, min/max, rate-of-change. Store pre-computed aggregates in a materialized hypertable. Implement continuous aggregates using TimescaleDB's built-in `CREATE MATERIALIZED VIEW` with `timescaledb.continuous`.

**Step 5: Train anomaly detection models.** For each sensor type, train: (1) Isolation Forest for point anomalies, (2) LSTM autoencoder (TensorFlow/Keras) for pattern anomalies (sequence of 24 readings). Serialize models and load on startup. Score each incoming batch. Flag readings with anomaly score > threshold.

**Step 6: Build the alert engine.** `alert_engine.py`: (1) evaluates each AlertRule against incoming data, (2) supports threshold (value > X), rate-of-change (delta > Y per minute), anomaly (score > Z), (3) deduplicates (same alert not re-fired within cooldown period), (4) triggers channels: email (SMTP), SMS (Twilio API), Webhook (POST to URL).

## Phase 3: Frontend
**Step 7: Build the real-time dashboard.** `SensorDashboard.tsx` using WebSocket connection for live updates. Grid of gauge widgets: each shows current value, 5-min trend sparkline, status indicator (normal/warning/critical). Use `react-gauge-chart` for analog-style gauges. Auto-arrange with `react-grid-layout`.

**Step 8: Build the time-series explorer.** `TimeSeriesExplorer.tsx`: date range picker, sensor selector overlay, zoomable chart using Recharts `LineChart` with `Brush` for timeline navigation. Overlay anomaly points in red. Toggle between raw values and aggregated views.

**Step 9: Build the alert rule builder.** `AlertRuleBuilder.tsx`: step form - (1) select sensor, (2) select condition type (threshold / rate-of-change / anomaly), (3) configure threshold value or sensitivity, (4) select notification channels, (5) set cooldown period. Preview simulated alerts on sample data.

## Phase 4: Integration
**Step 10: Add the device registry.** CRUD for sensors and devices. Show device health status (based on heartbeat timing) in a table view. Map view using Leaflet/Mapbox for sensor locations.

**Step 11: Dockerize.** docker-compose with: FastAPI (with Celery worker), TimescaleDB, Redis, Mosquitto, and frontend. Add `init.sql` script to create hypertables and continuous aggregates on first startup."""

BP["API Gateway & Developer Portal"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, Redis 7 for rate limiting. Dockerize with docker-compose. Use Traefik as the edge reverse proxy.

**Step 2: Design the data model.** `Developer` (id, name, email, password_hash, company, tier [free/pro/enterprise]), `ApiKey` (id, developer_id, key_hash, prefix, name, permissions JSON, expires_at, last_used_at), `ApiEndpoint` (id, path, method, description, rate_limit_config JSON), `UsageRecord` (id, api_key_id, endpoint_id, timestamp, response_time_ms, status_code), `Webhook` (id, developer_id, url, events JSON, secret, active), `RateLimitBucket` (key_hash, endpoint_pattern, window_start, count).

**Step 3: Build authentication.** Implement API key authentication middleware: extract key from `X-API-Key` header, hash it, look up in DB, check expiry, check rate limit, attach developer context to request. Use `passlib` with bcrypt for key hashing.

## Phase 2: Gateway Core
**Step 4: Build the rate limiter.** Implement two algorithms: (1) Token Bucket (for per-key limits), (2) Sliding Window (for per-endpoint limits). Use Redis sorted sets for sliding window: `ZREMRANGEBYSCORE` + `ZADD` + `ZCARD` pattern. Return `X-RateLimit-Limit`, `X-RateLimit-Remaining`, `X-RateLimit-Reset` headers.

**Step 5: Build the reverse proxy engine.** Create `proxy_service.py` using `httpx.AsyncClient`. When a request hits the gateway, the middleware: (1) authenticates, (2) checks rate limit, (3) transforms request (add headers, rewrite path), (4) proxies to upstream service, (5) transforms response, (6) logs usage. Use FastAPI's `mount` or catch-all route for proxying.

**Step 6: Build request/response transformation.** Implement transformer functions: `add_header(name, value)`, `remove_header(name)`, `rewrite_path(pattern, replacement)`, `add_query_param(name, value)`, `transform_body(jq_filter)`. Store transformations per endpoint in the APIEndpoint config. Apply in order during proxy pass-through.

## Phase 3: Developer Portal
**Step 7: Build the developer signup flow.** Registration form with email verification (JWT-based confirmation link). Login with session cookies (httpOnly, secure). Dashboard after login: overview of API usage, key management, recent activity.

**Step 8: Build the API key management UI.** `ApiKeyManager.tsx`: list of keys with prefix, name, status, last used, expiry. Create new key: opens modal with name, permissions checkboxes, tier selector. On creation, show the full key once with a warning. Revoke/re-enable keys. Regenerate.

**Step 9: Build the interactive API explorer.** `ApiExplorer.tsx`: (1) loads OpenAPI spec from the backend, (2) renders endpoint list grouped by tag, (3) click endpoint → expand with parameter inputs, authentication selector, "Try It" button, (4) sends request through a CORS proxy endpoint, (5) shows response with syntax highlighting.

**Step 10: Build the usage analytics dashboard.** `AnalyticsDashboard.tsx`: time-series chart of request volume (Recharts), latency percentiles (p50/p95/p99), error rate, top endpoints by usage. Date range picker. Data source: aggregate queries on UsageRecords table.

## Phase 4: Advanced Features
**Step 11: Add webhook management.** `WebhookManager.tsx`: create webhook (URL, events to subscribe to, secret), list sent deliveries (status, response code, body), retry failed deliveries. Backend: `webhook_service.py` sends events via Celery, with exponential backoff on failure.

**Step 12: Dockerize and deploy.** docker-compose with: FastAPI gateway (multiple replicas behind Traefik), PostgreSQL, Redis, and the frontend."""

BP["Social Media OSINT Analyzer"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL + Neo4j (graph database), React + TypeScript + Vite frontend. Dockerize with docker-compose including Neo4j 5.x.

**Step 2: Design the data model.** PostgreSQL tables: `Investigation` (id, name, description, created_at, status), `Username` (id, investigation_id, username, platform, profile_data JSON, checked_at, status). Neo4j nodes: `:Account` (username, platform, display_name, avatar_url, profile_url), `:ProfileField` (type, value). Neo4j relationships: `:SAME_AS` (between accounts on different platforms), `:MENTIONS` (between accounts), `:LOCATED_IN` (to location).

**Step 3: Build the async scraping framework.** Create `scrapers/` directory with a base `SiteScraper` abstract class: `async check(username) → Profile | None`, `async extract(url) → ProfileData`. Implement site-specific scrapers using `httpx.AsyncClient` with connection pooling and retry logic. Use Playwright as a fallback for JavaScript-heavy sites (Instagram, TikTok, etc.).

## Phase 2: Core Search Engine
**Step 4: Build the site adapter system.** Each site is defined in a YAML config file: `sites.yaml` entries with `name`, `url_pattern`, `check_method` (http/playwright), `extraction_selectors` (CSS selectors for profile data). The `SiteRegistry` loads all adapters on startup. Support 30+ high-value sites initially.

**Step 5: Implement the multi-search engine.** POST `/api/search` accepts a username + optional platform filters. The engine: (1) loads enabled site adapters, (2) runs checks in parallel using `asyncio.gather` with a semaphore (10 concurrent), (3) collects results, (4) inserts into Neo4j graph, (5) returns results as a stream via Server-Sent Events. Handle rate limiting with per-domain delay.

**Step 6: Build recursive search.** If a found profile contains other usernames (e.g., Twitter bio mentions Instagram handle), queue them for recursive search. Configurable depth limit. Use Neo4j to track visited usernames and avoid infinite loops.

## Phase 3: Frontend
**Step 7: Build the search dashboard.** `SearchDashboard.tsx`: multi-username input (textarea, one per line), platform filter checkboxes, "Start Search" button with progress indicator (animated bar showing sites checked / total). Real-time results stream using EventSource (SSE).

**Step 8: Build the graph visualization.** Use D3.js force-directed graph (`react-d3-graph` or custom `d3-force`). Nodes are accounts (sized by platform importance), edges are `SAME_AS` relationships. Color nodes by platform. Click a node → expand with profile details. Drag, zoom, pan. Search bar to highlight nodes.

**Step 9: Build the profile detail panel.** `ProfileDetail.tsx`: slides out from the right. Shows: avatar, username, platform, profile URL, extracted fields (name, bio, location, follower count). Buttons to open profile in browser, add note, tag as relevant/irrelevant. Timeline of recent posts (if extractable).

**Step 10: Build the report generator.** `ReportGenerator.tsx`: user selects an investigation, picks output format (PDF/HTML/CSV/JSON). Backend generates the report using Jinja2 templates (for HTML/PDF) or direct CSV/JSON serialization. PDF generation with `pdfkit` (wkhtmltopdf wrapper). Report includes: summary, account table, relationship graph (as static image via D3 export), timeline.

## Phase 4: Integration
**Step 11: Dockerize.** docker-compose with: FastAPI (with Celery worker for heavy scraping), PostgreSQL, Neo4j 5.x, Redis, and frontend. The browser exposes Neo4j Browser on port 7474 for direct graph exploration."""

BP["Multi-Agent AI Workflow Engine"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, Celery + Redis for async execution. Dockerize with docker-compose.

**Step 2: Design the data model.** `WorkflowDefinition` (id, name, description, yaml_definition TEXT, version, created_by), `WorkflowRun` (id, definition_id, status, triggered_by, started_at, completed_at, branch_name), `NodeExecution` (id, run_id, node_id, status, input JSON, output JSON, started_at, completed_at, attempts), `WorkflowTemplate` (id, name, description, yaml_definition TEXT, category, usage_count), `Conversation` (id, workflow_run_id, messages JSON).

**Step 3: Build the YAML workflow parser.** Implement `workflow_parser.py` that parses a YAML workflow definition into a DAG. Each node has: `id`, `depends_on` (list of node IDs), `type` (prompt/bash/loop/human), `prompt` (for AI nodes), `bash` (command for deterministic nodes), `loop` (loop config: `until`, `interactive`, `max_iterations`). Validate with Pydantic. Build adjacency list and topological ordering.

## Phase 2: Workflow Engine
**Step 4: Build the DAG executor.** `dag_executor.py`: (1) receives a WorkflowRun, (2) initializes a state dict (execution context), (3) starts worker threads for each ready node, (4) manages the dependency graph — when a node completes, check downstream dependencies, dispatch those that are now ready, (5) handles parallel execution with thread pool. Track state transitions in the NodeExecution table.

**Step 5: Implement node types.** `node_executors/`: `PromptNode` (calls OpenAI/Gemini API with context from previous nodes), `BashNode` (executes shell commands via `subprocess` in an isolated worktree), `LoopNode` (re-executes child nodes until `until` condition is met), `HumanApprovalNode` (pauses execution, sends notification, waits for user input via WebSocket). Each executor returns a `NodeResult` with stdout, stderr, and structured data.

**Step 6: Build the context management system.** Nodes share data through a context dict: `context["plan"]`, `context["code"]`, `context["test_results"]`, etc. Each node reads from and writes to this dict. The prompt template uses `{{context.plan}}`, `{{context.code}}` syntax. Use Jinja2 for template rendering.

## Phase 3: Frontend
**Step 7: Build the visual workflow editor.** `WorkflowEditor.tsx` using React Flow: (1) drag nodes from a palette (Prompt, Bash, Loop, Approval, etc.) onto the canvas, (2) connect nodes by dragging edges (directed), (3) click node → opens config panel (prompt text, bash command, retry settings), (4) Export as YAML and save as WorkflowDefinition.

**Step 8: Build the real-time execution view.** `ExecutionView.tsx`: (1) real-time node status updates via WebSocket, (2) nodes color-coded: gray (pending), blue (running), green (completed), red (failed), yellow (awaiting approval), (3) click a node → expand to see input, output, logs, timing, (4) timeline view showing execution sequence with durations.

**Step 9: Build the human approval interface.** `ApprovalPanel.tsx`: when a HumanApprovalNode is hit, (1) show a notification in the UI (and optionally via Slack/email), (2) present the current state (plan, diff, test results), (3) two buttons: Approve / Reject with optional comment, (4) on approve → workflow continues, on reject → node runs the "on_reject" path.

**Step 10: Build the workflow template library.** `TemplateLibrary.tsx`: grid of template cards (name, description, category, usage count). Click to preview the YAML. "Use Template" copies it as a new WorkflowDefinition. Pre-seed with 5 templates (feature development, bug fix, code review, PR creation, refactoring).

## Phase 4: Integration & Deployment
**Step 11: Dockerize.** docker-compose with: FastAPI (workflow engine), Celery worker pool (configurable count), PostgreSQL, Redis, frontend. Add health checks.

**Step 12: Add Slack integration.** Use Slack Bolt SDK. Users can trigger workflows from Slack: `/workflow-run feature-development`. Messages go through the same orchestrator, with results posted back to Slack."""

BP["Infrastructure Cost Optimizer"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, Celery + Redis for async data collection. Dockerize.

**Step 2: Design the data model.** `CloudAccount` (id, provider [aws/azure/gcp], credentials_encrypted, name, active, last_synced), `Resource` (id, account_id, provider_resource_id, resource_type, region, tags JSON, configuration JSON, hourly_cost, monthly_cost), `UsageMetric` (id, resource_id, timestamp, metric_name, metric_value, unit), `CostForecast` (id, account_id, forecast_date, predicted_cost, lower_bound, upper_bound), `Recommendation` (id, resource_id, recommendation_type, title, description, estimated_savings, implementation_steps TEXT, status [pending/applied/dismissed]).

**Step 3: Build cloud provider connectors.** Create `connectors/` directory: `AWSConnector` (uses `boto3` — Cost Explorer, CloudWatch, EC2, RDS, S3 APIs), `AzureConnector` (uses `azure-mgmt-costmanagement`, `azure-mgmt-compute`, `azure-mgmt-monitor`), `GCPConnector` (uses `google-cloud-billing`, `google-cloud-monitoring`). Each connector collects: resources list, utilization metrics, current cost, pricing model. Credentials encrypted at rest using `cryptography.fernet`.

## Phase 2: Data Collection & Analysis
**Step 4: Build the data collection pipeline.** Celery beat schedule (every 6 hours) triggers `collect_all_accounts` task. For each CloudAccount: (1) load and decrypt credentials, (2) instantiate the appropriate connector, (3) enumerate all resources, (4) collect utilization for past 30 days, (5) calculate current cost, (6) upsert into Resources and UsageMetrics tables. Track last_synced timestamp.

**Step 5: Implement the recommendation engine.** `recommendation_engine.py`: (1) `right_sizing` — analyze CPU/Memory utilization for compute resources, recommend instance type changes if avg utilization < 20% (downsize) or > 80% (upsize), (2) `reserved_instances` — analyze consistent usage over 30 days, recommend 1-year or 3-year reserved instance purchases, (3) `storage_optimization` — find unattached volumes, outdated snapshots, infrequently accessed S3 objects (use LastAccessDate), recommend lifecycle policies, (4) `spot_eligible` — identify fault-tolerant workloads that can use spot instances.

**Step 6: Train ML forecast model.** Use XGBoost for time-series forecasting of daily costs. Features: day-of-week, day-of-month, month, previous 7/30/90 day averages, number of resources, deployment events (from tags). Train per-account. Forecast 90 days with prediction intervals using quantile regression (alpha=0.1, 0.9). Re-train weekly.

## Phase 3: Frontend
**Step 7: Build the cost dashboard.** `CostDashboard.tsx`: (1) top-level KPI cards (current monthly spend, forecasted next month, estimated savings if recommendations applied), (2) interactive treemap (Recharts `Treemap`) showing cost breakdown by service / region / tag, (3) time-series chart of daily spend with forecast overlay (confidence interval shading).

**Step 8: Build the resource inventory.** `ResourceInventory.tsx`: searchable, filterable table of all resources with columns: name, type, region, monthly cost, utilization (heatmap bar), recommendation count. Server-side sorting and pagination. Click row → `ResourceDetail.tsx` with configuration, utilization charts, and applicable recommendations.

**Step 9: Build the recommendation UI.** `RecommendationList.tsx`: cards for each recommendation with: title, description, estimated savings ($/month), difficulty badge, "Apply" button (opens implementation guide). Filter by status (pending/applied/dismissed), type (right-size, RI, storage, spot), and savings range.

## Phase 4: Integration & Polish
**Step 10: Add budget alerts.** Define budget thresholds per account. Celery beat checks current spend vs budget daily. If forecasted spend > budget, send alert: email, Slack webhook. Show alert history in UI.

**Step 11: Dockerize.** docker-compose with: FastAPI, Celery worker, Celery beat, PostgreSQL, Redis, frontend."""

BP["Real-Time Dashboard Builder"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, WebSocket support. Dockerize.

**Step 2: Design the data model.** `Dashboard` (id, name, description, layout JSON, created_by, created_at, updated_at), `Widget` (id, dashboard_id, widget_type, title, config JSON, position JSON, data_source_id), `DataSource` (id, name, type [postgresql/rest_api/csv], connection_config JSON), `DashboardShare` (id, dashboard_id, user_id, permission [view/edit]).

**Step 3: Build the data source connector service.** Create `data_source_service.py` with connection pooling for PostgreSQL sources (SQLAlchemy engine pool), HTTP client for REST API sources (httpx with caching), and CSV parser (pandas with chunking). Each data source returns a normalized DataFrame-like result. Cache query results in Redis with configurable TTL (30s to 1h).

## Phase 2: Backend API
**Step 4: Build the SQL query endpoint.** POST `/api/query` accepts `data_source_id` and `sql_query`. The backend: (1) loads the data source config, (2) validates the SQL (read-only, no DDL/DML — parse with `sqlparse` and reject mutations), (3) executes against the data source, (4) returns results as JSON with column metadata. Set query timeout (30s). Cache identical queries.

**Step 5: Build the WebSocket real-time feed.** WS `/ws/dashboard/{id}`. When a dashboard has auto-refresh enabled, the backend runs the queries on schedule and pushes updated data to all connected clients. Uses Redis pub/sub to fan-out across multiple server instances.

**Step 6: Build the widget data pipeline.** `widget_data_service.py`: (1) receives widget config (type, data source, query, visualization options), (2) executes the query (Step 4), (3) transforms the result into the widget's expected format (e.g., time-series → `[{date, value}]`, categorical → `[{name, value}]`), (4) returns the transformed data.

## Phase 3: Frontend
**Step 7: Build the drag-and-drop dashboard canvas.** Use `react-grid-layout` for the grid. `DashboardCanvas.tsx`: (1) responsive grid with breakpoints (lg: 12 cols, md: 10, sm: 6), (2) widgets are grid items that can be resized and repositioned, (3) changes auto-save to the backend (debounced), (4) add widget toolbar: click "+" → opens widget picker modal.

**Step 8: Build the widget library.** Create individual widget components in `widgets/`: `LineChartWidget` (Recharts `LineChart` with zoom), `BarChartWidget`, `PieChartWidget`, `DataTableWidget` (sortable, filterable table with TanStack Table), `StatCardWidget` (big number + label + trend arrow), `GaugeWidget`. Each widget has a `configPanel.tsx` for customization (title, colors, dimensions, axes).

**Step 9: Build the widget configuration panel.** `WidgetConfigPanel.tsx`: slides in from the right when a widget is selected. Sections: (1) Data Source — select or connect new, (2) Query — SQL editor with `@codemirror/sql` or Monaco editor with syntax highlighting and autocomplete, (3) Visualization — chart type selector, color picker, axis labels, (4) Auto-refresh — interval selector (off / 30s / 1m / 5m / 15m).

**Step 10: Build the data source connection wizard.** `DataSourceWizard.tsx`: step form — Step 1 (name + type), Step 2 (connection config — PostgreSQL: host, port, db, user, password; REST: URL, headers, auth; CSV: file upload), Step 3 (test connection button, shows preview of first 10 rows), Step 4 (save).

## Phase 4: Integration
**Step 11: Add dashboard sharing.** `ShareDialog.tsx`: search users by email, set permission (view/edit), generate public link (with optional password protection). `dashboard_shares` table enforces access control on all API endpoints.

**Step 12: Dockerize.** docker-compose with: FastAPI, PostgreSQL, Redis, frontend."""

BP["AI-Powered Meeting Minutes & Action Tracker"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, Celery + Redis for async audio processing. Dockerize.

**Step 2: Design the data model.** `Meeting` (id, title, date, duration_seconds, status, transcript_text TEXT, summary TEXT, calendar_event_id), `Speaker` (id, meeting_id, speaker_label, display_name), `TranscriptSegment` (id, meeting_id, speaker_id, start_time, end_time, text, language), `ActionItem` (id, meeting_id, text, assignee, due_date, status, source_transcript_segment_id), `Decision` (id, meeting_id, text, context), `Topic` (id, meeting_id, name, start_time, end_time).

**Step 3: Build the audio processing pipeline.** Accept audio upload through POST `/api/meetings/upload` (multipart, accepts MP3, WAV, M4A, WebM). Store raw audio on disk or S3-compatible storage. Dispatch to Celery task `transcribe_meeting`. Use OpenAI Whisper (large-v3 model) for transcription with language auto-detection. For speaker diarization, use PyAnnote Audio 3.x pipeline.

## Phase 2: AI Processing
**Step 4: Implement speaker diarization.** After transcription, run PyAnnote's `SpeakerDiarization` pipeline: (1) splits audio into speaker-homogeneous segments, (2) clusters segments by speaker identity, (3) assigns speaker labels (SPEAKER_00, SPEAKER_01, etc.). Merge with Whisper transcription segments based on timestamps. Store in TranscriptSegment table. Implement a "name mapping" UI where users can assign real names to speaker labels.

**Step 5: Build the LLM extraction pipeline.** Use LangChain + OpenAI/Gemini to process the full transcript. Extract: (1) `ActionItems` — tasks with assignee inferred from context, (2) `Decisions` — key decisions made, (3) `Topics` — agenda topics with time ranges, (4) `Summary` — 3-5 sentence executive summary. Use structured output (Pydantic `BaseModel` as response format). Run as a Celery task chain: transcribe → diarize → extract.

**Step 6: Implement calendar integration.** `calendar_service.py` with abstract base `CalendarProvider`. Implement `GoogleCalendarProvider` (uses `google-api-python-client`, OAuth2 flow) and `OutlookCalendarProvider` (uses `msal` and Microsoft Graph API). On meeting completion: create/update calendar event with summary, attendees notified. Support "Join before meeting" for Zoom/Meet links.

## Phase 3: Frontend
**Step 7: Build the real-time transcript view.** `TranscriptView.tsx`: scrollable view of transcript segments with speaker name labels (color-coded), timestamps, and search highlighting. Auto-scroll during playback. Click a segment → opens context menu: create action item, add note, copy text. Show speaker timeline as colored bars at the top.

**Step 8: Build the action item board.** `ActionBoard.tsx`: kanban-style board (To Do, In Progress, Done) for action items. Each card shows: text, assignee avatar, due date, source meeting link. Drag-and-drop to change status. Click → expand detail: full context, linked transcript segment, status history.

**Step 9: Build the meeting timeline.** `MeetingTimeline.tsx`: horizontal timeline showing topics as colored segments. Click a topic → scrolls transcript to that section. Below the timeline: Decision cards (key decisions made during the meeting). Each card has the decision text and the context (linked transcript).

**Step 10: Build the meeting archive.** `MeetingArchive.tsx`: searchable, filterable list of past meetings. Full-text search across transcripts and summaries. Filter by date range, participants. Each row: title, date, participant count, action item count, summary preview. Click → opens full meeting detail.

## Phase 4: Integration
**Step 11: Dockerize.** docker-compose with: FastAPI, Celery worker (with GPU passthrough for Whisper if available), PostgreSQL, Redis, and frontend.

**Step 12: Add real-time collaboration.** While a meeting is in progress, collaborators can view the live transcript via WebSocket, add inline notes, and mark action items."""

BP["ML Data Drift Monitor & Alert System"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, Celery + Redis for periodic monitoring. Dockerize with Prometheus + Grafana for operational metrics.

**Step 2: Design the data model.** `Model` (id, name, version, endpoint_url, input_schema JSON, prediction_column, health_score FLOAT), `ReferenceDataset` (id, model_id, name, created_at, statistics JSON, distribution JSON), `MonitoringRun` (id, model_id, timestamp, data_count, health_score, drift_detected BOOL), `DriftResult` (id, monitoring_run_id, feature_name, drift_type [data/concept/label], test_name, statistic FLOAT, p_value FLOAT, threshold FLOAT, drifted BOOL), `Alert` (id, model_id, rule_id, triggered_at, resolved_at, severity, message).

**Step 3: Build the reference statistics calculator.** When a model is registered, compute reference statistics on a batch of "golden" data: (1) per-feature mean, std, quantiles (p1, p5, p25, p50, p75, p95, p99), (2) Pearson correlation matrix (top 20 features), (3) target distribution (bin counts for classification, mean/std for regression). Store as JSON blobs in ReferenceDataset.

## Phase 2: Drift Detection Engine
**Step 4: Implement statistical drift tests.** `drift_detector.py` using Evidently AI library: (1) `DataDriftPreset` — runs Kolmogorov-Smirnov test for numerical features, Jensen-Shannon divergence for categorical features, (2) `TargetDriftPreset` — compares prediction distributions, (3) `DataQualityPreset` — checks for missing values, new categories, value ranges. Each test returns a drift score and p-value. Flag features where p < 0.05.

**Step 5: Implement concept drift detection.** Track model performance metrics over time (accuracy, F1, precision, recall for classification; MAE, RMSE for regression). Use the Page-Hinkley test and ADWIN (Adaptive Windowing) algorithm to detect changes in the error distribution. Trigger alert when concept drift is detected.

**Step 6: Build the monitoring pipeline.** Celery beat triggers `run_monitoring` every hour for all active models. For each model: (1) fetch recent production data (last 1000 predictions from the endpoint or data lake), (2) compute current statistics, (3) run drift tests against reference, (4) compute current health score (weighted combination of drift severity × number of drifted features), (5) store MonitoringRun and DriftResult records, (6) if drift detected → evaluate alert rules and trigger.

## Phase 3: Frontend
**Step 7: Build the model health dashboard.** `ModelHealthDashboard.tsx`: (1) model cards with health score gauge (green/yellow/red), (2) health score trend line (last 30 runs), (3) alert count badge, (4) click → full model detail.

**Step 8: Build the drift visualizer.** `DriftVisualizer.tsx`: (1) feature-level drift overview — table with feature name, drift score, p-value, drift direction, (2) distribution comparison overlay (reference vs current) using Recharts `AreaChart` with transparency, (3) time-series of drift scores per feature (detect trends), (4) PSI (Population Stability Index) meter.

**Step 9: Build the alert management UI.** `AlertManager.tsx`: (1) alert timeline with severity indicators, (2) alert details: model name, drifted features, current vs reference performance, (3) acknowledge, dismiss, or escalate alerts, (4) configure alert rules: which features, drift threshold, cooldown period.

**Step 10: Build the automated retraining UI.** `RetrainingConfig.tsx`: (1) connect to a training pipeline (MLflow run, SageMaker pipeline, or custom script), (2) set trigger conditions (drift_severity > X, health_score < Y), (3) view retraining history (triggered by, result, performance comparison), (4) manually trigger retraining.

## Phase 4: Integration
**Step 11: Dockerize.** docker-compose with: FastAPI, Celery beat + worker, PostgreSQL, Redis, Prometheus (collects drift metrics), Grafana (pre-configured dashboards), and frontend.

**Step 12: Add Prometheus metrics integration.** Export key drift metrics as Prometheus gauges: `drift_score{model,feature}`, `health_score{model}`, `data_drift_detected{model}`. Grafana dashboards auto-imported on startup."""

BP["Competitive Programming Arena"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, Celery + Redis for async code execution. Dockerize.

**Step 2: Design the data model.** `User` (id, username, email, password_hash, rating, problems_solved), `Problem` (id, title, description TEXT, difficulty, time_limit_ms, memory_limit_mb, test_cases JSON, solution_template JSON), `Submission` (id, problem_id, user_id, language, code TEXT, status, passed_tests, total_tests, execution_time_ms, memory_used_kb, compiler_output TEXT, submitted_at), `Contest` (id, title, start_time, end_time, problems JSON, status [scheduled/running/finished]), `ContestParticipant` (contest_id, user_id, score, rank, finish_time), `RatingChange` (user_id, contest_id, old_rating, new_rating, change).

**Step 3: Build the Docker-based code execution sandbox.** Create `executor/` module: (1) on submission, the worker pulls a language-specific Docker image (python:3.11-slim, openjdk:17-slim, gcc:13, swift:5.9), (2) compiles the code inside the container with a timeout, (3) runs against test cases with strict resource limits (cgroups CPU/memory limits), (4) captures stdout, stderr, exit code, execution time, (5) returns results. Implement robust security: drop all capabilities, no network, read-only rootfs, pids limit, ulimit -t.

## Phase 2: Core Judge Engine
**Step 4: Build the submission pipeline.** POST `/api/submissions` — (1) saves code and creates Submission record (status: "pending"), (2) dispatches to Celery task `execute_and_judge`, (3) task runs inside Docker sandbox (Step 3), (4) for each test case: compare actual output with expected output (whitespace-tolerant diff), (5) compile results: pass/fail per test case, total time, peak memory, (6) update Submission record.

**Step 5: Implement the rating system.** Use Glicko-2 rating algorithm (preferred over Elo for its handling of rating uncertainty). On contest finish: (1) compute match results as pairwise comparisons (sorted by rank), (2) update each participant's rating and deviation, (3) store RatingChange history, (4) display rating progression chart on user profile.

**Step 6: Build the problem management API.** CRUD for problems. POST `/api/problems` — inputs: title, description (markdown), time/memory limits, test cases (TOML or JSON), solution template. The test case format: `[{"input": "...", "expected": "..."}]`. Store test cases encrypted at rest (they shouldn't be exposed via API). GET `/api/problems` lists only metadata (no test cases).

## Phase 3: Frontend
**Step 7: Build the code editor.** Use Monaco Editor (`@monaco-editor/react`) with: (1) language selector (Python, Java, C++, Swift), (2) problem statement panel (markdown rendered with `react-markdown`), (3) split-view layout: problem on left, editor + output on right, (4) "Run" button (runs against sample test cases) and "Submit" button (runs against all test cases).

**Step 8: Build the test case result panel.** `TestResults.tsx`: (1) status summary bar (passed X/Y tests, total time, peak memory), (2) individual test case results with expandable diff view (expected vs actual), (3) red/green indicators for each test, (4) compilation errors shown in a collapsible panel with highlighted error lines.

**Step 9: Build the real-time contest leaderboard.** `ContestLeaderboard.tsx` using WebSocket: (1) ranked list of participants with: rank, username, problems solved, total time, (2) each problem column shows submission count and time (green = solved, red = attempted, gray = untouched), (3) auto-updates when any participant submits, (4) "freeze" last hour of standings before contest ends (common ICPC/Codeforces style).

**Step 10: Build the user profile and history.** `UserProfile.tsx`: (1) rating progression chart (Recharts `AreaChart`), (2) problems solved list with difficulty distribution (pie chart), (3) recent submissions table with status, time, language, (4) contest history table.

## Phase 4: Integration
**Step 11: Dockerize.** docker-compose with: FastAPI, Celery worker (with Docker socket mounted for sandbox), PostgreSQL, Redis, frontend. The worker needs `docker.sock` access — this is a known trade-off; isolate with dedicated Docker-in-Docker or Sysbox runtime for production.

**Step 12: Add rate limiting per user.** Prevent abuse: max 10 submissions per 5 minutes per user. Reset on contest mode (unlimited during contests to avoid blocking)."""

BP["Hackathon Hub — Event & Project Manager"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, WebSocket support for real-time features. Dockerize.

**Step 2: Design the data model.** `Event` (id, name, description, start_date, end_date, status [draft/active/completed], location, max_teams, max_participants), `Participant` (id, event_id, user_id, team_id, skills JSON, registered_at), `Team` (id, event_id, name, description, max_members, created_at), `Project` (id, event_id, team_id, name, description, github_url, demo_url, tech_stack JSON, submitted_at), `Judge` (id, event_id, user_id), `Scorecard` (id, event_id, name, rubric JSON — array of criteria with name, max_score, weight), `Score` (id, scorecard_id, project_id, judge_id, scores JSON [{criterion: "code_quality", score: 8}], total_score, comments, submitted_at), `Sponsor` (id, event_id, name, tier [gold/silver/bronze], logo_url, website).

**Step 3: Build the event lifecycle state machine.** Implement `EventStateMachine` with states: `draft` (editable), `registration` (participants can join), `active` (hacking in progress, projects can be submitted), `judging` (submissions closed, judges scoring), `completed` (results published). Transitions are validated. Events auto-transition based on dates via Celery beat.

## Phase 2: Core Features
**Step 4: Build team formation with skill matching.** POST `/api/teams/join-requests`: users request to join a team or create one. GET `/api/events/{id}/find-team`: suggests teammates based on complementary skills (use simple Jaccard similarity on skills arrays). `Team` CRUD with `max_members` validation. Team invites via notification.

**Step 5: Build the project submission system.** POST `/api/projects` — requires GitHub repo URL. The backend fetches the repo metadata via GitHub API (description, stars, language, last commit). Validate submission deadline. Store project with submitted_at timestamp. Allow resubmission (update, not create new) before deadline.

**Step 6: Build the judging engine.** `judging_service.py`: (1) assign judges to projects (round-robin, ensuring no conflict of interest), (2) judges score via a scorecard interface, (3) scores are aggregated: weighted average based on rubric, (4) handle tiebreakers: highest innovation score wins, (5) publish results: top 3 per track, optionally all scores.

## Phase 3: Frontend
**Step 7: Build the event creation wizard.** `EventWizard.tsx`: multi-step form — Step 1 (name, description, dates), Step 2 (location, max participants, team size), Step 3 (tracks/themes), Step 4 (judges and scorecard configuration), Step 5 (sponsor management). Preview before publishing.

**Step 8: Build the team formation board.** `TeamBoard.tsx`: (1) list of teams with member count, needed skills, description, (2) "Join" button (with skill tags you'd bring), (3) "Create Team" button opens a modal, (4) drag-and-drop reordering of team members (for team leads), (5) live updates via WebSocket when teams change.

**Step 9: Build the judge scorecard interface.** `ScorecardInterface.tsx`: designed for tablet use during in-person events. (1) project selector (list or swipe), (2) scorecard with slider inputs (1-10) for each criterion, (3) comments textarea, (4) auto-save on change (debounced), (5) submission confirmation with review step.

**Step 10: Build the live leaderboard.** `LiveLeaderboard.tsx`: real-time top 10 via WebSocket. (1) animated ranking changes (gold/silver/bronze), (2) team names and project names, (3) score bars, (4) auto-updates during judging phase when scores are submitted, (5) freeze button: organizers can freeze the board.

## Phase 4: Integration
**Step 11: Dockerize.** docker-compose with: FastAPI, PostgreSQL, Redis, frontend.

**Step 12: Add sponsor management.** `SponsorDashboard.tsx`: (1) sponsor tier management, (2) logo upload, (3) sponsor booth info, (4) recruiting link. Display sponsors on the event landing page by tier."""

BP["Personal Knowledge Graph & Second Brain"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL + Neo4j, React + TypeScript + Vite frontend. Dockerize with docker-compose (Neo4j 5.x).

**Step 2: Design the data model.** PostgreSQL table: `Note` (id, title, content TEXT, embedding vector(1536), created_at, updated_at). Neo4j: `(:Note {id, title, created_at})`, `(:Tag {name})`, `(:Source {url, title})`, relationships `[:RELATES_TO {weight, relationship_type}]`, `[:TAGGED_WITH]`, `[:SOURCED_FROM]`, `[:BACKLINKS]`.

**Step 3: Set up the embedding pipeline.** On note creation/update: (1) split note into sections (by headers), (2) generate embeddings for each section using OpenAI `text-embedding-3-small` (or Gemini embedding API), (3) store in `Note.embedding` column. Use pgvector for similarity search (or Neo4j vector index).

## Phase 2: Core Features
**Step 4: Build the suggestion engine.** `suggestion_service.py`: (1) when a note is saved, compute its embedding, (2) perform vector similarity search against all other notes (cosine similarity threshold > 0.7), (3) also do keyword matching on title and tags, (4) combine results and present as "Related Notes" in the UI. User can accept suggestion (creates `[:RELATES_TO]` relationship) or dismiss.

**Step 5: Implement the spaced repetition system.** `srs_service.py` implementing SM-2 algorithm: (1) `Flashcard` (id, note_id, question, answer, ease_factor, interval, repetitions, next_review_date), (2) auto-generate flashcards from notes: extract Q&A pairs using an LLM prompt ("Generate 3 flashcards from this note"), (3) review queue: show due flashcards, user rates recall (0-5), algorithm updates interval, (4) daily Celery task to notify user of due cards.

**Step 6: Build the full-text + semantic search.** POST `/api/search`: (1) generate query embedding, (2) pgvector `<=>` search filter, (3) PostgreSQL full-text search (`ts_vector` on title + content), (4) combine with weighted RRF: 0.7 vector, 0.3 keyword. Return results with snippet highlighting.

## Phase 3: Frontend
**Step 7: Build the rich markdown editor.** Use TipTap editor (ProseMirror wrapper) with: (1) `/` slash menu for commands (heading, bold, italic, code block, bullet list, callout, image), (2) markdown shortcuts (`# ` for heading, `**` for bold), (3) auto-save on 3-second debounce, (4) backlink auto-complete (`[[` triggers note search), (5) drag-and-drop to create relationships.

**Step 8: Build the graph visualization.** Use `react-force-graph-2d` for the interactive knowledge graph. (1) nodes = notes (sized by number of connections), (2) edges = `[:RELATES_TO]` (thicker = stronger weight), (3) colors by tag, (4) click node → navigates to note, (5) drag nodes, zoom, pan, (6) search bar highlights matching nodes, (7) "Create Note" button opens a new node at the center of viewport.

**Step 9: Build the flashcard review UI.** `FlashcardReview.tsx`: (1) single card view: question first, click to reveal answer, (2) rate buttons (0-5) below the answer, (3) progress bar for today's due cards, (4) keyboard shortcuts (1-5 to rate, space to flip), (5) streak counter, (6) statistics: cards reviewed today, retention rate, next review count.

**Step 10: Build the backlink panel.** `BacklinkPanel.tsx` sidebar: (1) shows all notes that link to the current note, (2) shows "unlinked mentions" (notes that mention the title but aren't formally linked — detected via keyword search), (3) one-click "Create Link" button.

## Phase 4: Integration
**Step 11: Dockerize.** docker-compose with: FastAPI, PostgreSQL (with pgvector), Neo4j 5.x, Redis, and frontend.

**Step 12: Add data import.** Import from Markdown files (bulk upload), Notion export, or Roam Research JSON. Parse and create notes + relationships."""

BP["API Security Fuzzer & Vulnerability Scanner"] = """\
## Phase 1: Foundation
**Step 1: Scaffold the project.** FastAPI backend with SQLAlchemy + PostgreSQL, React + TypeScript + Vite frontend, Celery + Redis for async scanning. Dockerize.

**Step 2: Design the data model.** `ScanTarget` (id, name, base_url, openapi_spec TEXT, auth_config JSON, created_by), `ScanRun` (id, target_id, status, started_at, completed_at, endpoint_count, total_requests, vulnerabilities_found), `Endpoint` (id, target_id, path, method, parameters JSON, security_schema JSON), `Vulnerability` (id, scan_run_id, endpoint_id, vuln_type, severity [critical/high/medium/low/info], title, description, request_payload TEXT, response TEXT, evidence TEXT, cvss_score FLOAT, remediation TEXT), `FuzzPayload` (id, vuln_type, payload TEXT, description).

**Step 3: Build the OpenAPI spec parser.** `openapi_parser.py`: (1) accepts OpenAPI 3.x YAML/JSON spec, (2) parses endpoints, methods, parameters, request bodies, security schemes using `openapi-spec-validator` and `prance`, (3) generates typed test cases per endpoint (required params, example values from spec examples, type-appropriate fuzz seeds), (4) stores Endpoint records.

## Phase 2: Fuzzing Engine
**Step 4: Build the payload generator.** `payload_generator.py`: (1) `InjectionFuzzer` — generates SQL injection (`' OR 1=1--`), XSS (`<script>alert(1)</script>`), NoSQL injection, command injection, template injection payloads, (2) `AuthFuzzer` — tests for: missing auth, expired tokens, privilege escalation (modify JWT claims), rate limiting bypass, (3) `DataExposureFuzzer` — tests for: excessive data in responses, IDOR (increment IDs), mass assignment, (4) `LogicFuzzer` — boundary values, negative numbers, very long strings, null/empty payloads. Maintain 100+ payload templates.

**Step 5: Build the parallel scan engine.** `scan_engine.py`: (1) takes a ScanTarget, loads endpoints, (2) for each endpoint, generates fuzz test cases using all applicable fuzzers, (3) sends requests in parallel using `httpx.AsyncClient` with connection pooling (max 50 concurrent), (4) analyzes responses for vulnerability indicators, (5) batches results and writes Vulnerabilities. Run as a Celery task with progress reporting (X/Y endpoints scanned).

**Step 6: Implement vulnerability detection heuristics.** `detector.py`: (1) response analysis — check for SQL errors in response body (`SQL syntax.*MySQL`, `unclosed quotation mark`), XSS reflection (payload appears in response), stack traces (sensitive info disclosure), (2) timing analysis — measure response time, flag endpoints that take suspiciously long (potential time-based blind injection), (3) status code analysis — 500 on malformed input may indicate unhandled exceptions, 403 on modified IDs may indicate IDOR, (4) response size comparison — large response to small input may indicate data exposure.

## Phase 3: Frontend
**Step 7: Build the scan configuration UI.** `ScanConfig.tsx`: (1) input target base URL + upload OpenAPI spec (or paste URL to fetch), (2) authentication config: None / API Key / Bearer Token / Basic Auth, (3) select fuzz types to run (injection, auth, data exposure, logic), (4) set concurrency level and timeout, (5) "Start Scan" button.

**Step 8: Build the endpoint explorer.** `EndpointExplorer.tsx`: (1) tree view of endpoints grouped by tag (from OpenAPI), (2) each endpoint row: method badge (color-coded: GET=green, POST=blue, DELETE=red), path, parameters count, security badge, (3) expand to see: parameters table, security schema, example request, (4) security score for each endpoint (based on past scan results).

**Step 9: Build the vulnerability detail panel.** `VulnerabilityDetail.tsx`: (1) header: vuln type, severity (color-coded badge), CVSS score, (2) endpoint info: method + path, (3) request section: sent payload with syntax highlighting, (4) response section: response body with vulnerable part highlighted, (5) evidence: the specific indicator that triggered detection, (6) remediation: step-by-step fix guide with code examples.

**Step 10: Build the security trends dashboard.** `SecurityDashboard.tsx`: (1) vulnerability count by severity (stacked bar chart), (2) vulnerability trend over time (line chart, grouped by severity), (3) top vulnerability types (horizontal bar chart), (4) scan history table (date, target, endpoints scanned, vulns found), (5) overall security score (composite metric).

## Phase 4: CI/CD Integration
**Step 11: Build the CLI tool.** Create a CLI (using `typer` or `click`) that can run scans from the terminal: `api-fuzzer scan --spec ./openapi.yaml --target https://api.example.com`. Output results as JSON or SARIF format. Designed for CI/CD integration.

**Step 12: Build the GitHub Actions integration.** Create a GitHub Action that: (1) checks out the repo, (2) finds OpenAPI spec, (3) runs the fuzzer, (4) uploads results as a SARIF file, (5) optionally fails the build if critical vulnerabilities found. Provide `action.yml` in the repo.

**Step 13: Dockerize.** docker-compose with: FastAPI, Celery worker, PostgreSQL, Redis, and frontend. The CLI tool is pip-installable."""


def seed():
    db = SessionLocal()
    existing = db.query(Project).count()
    if existing > 0:
        print(f"Database already has {existing} projects. Skipping seed.")
        db.close()
        return

    for p in P:
        db.add(Project(**p))
    db.commit()
    db.close()
    print(f"Seeded {len(P)} projects.")


# ============================================================
# PROJECT 1
# ============================================================
a("AI Code Review Pipeline",
  "Automated PR analysis with ML-based bug prediction, style enforcement, and performance regression detection",
  "A GitHub-integrated service that automatically reviews pull requests using a combination of static analysis, ML models, and LLM reasoning. The system scores each PR on code quality, security, performance, and test coverage, providing inline feedback and a dashboard for team-wide metrics.",
  "Manual code reviews are inconsistent, time-consuming, and miss subtle bugs. Teams need automated, intelligent review that catches issues before they reach production.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "Celery"],
  ["Microservices", "Event-driven architecture", "Webhook-based integration", "Background task processing"],
  ["XGBoost", "OpenAI API", "SQLAlchemy", "Celery", "Pydantic", "Jinja2", "PyLint/Flake8 wrappers"],
  "Advanced",
  BP["AI Code Review Pipeline"],
  ["Interactive PR diff viewer with inline annotations", "Team dashboard with trend charts (Chart.js/Recharts)", "Configurable rule builder UI", "Historical analysis timeline", "Webhook status page"],
  ["https://github.com/santifer/career-ops", "https://github.com/soxoj/maigret"],
  "Adds distributed microservices experience, event-driven architecture, and advanced ML (XGBoost) beyond the single FastAPI app. Shows DevOps integration with GitHub APIs and background job processing.",
  ["ML-based bug risk scoring per commit", "Security vulnerability pattern detection", "Performance regression analysis", "Automated style enforcement with custom rules", "Team-wide quality metrics dashboard", "GitHub App integration with webhooks"],
  ["Building and orchestrating microservices", "ML model training for code analysis", "GitHub App development & webhooks", "Background task processing with Celery", "Real-time UI updates with WebSockets"],
  ["ML/AI", "Developer Tools", "DevOps", "Microservices", "Code Quality"])

# ============================================================
# PROJECT 2
# ============================================================
a("Real-Time Collaborative Whiteboard",
  "Multi-user drawing app with WebSocket sync, vector graphics export, and session replay",
  "A real-time collaborative whiteboard supporting multiple users simultaneously. Features include vector-based drawing tools, sticky notes, image imports, session recording/replay, and export to SVG/PNG/PDF. Built with FastAPI WebSockets for real-time sync and React for the canvas-based UI.",
  "Remote teams lack lightweight, real-time visual collaboration tools that are self-hosted and privacy-focused, unlike SaaS offerings.",
  ["FastAPI", "React", "TypeScript", "Redis", "PostgreSQL", "Docker", "Nginx"],
  ["WebSocket real-time communication", "CRDT-based state synchronization", "Event sourcing for session replay", "Stateless backend with Redis pub/sub"],
  ["FastAPI WebSockets", "Redis pub/sub", "roughjs", "perfect-freehand", "pdfkit", "Pydantic"],
  "Advanced",
  BP["Real-Time Collaborative Whiteboard"],
  ["Infinite canvas with pan/zoom", "Toolbar with drawing, text, shape, and image tools", "Real-time cursor presence indicators", "Layer panel with reordering", "Session timeline scrubber for replay", "Export dialog (SVG/PNG/PDF)"],
  ["https://github.com/soxoj/maigret", "https://github.com/coleam00/Archon"],
  "Demonstrates real-time systems expertise (WebSockets, CRDT), advanced frontend canvas work, and event sourcing — none of which appear on the current resume. Shows full-stack capability beyond CRUD APIs.",
  ["Multi-user real-time co-drawing", "Session recording with playback", "Vector graphics export", "Undo/redo with branching history", "Image import and positioning", "Self-hosted with Docker"],
  ["WebSocket lifecycle and connection management", "CRDT-based conflict-free data structures", "Canvas/SVG rendering optimization", "Event sourcing patterns", "Real-time communication at scale"],
  ["Real-Time", "Collaboration", "Full-Stack", "WebSockets", "UI/UX"])

# ============================================================
# PROJECT 3
# ============================================================
a("ML Model Registry & A/B Testing Platform",
  "Version-controlled model registry with shadow deployments, online evaluation, and automated rollback",
  "A platform for data science teams to register, version, deploy, and A/B test ML models in production. Supports shadow scoring (deploy new model alongside current, compare results), gradual rollout, automated rollback on metric degradation, and a rich dashboard for comparing model performance.",
  "Data science teams lack a unified system to version, deploy, and evaluate ML models in production. Shadow deployments and A/B testing are done ad-hoc, leading to risky rollouts and no performance regression tracking.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "MLflow"],
  ["Multi-tenant SaaS architecture", "Shadow deployment pattern", "Canary release pipeline", "Event-driven metric collection"],
  ["MLflow", "XGBoost", "LightGBM", "scikit-learn", "Prometheus client", "SQLAlchemy", "Pydantic"],
  "Advanced",
  BP["ML Model Registry & A/B Testing Platform"],
  ["Model registry browser with version diff view", "A/B test configuration wizard", "Real-time metric comparison charts", "Deployment pipeline visualization", "Alert configuration panel", "Shadow traffic analysis dashboard"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Extends Tejas's existing LightGBM experience into a full ML engineering platform. Adds MLOps, model lifecycle management, canary deployments, and A/B testing — critical skills for ML engineer roles.",
  ["Model versioning with metadata", "Shadow deployment for risk-free testing", "A/B test assignment and tracking", "Automated rollback on metric degradation", "Performance comparison dashboards", "REST API for model inference"],
  ["MLOps best practices and model lifecycle", "Canary and shadow deployment patterns", "Statistical A/B testing methodology", "Prometheus metric collection and alerting", "Multi-tenant SaaS architecture design"],
  ["ML/AI", "MLOps", "DevOps", "Full-Stack", "Data Engineering"])

# ============================================================
# PROJECT 4
# ============================================================
a("Distributed Task Orchestrator & Monitor",
  "Celery-based task queue with real-time monitoring, retry policies, DAG workflows, and Slack integration",
  "A distributed task queue system built on Celery and Redis, with a rich monitoring dashboard. Supports DAG-based workflow definitions, configurable retry policies, task scheduling, worker auto-scaling, and Slack/email notifications. Provides real-time task tracing and performance analytics.",
  "Background job failures in distributed systems are hard to debug without centralized tracing, retry policies, and real-time visibility into worker health and queue depths.",
  ["FastAPI", "React", "TypeScript", "Redis", "PostgreSQL", "Docker", "Celery", "Flower"],
  ["Distributed task queue", "Producer-consumer pattern", "DAG execution engine", "Event-driven monitoring"],
  ["Celery", "Redis-py", "SQLAlchemy", "WebSockets", "Recharts", "Pydantic", "APScheduler"],
  "Advanced",
  BP["Distributed Task Orchestrator & Monitor"],
  ["Live task stream with filtering", "DAG workflow visual editor", "Worker pool dashboard with metrics", "Task timeline and trace viewer", "Retry policy configuration panel", "Alert/notification rule builder"],
  ["https://github.com/coleam00/Archon", "https://github.com/santifer/career-ops"],
  "Showcases distributed systems architecture, background processing, and real-time monitoring — major gaps in the current resume. Essential for backend/infrastructure roles.",
  ["DAG-based workflow definitions (YAML)", "Real-time task tracing with spans", "Intelligent retry with exponential backoff", "Worker auto-scaling based on queue depth", "Slack/email/webhook notifications", "Task scheduling and cron support"],
  ["Distributed task queue internals", "DAG execution engine design", "Real-time monitoring systems", "Graceful failure handling patterns", "Horizontal worker scaling strategies"],
  ["Distributed Systems", "Backend", "DevOps", "Real-Time", "Infrastructure"])

# ============================================================
# PROJECT 5
# ============================================================
a("Personal Finance Intelligence Engine",
  "AI-powered financial aggregator with spending forecasts, anomaly detection, and goal tracking",
  "A personal finance platform that connects to bank accounts via Plaid, categorizes transactions using ML, predicts future spending patterns, detects anomalies (fraud, unusual subscriptions), and provides an interactive dashboard for budgeting and goal tracking.",
  "Personal finance tools either lack ML-powered insights or require manual categorization. Users want automated spending analysis, predictive budgeting, and anomaly alerts without sharing data with third-party aggregators.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis"],
  ["Hexagonal architecture", "Third-party API integration", "Batch ML inference pipeline", "Event-driven anomaly detection"],
  ["LightGBM", "XGBoost", "Plaid API", "SQLAlchemy", "Pydantic", "Recharts", "date-fns"],
  "Intermediate",
  BP["Personal Finance Intelligence Engine"],
  ["Dashboard with spending breakdown (pie/bar charts)", "Transaction feed with ML-based categorization", "Budget setting with progress rings", "Anomaly alert timeline", "Forecast projection chart", "Goal tracking with milestone visualization"],
  ["https://github.com/santifer/career-ops", "https://github.com/soxoj/maigret"],
  "Strengthens the ML + finance angle from Prophecy project with a more polished product. Adds third-party API integration (Plaid), unsupervised anomaly detection, and advanced data visualization.",
  ["Plaid API transaction sync", "ML-based transaction categorization", "Spending forecast with confidence intervals", "Anomaly and fraud detection", "Multi-account aggregation", "Savings goal tracking with projections"],
  ["Third-party financial API integration", "Time series forecasting with ML", "Anomaly detection techniques", "Data pipeline design for ML inference", "Interactive financial dashboards"],
  ["ML/AI", "FinTech", "Full-Stack", "Data Visualization", "Personal Finance"])

# ============================================================
# PROJECT 6
# ============================================================
a("Semantic Document Search & QA Platform",
  "RAG-powered enterprise search across documents with citation-backed answers, source management, and access control",
  "An enterprise document search platform using Retrieval-Augmented Generation (RAG). Users upload documents (PDF, DOCX, HTML), the system chunks and indexes them with embeddings, then provides natural language Q&A with cited sources. Includes user access control, document versioning, and sharing.",
  "Enterprise knowledge is trapped in siloed documents. Traditional keyword search fails to answer natural language questions, and existing RAG solutions are complex to deploy and lack access control.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "ChromaDB", "Redis"],
  ["RAG (Retrieval-Augmented Generation)", "Embedding-based vector search", "Document pipeline with chunking", "Multi-tenant data isolation"],
  ["LangChain", "OpenAI API / Gemini API", "ChromaDB", "pgvector", "Unstructured (document parsing)", "SQLAlchemy"],
  "Intermediate",
  BP["Semantic Document Search & QA Platform"],
  ["Document upload and management UI", "Chat interface with source citation cards", "Search results with relevance highlighting", "Collection/tag browser sidebar", "Document preview with embedded viewer", "Share and permission settings panel"],
  ["https://github.com/coleam00/Archon", "https://github.com/soxoj/maigret"],
  "Adds LLM/RAG experience, vector databases, and LangChain — currently missing from resume. Enterprise search is a high-demand skill. Shows ability to build AI-powered products beyond basic ML prediction.",
  ["Multi-format document parsing (PDF/DOCX/HTML)", "Semantic search with hybrid (vector + keyword)", "Citation-backed Q&A responses", "Document collections and tagging", "User access control and sharing", "Batch document ingestion pipeline"],
  ["RAG architecture and retrieval strategies", "Vector database design and tuning", "LangChain for LLM application development", "Document chunking strategies", "Hybrid search (vector + keyword) implementation"],
  ["ML/AI", "LLM", "RAG", "Full-Stack", "Search"])

# ============================================================
# PROJECT 7
# ============================================================
a("IoT Sensor Data Lake & Alerting System",
  "Time-series ingestion pipeline for IoT sensors with real-time dashboards, ML-based anomaly detection, and SMS alerts",
  "A scalable IoT data platform that ingests sensor data via MQTT/HTTP, stores in TimescaleDB, processes with streaming analytics, detects anomalies using ML (Isolation Forest, LSTM), and triggers alerts through SMS/email/webhook. Includes a real-time operational dashboard.",
  "IoT deployments generate massive time-series data that is difficult to store, query, and monitor in real time. Off-the-shelf solutions are expensive and don't support custom ML-based anomaly detection.",
  ["FastAPI", "React", "TypeScript", "TimescaleDB", "Docker", "MQTT", "Redis"],
  ["Event-driven ingestion pipeline", "Time-series data modeling", "Streaming analytics with windowing", "CQRS (read/write separation)"],
  ["scikit-learn (Isolation Forest)", "TensorFlow/Keras (LSTM)", "psycopg2", "paho-mqtt", "WebSockets", "Recharts", "Twilio API"],
  "Advanced",
  BP["IoT Sensor Data Lake & Alerting System"],
  ["Real-time sensor dashboard with gauges", "Time-series chart explorer with zoom", "Alert rule builder (threshold/ML)", "Incident timeline view", "Device registry and management panel", "Live map of sensor locations"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Adds IoT/embedded systems experience, time-series databases, streaming analytics, and anomaly detection — completely new territory that distinguishes Tejas from typical SWE candidates.",
  ["MQTT sensor data ingestion", "Time-series compression and retention policies", "Real-time dashboard with sub-second updates", "ML-based anomaly detection (Isolation Forest + LSTM)", "Multi-channel alerting (SMS/email/webhook)", "Device registry and health monitoring"],
  ["Time-series database design (TimescaleDB)", "MQTT protocol and IoT communication", "Streaming analytics and windowing", "Anomaly detection for time-series data", "Real-time data pipeline architecture"],
  ["IoT", "Real-Time", "ML/AI", "Data Engineering", "Infrastructure"])

# ============================================================
# PROJECT 8
# ============================================================
a("API Gateway & Developer Portal",
  "Self-service API gateway with rate limiting, key management, usage analytics, and interactive API documentation",
  "A full-featured API gateway that sits in front of microservices, handling authentication, rate limiting, API key management, request/response transformation, and usage analytics. Includes a developer portal where users can sign up, get keys, browse APIs, test endpoints, and view usage.",
  "Microservice teams need a unified API layer for authentication, rate limiting, and developer onboarding. Existing API gateways are either too heavy (Kong) or too cloud-specific (AWS API Gateway).",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Redis", "Docker", "Traefik"],
  ["API Gateway pattern", "Reverse proxy with middleware chain", "Token-based authentication", "Usage-based billing tier model"],
  ["httpx", "SQLAlchemy", "Pydantic", "Recharts", "react-syntax-highlighter", "Swagger/OpenAPI", "Redis-py"],
  "Intermediate",
  BP["API Gateway & Developer Portal"],
  ["Interactive API explorer with live testing", "API key management dashboard", "Usage analytics with time-series charts", "Rate limit configuration panel", "Developer signup and onboarding flow", "Webhook subscription manager"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Demonstrates API design expertise, middleware architecture, and developer experience — critical for platform engineering roles. Rate limiting and key management systems are directly applicable to cloud platform roles.",
  ["API key generation and rotation", "Configurable rate limiting (per-key, per-endpoint)", "Usage analytics and billing reports", "Interactive API documentation", "Request/response transformation", "Webhook event delivery system"],
  ["API Gateway architecture and middleware chain", "Rate limiting algorithms (token bucket, leaky bucket)", "Developer portal UX patterns", "API monetization and tiered access", "Reverse proxy internals"],
  ["Backend", "API", "DevOps", "Platform Engineering", "Full-Stack"])

# ============================================================
# PROJECT 9
# ============================================================
a("Social Media OSINT Analyzer",
  "Multi-platform social media search and analysis tool with graph-based relationship mapping and PDF reporting",
  "An investigation platform that searches for usernames across 100+ social platforms, extracts profile information, maps relationships between accounts, analyzes posting patterns, and generates professional PDF/HTML reports. Inspired by maigret but with a modern web UI and graph database backend.",
  "Investigators need to find and correlate user identities across dozens of social platforms. Existing tools either lack a web UI, have limited platform coverage, or don't visualize relationship graphs.",
  ["FastAPI", "React", "TypeScript", "Neo4j", "PostgreSQL", "Docker", "Redis"],
  ["Graph database model", "Async web scraping pipeline", "Plugin-based site adapters", "Report generation pipeline"],
  ["httpx (async)", "BeautifulSoup4", "Neo4j Python driver", "Playwright", "Jinja2", "pdfkit", "NetworkX", "D3.js"],
  "Advanced",
  BP["Social Media OSINT Analyzer"],
  ["Interactive graph visualization (D3.js force-directed)", "Search dashboard with multi-username input", "Profile detail panel with extracted data", "Relationship explorer with expand/collapse", "Report preview and download page", "Tag and case management sidebar"],
  ["https://github.com/soxoj/maigret", "https://github.com/santifer/career-ops"],
  "Adds async web scraping, graph databases (Neo4j), OSINT domain knowledge, and professional reporting — completely new skill areas. Shows C++-level performance thinking applied to Python async scraping.",
  ["Username search across 100+ platforms", "Profile data extraction and enrichment", "Relationship graph mapping between accounts", "Temporal posting pattern analysis", "PDF/HTML/CSV report generation", "Case-based investigation management"],
  ["Graph database modeling with Neo4j", "Async web scraping at scale", "Plugin/adapter architecture patterns", "Professional report generation", "OSINT methodology and ethical considerations"],
  ["OSINT", "Data Engineering", "Graph Database", "Async", "Security"])

# ============================================================
# PROJECT 10
# ============================================================
a("Multi-Agent AI Workflow Engine",
  "Define, execute, and monitor multi-step AI agent workflows with human-in-the-loop gates and parallel execution",
  "A workflow engine for orchestrating multiple AI agents. Define DAG-based workflows in YAML where each node is an agent task (code generation, research, review, etc.). Supports parallel execution, human approval gates, loop-until nodes, and a web dashboard for monitoring. Inspired by Archon's workflow model.",
  "AI coding agents produce inconsistent results because they lack structured, repeatable workflows. Teams need deterministic multi-agent pipelines with human oversight and parallel execution.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "Celery"],
  ["DAG-based workflow execution", "Multi-agent orchestration", "Human-in-the-loop pattern", "Event-driven state machine"],
  ["LangChain", "OpenAI API / Gemini API", "Celery", "SQLAlchemy", "React Flow", "Pydantic", "NetworkX"],
  "Advanced",
  BP["Multi-Agent AI Workflow Engine"],
  ["Visual workflow builder (drag-and-drop DAG editor)", "Real-time execution progress view", "Agent output inspection panel", "Human approval request interface", "Workflow template library", "Execution history with diff comparison"],
  ["https://github.com/coleam00/Archon", "https://github.com/santifer/career-ops"],
  "Shows AI agent orchestration, workflow engine design, and DAG execution — cutting-edge skills that directly align with the Archon-style projects employers are excited about. Positions Tejas at the forefront of AI engineering.",
  ["YAML-based workflow definitions", "Parallel agent execution with dependency resolution", "Human-in-the-loop approval gates", "Loop-until nodes with condition evaluation", "Real-time execution monitoring", "Template system for reusable workflows"],
  ["DAG execution engine design", "Multi-agent orchestration patterns", "Human-in-the-loop system design", "State machine implementation", "Visual workflow editor development"],
  ["ML/AI", "AI Agents", "Workflow", "Full-Stack", "Automation"])

# ============================================================
# PROJECT 11
# ============================================================
a("Infrastructure Cost Optimizer",
  "Cloud cost analysis and optimization platform with resource right-sizing, usage forecasting, and automated recommendations",
  "A platform that connects to AWS/Azure/GCP accounts, analyzes resource usage patterns, identifies cost-saving opportunities (right-sizing, reserved instances, spot instances), forecasts future costs using ML, and generates actionable optimization reports with estimated savings.",
  "Cloud costs spiral out of control without visibility into resource utilization. Teams need automated right-sizing recommendations and cost forecasting to optimize spending across multi-cloud environments.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "Celery"],
  ["Multi-cloud provider abstraction", "Batch data collection pipeline", "ML forecasting pipeline", "Recommendation engine"],
  ["boto3", "azure-mgmt-costmanagement", "XGBoost", "scikit-learn", "Celery", "Recharts", "SQLAlchemy"],
  "Intermediate",
  BP["Infrastructure Cost Optimizer"],
  ["Cost breakdown dashboard with treemap", "Resource inventory with utilization heatmap", "Recommendation cards with savings estimates", "Forecast chart with what-if scenarios", "Budget alert configuration panel", "Exportable report generator"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Leverages Tejas's AWS research background (Bytepoint Consulting) into a tangible engineering product. Adds multi-cloud experience, cost optimization expertise, and ML forecasting — directly applicable to cloud/SRE roles.",
  ["Multi-cloud account connection (AWS/Azure/GCP)", "Resource right-sizing recommendations", "Reserved instance purchase optimizer", "ML-based cost forecasting", "Budget tracking with alerts", "Optimization report export (PDF/CSV)"],
  ["Cloud provider APIs and cost models", "ML for time-series forecasting", "Multi-cloud abstraction layer design", "Cost optimization strategies", "FinOps best practices"],
  ["Cloud", "DevOps", "ML/AI", "FinOps", "Infrastructure"])

# ============================================================
# PROJECT 12
# ============================================================
a("Real-Time Dashboard Builder",
  "Drag-and-drop dashboard constructor with custom widgets, SQL data sources, and auto-refresh",
  "A self-service dashboard builder where users connect data sources (PostgreSQL, REST APIs, CSV), build interactive visualizations with a drag-and-drop editor, set up auto-refresh schedules, and share dashboards with team members. Features a library of widget types (charts, tables, gauges, maps).",
  "Teams need custom dashboards that combine data from multiple sources, but existing solutions (Grafana, Metabase) require complex setup or don't support drag-and-drop widget configuration.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "WebSockets"],
  ["Micro-frontend widget architecture", "WebSocket-driven live updates", "Multi-tenant data isolation", "Plugin system for custom widgets"],
  ["react-grid-layout", "Recharts", "SQLAlchemy", "Pydantic", "Pandas", "WebSockets", "react-query"],
  "Intermediate",
  BP["Real-Time Dashboard Builder"],
  ["Drag-and-drop grid canvas", "Widget configuration sidebar", "SQL query editor with autocomplete", "Data source connection wizard", "Dashboard template gallery", "Share and permission settings"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Demonstrates advanced frontend skills (drag-and-drop, grid layouts, widget architecture) beyond basic React. Shows data connectivity and visualization expertise — highly valued in data/platform engineering roles.",
  ["Drag-and-drop dashboard layout editor", "SQL and REST API data sources", "Auto-refresh with configurable intervals", "Widget library (charts, tables, gauges, maps)", "Dashboard template system", "Team sharing with role-based access"],
  ["Drag-and-drop UI architecture", "Micro-frontend and widget plugin patterns", "Real-time data refresh strategies", "SQL query builder implementation", "Dashboard UX design principles"],
  ["Data Visualization", "Frontend", "Full-Stack", "Real-Time", "Analytics"])

# ============================================================
# PROJECT 13
# ============================================================
a("AI-Powered Meeting Minutes & Action Tracker",
  "Speech-to-text meeting transcription with speaker diarization, action item extraction, and calendar integration",
  "A meeting intelligence platform that joins video calls, generates real-time transcripts with speaker identification, uses LLMs to extract action items, decisions, and key discussion points, and automatically creates calendar events with summaries. Includes a searchable meeting archive.",
  "Meeting notes are manually taken, incomplete, and action items get lost. Teams need automated transcription with speaker identification and structured extraction of decisions and follow-ups.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "Celery"],
  ["Event-driven processing pipeline", "Async audio streaming", "LLM-powered extraction pipeline", "Calendar API integration"],
  ["OpenAI Whisper", "LangChain", "Google Calendar API / Outlook API", "SQLAlchemy", "Celery", "WebSockets", "Pydantic"],
  "Advanced",
  BP["AI-Powered Meeting Minutes & Action Tracker"],
  ["Real-time transcript view with speaker colors", "Action item board with assignee tracking", "Meeting timeline with topic markers", "Searchable meeting archive", "Calendar integration settings", "Email summary delivery configuration"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Adds speech-to-text/Audio AI experience, real-time streaming, and calendar API integration. Shows ability to work with unstructured data (audio) and extract structured insights using LLMs.",
  ["Real-time speech-to-text transcription", "Speaker diarization (who said what)", "LLM-based action item extraction", "Automatic calendar event creation", "Email summary delivery", "Searchable meeting archive with full-text search"],
  ["Audio processing and streaming", "Speaker diarization techniques", "LLM prompt engineering for extraction", "Calendar API integration patterns", "Real-time collaborative editing"],
  ["ML/AI", "LLM", "Real-Time", "Productivity", "Full-Stack"])

# ============================================================
# PROJECT 14
# ============================================================
a("ML Data Drift Monitor & Alert System",
  "Production ML model monitoring with data drift detection, concept drift alerts, and automated retraining triggers",
  "A monitoring platform for production ML models that continuously tracks input data distributions, detects drift (data drift, concept drift, label drift), generates alerts, and can trigger automated retraining pipelines. Includes a dashboard for comparing distributions and a model health score.",
  "ML models degrade in production as data distributions shift over time. Teams need automated drift detection and alerting to maintain model performance without manual dashboard staring.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "Prometheus"],
  ["Streaming data analysis pipeline", "Statistical test automation", "Model health scoring system", "Automated retraining trigger"],
  ["Evidently AI", "scikit-learn", "XGBoost", "LightGBM", "Prometheus client", "SQLAlchemy", "Recharts", "Pandas"],
  "Advanced",
  BP["ML Data Drift Monitor & Alert System"],
  ["Model health score dashboard", "Distribution comparison charts (drift visualizer)", "Alert timeline with severity indicators", "Feature-level drift detail panels", "Automated retraining configuration", "Model performance over time charts"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Builds on Tejas's LightGBM/ML experience into MLOps monitoring — a critical skill gap. Model monitoring and drift detection are top requirements for ML engineer roles. Shows production ML thinking beyond just building models.",
  ["Data drift detection (PSI, KS test, Jensen-Shannon)", "Concept drift detection", "Model performance tracking over time", "Automated alerting with severity levels", "Retraining pipeline trigger", "Drift report generation"],
  ["ML model monitoring in production", "Statistical drift detection methods", "Evidently AI library for drift analysis", "Prometheus metrics for ML systems", "Automated ML pipeline design"],
  ["ML/AI", "MLOps", "Data Engineering", "Monitoring", "DevOps"])

# ============================================================
# PROJECT 15
# ============================================================
a("Competitive Programming Arena",
  "Online judge platform with real-time code execution, test case validation, leaderboards, and contest management",
  "A competitive programming platform where users solve algorithmic challenges with real-time code execution in sandboxed environments. Supports multiple languages (Python, Java, C++, Swift), automated test case validation, contest scheduling, rating system, and a rich problem editor.",
  "Aspiring competitive programmers lack a self-hosted platform with sandboxed multi-language execution, contest management, and rating systems similar to LeetCode or Codeforces.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "Celery"],
  ["Sandboxed code execution", "Event-driven submission pipeline", "Elo/Glicko rating system", "Real-time leaderboard updates"],
  ["Docker SDK (spawn containers)", "Celery", "WebSockets", "Monaco Editor", "SQLAlchemy", "Pydantic", "Redis-py"],
  "Advanced",
  BP["Competitive Programming Arena"],
  ["Code editor with Monaco (syntax highlighting, themes)", "Test case result panel with diff view", "Real-time contest leaderboard", "Problem statement viewer with markdown", "Submission history with status timeline", "Rating progression chart"],
  ["https://github.com/soxoj/maigret", "https://github.com/coleam00/Archon"],
  "Leverages Tejas's C++, Java, Python, Swift knowledge into a unified platform. Shows sandboxed execution, rating systems, and real-time competitive features. Demonstrates full-stack depth across multiple languages.",
  ["Multi-language code execution (Python, Java, C++, Swift)", "Docker-based sandboxed execution environment", "Custom test case validation with diff output", "Contest management with scheduling", "Elo/Glicko player rating system", "Real-time leaderboard with WebSockets"],
  ["Sandboxed code execution security", "Docker container lifecycle management", "Rating system mathematics (Elo/Glicko)", "Real-time competitive event systems", "Online judge architecture patterns"],
  ["Full-Stack", "Real-Time", "Developer Tools", "Education", "Multi-Language"])

# ============================================================
# PROJECT 16
# ============================================================
a("Hackathon Hub — Event & Project Manager",
  "Full hackathon lifecycle platform: event management, team formation, project submission, judging, and sponsor tracking",
  "A complete hackathon management platform covering the entire event lifecycle. Features include event creation with scheduling, team formation with skill matching, project submission with repo linking, multi-criteria judging with scoring rubrics, sponsor management, and real-time live leaderboards.",
  "Hackathon organizers juggle spreadsheets, multiple tools, and manual processes for team formation, project submissions, and judging. A unified platform is needed to manage the entire lifecycle.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "WebSockets"],
  ["Modular event lifecycle state machine", "Multi-tenant organization model", "Real-time scoring aggregation", "Plugin-based judging criteria"],
  ["SQLAlchemy", "Pydantic", "WebSockets", "Recharts", "react-beautiful-dnd", "date-fns", "Pandas (export)"],
  "Intermediate",
  BP["Hackathon Hub — Event & Project Manager"],
  ["Event creation wizard with timeline", "Team formation board with skill tags", "Project submission portal with GitHub integration", "Judge scorecard interface with rubrics", "Live leaderboard with WebSocket updates", "Sponsor management dashboard"],
  ["https://github.com/santifer/career-ops", "https://github.com/coleam00/Archon"],
  "Perfectly leverages Tejas's DECA/Design Society leadership experience into an engineering product. Shows event systems expertise, real-time scoring, and organizational workflow management — unique angle most SWE resumes lack.",
  ["Hackathon lifecycle management (create to archive)", "Skill-based team formation matching", "GitHub integration for project submission", "Customizable judging rubrics", "Real-time scoring and leaderboard", "Sponsor tier management"],
  ["Event lifecycle state machine design", "Team matching algorithm implementation", "Real-time aggregation and broadcasting", "Multi-criteria judging system design", "Export and reporting pipeline"],
  ["Full-Stack", "Real-Time", "Event Management", "Community", "Productivity"])

# ============================================================
# PROJECT 17
# ============================================================
a("Personal Knowledge Graph & Second Brain",
  "Note-taking with graph-based connections, semantic search, auto-tagging, and spaced repetition flashcards",
  "A personal knowledge management system that stores notes as nodes in a graph database, automatically suggests connections between related notes using embeddings, provides semantic search, and generates spaced repetition flashcards from notes. Features a rich markdown editor and graph visualization.",
  "Traditional note-taking apps lack intelligent connections between ideas. Users want a second brain that surfaces related notes, suggests links, and reinforces learning through spaced repetition.",
  ["FastAPI", "React", "TypeScript", "Neo4j", "Docker", "Redis", "PostgreSQL"],
  ["Graph database for knowledge representation", "Embedding-based similarity search", "Event-driven suggestion pipeline", "Spaced repetition algorithm"],
  ["Neo4j Python driver", "OpenAI/Gemini embeddings", "react-force-graph-2d", "TipTap editor", "SQLAlchemy", "Pydantic"],
  "Intermediate",
  BP["Personal Knowledge Graph & Second Brain"],
  ["Interactive knowledge graph visualization", "Rich markdown editor (TipTap)", "Note detail panel with backlinks", "Auto-suggestion sidebar", "Flashcard review interface (spaced repetition)", "Tag and filter sidebar"],
  ["https://github.com/coleam00/Archon", "https://github.com/soxoj/maigret"],
  "Second Neo4j project reinforcing graph database skills. Adds rich text editing, embedding-based recommendations, and spaced repetition algorithms. Shows ability to build complex, interconnected data models.",
  ["Graph-based note organization", "AI-powered connection suggestions", "Semantic search across notes", "Auto-generated spaced repetition flashcards", "Markdown editing with live preview", "Backlink and reference tracking"],
  ["Graph database modeling for knowledge", "Text embedding and similarity search", "Spaced repetition algorithm (SM-2)", "Rich text editor integration", "Graph visualization with force-directed layouts"],
  ["Graph Database", "ML/AI", "Productivity", "Full-Stack", "Knowledge Management"])

# ============================================================
# PROJECT 18
# ============================================================
a("API Security Fuzzer & Vulnerability Scanner",
  "Automated API security testing with intelligent fuzzing, OWASP top 10 detection, and CI/CD integration",
  "A security testing tool that takes an OpenAPI spec, generates intelligent fuzz payloads, tests endpoints for OWASP Top 10 vulnerabilities (injection, broken auth, excessive data exposure, etc.), and produces detailed security reports. Integrates with CI/CD pipelines via CLI and GitHub Actions.",
  "API security testing is often manual or requires expensive commercial scanners. Teams need an open-source, automated fuzzer that integrates directly into their CI/CD pipeline.",
  ["FastAPI", "React", "TypeScript", "PostgreSQL", "Docker", "Redis", "Celery"],
  ["Plugin-based payload generator", "CI/CD pipeline integration", "Parallel security testing engine", "Report generation pipeline"],
  ["httpx", "Pydantic", "Jinja2", "Celery", "Recharts", "react-syntax-highlighter", "OpenAPI parser"],
  "Advanced",
  BP["API Security Fuzzer & Vulnerability Scanner"],
  ["API endpoint explorer with security scores", "Fuzz testing configuration wizard", "Vulnerability detail panel with remediation steps", "CI/CD integration setup guide", "Security trend dashboard over time", "Report preview and export (PDF/HTML)"],
  ["https://github.com/soxoj/maigret", "https://github.com/santifer/career-ops"],
  "Adds security engineering expertise — a high-demand skill area. Shows CI/CD integration, fuzz testing methodologies, and OWASP knowledge. Security engineers are consistently in short supply.",
  ["OpenAPI spec parsing and endpoint discovery", "Intelligent fuzz payload generation", "OWASP Top 10 vulnerability detection", "Parallel async security testing", "CI/CD integration (GitHub Actions, CLI)", "Detailed security reports with remediation"],
  ["API security testing methodologies", "Fuzz testing and payload generation", "OWASP Top 10 vulnerability patterns", "CI/CD pipeline integration patterns", "Security report generation standards"],
  ["Security", "API", "DevOps", "Testing", "Automation"])


if __name__ == "__main__":
    seed()
