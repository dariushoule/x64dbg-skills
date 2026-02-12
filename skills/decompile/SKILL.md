---
name: decompile
description: Decompile a function to C-like pseudocode using angr
allowed-tools: mcp__x64dbg__get_debugger_status, mcp__x64dbg__get_register, mcp__x64dbg__eval_expression, mcp__x64dbg__get_symbol, Bash, Read
---

# decompile

Decompile a function from the debugged binary into C-like pseudocode using angr.

If no address is specified, decompiles the function containing the current instruction pointer. Accepts an address or symbol name as an argument.

## Instructions

Follow these steps exactly:

### 1. Check prerequisites

Run `pip show angr` via Bash. If angr is not installed, tell the user:

> angr is not installed. Install it with `pip install angr` (requires Python >= 3.10). Note: angr is a large package (~500MB+).

Then stop.

### 2. Verify debugger connection

Call `mcp__x64dbg__get_debugger_status` to confirm the debugger is connected and paused. If not debugging, tell the user and stop.

### 3. Determine target function address

**If the user provided an address or symbol as an argument:**
- If it looks like a hex address, use it directly
- If it looks like a symbol name, resolve it via `mcp__x64dbg__eval_expression`

**If no argument was provided:**
- Get the current instruction pointer via `mcp__x64dbg__get_register` (register `rip` for 64-bit, `eip` for 32-bit)
- Use the current RIP/EIP value as the target address

Call this resolved value `target_addr`.

### 4. Resolve module path and compute RVA

Use `mcp__x64dbg__eval_expression` to evaluate:
- `mod.path(target_addr)` — to get the on-disk path of the module containing the address
- `mod.base(target_addr)` — to get the module's base address

Compute the RVA: `target_addr - module_base`

If `mod.path` fails, the address may not belong to a loaded module. Tell the user and stop.

### 5. Run the decompile script

Execute:

```
python "<skill_base_dir>\scripts\decompile.py" --binary "<module_path>" --address <rva_hex>
```

Where:
- `<skill_base_dir>` is the base directory provided at the top of this skill's invocation context
- `<module_path>` is the on-disk path from step 4
- `<rva_hex>` is the RVA in hex (e.g. `0x1060`)

The script may take 10-30 seconds for large binaries (CFG generation is the bottleneck). Use a timeout of at least 120 seconds.

### 6. Present results

The script outputs decompiled C pseudocode to stdout and status messages to stderr.

Present the decompiled code to the user in a ```c code block. If the script failed, relay the error message from stderr (e.g., function not found, decompilation failed) and suggest nearby functions if listed.
