# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import httpx

from ..._types import NOT_GIVEN, Body, Query, Headers, NotGiven
from ..._utils import maybe_transform, async_maybe_transform
from ..._compat import cached_property
from ..._resource import SyncAPIResource, AsyncAPIResource
from ..._response import (
    to_raw_response_wrapper,
    to_streamed_response_wrapper,
    async_to_raw_response_wrapper,
    async_to_streamed_response_wrapper,
)
from ..._base_client import make_request_options
from ...types.devboxes import (
    FileUri,
    FilePath,
    SymbolType,
    lsp_file_params,
    lsp_formatting_params,
    lsp_references_params,
    lsp_diagnostics_params,
    lsp_code_actions_params,
    lsp_file_definition_params,
    lsp_document_symbols_params,
    lsp_apply_code_action_params,
    lsp_get_signature_help_params,
    lsp_set_watch_directory_params,
    lsp_get_code_segment_info_params,
    lsp_get_code_actions_for_diagnostic_params,
)
from ...types.devboxes.file_uri import FileUri
from ...types.devboxes.file_path import FilePath
from ...types.devboxes.range_param import RangeParam
from ...types.devboxes.symbol_type import SymbolType
from ...types.devboxes.base_command_param import BaseCommandParam
from ...types.devboxes.lsp_files_response import LspFilesResponse
from ...types.devboxes.formatting_response import FormattingResponse
from ...types.devboxes.references_response import ReferencesResponse
from ...types.devboxes.diagnostics_response import DiagnosticsResponse
from ...types.devboxes.base_diagnostic_param import BaseDiagnosticParam
from ...types.devboxes.code_actions_response import CodeActionsResponse
from ...types.devboxes.file_contents_response import FileContentsResponse
from ...types.devboxes.health_status_response import HealthStatusResponse
from ...types.devboxes.signature_help_response import SignatureHelpResponse
from ...types.devboxes.document_symbol_response import DocumentSymbolResponse
from ...types.devboxes.file_definition_response import FileDefinitionResponse
from ...types.devboxes.base_workspace_edit_param import BaseWorkspaceEditParam
from ...types.devboxes.code_action_context_param import CodeActionContextParam
from ...types.devboxes.code_segment_info_response import CodeSegmentInfoResponse
from ...types.devboxes.code_action_application_result import CodeActionApplicationResult
from ...types.devboxes.lsp_get_code_actions_for_diagnostic_response import LspGetCodeActionsForDiagnosticResponse

__all__ = ["LspResource", "AsyncLspResource"]


