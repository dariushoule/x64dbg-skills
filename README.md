# x64dbg-skills

Claude Code plugin providing skills for x64dbg debugger automation.

## Skills

### `/state-snapshot`

Captures a full debuggee state snapshot to disk for offline analysis:
- All committed memory regions as raw binary files
- Complete processor state (registers) as JSON

### `/state-diff`

Compares two state snapshots to identify what changed between two points in time:
- Register changes (instruction pointer advancement, stack movement, flags, etc.)
- Memory region modifications (stack writes, heap mutations, code changes)
- Synthesized narrative explaining what the program did between snapshots

## Prerequisites

- [x64dbg](https://x64dbg.com/) installed
- [x64dbg MCP server](https://github.com/dariushoule/x64dbg-automate-mcp) configured in Claude Code
- Python 3 with the `x64dbg_automate` pip package installed:
  ```
  pip install x64dbg_automate[mcp] --upgrade
  ```

## Installation

Add the marketplace and install the plugin:

```
/plugin marketplace add dariushoule/x64dbg-skills
/plugin install x64dbg-skills
```

## Updating

To update to the latest version:

```
/plugin install x64dbg-skills
```

## Usage

<TODO BLOG>

## License

MIT
