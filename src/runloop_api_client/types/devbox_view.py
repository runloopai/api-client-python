# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from typing import Dict, List, Optional
from typing_extensions import Literal

from .._models import BaseModel
from .tunnel_view import TunnelView
from .shared.launch_parameters import LaunchParameters

__all__ = ["DevboxView", "StateTransition", "GatewaySpecs", "McpSpecs"]


class StateTransition(BaseModel):
    status: Optional[
        Literal[
            "scheduled",
            "provisioning",
            "initializing",
            "running",
            "suspending",
            "suspended",
            "resuming",
            "failure",
            "shutdown",
        ]
    ] = None
    """The status of the Devbox.

    scheduled: The Devbox is scheduled to run but infrastructure allocation has not
    started yet. provisioning: Runloop is allocating and booting the necessary
    infrastructure resources. initializing: Runloop defined boot scripts are running
    to enable the environment for interaction. running: The Devbox is ready for
    interaction. suspending: The Devbox disk is being snapshotted as part of
    suspension. suspended: The Devbox disk is saved and no more active compute is
    being used for the Devbox. resuming: The Devbox disk is being loaded as part of
    booting a suspended Devbox. failure: The Devbox failed as part of booting or
    running user requested actions. shutdown: The Devbox was successfully shutdown
    and no more active compute is being used.
    """

    transition_time_ms: Optional[object] = None
    """The time the status change occurred"""


class GatewaySpecs(BaseModel):
    gateway_config_id: str
    """The ID of the gateway config (e.g., gwc_123abc)."""

    secret_id: str
    """The ID of the secret containing the credential."""


class McpSpecs(BaseModel):
    mcp_config_id: str
    """The ID of the MCP config (e.g., mcp_123abc)."""

    secret_id: str
    """The ID of the secret containing the credential."""


class DevboxView(BaseModel):
    """A Devbox represents a virtual development environment.

    It is an isolated sandbox that can be given to agents and used to run arbitrary code such as AI generated code.
    """

    id: str
    """The ID of the Devbox."""

    capabilities: List[Literal["unknown", "docker_in_docker"]]
    """A list of capability groups this devbox has access to."""

    create_time_ms: int
    """Creation time of the Devbox (Unix timestamp milliseconds)."""

    end_time_ms: Optional[int] = None
    """The time the Devbox finished execution (Unix timestamp milliseconds).

    Present if the Devbox is in a terminal state.
    """

    launch_parameters: LaunchParameters
    """The launch parameters used to create the Devbox."""

    metadata: Dict[str, str]
    """The user defined Devbox metadata."""

    state_transitions: List[StateTransition]
    """A list of state transitions in order with durations"""

    status: Literal[
        "scheduled",
        "provisioning",
        "initializing",
        "running",
        "suspending",
        "suspended",
        "resuming",
        "failure",
        "shutdown",
    ]
    """The current status of the Devbox."""

    blueprint_id: Optional[str] = None
    """
    The Blueprint ID used in creation of the Devbox, if the devbox was created from
    a Blueprint.
    """

    failure_reason: Optional[Literal["out_of_memory", "out_of_disk", "execution_failed", "health_check_failed"]] = None
    """The category of failure experienced by the Devbox.

    out_of_memory: The Devbox ran out of memory at runtime. Use launch parameters to
    request a larger resource size. out_of_disk: The Devbox ran out of disk at
    runtime. Please reach out to support for us to better support your use case.
    execution_failed: The Devbox failed at runtime. Please use the dashboard to look
    at the logs of the failure. health_check_failed: The Devbox failed its health
    checks. This may indicate resource utilization is close to the maximum. Consider
    requesting a larger resource size.
    """

    gateway_specs: Optional[Dict[str, GatewaySpecs]] = None
    """Gateway specifications configured for this devbox.

    Map key is the environment variable prefix (e.g., 'GWS_ANTHROPIC').
    """

    initiator_id: Optional[str] = None
    """The ID of the initiator that created the Devbox."""

    initiator_type: Optional[Literal["unknown", "api", "scenario", "scoring_validation", "reflex"]] = None
    """The type of initiator that created the Devbox."""

    mcp_specs: Optional[Dict[str, McpSpecs]] = None
    """[Beta] MCP specifications configured for this devbox.

    Map key is the environment variable name for the MCP token envelope. Each spec
    links an MCP config to a secret for MCP server access through the MCP hub.
    """

    name: Optional[str] = None
    """The name of the Devbox."""

    shutdown_reason: Optional[
        Literal["api_shutdown", "keep_alive_timeout", "entrypoint_exit", "idle", "ttl_expired"]
    ] = None
    """The reason that caused the transition of the Devbox to the shutown state.

    api_shutdown: The Devbox shutdown due to API request. entrypoint_exit: The
    Devbox entrypoint program completed. idle: The Devbox shutdown due to configured
    action on idle configuration. ttl_expired: The Devbox shutdown due to TTL
    expiration.
    """

    snapshot_id: Optional[str] = None
    """
    The Snapshot ID used in creation of the Devbox, if the devbox was created from a
    Snapshot.
    """

    tunnel: Optional[TunnelView] = None
    """A V2 tunnel provides secure HTTP access to services running on a Devbox.

    Tunnels allow external clients to reach web servers, APIs, or other HTTP
    services running inside a Devbox without requiring direct network access. Each
    tunnel is uniquely identified by an encrypted tunnel_key and can be configured
    for either open (public) or authenticated access. Usage:
    https://{port}-{tunnel_key}.tunnel.runloop.ai. Authenticated tunnels should pass
    auth_token as X-Runloop-Tunnel-Authorization: Bearer {auth_token}.
    """
