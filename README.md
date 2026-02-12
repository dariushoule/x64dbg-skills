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

### `/decompile`

Decompiles a function to C-like pseudocode using [angr](https://angr.io/):
- Decompiles the function at the current instruction pointer if no address is specified
- Accepts a specific address or symbol as an argument
- Tries multiple decompiler strategies for best results
- Suggests nearby functions if the specified address isn't a function entry

## Prerequisites

- [x64dbg](https://x64dbg.com/) installed
- [x64dbg MCP server](https://github.com/dariushoule/x64dbg-automate-mcp) configured in Claude Code
- Python 3 with the `x64dbg_automate` pip package installed:
  ```
  pip install x64dbg_automate[mcp] --upgrade
  ```
- For the `/decompile` skill: [angr](https://pypi.org/project/angr/) (Python >= 3.10):
  ```
  pip install angr
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
