#!/usr/bin/env python3
"""
Pipeline Step 1: Obfuscation and I/O Test Generation
Transforms 4 core benchmark C programs using Tigress Flatten transform.
Compiles both baseline (-O0) and obfuscated (-O0) binaries.
Verifies functional equivalence across test cases and writes I/O suites.
"""

import os
import sys
import json
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
TIGRESS_HOME = ROOT_DIR / "tools" / "tigress" / "3.3.3"
TIGRESS_BIN = TIGRESS_HOME / "tigress"

SAMPLES = [
    {
        "id": "sample1_bitmix",
        "category": "arithmetic_bit_manipulation",
        "source": "dataset/src/sample1_bitmix.c",
        "target_func": "sample1_bitmix",
        "test_inputs": [
            ["0"],
            ["1"],
            ["42"],
            ["100"],
            ["1000"],
            ["0x12345678"],
            ["0x80000000"],
            ["0xFFFFFFFF"]
        ]
    },
    {
        "id": "sample2_xtea",
        "category": "crypto_primitive",
        "source": "dataset/src/sample2_xtea.c",
        "target_func": "sample2_xtea_round",
        "test_inputs": [
            ["0", "0", "0", "0"],
            ["1", "2", "3", "4"],
            ["42", "100", "200", "300"],
            ["0x12345678", "0x9ABCDEF0", "0xCAFEBABE", "0xDEADBEEF"],
            ["0xFFFFFFFF", "0x7FFFFFFF", "0x1234", "0x5678"]
        ]
    },
    {
        "id": "sample3_parser",
        "category": "string_token_parser",
        "source": "dataset/src/sample3_parser.c",
        "target_func": "sample3_parser",
        "test_inputs": [
            ["A:123;"],
            ["B:-45;"],
            ["Z:0;"],
            ["ABC:999;"],
            ["XYZ:-12345;"],
            ["HELLO:42;"]
        ]
    },
    {
        "id": "sample4_fsm",
        "category": "state_machine",
        "source": "dataset/src/sample4_fsm.c",
        "target_func": "sample4_fsm",
        "test_inputs": [
            ["c"],
            ["cc"],
            ["ccb"],
            ["ccbv"],
            ["ccbvr"],
            ["ccr"],
            ["ccccbv"],
            ["cb"]
        ]
    }
]

def run_cmd(cmd, cwd=None, env=None):
    res = subprocess.run(cmd, cwd=cwd, env=env, capture_output=True, text=True)
    if res.returncode != 0:
        raise RuntimeError(f"Command failed (code {res.returncode}): {' '.join(str(x) for x in cmd)}\nStderr: {res.stderr}\nStdout: {res.stdout}")
    return res.stdout.strip()

def main():
    print("=" * 60)
    print("Step 1: Compiling Baseline, Obfuscating with Tigress, Generating I/O")
    print("=" * 60)
    
    os.makedirs(ROOT_DIR / "dataset" / "binaries_baseline", exist_ok=True)
    os.makedirs(ROOT_DIR / "dataset" / "binaries_obfuscated", exist_ok=True)
    os.makedirs(ROOT_DIR / "dataset" / "src_obfuscated", exist_ok=True)
    os.makedirs(ROOT_DIR / "dataset" / "io_tests", exist_ok=True)
    
    env = os.environ.copy()
    env["TIGRESS_HOME"] = str(TIGRESS_HOME)
    
    manifest_entries = []
    
    for sample in SAMPLES:
        s_id = sample["id"]
        src_path = ROOT_DIR / sample["source"]
        obf_src_path = ROOT_DIR / "dataset" / "src_obfuscated" / f"{s_id}_obf.c"
        base_bin_path = ROOT_DIR / "dataset" / "binaries_baseline" / s_id
        obf_bin_path = ROOT_DIR / "dataset" / "binaries_obfuscated" / s_id
        io_test_path = ROOT_DIR / "dataset" / "io_tests" / f"{s_id}.json"
        
        print(f"\nProcessing [{s_id}] ({sample['category']})...")
        
        # 1. Compile baseline binary with -O0
        print(f"  [1/4] Compiling baseline binary (-O0)...")
        run_cmd(["clang", "-O0", str(src_path), "-o", str(base_bin_path)])
        
        # 2. Obfuscate with Tigress Flatten
        print(f"  [2/4] Obfuscating with Tigress Flatten on function [{sample['target_func']}]...")
        tigress_cmd = [
            str(TIGRESS_BIN),
            "--Environment=arm64:Darwin:Clang:5.1",
            "--Transform=Flatten",
            f"--Functions={sample['target_func']}",
            f"--out={obf_src_path}",
            str(src_path)
        ]
        run_cmd(tigress_cmd, env=env)
        
        # 3. Compile obfuscated binary with -O0
        print(f"  [3/4] Compiling obfuscated binary (-O0)...")
        run_cmd(["clang", "-O0", str(obf_src_path), "-o", str(obf_bin_path)])
        
        # 4. Generate and verify I/O tests
        print(f"  [4/4] Verifying I/O equivalence across {len(sample['test_inputs'])} test cases...")
        io_records = []
        for args in sample["test_inputs"]:
            base_out = run_cmd([str(base_bin_path)] + args)
            obf_out = run_cmd([str(obf_bin_path)] + args)
            if base_out != obf_out:
                raise ValueError(f"Equivalence mismatch for {s_id} with args {args}: base={base_out} vs obf={obf_out}")
            io_records.append({
                "args": args,
                "expected_output": base_out
            })
            
        with open(io_test_path, "w") as f:
            json.dump(io_records, f, indent=2)
            
        manifest_entries.append({
            "id": s_id,
            "category": sample["category"],
            "target_function": sample["target_func"],
            "source_path": str(src_path.relative_to(ROOT_DIR)),
            "obfuscated_source_path": str(obf_src_path.relative_to(ROOT_DIR)),
            "baseline_binary": str(base_bin_path.relative_to(ROOT_DIR)),
            "obfuscated_binary": str(obf_bin_path.relative_to(ROOT_DIR)),
            "io_test_path": str(io_test_path.relative_to(ROOT_DIR)),
            "obfuscation_flags": ["--Transform=Flatten", f"--Functions={sample['target_func']}"],
            "num_io_tests": len(io_records),
            "compilation_flags": "-O0"
        })
        print(f"  ✓ {s_id} verified and manifest record generated.")
        
    manifest_path = ROOT_DIR / "dataset" / "manifest.json"
    with open(manifest_path, "w") as f:
        json.dump({
            "project": "Hybrid angr + LLM CFF Deobfuscation",
            "samples": manifest_entries
        }, f, indent=2)
        
    print("\n" + "=" * 60)
    print(f"Manifest written to {manifest_path}")
    print("Step 1 successfully completed.")
    print("=" * 60)

if __name__ == "__main__":
    main()
