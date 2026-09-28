#!/usr/bin/env python3
"""
Pipeline Step 2: Ground Truth CFG Extraction using angr CFGFast
Extracts clean baseline Control Flow Graph representation for all target functions.
Saves block counts, block addresses, and CFG edges for structural comparison.
"""

import os
import sys
import json
from pathlib import Path
import angr

ROOT_DIR = Path(__file__).resolve().parent.parent

def extract_cfg(binary_path, func_name):
    proj = angr.Project(str(binary_path), auto_load_libs=False)
    cfg = proj.analyses.CFGFast()
    
    # Locate target function
    target_func = None
    for addr, func in cfg.functions.items():
        # Match symbol name or demangled name
        if func.name == func_name or func.name == f"_{func_name}":
            target_func = func
            break
            
    if target_func is None:
        # Fallback: search symbols
        sym = proj.loader.find_symbol(func_name) or proj.loader.find_symbol(f"_{func_name}")
        if sym and sym.rebased_addr in cfg.functions:
            target_func = cfg.functions[sym.rebased_addr]
        else:
            raise ValueError(f"Could not find function {func_name} in {binary_path}")
            
    subgraph = target_func.transition_graph
    nodes = []
    for node in target_func.nodes:
        nodes.append({
            "addr": hex(node.addr),
            "size": node.size,
            "instruction_addrs": [hex(i) for i in getattr(node, "instruction_addrs", [])]
        })
        
    edges = []
    for src, dst, data in subgraph.edges(data=True):
        edges.append({
            "src": hex(src.addr),
            "dst": hex(dst.addr),
            "jumpkind": data.get("jumpkind", "unknown")
        })
        
    return {
        "function_name": func_name,
        "entry_addr": hex(target_func.addr),
        "num_blocks": len(nodes),
        "num_edges": len(edges),
        "blocks": nodes,
        "edges": edges
    }

def main():
    print("=" * 60)
    print("Step 2: Extracting Ground Truth CFGs via angr CFGFast")
    print("=" * 60)
    
    manifest_path = ROOT_DIR / "dataset" / "manifest.json"
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
        
    os.makedirs(ROOT_DIR / "dataset" / "ground_truth_cfgs", exist_ok=True)
    
    for item in manifest["samples"]:
        s_id = item["id"]
        func_name = item["target_function"]
        base_bin = ROOT_DIR / item["baseline_binary"]
        cfg_out_path = ROOT_DIR / "dataset" / "ground_truth_cfgs" / f"{s_id}_cfg.json"
        
        print(f"\nAnalyzing [{s_id}] ({func_name}) at {base_bin}...")
        cfg_data = extract_cfg(base_bin, func_name)
        
        with open(cfg_out_path, "w") as f:
            json.dump(cfg_data, f, indent=2)
            
        item["ground_truth_cfg"] = str(cfg_out_path.relative_to(ROOT_DIR))
        item["baseline_num_blocks"] = cfg_data["num_blocks"]
        item["baseline_num_edges"] = cfg_data["num_edges"]
        
        print(f"  ✓ Ground truth CFG extracted: {cfg_data['num_blocks']} blocks, {cfg_data['num_edges']} edges -> {cfg_out_path.name}")
        
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
        
    print("\n" + "=" * 60)
    print("Ground truth extraction complete. Updated manifest.json")
    print("=" * 60)

if __name__ == "__main__":
    main()
