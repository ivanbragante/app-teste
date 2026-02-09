# Directive: Logging Standard

## Goal
Establish a unified logging mechanism for all automation scripts to facilitate monitoring and debugging.

## Standard
All execution scripts MUST log their activities to a centralized file: `logs/activities.jsonl`.

### Log Format (JSON Lines)
Each log entry must be a JSON object on a new line with the following fields:
- `timestamp`: (ISO 8601 string) When the event occurred.
- `script`: (String) Name of the script executing.
- `level`: (String) "INFO", "WARNING", "ERROR".
- `message`: (String) Description of the event.
- `data`: (Object, Optional) Additional context (e.g., args, results count).

### Implementation Guide
1. Import `json`, `datetime`, `os`.
2. Define a `log_activity` function.
3. Append to `logs/activities.jsonl`.
4. Log at start, significant steps, and completion/failure.

## Viewer
Use `execution/view_logs.py` to filter and visualize these logs.