class LspResource(SyncAPIResource):
    @cached_property
    def with_raw_response(self) -> LspResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return LspResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> LspResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return LspResourceWithStreamingResponse(self)

    def apply_code_action(
        self,
        id: str,
        *,
        title: str,
        command: BaseCommandParam | NotGiven = NOT_GIVEN,
        edit: BaseWorkspaceEditParam | NotGiven = NOT_GIVEN,
        is_preferred: bool | NotGiven = NOT_GIVEN,
        kind: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> CodeActionApplicationResult:
        """
        Apply a code action to a given code segment not all code actions are supported
        yet

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/apply-code-action",
            body=maybe_transform(
                {
                    "title": title,
                    "command": command,
                    "edit": edit,
                    "is_preferred": is_preferred,
                    "kind": kind,
                },
                lsp_apply_code_action_params.LspApplyCodeActionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CodeActionApplicationResult,
        )

    def code_actions(
        self,
        id: str,
        *,
        uri: str,
        context: CodeActionContextParam | NotGiven = NOT_GIVEN,
        range: RangeParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> CodeActionsResponse:
        """Get code actions for a part of a document.

        This method calls the
        `getCodeActions` method of the `LanguageService` class, which in turn
        communicates with the TypeScript language server to retrieve code actions for a
        given document.
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_codeAction

        Args:
          context: Contains additional diagnostic information about the context in which a {@link
              CodeActionProvider.provideCodeActions code action} is run. The CodeActionContext
              namespace provides helper functions to work with {@link CodeActionContext}
              literals.

          range: A range in a text document expressed as (zero-based) start and end positions.

              If you want to specify a range that contains a line including the line ending
              character(s) then use an end position denoting the start of the next line. For
              example:

              ```ts
              {
                  start: { line: 5, character: 23 }
                  end : { line 6, character : 0 }
              }
              ```

              The Range namespace provides helper functions to work with {@link Range}
              literals.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/code-actions",
            body=maybe_transform(
                {
                    "uri": uri,
                    "context": context,
                    "range": range,
                },
                lsp_code_actions_params.LspCodeActionsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CodeActionsResponse,
        )

    def diagnostics(
        self,
        id: str,
        *,
        uri: FileUri,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DiagnosticsResponse:
        """
        Get diagnostics for a given file URI from the language server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/diagnostics",
            body=maybe_transform({"uri": uri}, lsp_diagnostics_params.LspDiagnosticsParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DiagnosticsResponse,
        )

    def document_symbols(
        self,
        id: str,
        *,
        uri: FileUri,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DocumentSymbolResponse:
        """
        Get document symbols for a given document.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/document-symbols",
            body=maybe_transform({"uri": uri}, lsp_document_symbols_params.LspDocumentSymbolsParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DocumentSymbolResponse,
        )

    def file(
        self,
        id: str,
        *,
        path: FilePath,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> FileContentsResponse:
        """
        Get the contents of a file at a given path relative to the root directory

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/file",
            body=maybe_transform({"path": path}, lsp_file_params.LspFileParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileContentsResponse,
        )

    def file_definition(
        self,
        id: str,
        *,
        character: float,
        line: float,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> FileDefinitionResponse:
        """
        Get the definition of a symbol at a given position in a file
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_definition

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/file-definition",
            body=maybe_transform(
                {
                    "character": character,
                    "line": line,
                    "uri": uri,
                },
                lsp_file_definition_params.LspFileDefinitionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileDefinitionResponse,
        )

    def files(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LspFilesResponse:
        """
        Get a list of all files being watched by the language server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/devboxes/{id}/lsp/files",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LspFilesResponse,
        )

    def formatting(
        self,
        id: str,
        *,
        uri: FileUri,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> FormattingResponse:
        """
        Get formatting changes for a given document.
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_formatting

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/formatting",
            body=maybe_transform({"uri": uri}, lsp_formatting_params.LspFormattingParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FormattingResponse,
        )

    def get_code_actions_for_diagnostic(
        self,
        id: str,
        *,
        diagnostic: BaseDiagnosticParam,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> LspGetCodeActionsForDiagnosticResponse:
        """
        Get a list of code actions for a given diagnostic

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/get-code-actions-for-diagnostic",
            body=maybe_transform(
                {
                    "diagnostic": diagnostic,
                    "uri": uri,
                },
                lsp_get_code_actions_for_diagnostic_params.LspGetCodeActionsForDiagnosticParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=LspGetCodeActionsForDiagnosticResponse,
        )

    def get_code_segment_info(
        self,
        id: str,
        *,
        symbol_name: str,
        uri: FileUri,
        symbol_type: SymbolType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> CodeSegmentInfoResponse:
        """
        Get the symbol, reference, and diagnostic information for a given code segment
        in a file at a given depth

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/get-code-segment-info",
            body=maybe_transform(
                {
                    "symbol_name": symbol_name,
                    "uri": uri,
                    "symbol_type": symbol_type,
                },
                lsp_get_code_segment_info_params.LspGetCodeSegmentInfoParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CodeSegmentInfoResponse,
        )

    def get_signature_help(
        self,
        id: str,
        *,
        character: float,
        line: float,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> SignatureHelpResponse:
        """
        Get the symbol, reference, and diagnostic information for a given code segment
        in a file at a given depth

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/get-signature-help",
            body=maybe_transform(
                {
                    "character": character,
                    "line": line,
                    "uri": uri,
                },
                lsp_get_signature_help_params.LspGetSignatureHelpParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SignatureHelpResponse,
        )

    def health(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HealthStatusResponse:
        """
        This method provides a health check for the language server, including its
        status, uptime, the directory being watched, and the name of the module.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._get(
            f"/v1/devboxes/{id}/lsp/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HealthStatusResponse,
        )

    def references(
        self,
        id: str,
        *,
        character: float,
        line: float,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> ReferencesResponse:
        """Get references for a given symbol.

        This method calls the `getReferences` method
        of the `LanguageService` class, which in turn communicates with the TypeScript
        language server to retrieve references for a given symbol in the document.
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_references

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/references",
            body=maybe_transform(
                {
                    "character": character,
                    "line": line,
                    "uri": uri,
                },
                lsp_references_params.LspReferencesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ReferencesResponse,
        )

    def set_watch_directory(
        self,
        id: str,
        *,
        path: FilePath,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Set the watch directory for the language server to a new path and restart the
        server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return self._post(
            f"/v1/devboxes/{id}/lsp/set-watch-directory",
            body=maybe_transform({"path": path}, lsp_set_watch_directory_params.LspSetWatchDirectoryParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )


class AsyncLspResource(AsyncAPIResource):
    @cached_property
    def with_raw_response(self) -> AsyncLspResourceWithRawResponse:
        """
        This property can be used as a prefix for any HTTP method call to return
        the raw response object instead of the parsed content.

        For more information, see https://www.github.com/runloopai/api-client-python#accessing-raw-response-data-eg-headers
        """
        return AsyncLspResourceWithRawResponse(self)

    @cached_property
    def with_streaming_response(self) -> AsyncLspResourceWithStreamingResponse:
        """
        An alternative to `.with_raw_response` that doesn't eagerly read the response body.

        For more information, see https://www.github.com/runloopai/api-client-python#with_streaming_response
        """
        return AsyncLspResourceWithStreamingResponse(self)

    async def apply_code_action(
        self,
        id: str,
        *,
        title: str,
        command: BaseCommandParam | NotGiven = NOT_GIVEN,
        edit: BaseWorkspaceEditParam | NotGiven = NOT_GIVEN,
        is_preferred: bool | NotGiven = NOT_GIVEN,
        kind: str | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> CodeActionApplicationResult:
        """
        Apply a code action to a given code segment not all code actions are supported
        yet

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/apply-code-action",
            body=await async_maybe_transform(
                {
                    "title": title,
                    "command": command,
                    "edit": edit,
                    "is_preferred": is_preferred,
                    "kind": kind,
                },
                lsp_apply_code_action_params.LspApplyCodeActionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CodeActionApplicationResult,
        )

    async def code_actions(
        self,
        id: str,
        *,
        uri: str,
        context: CodeActionContextParam | NotGiven = NOT_GIVEN,
        range: RangeParam | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> CodeActionsResponse:
        """Get code actions for a part of a document.

        This method calls the
        `getCodeActions` method of the `LanguageService` class, which in turn
        communicates with the TypeScript language server to retrieve code actions for a
        given document.
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_codeAction

        Args:
          context: Contains additional diagnostic information about the context in which a {@link
              CodeActionProvider.provideCodeActions code action} is run. The CodeActionContext
              namespace provides helper functions to work with {@link CodeActionContext}
              literals.

          range: A range in a text document expressed as (zero-based) start and end positions.

              If you want to specify a range that contains a line including the line ending
              character(s) then use an end position denoting the start of the next line. For
              example:

              ```ts
              {
                  start: { line: 5, character: 23 }
                  end : { line 6, character : 0 }
              }
              ```

              The Range namespace provides helper functions to work with {@link Range}
              literals.

          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/code-actions",
            body=await async_maybe_transform(
                {
                    "uri": uri,
                    "context": context,
                    "range": range,
                },
                lsp_code_actions_params.LspCodeActionsParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CodeActionsResponse,
        )

    async def diagnostics(
        self,
        id: str,
        *,
        uri: FileUri,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DiagnosticsResponse:
        """
        Get diagnostics for a given file URI from the language server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/diagnostics",
            body=await async_maybe_transform({"uri": uri}, lsp_diagnostics_params.LspDiagnosticsParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DiagnosticsResponse,
        )

    async def document_symbols(
        self,
        id: str,
        *,
        uri: FileUri,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> DocumentSymbolResponse:
        """
        Get document symbols for a given document.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/document-symbols",
            body=await async_maybe_transform({"uri": uri}, lsp_document_symbols_params.LspDocumentSymbolsParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=DocumentSymbolResponse,
        )

    async def file(
        self,
        id: str,
        *,
        path: FilePath,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> FileContentsResponse:
        """
        Get the contents of a file at a given path relative to the root directory

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/file",
            body=await async_maybe_transform({"path": path}, lsp_file_params.LspFileParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileContentsResponse,
        )

    async def file_definition(
        self,
        id: str,
        *,
        character: float,
        line: float,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> FileDefinitionResponse:
        """
        Get the definition of a symbol at a given position in a file
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_definition

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/file-definition",
            body=await async_maybe_transform(
                {
                    "character": character,
                    "line": line,
                    "uri": uri,
                },
                lsp_file_definition_params.LspFileDefinitionParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FileDefinitionResponse,
        )

    async def files(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> LspFilesResponse:
        """
        Get a list of all files being watched by the language server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/devboxes/{id}/lsp/files",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=LspFilesResponse,
        )

    async def formatting(
        self,
        id: str,
        *,
        uri: FileUri,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> FormattingResponse:
        """
        Get formatting changes for a given document.
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_formatting

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/formatting",
            body=await async_maybe_transform({"uri": uri}, lsp_formatting_params.LspFormattingParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=FormattingResponse,
        )

    async def get_code_actions_for_diagnostic(
        self,
        id: str,
        *,
        diagnostic: BaseDiagnosticParam,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> LspGetCodeActionsForDiagnosticResponse:
        """
        Get a list of code actions for a given diagnostic

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/get-code-actions-for-diagnostic",
            body=await async_maybe_transform(
                {
                    "diagnostic": diagnostic,
                    "uri": uri,
                },
                lsp_get_code_actions_for_diagnostic_params.LspGetCodeActionsForDiagnosticParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=LspGetCodeActionsForDiagnosticResponse,
        )

    async def get_code_segment_info(
        self,
        id: str,
        *,
        symbol_name: str,
        uri: FileUri,
        symbol_type: SymbolType | NotGiven = NOT_GIVEN,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> CodeSegmentInfoResponse:
        """
        Get the symbol, reference, and diagnostic information for a given code segment
        in a file at a given depth

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/get-code-segment-info",
            body=await async_maybe_transform(
                {
                    "symbol_name": symbol_name,
                    "uri": uri,
                    "symbol_type": symbol_type,
                },
                lsp_get_code_segment_info_params.LspGetCodeSegmentInfoParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=CodeSegmentInfoResponse,
        )

    async def get_signature_help(
        self,
        id: str,
        *,
        character: float,
        line: float,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> SignatureHelpResponse:
        """
        Get the symbol, reference, and diagnostic information for a given code segment
        in a file at a given depth

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/get-signature-help",
            body=await async_maybe_transform(
                {
                    "character": character,
                    "line": line,
                    "uri": uri,
                },
                lsp_get_signature_help_params.LspGetSignatureHelpParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=SignatureHelpResponse,
        )

    async def health(
        self,
        id: str,
        *,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
    ) -> HealthStatusResponse:
        """
        This method provides a health check for the language server, including its
        status, uptime, the directory being watched, and the name of the module.

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._get(
            f"/v1/devboxes/{id}/lsp/health",
            options=make_request_options(
                extra_headers=extra_headers, extra_query=extra_query, extra_body=extra_body, timeout=timeout
            ),
            cast_to=HealthStatusResponse,
        )

    async def references(
        self,
        id: str,
        *,
        character: float,
        line: float,
        uri: str,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> ReferencesResponse:
        """Get references for a given symbol.

        This method calls the `getReferences` method
        of the `LanguageService` class, which in turn communicates with the TypeScript
        language server to retrieve references for a given symbol in the document.
        https://microsoft.github.io/language-server-protocol/specifications/specification-current/#textDocument_references

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/references",
            body=await async_maybe_transform(
                {
                    "character": character,
                    "line": line,
                    "uri": uri,
                },
                lsp_references_params.LspReferencesParams,
            ),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=ReferencesResponse,
        )

    async def set_watch_directory(
        self,
        id: str,
        *,
        path: FilePath,
        # Use the following arguments if you need to pass additional parameters to the API that aren't available via kwargs.
        # The extra values given here take precedence over values defined on the client or passed to this method.
        extra_headers: Headers | None = None,
        extra_query: Query | None = None,
        extra_body: Body | None = None,
        timeout: float | httpx.Timeout | None | NotGiven = NOT_GIVEN,
        idempotency_key: str | None = None,
    ) -> str:
        """
        Set the watch directory for the language server to a new path and restart the
        server

        Args:
          extra_headers: Send extra headers

          extra_query: Add additional query parameters to the request

          extra_body: Add additional JSON properties to the request

          timeout: Override the client-level default timeout for this request, in seconds

          idempotency_key: Specify a custom idempotency key for this request
        """
        if not id:
            raise ValueError(f"Expected a non-empty value for `id` but received {id!r}")
        return await self._post(
            f"/v1/devboxes/{id}/lsp/set-watch-directory",
            body=await async_maybe_transform({"path": path}, lsp_set_watch_directory_params.LspSetWatchDirectoryParams),
            options=make_request_options(
                extra_headers=extra_headers,
                extra_query=extra_query,
                extra_body=extra_body,
                timeout=timeout,
                idempotency_key=idempotency_key,
            ),
            cast_to=str,
        )


class LspResourceWithRawResponse:
    def __init__(self, lsp: LspResource) -> None:
        self._lsp = lsp

        self.apply_code_action = to_raw_response_wrapper(
            lsp.apply_code_action,
        )
        self.code_actions = to_raw_response_wrapper(
            lsp.code_actions,
        )
        self.diagnostics = to_raw_response_wrapper(
            lsp.diagnostics,
        )
        self.document_symbols = to_raw_response_wrapper(
            lsp.document_symbols,
        )
        self.file = to_raw_response_wrapper(
            lsp.file,
        )
        self.file_definition = to_raw_response_wrapper(
            lsp.file_definition,
        )
        self.files = to_raw_response_wrapper(
            lsp.files,
        )
        self.formatting = to_raw_response_wrapper(
            lsp.formatting,
        )
        self.get_code_actions_for_diagnostic = to_raw_response_wrapper(
            lsp.get_code_actions_for_diagnostic,
        )
        self.get_code_segment_info = to_raw_response_wrapper(
            lsp.get_code_segment_info,
        )
        self.get_signature_help = to_raw_response_wrapper(
            lsp.get_signature_help,
        )
        self.health = to_raw_response_wrapper(
            lsp.health,
        )
        self.references = to_raw_response_wrapper(
            lsp.references,
        )
        self.set_watch_directory = to_raw_response_wrapper(
            lsp.set_watch_directory,
        )


class AsyncLspResourceWithRawResponse:
    def __init__(self, lsp: AsyncLspResource) -> None:
        self._lsp = lsp

        self.apply_code_action = async_to_raw_response_wrapper(
            lsp.apply_code_action,
        )
        self.code_actions = async_to_raw_response_wrapper(
            lsp.code_actions,
        )
        self.diagnostics = async_to_raw_response_wrapper(
            lsp.diagnostics,
        )
        self.document_symbols = async_to_raw_response_wrapper(
            lsp.document_symbols,
        )
        self.file = async_to_raw_response_wrapper(
            lsp.file,
        )
        self.file_definition = async_to_raw_response_wrapper(
            lsp.file_definition,
        )
        self.files = async_to_raw_response_wrapper(
            lsp.files,
        )
        self.formatting = async_to_raw_response_wrapper(
            lsp.formatting,
        )
        self.get_code_actions_for_diagnostic = async_to_raw_response_wrapper(
            lsp.get_code_actions_for_diagnostic,
        )
        self.get_code_segment_info = async_to_raw_response_wrapper(
            lsp.get_code_segment_info,
        )
        self.get_signature_help = async_to_raw_response_wrapper(
            lsp.get_signature_help,
        )
        self.health = async_to_raw_response_wrapper(
            lsp.health,
        )
        self.references = async_to_raw_response_wrapper(
            lsp.references,
        )
        self.set_watch_directory = async_to_raw_response_wrapper(
            lsp.set_watch_directory,
        )


class LspResourceWithStreamingResponse:
    def __init__(self, lsp: LspResource) -> None:
        self._lsp = lsp

        self.apply_code_action = to_streamed_response_wrapper(
            lsp.apply_code_action,
        )
        self.code_actions = to_streamed_response_wrapper(
            lsp.code_actions,
        )
        self.diagnostics = to_streamed_response_wrapper(
            lsp.diagnostics,
        )
        self.document_symbols = to_streamed_response_wrapper(
            lsp.document_symbols,
        )
        self.file = to_streamed_response_wrapper(
            lsp.file,
        )
        self.file_definition = to_streamed_response_wrapper(
            lsp.file_definition,
        )
        self.files = to_streamed_response_wrapper(
            lsp.files,
        )
        self.formatting = to_streamed_response_wrapper(
            lsp.formatting,
        )
        self.get_code_actions_for_diagnostic = to_streamed_response_wrapper(
            lsp.get_code_actions_for_diagnostic,
        )
        self.get_code_segment_info = to_streamed_response_wrapper(
            lsp.get_code_segment_info,
        )
        self.get_signature_help = to_streamed_response_wrapper(
            lsp.get_signature_help,
        )
        self.health = to_streamed_response_wrapper(
            lsp.health,
        )
        self.references = to_streamed_response_wrapper(
            lsp.references,
        )
        self.set_watch_directory = to_streamed_response_wrapper(
            lsp.set_watch_directory,
        )


class AsyncLspResourceWithStreamingResponse:
    def __init__(self, lsp: AsyncLspResource) -> None:
        self._lsp = lsp

        self.apply_code_action = async_to_streamed_response_wrapper(
            lsp.apply_code_action,
        )
        self.code_actions = async_to_streamed_response_wrapper(
            lsp.code_actions,
        )
        self.diagnostics = async_to_streamed_response_wrapper(
            lsp.diagnostics,
        )
        self.document_symbols = async_to_streamed_response_wrapper(
            lsp.document_symbols,
        )
        self.file = async_to_streamed_response_wrapper(
            lsp.file,
        )
        self.file_definition = async_to_streamed_response_wrapper(
            lsp.file_definition,
        )
        self.files = async_to_streamed_response_wrapper(
            lsp.files,
        )
        self.formatting = async_to_streamed_response_wrapper(
            lsp.formatting,
        )
        self.get_code_actions_for_diagnostic = async_to_streamed_response_wrapper(
            lsp.get_code_actions_for_diagnostic,
        )
        self.get_code_segment_info = async_to_streamed_response_wrapper(
            lsp.get_code_segment_info,
        )
        self.get_signature_help = async_to_streamed_response_wrapper(
            lsp.get_signature_help,
        )
        self.health = async_to_streamed_response_wrapper(
            lsp.health,
        )
        self.references = async_to_streamed_response_wrapper(
            lsp.references,
        )
        self.set_watch_directory = async_to_streamed_response_wrapper(
            lsp.set_watch_directory,
        )
