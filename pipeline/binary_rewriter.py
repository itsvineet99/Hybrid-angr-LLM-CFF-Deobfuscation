#!/usr/bin/env python3
"""
Pipeline Step 4 (Advanced Research Extension): Automated Binary Deflattening & Rewriter
Performs direct machine-code binary patching on obfuscated Mach-O/ELF binaries:
1. Takes the intermediate symbolic transition graph from angr
2. Computes direct branch displacement targets (b <target>) to bypass the switch dispatcher
3. Patches the machine instructions directly in the binary .text segment
4. Applies ad-hoc code-signing for macOS Apple Silicon (codesign -f -s -)
5. Validates functional equivalence on the patched executable binary
"""

import os
import sys
import json
import struct
import shutil
import subprocess
from pathlib import Path
import angr
from capstone import Cs, CS_ARCH_ARM64, CS_MODE_ARM

ROOT_DIR = Path(__file__).resolve().parent.parent

def encode_arm64_branch(from_addr, to_addr):
    offset = to_addr - from_addr
    imm26 = (offset // 4) & 0x03FFFFFF
    insn_val = 0x14000000 | imm26
    return struct.pack("<I", insn_val)

def patch_binary(s_id, manifest_entry):
    angr_json_path = ROOT_DIR / "results" / "angr_baseline" / f"{s_id}_angr.json"
    if not angr_json_path.exists():
        print(f"  [Skip] {angr_json_path.name} not found.")
        return None
        
    with open(angr_json_path) as f:
        artifact = json.load(f)
        
    if artifact.get("solve_status") == "failed":
        print(f"  [Skip] {s_id} marked as failed in angr baseline.")
        return None
        
    obf_bin_path = ROOT_DIR / manifest_entry["obfuscated_binary"]
    out_dir = ROOT_DIR / "results" / "patched_binaries"
    os.makedirs(out_dir, exist_ok=True)
    patched_bin_path = out_dir / f"{s_id}_deobfuscated_bin"
    
    shutil.copy2(obf_bin_path, patched_bin_path)
    
    proj = angr.Project(str(obf_bin_path), auto_load_libs=False)
    cfg = proj.analyses.CFGFast()
    func = [f for f in cfg.functions.values() if manifest_entry["target_function"] in f.name][0]
    
    latch_addr = int(artifact.get("latch_addr", "0x0"), 16)
    dispatcher_addr = int(artifact.get("dispatcher_addr", "0x0"), 16)
    
    # Build state-to-handler lookup
    state_to_handler = {}
    for blk in artifact.get("blocks", []):
        if "next_states" in blk:
            addr = int(blk["addr"], 16)
            # Find the state values that jump here
            state_to_handler[addr] = addr

    cs = Cs(CS_ARCH_ARM64, CS_MODE_ARM)
    patches_applied = 0
    
    with open(patched_bin_path, "r+b") as f:
        for blk in artifact.get("blocks", []):
            blk_addr = int(blk["addr"], 16)
            b = proj.factory.block(blk_addr)
            
            # Find the trailing jump instruction
            last_insn = None
            for insn in b.capstone.insns:
                if insn.mnemonic.startswith("b") and not insn.mnemonic.startswith("b."):
                    last_insn = insn
                    
            if last_insn and blk.get("next_states") and len(blk["next_states"]) == 1:
                next_st = blk["next_states"][0]
                # Find target block address matching this state
                target_block_addr = None
                for candidate in artifact.get("blocks", []):
                    # Check entry state
                    if candidate.get("entry_state") == f"state_{next_st}" or candidate.get("entry_state") == hex(next_st):
                        target_block_addr = int(candidate["addr"], 16)
                        break
                        
                if target_block_addr and target_block_addr != blk_addr:
                    # Virtual address to file offset
                    file_offset = proj.loader.find_object_containing(last_insn.address).addr_to_offset(last_insn.address)
                    new_insn_bytes = encode_arm64_branch(last_insn.address, target_block_addr)
                    
                    f.seek(file_offset)
                    f.write(new_insn_bytes)
                    patches_applied += 1
                    
    # Re-sign patched Mach-O binary for Apple Silicon
    os.chmod(patched_bin_path, 0o755)
    subprocess.run(["codesign", "-f", "-s", "-", str(patched_bin_path)], capture_output=True)
    
    # Validate against I/O test suite
    io_test_file = ROOT_DIR / manifest_entry["io_test_path"]
    with open(io_test_file) as f:
        io_tests = json.load(f)
        
    passed = 0
    total = len(io_tests)
    for test in io_tests:
        res = subprocess.run([str(patched_bin_path)] + test["args"], capture_output=True, text=True)
        if res.returncode == 0 and res.stdout.strip() == test["expected_output"]:
            passed += 1
            
    pass_rate = passed / total
    print(f"  ✓ Patched Binary {patched_bin_path.name}: {patches_applied} branches rewritten. I/O Pass: {passed}/{total} ({pass_rate*100:.1f}%)")
    
    return {
        "sample_id": s_id,
        "patched_binary_path": str(patched_bin_path.relative_to(ROOT_DIR)),
        "patches_applied": patches_applied,
        "io_pass_rate": pass_rate,
        "passed_tests": f"{passed}/{total}"
    }

def main():
    print("=" * 60)
    print("Step 4 (Research Extension): Automated Binary Deflattening")
    print("Direct Machine-Code Patching on Compiled Binaries")
    print("=" * 60)
    
    manifest_path = ROOT_DIR / "dataset" / "manifest.json"
    with open(manifest_path) as f:
        manifest = json.load(f)
        
    summary = {}
    for item in manifest["samples"]:
        s_id = item["id"]
        print(f"\nProcessing Binary Deflattening for [{s_id}]...")
        res = patch_binary(s_id, item)
        if res:
            summary[s_id] = res
            
    out_file = ROOT_DIR / "results" / "patched_binaries" / "patching_summary.json"
    with open(out_file, "w") as f:
        json.dump(summary, f, indent=2)
        
    print("\n" + "=" * 60)
    print(f"Binary deflattening summary saved to: {out_file}")
    print("=" * 60)

if __name__ == "__main__":
    main()
