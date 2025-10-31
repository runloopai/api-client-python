# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import httpx

RAW_RESPONSE_HEADER = "X-Stainless-Raw-Response"
OVERRIDE_CAST_TO_HEADER = "____stainless_override_cast_to"

# default timeout is 30 seconds
DEFAULT_TIMEOUT = httpx.Timeout(timeout=30, connect=5.0)
DEFAULT_MAX_RETRIES = 5
DEFAULT_CONNECTION_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)

INITIAL_RETRY_DELAY = 1.0
MAX_RETRY_DELAY = 60.0

# Maximum allowed size (in bytes) for individual entries in `file_mounts` when creating Blueprints
FILE_MOUNT_MAX_SIZE_BYTES = 512 * 1024

# Maximum allowed total size (in bytes) across all `file_mounts` when creating Blueprints
FILE_MOUNT_TOTAL_MAX_SIZE_BYTES = 1024 * 1024
