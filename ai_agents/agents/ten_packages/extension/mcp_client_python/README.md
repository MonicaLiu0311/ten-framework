# mcp_client_python

An extension for integrating Model Context Protocol (MCP) servers into your application, enabling dynamic tool discovery and execution from external MCP servers.

## Features

- MCP Server Integration: Connect to MCP servers via Server-Sent Events (SSE)
- Dynamic Tool Discovery: Automatically discover and register tools from MCP servers
- Tool Execution: Execute MCP tools with parameter validation and result handling
- Async Support: Fully asynchronous implementation for non-blocking operations

## API

Refer to `api` definition in [manifest.json] and default values in [property.json](property.json).

| **Property** | **Type** | **Description**                                    |
|--------------|----------|----------------------------------------------------|
| `url`        | `string` | SSE endpoint URL of the MCP server to connect to   |

### Command Out:

- `tool_register`: Auto-register discovered tools to LLM

### Command In:

- `tool_call`: Execute a tool on the MCP server with provided arguments

## Development

### Build

This extension requires the `mcp` Python package version 1.2.1 or higher. The package is listed in `requirements.txt` and will be installed during the TEN Framework build process.

### Unit test

Refer to the test script defined in the `manifest.json` under the `scripts.test` section.

## Misc

The extension uses the MCP SSE client to connect to MCP servers and implements the AsyncLLMToolBaseExtension interface for seamless integration with LLM-based agents in the TEN Framework.
