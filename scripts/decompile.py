"""
Decompile a function from a binary using angr's decompiler.

Usage:
    python decompile.py --binary <path> --address <rva_hex>
"""

import argparse
import logging
import sys

# Suppress noisy angr/cle/claripy warnings before import
logging.getLogger("angr").setLevel(logging.CRITICAL)
logging.getLogger("cle").setLevel(logging.CRITICAL)
logging.getLogger("claripy").setLevel(logging.CRITICAL)
logging.getLogger("pyvex").setLevel(logging.CRITICAL)

try:
    import angr
except ImportError:
    print("Error: angr is not installed. Install it with: pip install angr", file=sys.stderr)
    sys.exit(1)


def parse_args():
    parser = argparse.ArgumentParser(description="Decompile a function using angr")
    parser.add_argument("--binary", required=True, help="Path to the binary on disk")
    parser.add_argument("--address", required=True, help="RVA of the function to decompile (hex, e.g. 0x1060)")
    parser.add_argument("--base-address", default=None, help="Override image base address (hex)")
    return parser.parse_args()


def main():
    args = parse_args()

    rva = int(args.address, 16)

    print(f"[*] Loading binary: {args.binary}", file=sys.stderr)
    project = angr.Project(args.binary, auto_load_libs=False)

    base = project.loader.main_object.mapped_base
    if args.base_address is not None:
        base = int(args.base_address, 16)

    va = base + rva
    print(f"[*] Target function VA: {hex(va)} (base {hex(base)} + RVA {hex(rva)})", file=sys.stderr)

    print(f"[*] Generating CFG...", file=sys.stderr)
    cfg = project.analyses.CFGFast(normalize=True)
    print(f"[*] CFG complete: {len(cfg.functions)} functions discovered", file=sys.stderr)

    func = cfg.functions.get(va)
    if func is None:
        print(f"[!] No function found at {hex(va)}", file=sys.stderr)

        # Find nearby functions as suggestions
        nearby = sorted(cfg.functions.values(), key=lambda f: abs(f.addr - va))[:5]
        if nearby:
            print(f"[*] Nearby functions:", file=sys.stderr)
            for f in nearby:
                offset = f.addr - base
                print(f"    {f.name} at {hex(f.addr)} (RVA {hex(offset)})", file=sys.stderr)

        sys.exit(1)

    print(f"[*] Decompiling {func.name} ({func.size} bytes)...", file=sys.stderr)

    # Try multiple decompiler configurations — angr can be finicky
    attempts = [
        {"label": "default", "opts": {}},
        {"label": "Phoenix structurer", "opts": {"options": [("structurer_cls", "Phoenix")]}},
        {"label": "no optimization", "opts": {"peephole_optimizations": False}},
    ]

    decomp = None
    for attempt in attempts:
        try:
            print(f"[*] Trying {attempt['label']}...", file=sys.stderr)
            decomp = project.analyses.Decompiler(func, cfg=cfg, **attempt["opts"])
            if decomp.codegen is not None:
                break
            decomp = None
        except Exception as e:
            print(f"[!] {attempt['label']} failed: {e}", file=sys.stderr)
            decomp = None

    if decomp is None or decomp.codegen is None:
        print(f"[!] Decompiler produced no output for {func.name} after all attempts", file=sys.stderr)
        sys.exit(1)

    # Output the decompiled code to stdout
    print(decomp.codegen.text)
    print(f"[+] Decompilation complete", file=sys.stderr)


if __name__ == "__main__":
    main()
