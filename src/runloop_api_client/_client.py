# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import TYPE_CHECKING, Any, Mapping
from typing_extensions import Self, override

import httpx

from . import _exceptions
from ._qs import Querystring
from ._types import (
    Omit,
    Timeout,
    NotGiven,
    Transport,
    ProxiesTypes,
    RequestOptions,
    not_given,
)
from ._utils import is_given, get_async_library
from ._compat import cached_property
from ._version import __version__
from ._streaming import Stream as Stream, AsyncStream as AsyncStream
from ._exceptions import RunloopError, APIStatusError
from ._base_client import (
    DEFAULT_MAX_RETRIES,
    SyncAPIClient,
    AsyncAPIClient,
)

if TYPE_CHECKING:
    from .resources import agents, objects, secrets, devboxes, scenarios, benchmarks, blueprints, repositories
    from .resources.agents import AgentsResource, AsyncAgentsResource
    from .resources.objects import ObjectsResource, AsyncObjectsResource
    from .resources.secrets import SecretsResource, AsyncSecretsResource
    from .resources.blueprints import BlueprintsResource, AsyncBlueprintsResource
    from .resources.repositories import RepositoriesResource, AsyncRepositoriesResource
    from .resources.devboxes.devboxes import DevboxesResource, AsyncDevboxesResource
    from .resources.scenarios.scenarios import ScenariosResource, AsyncScenariosResource
    from .resources.benchmarks.benchmarks import BenchmarksResource, AsyncBenchmarksResource

__all__ = ["Timeout", "Transport", "ProxiesTypes", "RequestOptions", "Runloop", "AsyncRunloop", "Client", "AsyncClient"]


