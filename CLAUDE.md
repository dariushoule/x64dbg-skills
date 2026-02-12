# x64dbg-skills

Claude Code plugin providing skills for x64dbg debugger automation.

## Structure

- `skills/` — Skill definitions (SKILL.md files define each skill's steps and allowed tools)
- Each skill folder contains its own Python script (e.g. `skills/decompile/decompile.py`)
- `.claude-plugin/` — Plugin metadata (`plugin.json`, `marketplace.json`)
- `.claude/settings.local.json` — Default permission grants for x64dbg MCP tools

## Skills

- `/state-snapshot` — Captures all committed memory regions + registers to disk
- `/state-diff` — Compares two snapshots and explains what changed
- `/decompile` — Decompiles a function to C pseudocode via angr
- `/yara-sigs` — Scans snapshot memory dumps with YARA signatures (packers, crypto, anti-debug, etc.)
- `/tracealyzer` — Traces execution and analyzes the recorded instruction log

## Key Patterns

- Skills that require raw `X64DbgClient` access disconnect the MCP client before running Python scripts (only one ZMQ client allowed at a time), then reconnect after
    - Python scripts can use the `x64dbg_automate` package and `X64DbgClient` to communicate directly with x64dbg
    - Skills should only communicate directly when MCP access would be poor use of context, slow, or generally innefficient
- Addresses are hex strings throughout (e.g. `0x7FF6A0001000`)
- The plugin targets both 32-bit and 64-bit debuggees (use `eip`/`rip` accordingly)

## Dependencies

- `x64dbg_automate[mcp]` (pip) — required for all skills
- `angr` (pip) — required only for `/decompile`
- `yara-python` (pip) — required only for `/yara-sigs`
