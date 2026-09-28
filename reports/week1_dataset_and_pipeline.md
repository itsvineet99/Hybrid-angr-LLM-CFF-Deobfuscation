# Week 1 Research Report: Environment Setup, Custom Dataset & Obfuscation Pipeline

**Project**: Hybrid angr + LLM CFF Deobfuscation (Academic Final Year Project)  
**Date**: September 2026  
**Status**: Week 1 Deliverables Complete  

---

## 1. Executive Summary

Week 1 focused on constructing a reproducible, robust experimental foundation:
1. Configuring a modern native toolchain on **Python 3.12+** (macOS Darwin ARM64).
2. Pinning and integrating the **Tigress Obfuscator (v3.3.3)** for C-source level Control Flow Flattening (CFF).
3. Authoring **4 bespoke benchmark C programs** spanning four distinct programmatic domains (under 10 basic blocks pre-obfuscation).
4. Compiling both unobfuscated baseline and obfuscated variants with identical optimization levels (`-O0`).
5. Extracting ground-truth Control Flow Graphs (CFGs) directly at the binary level using **angr CFGFast**.
6. Synthesizing deterministic Input/Output (I/O) verification test suites and persisting a unified dataset manifest.

---

## 2. Toolchain Configuration & Decisions

### 2.1 Python 3.12+ and angr 10.0+
As established in recent binary analysis literature, modern `angr` (v10.0.0+) requires Python 3.12+. The local environment was initialized using a clean Python 3.12.6 virtual environment (`.venv`), deploying:
- `angr` (10.0.0)
- `claripy` (9.2.14)
- `capstone` (5.0.9)
- `z3-solver` (5.1.0.0)

### 2.2 Obfuscator Selection: Tigress vs. Hikari
The original Hikari LLVM project has been archived, with modern forks remaining unstable and labor-intensive to build. Consequently, **Tigress (v3.3.3)** was selected as the core obfuscator. 

Tigress performs transformations at the C AST level rather than inside LLVM IR. Crucially, its `Flatten` transform generates standard switch-dispatcher Control Flow Flattening (CFF) with an explicit state variable, matching the exact attack surface studied in foundational literature (e.g., ALFREDO, CaDeCFF).

---

## 3. Dataset Architecture: Four Core Custom Samples

To avoid memorization confounds inherent in standard textbook snippets (e.g., standard quicksort or MD5 implementations memorized by LLM pretraining corpora), four self-contained C samples were custom-authored. Each sample is scoped to ~10 basic blocks pre-obfuscation to minimize angr state-space explosion while keeping LLM context tokens manageable.

| Sample ID | Category | Target Function | Pre-Obf Blocks | Pre-Obf Edges | Functional Description |
| :--- | :--- | :--- | :---: | :---: | :--- |
| `sample1_bitmix` | Arithmetic / Bit Manipulation | `sample1_bitmix` | 9 | 10 | Non-linear 32-bit mixing, rotations, conditional parity XOR |
| `sample2_xtea` | Crypto Primitive | `sample2_xtea_round` | 9 | 10 | Single Feistel cipher round with golden ratio delta constant |
| `sample3_parser` | String / Token Parser | `sample3_parser` | 39 | 50 | Tagged integer protocol parser (`<TAG>:<VAL>;`) with sign handling |
| `sample4_fsm` | State Machine | `sample4_fsm` | 51 | 64 | Vending machine / protocol FSM with balance & dispense logic |

### Source Locations:
- [`sample1_bitmix.c`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/src/sample1_bitmix.c)
- [`sample2_xtea.c`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/src/sample2_xtea.c)
- [`sample3_parser.c`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/src/sample3_parser.c)
- [`sample4_fsm.c`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/src/sample4_fsm.c)

---

## 4. Obfuscation Pipeline & Compilation Discipline

### 4.1 Single-Variable Compilation Discipline
To guarantee that optimization levels do not introduce hidden variables into CFG complexity or ground truth semantics:
- Baseline binaries were compiled with: `clang -O0 <src>.c -o <bin>`
- Obfuscated code was generated with: `tigress --Environment=arm64:Darwin:Clang:5.1 --Transform=Flatten --Functions=<target_func>`
- Obfuscated binaries were compiled with: `clang -O0 <obf_src>.c -o <obf_bin>`

### 4.2 Structural Expansion Under Flattening
Tigress Flatten transforms linear and structured control flow into an indirect switch dispatcher with basic block handlers looping back to a central latch.

```
+-----------------------------------------------------------+
|               Complexity Expansion Ratio                  |
| Sample 1 (BitMix):  9  blocks -> 34 blocks (3.78x growth) |
| Sample 2 (XTEA):    9  blocks -> 34 blocks (3.78x growth) |
| Sample 3 (Parser):  39 blocks -> 75 blocks (1.92x growth) |
| Sample 4 (FSM):     51 blocks -> 89 blocks (1.75x growth) |
+-----------------------------------------------------------+
```

---

## 5. Ground Truth CFG Extraction via angr CFGFast

Rather than extracting ground truth via LLVM IR passes (which introduces representation mismatch when comparing against machine-level binary CFGs), ground truth was recovered directly from unobfuscated binaries via `angr.analyses.CFGFast()`.

The ground-truth CFGs are stored as JSON artifacts:
- [`sample1_bitmix_cfg.json`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/ground_truth_cfgs/sample1_bitmix_cfg.json)
- [`sample2_xtea_cfg.json`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/ground_truth_cfgs/sample2_xtea_cfg.json)
- [`sample3_parser_cfg.json`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/ground_truth_cfgs/sample3_parser_cfg.json)
- [`sample4_fsm_cfg.json`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/ground_truth_cfgs/sample4_fsm_cfg.json)

---

## 6. Functional Equivalence Test Suites & Manifest

For each sample, deterministic test inputs covering edge cases (zeroes, boundary conditions, negative integers, malformed tokens) were executed against both baseline and obfuscated binaries. 100% equivalence was confirmed across all 27 total test cases.

The entire dataset state is recorded in [`dataset/manifest.json`](file:///Users/vineetdorikar/Developer/final_yr_project/dataset/manifest.json).
