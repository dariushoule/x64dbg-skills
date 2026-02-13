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

### `/yara-sigs`

Scans snapshot memory dumps with [YARA](https://virustotal.github.io/yara/) signatures from the [x64dbg yarasigs](https://github.com/x64dbg/yarasigs) database:
- Automatically clones the yarasigs repo (including Yara-Rules and citizenlab submodules) on first use
- Scan categories: **packers & compilers**, **crypto constants**, **anti-debug / anti-VM**, or **all signatures**
- Builds on `/state-snapshot` — uses an existing snapshot or takes a fresh one
- Reports matches grouped by rule with memory region addresses and metadata

### `/tracealyzer`

Traces execution (into or over calls) for N steps or until a condition is met, then analyzes the recorded instruction log:
- Configurable trace mode: step **into** calls or step **over** calls
- Stop on a max instruction count, an x64dbg expression (e.g. `cip == 0x401000`), or both
- Captures a full instruction log to `traces/` with addresses, disassembly, labels, and comments
- Summarizes execution flow, hot spots, API calls, loops, and notable patterns
- Follow-up actions: annotate key addresses in x64dbg, deeper sub-region analysis, deobfuscation

## Prerequisites

- [x64dbg](https://x64dbg.com/) and [x64dbg Automate](https://dariushoule.github.io/x64dbg-automate-pyclient/installation/) installed
- [x64dbg MCP server](https://dariushoule.github.io/x64dbg-automate-pyclient/mcp-server/) configured in Claude Code
- Python 3 with the `x64dbg_automate` pip package installed:
  ```
  pip install x64dbg_automate[mcp] --upgrade
  ```
- For the `/decompile` skill: [angr](https://pypi.org/project/angr/) (Python >= 3.10):
  ```
  pip install angr
  ```
- For the `/yara-sigs` skill: [yara-python](https://pypi.org/project/yara-python/) and [Git](https://git-scm.com/):
  ```
  pip install yara-python
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

A decent guide that gives good ideas on how to use these skills: [Cooking with x64dbg and MCP](https://x64.ooo/posts/2026-02-12-cooking-with-x64dbg-and-mcp)

## License

MIT