class Runloop(SyncAPIClient):
    # client options
    bearer_token: str

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#client) for more details.
        http_client: httpx.Client | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new synchronous Runloop client instance.

        This automatically infers the `bearer_token` argument from the `RUNLOOP_API_KEY` environment variable if it is not provided.
        """
        if bearer_token is None:
            bearer_token = os.environ.get("RUNLOOP_API_KEY")
        if bearer_token is None:
            raise RunloopError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the RUNLOOP_API_KEY environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("RUNLOOP_BASE_URL")
        if base_url is None:
            base_url = f"https://api.runloop.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._idempotency_header = "x-request-id"

    @cached_property
    def benchmarks(self) -> BenchmarksResource:
        from .resources.benchmarks import BenchmarksResource

        return BenchmarksResource(self)

    @cached_property
    def agents(self) -> AgentsResource:
        from .resources.agents import AgentsResource

        return AgentsResource(self)

    @cached_property
    def blueprints(self) -> BlueprintsResource:
        from .resources.blueprints import BlueprintsResource

        return BlueprintsResource(self)

    @cached_property
    def devboxes(self) -> DevboxesResource:
        from .resources.devboxes import DevboxesResource

        return DevboxesResource(self)

    @cached_property
    def scenarios(self) -> ScenariosResource:
        from .resources.scenarios import ScenariosResource

        return ScenariosResource(self)

    @cached_property
    def objects(self) -> ObjectsResource:
        from .resources.objects import ObjectsResource

        return ObjectsResource(self)

    @cached_property
    def repositories(self) -> RepositoriesResource:
        from .resources.repositories import RepositoriesResource

        return RepositoriesResource(self)

    @cached_property
    def secrets(self) -> SecretsResource:
        from .resources.secrets import SecretsResource

        return SecretsResource(self)

    @cached_property
    def with_raw_response(self) -> RunloopWithRawResponse:
        return RunloopWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> RunloopWithStreamedResponse:
        return RunloopWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": "false",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.Client | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class AsyncRunloop(AsyncAPIClient):
    # client options
    bearer_token: str

    def __init__(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        max_retries: int = DEFAULT_MAX_RETRIES,
        default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        # Configure a custom httpx client.
        # We provide a `DefaultAsyncHttpxClient` class that you can pass to retain the default values we use for `limits`, `timeout` & `follow_redirects`.
        # See the [httpx documentation](https://www.python-httpx.org/api/#asyncclient) for more details.
        http_client: httpx.AsyncClient | None = None,
        # Enable or disable schema validation for data returned by the API.
        # When enabled an error APIResponseValidationError is raised
        # if the API responds with invalid data for the expected schema.
        #
        # This parameter may be removed or changed in the future.
        # If you rely on this feature, please open a GitHub issue
        # outlining your use-case to help us decide if it should be
        # part of our public interface in the future.
        _strict_response_validation: bool = False,
    ) -> None:
        """Construct a new async AsyncRunloop client instance.

        This automatically infers the `bearer_token` argument from the `RUNLOOP_API_KEY` environment variable if it is not provided.
        """
        if bearer_token is None:
            bearer_token = os.environ.get("RUNLOOP_API_KEY")
        if bearer_token is None:
            raise RunloopError(
                "The bearer_token client option must be set either by passing bearer_token to the client or by setting the RUNLOOP_API_KEY environment variable"
            )
        self.bearer_token = bearer_token

        if base_url is None:
            base_url = os.environ.get("RUNLOOP_BASE_URL")
        if base_url is None:
            base_url = f"https://api.runloop.ai"

        super().__init__(
            version=__version__,
            base_url=base_url,
            max_retries=max_retries,
            timeout=timeout,
            http_client=http_client,
            custom_headers=default_headers,
            custom_query=default_query,
            _strict_response_validation=_strict_response_validation,
        )

        self._idempotency_header = "x-request-id"

    @cached_property
    def benchmarks(self) -> AsyncBenchmarksResource:
        from .resources.benchmarks import AsyncBenchmarksResource

        return AsyncBenchmarksResource(self)

    @cached_property
    def agents(self) -> AsyncAgentsResource:
        from .resources.agents import AsyncAgentsResource

        return AsyncAgentsResource(self)

    @cached_property
    def blueprints(self) -> AsyncBlueprintsResource:
        from .resources.blueprints import AsyncBlueprintsResource

        return AsyncBlueprintsResource(self)

    @cached_property
    def devboxes(self) -> AsyncDevboxesResource:
        from .resources.devboxes import AsyncDevboxesResource

        return AsyncDevboxesResource(self)

    @cached_property
    def scenarios(self) -> AsyncScenariosResource:
        from .resources.scenarios import AsyncScenariosResource

        return AsyncScenariosResource(self)

    @cached_property
    def objects(self) -> AsyncObjectsResource:
        from .resources.objects import AsyncObjectsResource

        return AsyncObjectsResource(self)

    @cached_property
    def repositories(self) -> AsyncRepositoriesResource:
        from .resources.repositories import AsyncRepositoriesResource

        return AsyncRepositoriesResource(self)

    @cached_property
    def secrets(self) -> AsyncSecretsResource:
        from .resources.secrets import AsyncSecretsResource

        return AsyncSecretsResource(self)

    @cached_property
    def with_raw_response(self) -> AsyncRunloopWithRawResponse:
        return AsyncRunloopWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncRunloopWithStreamedResponse:
        return AsyncRunloopWithStreamedResponse(self)

    @property
    @override
    def qs(self) -> Querystring:
        return Querystring(array_format="comma")

    @property
    @override
    def auth_headers(self) -> dict[str, str]:
        bearer_token = self.bearer_token
        return {"Authorization": f"Bearer {bearer_token}"}

    @property
    @override
    def default_headers(self) -> dict[str, str | Omit]:
        return {
            **super().default_headers,
            "X-Stainless-Async": f"async:{get_async_library()}",
            **self._custom_headers,
        }

    def copy(
        self,
        *,
        bearer_token: str | None = None,
        base_url: str | httpx.URL | None = None,
        timeout: float | Timeout | None | NotGiven = not_given,
        http_client: httpx.AsyncClient | None = None,
        max_retries: int | NotGiven = not_given,
        default_headers: Mapping[str, str] | None = None,
        set_default_headers: Mapping[str, str] | None = None,
        default_query: Mapping[str, object] | None = None,
        set_default_query: Mapping[str, object] | None = None,
        _extra_kwargs: Mapping[str, Any] = {},
    ) -> Self:
        """
        Create a new client instance re-using the same options given to the current client with optional overriding.
        """
        if default_headers is not None and set_default_headers is not None:
            raise ValueError("The `default_headers` and `set_default_headers` arguments are mutually exclusive")

        if default_query is not None and set_default_query is not None:
            raise ValueError("The `default_query` and `set_default_query` arguments are mutually exclusive")

        headers = self._custom_headers
        if default_headers is not None:
            headers = {**headers, **default_headers}
        elif set_default_headers is not None:
            headers = set_default_headers

        params = self._custom_query
        if default_query is not None:
            params = {**params, **default_query}
        elif set_default_query is not None:
            params = set_default_query

        http_client = http_client or self._client
        return self.__class__(
            bearer_token=bearer_token or self.bearer_token,
            base_url=base_url or self.base_url,
            timeout=self.timeout if isinstance(timeout, NotGiven) else timeout,
            http_client=http_client,
            max_retries=max_retries if is_given(max_retries) else self.max_retries,
            default_headers=headers,
            default_query=params,
            **_extra_kwargs,
        )

    # Alias for `copy` for nicer inline usage, e.g.
    # client.with_options(timeout=10).foo.create(...)
    with_options = copy

    @override
    def _make_status_error(
        self,
        err_msg: str,
        *,
        body: object,
        response: httpx.Response,
    ) -> APIStatusError:
        if response.status_code == 400:
            return _exceptions.BadRequestError(err_msg, response=response, body=body)

        if response.status_code == 401:
            return _exceptions.AuthenticationError(err_msg, response=response, body=body)

        if response.status_code == 403:
            return _exceptions.PermissionDeniedError(err_msg, response=response, body=body)

        if response.status_code == 404:
            return _exceptions.NotFoundError(err_msg, response=response, body=body)

        if response.status_code == 409:
            return _exceptions.ConflictError(err_msg, response=response, body=body)

        if response.status_code == 422:
            return _exceptions.UnprocessableEntityError(err_msg, response=response, body=body)

        if response.status_code == 429:
            return _exceptions.RateLimitError(err_msg, response=response, body=body)

        if response.status_code >= 500:
            return _exceptions.InternalServerError(err_msg, response=response, body=body)
        return APIStatusError(err_msg, response=response, body=body)


class RunloopWithRawResponse:
    _client: Runloop

    def __init__(self, client: Runloop) -> None:
        self._client = client

    @cached_property
    def benchmarks(self) -> benchmarks.BenchmarksResourceWithRawResponse:
        from .resources.benchmarks import BenchmarksResourceWithRawResponse

        return BenchmarksResourceWithRawResponse(self._client.benchmarks)

    @cached_property
    def agents(self) -> agents.AgentsResourceWithRawResponse:
        from .resources.agents import AgentsResourceWithRawResponse

        return AgentsResourceWithRawResponse(self._client.agents)

    @cached_property
    def blueprints(self) -> blueprints.BlueprintsResourceWithRawResponse:
        from .resources.blueprints import BlueprintsResourceWithRawResponse

        return BlueprintsResourceWithRawResponse(self._client.blueprints)

    @cached_property
    def devboxes(self) -> devboxes.DevboxesResourceWithRawResponse:
        from .resources.devboxes import DevboxesResourceWithRawResponse

        return DevboxesResourceWithRawResponse(self._client.devboxes)

    @cached_property
    def scenarios(self) -> scenarios.ScenariosResourceWithRawResponse:
        from .resources.scenarios import ScenariosResourceWithRawResponse

        return ScenariosResourceWithRawResponse(self._client.scenarios)

    @cached_property
    def objects(self) -> objects.ObjectsResourceWithRawResponse:
        from .resources.objects import ObjectsResourceWithRawResponse

        return ObjectsResourceWithRawResponse(self._client.objects)

    @cached_property
    def repositories(self) -> repositories.RepositoriesResourceWithRawResponse:
        from .resources.repositories import RepositoriesResourceWithRawResponse

        return RepositoriesResourceWithRawResponse(self._client.repositories)

    @cached_property
    def secrets(self) -> secrets.SecretsResourceWithRawResponse:
        from .resources.secrets import SecretsResourceWithRawResponse

        return SecretsResourceWithRawResponse(self._client.secrets)


class AsyncRunloopWithRawResponse:
    _client: AsyncRunloop

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    @cached_property
    def benchmarks(self) -> benchmarks.AsyncBenchmarksResourceWithRawResponse:
        from .resources.benchmarks import AsyncBenchmarksResourceWithRawResponse

        return AsyncBenchmarksResourceWithRawResponse(self._client.benchmarks)

    @cached_property
    def agents(self) -> agents.AsyncAgentsResourceWithRawResponse:
        from .resources.agents import AsyncAgentsResourceWithRawResponse

        return AsyncAgentsResourceWithRawResponse(self._client.agents)

    @cached_property
    def blueprints(self) -> blueprints.AsyncBlueprintsResourceWithRawResponse:
        from .resources.blueprints import AsyncBlueprintsResourceWithRawResponse

        return AsyncBlueprintsResourceWithRawResponse(self._client.blueprints)

    @cached_property
    def devboxes(self) -> devboxes.AsyncDevboxesResourceWithRawResponse:
        from .resources.devboxes import AsyncDevboxesResourceWithRawResponse

        return AsyncDevboxesResourceWithRawResponse(self._client.devboxes)

    @cached_property
    def scenarios(self) -> scenarios.AsyncScenariosResourceWithRawResponse:
        from .resources.scenarios import AsyncScenariosResourceWithRawResponse

        return AsyncScenariosResourceWithRawResponse(self._client.scenarios)

    @cached_property
    def objects(self) -> objects.AsyncObjectsResourceWithRawResponse:
        from .resources.objects import AsyncObjectsResourceWithRawResponse

        return AsyncObjectsResourceWithRawResponse(self._client.objects)

    @cached_property
    def repositories(self) -> repositories.AsyncRepositoriesResourceWithRawResponse:
        from .resources.repositories import AsyncRepositoriesResourceWithRawResponse

        return AsyncRepositoriesResourceWithRawResponse(self._client.repositories)

    @cached_property
    def secrets(self) -> secrets.AsyncSecretsResourceWithRawResponse:
        from .resources.secrets import AsyncSecretsResourceWithRawResponse

        return AsyncSecretsResourceWithRawResponse(self._client.secrets)


class RunloopWithStreamedResponse:
    _client: Runloop

    def __init__(self, client: Runloop) -> None:
        self._client = client

    @cached_property
    def benchmarks(self) -> benchmarks.BenchmarksResourceWithStreamingResponse:
        from .resources.benchmarks import BenchmarksResourceWithStreamingResponse

        return BenchmarksResourceWithStreamingResponse(self._client.benchmarks)

    @cached_property
    def agents(self) -> agents.AgentsResourceWithStreamingResponse:
        from .resources.agents import AgentsResourceWithStreamingResponse

        return AgentsResourceWithStreamingResponse(self._client.agents)

    @cached_property
    def blueprints(self) -> blueprints.BlueprintsResourceWithStreamingResponse:
        from .resources.blueprints import BlueprintsResourceWithStreamingResponse

        return BlueprintsResourceWithStreamingResponse(self._client.blueprints)

    @cached_property
    def devboxes(self) -> devboxes.DevboxesResourceWithStreamingResponse:
        from .resources.devboxes import DevboxesResourceWithStreamingResponse

        return DevboxesResourceWithStreamingResponse(self._client.devboxes)

    @cached_property
    def scenarios(self) -> scenarios.ScenariosResourceWithStreamingResponse:
        from .resources.scenarios import ScenariosResourceWithStreamingResponse

        return ScenariosResourceWithStreamingResponse(self._client.scenarios)

    @cached_property
    def objects(self) -> objects.ObjectsResourceWithStreamingResponse:
        from .resources.objects import ObjectsResourceWithStreamingResponse

        return ObjectsResourceWithStreamingResponse(self._client.objects)

    @cached_property
    def repositories(self) -> repositories.RepositoriesResourceWithStreamingResponse:
        from .resources.repositories import RepositoriesResourceWithStreamingResponse

        return RepositoriesResourceWithStreamingResponse(self._client.repositories)

    @cached_property
    def secrets(self) -> secrets.SecretsResourceWithStreamingResponse:
        from .resources.secrets import SecretsResourceWithStreamingResponse

        return SecretsResourceWithStreamingResponse(self._client.secrets)


class AsyncRunloopWithStreamedResponse:
    _client: AsyncRunloop

    def __init__(self, client: AsyncRunloop) -> None:
        self._client = client

    @cached_property
    def benchmarks(self) -> benchmarks.AsyncBenchmarksResourceWithStreamingResponse:
        from .resources.benchmarks import AsyncBenchmarksResourceWithStreamingResponse

        return AsyncBenchmarksResourceWithStreamingResponse(self._client.benchmarks)

    @cached_property
    def agents(self) -> agents.AsyncAgentsResourceWithStreamingResponse:
        from .resources.agents import AsyncAgentsResourceWithStreamingResponse

        return AsyncAgentsResourceWithStreamingResponse(self._client.agents)

    @cached_property
    def blueprints(self) -> blueprints.AsyncBlueprintsResourceWithStreamingResponse:
        from .resources.blueprints import AsyncBlueprintsResourceWithStreamingResponse

        return AsyncBlueprintsResourceWithStreamingResponse(self._client.blueprints)

    @cached_property
    def devboxes(self) -> devboxes.AsyncDevboxesResourceWithStreamingResponse:
        from .resources.devboxes import AsyncDevboxesResourceWithStreamingResponse

        return AsyncDevboxesResourceWithStreamingResponse(self._client.devboxes)

    @cached_property
    def scenarios(self) -> scenarios.AsyncScenariosResourceWithStreamingResponse:
        from .resources.scenarios import AsyncScenariosResourceWithStreamingResponse

        return AsyncScenariosResourceWithStreamingResponse(self._client.scenarios)

    @cached_property
    def objects(self) -> objects.AsyncObjectsResourceWithStreamingResponse:
        from .resources.objects import AsyncObjectsResourceWithStreamingResponse

        return AsyncObjectsResourceWithStreamingResponse(self._client.objects)

    @cached_property
    def repositories(self) -> repositories.AsyncRepositoriesResourceWithStreamingResponse:
        from .resources.repositories import AsyncRepositoriesResourceWithStreamingResponse

        return AsyncRepositoriesResourceWithStreamingResponse(self._client.repositories)

    @cached_property
    def secrets(self) -> secrets.AsyncSecretsResourceWithStreamingResponse:
        from .resources.secrets import AsyncSecretsResourceWithStreamingResponse

        return AsyncSecretsResourceWithStreamingResponse(self._client.secrets)


Client = Runloop

AsyncClient = AsyncRunloop
