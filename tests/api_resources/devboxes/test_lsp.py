# File generated from our OpenAPI spec by Stainless. See CONTRIBUTING.md for details.

from __future__ import annotations

import os
from typing import Any, cast

import pytest

from tests.utils import assert_matches_type
from runloop_api_client import Runloop, AsyncRunloop
from runloop_api_client.types.devboxes import (
    LspFilesResponse,
    FormattingResponse,
    ReferencesResponse,
    CodeActionsResponse,
    DiagnosticsResponse,
    FileContentsResponse,
    HealthStatusResponse,
    SignatureHelpResponse,
    DocumentSymbolResponse,
    FileDefinitionResponse,
    CodeSegmentInfoResponse,
    CodeActionApplicationResult,
    LspGetCodeActionsForDiagnosticResponse,
)

base_url = os.environ.get("TEST_API_BASE_URL", "http://127.0.0.1:4010")


class TestLsp:
    parametrize = pytest.mark.parametrize("client", [False, True], indirect=True, ids=["loose", "strict"])

    @parametrize
    def test_method_apply_code_action(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.apply_code_action(
            id="id",
            title="title",
        )
        assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

    @parametrize
    def test_method_apply_code_action_with_all_params(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.apply_code_action(
            id="id",
            title="title",
            command={
                "command": "command",
                "title": "title",
                "arguments": [{}],
            },
            edit={
                "changes": {
                    "foo": [
                        {
                            "new_text": "newText",
                            "range": {
                                "end": {
                                    "character": 0,
                                    "line": 0,
                                },
                                "start": {
                                    "character": 0,
                                    "line": 0,
                                },
                            },
                        }
                    ]
                }
            },
            is_preferred=True,
            kind="kind",
        )
        assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

    @parametrize
    def test_raw_response_apply_code_action(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.apply_code_action(
            id="id",
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

    @parametrize
    def test_streaming_response_apply_code_action(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.apply_code_action(
            id="id",
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_apply_code_action(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.apply_code_action(
                id="",
                title="title",
            )

    @parametrize
    def test_method_code_actions(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.code_actions(
            id="id",
            uri="uri",
        )
        assert_matches_type(CodeActionsResponse, lsp, path=["response"])

    @parametrize
    def test_method_code_actions_with_all_params(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.code_actions(
            id="id",
            uri="uri",
            context={
                "diagnostics": [
                    {
                        "message": "message",
                        "range": {
                            "end": {
                                "character": 0,
                                "line": 0,
                            },
                            "start": {
                                "character": 0,
                                "line": 0,
                            },
                        },
                        "code": 0,
                        "code_description": {"href": "string"},
                        "data": {},
                        "related_information": [
                            {
                                "location": {
                                    "range": {
                                        "end": {
                                            "character": 0,
                                            "line": 0,
                                        },
                                        "start": {
                                            "character": 0,
                                            "line": 0,
                                        },
                                    },
                                    "uri": "string",
                                },
                                "message": "message",
                            }
                        ],
                        "severity": 1,
                        "source": "source",
                        "tags": [1],
                    }
                ],
                "only": ["string"],
                "trigger_kind": 1,
            },
            range={
                "end": {
                    "character": 0,
                    "line": 0,
                },
                "start": {
                    "character": 0,
                    "line": 0,
                },
            },
        )
        assert_matches_type(CodeActionsResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_code_actions(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.code_actions(
            id="id",
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(CodeActionsResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_code_actions(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.code_actions(
            id="id",
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(CodeActionsResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_code_actions(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.code_actions(
                id="",
                uri="uri",
            )

    @parametrize
    def test_method_diagnostics(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.diagnostics(
            id="id",
            uri="string",
        )
        assert_matches_type(DiagnosticsResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_diagnostics(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.diagnostics(
            id="id",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(DiagnosticsResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_diagnostics(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.diagnostics(
            id="id",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(DiagnosticsResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_diagnostics(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.diagnostics(
                id="",
                uri="string",
            )

    @parametrize
    def test_method_document_symbols(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.document_symbols(
            id="id",
            uri="string",
        )
        assert_matches_type(DocumentSymbolResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_document_symbols(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.document_symbols(
            id="id",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(DocumentSymbolResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_document_symbols(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.document_symbols(
            id="id",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(DocumentSymbolResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_document_symbols(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.document_symbols(
                id="",
                uri="string",
            )

    @parametrize
    def test_method_file(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.file(
            id="id",
            path="string",
        )
        assert_matches_type(FileContentsResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_file(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.file(
            id="id",
            path="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(FileContentsResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_file(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.file(
            id="id",
            path="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(FileContentsResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_file(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.file(
                id="",
                path="string",
            )

    @parametrize
    def test_method_file_definition(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.file_definition(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )
        assert_matches_type(FileDefinitionResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_file_definition(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.file_definition(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(FileDefinitionResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_file_definition(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.file_definition(
            id="id",
            character=0,
            line=0,
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(FileDefinitionResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_file_definition(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.file_definition(
                id="",
                character=0,
                line=0,
                uri="uri",
            )

    @parametrize
    def test_method_files(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.files(
            "id",
        )
        assert_matches_type(LspFilesResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_files(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.files(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(LspFilesResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_files(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.files(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(LspFilesResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_files(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.files(
                "",
            )

    @parametrize
    def test_method_formatting(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.formatting(
            id="id",
            uri="string",
        )
        assert_matches_type(FormattingResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_formatting(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.formatting(
            id="id",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(FormattingResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_formatting(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.formatting(
            id="id",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(FormattingResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_formatting(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.formatting(
                id="",
                uri="string",
            )

    @parametrize
    def test_method_get_code_actions_for_diagnostic(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
            },
            uri="uri",
        )
        assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

    @parametrize
    def test_method_get_code_actions_for_diagnostic_with_all_params(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
                "code": 0,
                "severity": 1,
                "source": "source",
            },
            uri="uri",
        )
        assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_get_code_actions_for_diagnostic(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
            },
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_get_code_actions_for_diagnostic(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
            },
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_code_actions_for_diagnostic(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.get_code_actions_for_diagnostic(
                id="",
                diagnostic={
                    "message": "message",
                    "range": {
                        "end": {
                            "character": 0,
                            "line": 0,
                        },
                        "start": {
                            "character": 0,
                            "line": 0,
                        },
                    },
                },
                uri="uri",
            )

    @parametrize
    def test_method_get_code_segment_info(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
        )
        assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

    @parametrize
    def test_method_get_code_segment_info_with_all_params(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
            symbol_type="function",
        )
        assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_get_code_segment_info(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_get_code_segment_info(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_code_segment_info(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.get_code_segment_info(
                id="",
                symbol_name="symbolName",
                uri="string",
            )

    @parametrize
    def test_method_get_signature_help(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.get_signature_help(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )
        assert_matches_type(SignatureHelpResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_get_signature_help(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.get_signature_help(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(SignatureHelpResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_get_signature_help(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.get_signature_help(
            id="id",
            character=0,
            line=0,
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(SignatureHelpResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_get_signature_help(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.get_signature_help(
                id="",
                character=0,
                line=0,
                uri="uri",
            )

    @parametrize
    def test_method_health(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.health(
            "id",
        )
        assert_matches_type(HealthStatusResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_health(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.health(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(HealthStatusResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_health(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.health(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(HealthStatusResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_health(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.health(
                "",
            )

    @parametrize
    def test_method_references(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.references(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )
        assert_matches_type(ReferencesResponse, lsp, path=["response"])

    @parametrize
    def test_raw_response_references(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.references(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(ReferencesResponse, lsp, path=["response"])

    @parametrize
    def test_streaming_response_references(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.references(
            id="id",
            character=0,
            line=0,
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(ReferencesResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_references(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.references(
                id="",
                character=0,
                line=0,
                uri="uri",
            )

    @parametrize
    def test_method_set_watch_directory(self, client: Runloop) -> None:
        lsp = client.devboxes.lsp.set_watch_directory(
            id="id",
            path="string",
        )
        assert_matches_type(str, lsp, path=["response"])

    @parametrize
    def test_raw_response_set_watch_directory(self, client: Runloop) -> None:
        response = client.devboxes.lsp.with_raw_response.set_watch_directory(
            id="id",
            path="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = response.parse()
        assert_matches_type(str, lsp, path=["response"])

    @parametrize
    def test_streaming_response_set_watch_directory(self, client: Runloop) -> None:
        with client.devboxes.lsp.with_streaming_response.set_watch_directory(
            id="id",
            path="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = response.parse()
            assert_matches_type(str, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    def test_path_params_set_watch_directory(self, client: Runloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            client.devboxes.lsp.with_raw_response.set_watch_directory(
                id="",
                path="string",
            )


class TestAsyncLsp:
    parametrize = pytest.mark.parametrize(
        "async_client", [False, True, {"http_client": "aiohttp"}], indirect=True, ids=["loose", "strict", "aiohttp"]
    )

    @parametrize
    async def test_method_apply_code_action(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.apply_code_action(
            id="id",
            title="title",
        )
        assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

    @parametrize
    async def test_method_apply_code_action_with_all_params(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.apply_code_action(
            id="id",
            title="title",
            command={
                "command": "command",
                "title": "title",
                "arguments": [{}],
            },
            edit={
                "changes": {
                    "foo": [
                        {
                            "new_text": "newText",
                            "range": {
                                "end": {
                                    "character": 0,
                                    "line": 0,
                                },
                                "start": {
                                    "character": 0,
                                    "line": 0,
                                },
                            },
                        }
                    ]
                }
            },
            is_preferred=True,
            kind="kind",
        )
        assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

    @parametrize
    async def test_raw_response_apply_code_action(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.apply_code_action(
            id="id",
            title="title",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_apply_code_action(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.apply_code_action(
            id="id",
            title="title",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(CodeActionApplicationResult, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_apply_code_action(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.apply_code_action(
                id="",
                title="title",
            )

    @parametrize
    async def test_method_code_actions(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.code_actions(
            id="id",
            uri="uri",
        )
        assert_matches_type(CodeActionsResponse, lsp, path=["response"])

    @parametrize
    async def test_method_code_actions_with_all_params(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.code_actions(
            id="id",
            uri="uri",
            context={
                "diagnostics": [
                    {
                        "message": "message",
                        "range": {
                            "end": {
                                "character": 0,
                                "line": 0,
                            },
                            "start": {
                                "character": 0,
                                "line": 0,
                            },
                        },
                        "code": 0,
                        "code_description": {"href": "string"},
                        "data": {},
                        "related_information": [
                            {
                                "location": {
                                    "range": {
                                        "end": {
                                            "character": 0,
                                            "line": 0,
                                        },
                                        "start": {
                                            "character": 0,
                                            "line": 0,
                                        },
                                    },
                                    "uri": "string",
                                },
                                "message": "message",
                            }
                        ],
                        "severity": 1,
                        "source": "source",
                        "tags": [1],
                    }
                ],
                "only": ["string"],
                "trigger_kind": 1,
            },
            range={
                "end": {
                    "character": 0,
                    "line": 0,
                },
                "start": {
                    "character": 0,
                    "line": 0,
                },
            },
        )
        assert_matches_type(CodeActionsResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_code_actions(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.code_actions(
            id="id",
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(CodeActionsResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_code_actions(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.code_actions(
            id="id",
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(CodeActionsResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_code_actions(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.code_actions(
                id="",
                uri="uri",
            )

    @parametrize
    async def test_method_diagnostics(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.diagnostics(
            id="id",
            uri="string",
        )
        assert_matches_type(DiagnosticsResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_diagnostics(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.diagnostics(
            id="id",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(DiagnosticsResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_diagnostics(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.diagnostics(
            id="id",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(DiagnosticsResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_diagnostics(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.diagnostics(
                id="",
                uri="string",
            )

    @parametrize
    async def test_method_document_symbols(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.document_symbols(
            id="id",
            uri="string",
        )
        assert_matches_type(DocumentSymbolResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_document_symbols(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.document_symbols(
            id="id",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(DocumentSymbolResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_document_symbols(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.document_symbols(
            id="id",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(DocumentSymbolResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_document_symbols(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.document_symbols(
                id="",
                uri="string",
            )

    @parametrize
    async def test_method_file(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.file(
            id="id",
            path="string",
        )
        assert_matches_type(FileContentsResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_file(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.file(
            id="id",
            path="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(FileContentsResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_file(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.file(
            id="id",
            path="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(FileContentsResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_file(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.file(
                id="",
                path="string",
            )

    @parametrize
    async def test_method_file_definition(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.file_definition(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )
        assert_matches_type(FileDefinitionResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_file_definition(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.file_definition(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(FileDefinitionResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_file_definition(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.file_definition(
            id="id",
            character=0,
            line=0,
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(FileDefinitionResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_file_definition(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.file_definition(
                id="",
                character=0,
                line=0,
                uri="uri",
            )

    @parametrize
    async def test_method_files(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.files(
            "id",
        )
        assert_matches_type(LspFilesResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_files(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.files(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(LspFilesResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_files(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.files(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(LspFilesResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_files(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.files(
                "",
            )

    @parametrize
    async def test_method_formatting(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.formatting(
            id="id",
            uri="string",
        )
        assert_matches_type(FormattingResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_formatting(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.formatting(
            id="id",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(FormattingResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_formatting(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.formatting(
            id="id",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(FormattingResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_formatting(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.formatting(
                id="",
                uri="string",
            )

    @parametrize
    async def test_method_get_code_actions_for_diagnostic(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
            },
            uri="uri",
        )
        assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

    @parametrize
    async def test_method_get_code_actions_for_diagnostic_with_all_params(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
                "code": 0,
                "severity": 1,
                "source": "source",
            },
            uri="uri",
        )
        assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_get_code_actions_for_diagnostic(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
            },
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_get_code_actions_for_diagnostic(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.get_code_actions_for_diagnostic(
            id="id",
            diagnostic={
                "message": "message",
                "range": {
                    "end": {
                        "character": 0,
                        "line": 0,
                    },
                    "start": {
                        "character": 0,
                        "line": 0,
                    },
                },
            },
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(LspGetCodeActionsForDiagnosticResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_code_actions_for_diagnostic(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.get_code_actions_for_diagnostic(
                id="",
                diagnostic={
                    "message": "message",
                    "range": {
                        "end": {
                            "character": 0,
                            "line": 0,
                        },
                        "start": {
                            "character": 0,
                            "line": 0,
                        },
                    },
                },
                uri="uri",
            )

    @parametrize
    async def test_method_get_code_segment_info(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
        )
        assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

    @parametrize
    async def test_method_get_code_segment_info_with_all_params(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
            symbol_type="function",
        )
        assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_get_code_segment_info(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_get_code_segment_info(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.get_code_segment_info(
            id="id",
            symbol_name="symbolName",
            uri="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(CodeSegmentInfoResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_code_segment_info(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.get_code_segment_info(
                id="",
                symbol_name="symbolName",
                uri="string",
            )

    @parametrize
    async def test_method_get_signature_help(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.get_signature_help(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )
        assert_matches_type(SignatureHelpResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_get_signature_help(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.get_signature_help(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(SignatureHelpResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_get_signature_help(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.get_signature_help(
            id="id",
            character=0,
            line=0,
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(SignatureHelpResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_get_signature_help(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.get_signature_help(
                id="",
                character=0,
                line=0,
                uri="uri",
            )

    @parametrize
    async def test_method_health(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.health(
            "id",
        )
        assert_matches_type(HealthStatusResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_health(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.health(
            "id",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(HealthStatusResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_health(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.health(
            "id",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(HealthStatusResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_health(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.health(
                "",
            )

    @parametrize
    async def test_method_references(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.references(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )
        assert_matches_type(ReferencesResponse, lsp, path=["response"])

    @parametrize
    async def test_raw_response_references(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.references(
            id="id",
            character=0,
            line=0,
            uri="uri",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(ReferencesResponse, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_references(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.references(
            id="id",
            character=0,
            line=0,
            uri="uri",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(ReferencesResponse, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_references(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.references(
                id="",
                character=0,
                line=0,
                uri="uri",
            )

    @parametrize
    async def test_method_set_watch_directory(self, async_client: AsyncRunloop) -> None:
        lsp = await async_client.devboxes.lsp.set_watch_directory(
            id="id",
            path="string",
        )
        assert_matches_type(str, lsp, path=["response"])

    @parametrize
    async def test_raw_response_set_watch_directory(self, async_client: AsyncRunloop) -> None:
        response = await async_client.devboxes.lsp.with_raw_response.set_watch_directory(
            id="id",
            path="string",
        )

        assert response.is_closed is True
        assert response.http_request.headers.get("X-Stainless-Lang") == "python"
        lsp = await response.parse()
        assert_matches_type(str, lsp, path=["response"])

    @parametrize
    async def test_streaming_response_set_watch_directory(self, async_client: AsyncRunloop) -> None:
        async with async_client.devboxes.lsp.with_streaming_response.set_watch_directory(
            id="id",
            path="string",
        ) as response:
            assert not response.is_closed
            assert response.http_request.headers.get("X-Stainless-Lang") == "python"

            lsp = await response.parse()
            assert_matches_type(str, lsp, path=["response"])

        assert cast(Any, response.is_closed) is True

    @parametrize
    async def test_path_params_set_watch_directory(self, async_client: AsyncRunloop) -> None:
        with pytest.raises(ValueError, match=r"Expected a non-empty value for `id` but received ''"):
            await async_client.devboxes.lsp.with_raw_response.set_watch_directory(
                id="",
                path="string",
            )
