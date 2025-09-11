# Smoke tests

End-to-end smoke tests run against the real API to validate critical flows (devboxes, snapshots, blueprints, executions/log tailing, scenarios/benchmarks). Theses smoketests run both the 
async and sync clients.

- Local run (requires `RUNLOOP_API_KEY`):

```bash
export RUNLOOP_API_KEY=...  # required
# optionally override API base
# export RUNLOOP_BASE_URL=https://api.runloop.ai

# Install deps and run via uv
uv pip install -r requirements-dev.lock

# Run all tests
RUN_SMOKETESTS=1 uv run pytest -q -vv -m smoketest tests/smoketests

# Run a single file
RUN_SMOKETESTS=1 uv run pytest -q -vv -m smoketest tests/smoketests/test_devboxes.py

# Run a single test by name
RUN_SMOKETESTS=1 uv run pytest -q -k -m smoketest "test_create_and_await_running_timeout" tests/smoketests/test_devboxes.py
```

- GitHub Actions: add repo secret `RUNLOOP_SMOKETEST_DEV_API_KEY` and `RUNLOOP_SMOKETEST_PROD_API_KEY`. The workflow `.github/workflows/smoketests.yml` supports an input `environment` (dev|prod) and runs these tests in CI.


