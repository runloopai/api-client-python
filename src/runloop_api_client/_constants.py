# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

import httpx

RAW_RESPONSE_HEADER = "X-Stainless-Raw-Response"
OVERRIDE_CAST_TO_HEADER = "____stainless_override_cast_to"

# default timeout is 30 seconds
DEFAULT_TIMEOUT = httpx.Timeout(timeout=30, connect=5.0)
DEFAULT_MAX_RETRIES = 3
DEFAULT_CONNECTION_LIMITS = httpx.Limits(max_connections=100, max_keepalive_connections=20)

INITIAL_RETRY_DELAY = 1.0
MAX_RETRY_DELAY = 15.0
