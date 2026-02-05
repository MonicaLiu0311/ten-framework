# streamid_adapter

An extension that adapts audio frames by adding session metadata based on stream ID, enabling session-aware audio processing in multi-stream scenarios.

## Features

- Stream ID to Session ID Mapping: Converts stream_id property to session_id metadata
- Audio Frame Metadata Enrichment: Adds structured metadata to audio frames for downstream processing
- Pass-through Processing: Forwards audio frames with minimal latency
- Multi-stream Support: Handles multiple concurrent audio streams with unique identifiers

## API

Refer to `api` definition in [manifest.json] and default values in [property.json](property.json).

### Audio Frame In:

| **Name**       | **Property** | **Type** | **Description**                           |
|----------------|--------------|----------|-------------------------------------------|
| `audio_frame`  | `stream_id`  | `int`    | Input audio frame with stream identifier  |

### Audio Frame Out:

| **Name**       | **Property** | **Type** | **Description**                                    |
|----------------|--------------|----------|----------------------------------------------------|
| `audio_frame`  | `metadata`   | `string` | Output audio frame with session_id in JSON metadata|

## Development

### Build

This extension is written in Python and uses the TEN Framework Python runtime. No additional build steps are required beyond the standard TEN Framework build process.

### Unit test

Refer to the test script defined in the `manifest.json` under the `scripts.test` section (if applicable).

## Misc

This extension is useful in scenarios where audio streams need to be associated with specific sessions for features like:
- Multi-user voice assistants
- Session-based audio analytics
- User-specific audio processing pipelines
- Session isolation in concurrent audio streams
