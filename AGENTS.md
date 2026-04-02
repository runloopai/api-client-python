# Agent Workflow Guidelines

## Making Code Changes

When making changes to the codebase, follow this workflow to ensure code quality:

### 1. Run Lint Before Changes

Before making any code changes, run the linter to establish a baseline:

```bash
./scripts/lint
```

This runs:
- `pyright` - Type checking
- `mypy` - Additional type checking
- `ruff check` - Code linting
- `ruff format --check` - Format checking
- Import validation

### 2. Make Your Changes

Make the necessary code changes, ensuring you:
- Follow existing code patterns
- Update type annotations
- Handle edge cases (e.g., `Omit`, `NotGiven`, `None`)
- Maintain backward compatibility

### 3. Update Tests

Update or add tests for your changes:
- Unit tests in `tests/`
- Smoke tests in `tests/smoketests/`
- Ensure tests match the new behavior

### 4. Run Lint After Changes

After making changes, run the linter again to catch any issues:

```bash
./scripts/lint
```

Fix any new errors or warnings that appear.

### 5. Run Tests

Run the test suite to ensure everything works:

```bash
# Run all tests
uv run pytest

# Run specific tests
uv run pytest tests/test_axon_sse_reconnect.py -xvs

# Run smoke tests
uv run pytest tests/smoketests/ -m smoketest
```

### 6. Commit Changes

Once lint and tests pass, commit your changes:

```bash
git add -A
git commit -m "type: description

Detailed explanation of changes

Co-Authored-By: Claude Sonnet 4.5 <noreply@anthropic.com>"
```

## Common Patterns

### Handling Optional Parameters

When dealing with parameters that can be omitted:

```python
# Parameter definition
def method(self, param: int | Omit = omit):
    ...

# In implementation, check for Omit before using
if not isinstance(param, Omit):
    use_param(param)
else:
    # param was omitted, use default behavior
    pass
```

### Type-Safe Transformations

The `transform` function automatically filters out `Omit` and `NotGiven` values:

```python
# This dict with omitted values
{"field": omit, "other": 123}

# Becomes this after transform
{"other": 123}
```

### Testing with Mocks

When testing methods that call `_get` or similar:

```python
with patch.object(client.resource, "_get") as mock_get:
    mock_stream = Mock(spec=Stream)
    mock_get.return_value = mock_stream

    # Your test code
    result = client.resource.method()

    # Verify the call
    call_args = mock_get.call_args
    options = call_args.kwargs["options"]
    assert options["params"]["field"] == expected_value
```

## Merge Conflict Resolution

When merging branches:

1. **Understand both changes** - Read the diff from both sides
2. **Combine features intelligently** - Don't just pick one side
3. **Update tests** - Tests may need adjustments for merged behavior
4. **Fix type errors** - Merges can introduce type mismatches
5. **Validate syntax** - Run `python3 -m py_compile` on changed files
6. **Run full lint** - Ensure everything passes

## Example: Recent Merge Fix

The merge of `origin/main` into `feature/ts-pr-765-port` required:

1. **Code fix** - Handle `Omit` type properly in reconnection logic
2. **Test fix** - Update assertions from `is None` to `not in dict`
3. **Syntax check** - Verify Python syntax is valid
4. **Type check** - Ensure mypy/pyright pass

See commit history for the resolution pattern.
