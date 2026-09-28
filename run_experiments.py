#!/usr/bin/env python3
"""
Master Experiment Orchestration Script: Hybrid angr + LLM CFF Deobfuscation
Executes the full 6-week research workflow end-to-end:
1. Obfuscation pipeline & I/O test verification (pipeline/obfuscate.py)
2. Ground-truth CFG extraction via angr CFGFast (pipeline/extract_ground_truth.py)
3. angr symbolic baseline & artifact serialization (pipeline/angr_deobf.py)
4. LLM-only & Hybrid agent evaluation with single-variable discipline (pipeline/llm_agent.py)
5. Evaluation engine, markdown tables & chart generation (pipeline/evaluate.py)
"""

import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent

def run_step(step_name, script_path):
    print("\n" + "#" * 70)
    print(f"# RUNNING: {step_name}")
    print(f"# Script:  {script_path}")
    print("#" * 70 + "\n")
    
    python_bin = sys.executable
    cmd = [python_bin, str(script_path)]
    res = subprocess.run(cmd, cwd=str(ROOT_DIR))
    if res.returncode != 0:
        print(f"\n[ERROR] Step {step_name} failed with exit code {res.returncode}")
        sys.exit(res.returncode)

def main():
    print("=" * 70)
    print("HYBRID ANGR + LLM CFF DEOBFUSCATION: MASTER EXPERIMENT RUNNER")
    print("=" * 70)
    
    run_step("1. Obfuscation & I/O Generation", ROOT_DIR / "pipeline" / "obfuscate.py")
    run_step("2. Ground Truth CFG Extraction", ROOT_DIR / "pipeline" / "extract_ground_truth.py")
    run_step("3. angr Baseline & Intermediate Serialization", ROOT_DIR / "pipeline" / "angr_deobf.py")
    run_step("4. LLM-Only & Hybrid Deobfuscation", ROOT_DIR / "pipeline" / "llm_agent.py")
    run_step("5. Evaluation, Table & Chart Generation", ROOT_DIR / "pipeline" / "evaluate.py")
    
    print("\n" + "=" * 70)
    print("ALL EXPERIMENT PHASES COMPLETED SUCCESSFULLY!")
    print(f"Results Table:  file://{ROOT_DIR}/results/evaluation_table.md")
    print(f"Chart 1:        file://{ROOT_DIR}/results/charts/pass_rate_by_condition.png")
    print(f"Chart 2:        file://{ROOT_DIR}/results/charts/time_cost_by_condition.png")
    print(f"Reports:        file://{ROOT_DIR}/reports/")
    print("=" * 70)

if __name__ == "__main__":
    main()
