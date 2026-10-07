# Hybrid angr + LLM Control Flow Flattening (CFF) Deobfuscation

A publication-grade research project combining **angr symbolic execution** with **Large Language Models (LLMs)** to deobfuscate Tigress Control Flow Flattening under strict single-variable experimental discipline, evaluated across **7 production-grade benchmarks** (including GNU Coreutils & OpenSSL AES) with automated ARM64 machine-code binary deflattening.

---

## 🚀 Quick Start & Reproducibility ($0 Cost, 8 GB RAM)

To re-run the entire end-to-end research pipeline across all 6 phases:

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Configure .env with your free Groq or Gemini API keys
# GROQ_API_KEY=gsk_...
# GROQ_MODEL=qwen/qwen3.8-27b
# GEMINI_API_KEY=...
# GEMINI_MODEL=gemini-flash-latest

# 3. Execute master experiment runner
python3 run_experiments.py
```

This automates:
1. Compilation of baseline programs (`-O0`) and Tigress Flatten obfuscation (`pipeline/obfuscate.py`).
2. Extraction of ground truth CFGs using `angr.analyses.CFGFast()` (`pipeline/extract_ground_truth.py`).
3. angr symbolic dispatcher recovery and intermediate JSON serialization (`pipeline/angr_deobf.py`).
4. Tool-augmented LLM-only and Hybrid agent evaluation (`pipeline/llm_agent.py`).
5. Direct ARM64 machine-code branch patching and ad-hoc codesigning (`pipeline/binary_rewriter.py`).
6. Evaluation engine, markdown table generation, and publication chart plotting (`pipeline/evaluate.py`).

---

## 📊 Master Evaluation Results (7 Benchmarks)

| Benchmark Sample | Category | Condition | Outcome Bucket | I/O Pass Rate | CFG Overlap | Complexity Reduction | Wall Time (s) | Cost ($ USD) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`sample1_bitmix`** | Custom | angr-only | **Solved** | 100.0% (8/8) | 100.0% | - | 0.075s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/8) | 0.0% | -0.0% (13→0) | 1.223s | $0.0000 |
| | | **Hybrid** | **Partial** | **25.0% (2/8)** | **100.0%** | **-69.2% (13→4)** | **1.239s** | **$0.0000** |
| **`sample2_xtea`** | Crypto | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.068s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/5) | 0.0% | -0.0% (13→0) | 0.548s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-69.2% (13→4)** | **8.183s** | **$0.0000** |
| **`sample3_parser`** | Parsing | angr-only | **Solved** | 100.0% (6/6) | 100.0% | - | 0.627s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/6) | 0.0% | -0.0% (37→0) | 9.403s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (6/6)** | **100.0%** | **-62.2% (37→14)** | **37.028s** | **$0.0000** |
| **`sample4_fsm`** | State Machine | angr-only | **Solved** | 100.0% (8/8) | 100.0% | - | 0.516s | $0.0000 |
| | | LLM-only | **Partial** | 25.0% (2/8) | 45.1% | -77.3% (44→10) | 9.107s | $0.0000 |
| | | **Hybrid** | **Failed-or-timeout** | **0.0% (0/8)** | **0.0%** | **-68.2% (44→14)** | **57.661s** | **$0.0000** |
| **`sample5_coreutils_base64`** | GNU Coreutils | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.884s | $0.0000 |
| | | LLM-only | **Compiles-but-wrong** | 0.0% (0/5) | 72.0% | -77.4% (31→7) | 17.723s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-71.0% (31→9)** | **32.895s** | **$0.0000** |
| **`sample6_coreutils_md5`** | GNU Coreutils | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.266s | $0.0000 |
| | | LLM-only | **Solved** | 100.0% (5/5) | 92.9% | -62.5% (16→6) | 11.676s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-68.8% (16→5)** | **32.955s** | **$0.0000** |
| **`sample7_crypto_aes`** | OpenSSL Crypto | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.042s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/5) | 0.0% | -0.0% (13→0) | 10.023s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-69.2% (13→4)** | **23.650s** | **$0.0000** |

```
=================================================================================================
Summary Dimension                    angr-only            LLM-only             Hybrid
=================================================================================================
Functional Solve Rate (100% I/O)     7 / 7 (100.0%)       1 / 7 (14.3%)        5 / 7 (71.4%)
Mean I/O Test Pass Rate              100.0%               17.9%                75.0%
Mean Ground-Truth CFG Overlap        100.0%               30.0%                85.7%
Mean Cyclomatic Complexity Reduction N/A (assembly)       -31.0%               -68.3%
Mean Execution Latency               0.354s               8.529s               27.659s
Monetary Cost (7 Benchmarks)         $0.0000              $0.0000              $0.0000
=================================================================================================
```

---

## 📈 Generated Figures & Visualizations

- **Figure 1**: [Functional Equivalence (I/O Pass Rate) & Structural Recovery (CFG Overlap)](results/charts/pass_rate_by_condition.png)
- **Figure 2**: [Wall-Clock Latency & Economic Cost Comparison](results/charts/time_cost_by_condition.png)

---

## 📑 Research Reports Directory (`reports/`)

Comprehensive markdown reports documenting each phase of the project:

- [Week 1: Environment Setup, Custom Dataset & Obfuscation Pipeline](reports/week1_dataset_and_pipeline.md)
- [Week 2: angr Walking Skeleton & LLM Agent Scaffold](reports/week2_angr_skeleton_and_llm_scaffold.md)
- [Week 3: Independent Baselines (angr-Only & LLM-Only)](reports/week3_baselines_angr_and_llm.md)
- [Week 4: Hybrid Pipeline & Strict Single-Variable Discipline](reports/week4_hybrid_pipeline.md)
- [Week 5: Empirical Evaluation, Compile-Repair Loop & Benchmark Metrics](reports/week5_evaluation_and_benchmarks.md)
- [Week 6: Final Academic Research Report & Viva Defense Guide](reports/week6_final_research_report.md)

---

## 📁 Repository Structure

```
final_yr_project/
├── dataset/
│   ├── src/                         # Original C benchmarks (Bitmix, XTEA, Parser, FSM, Base64, MD5, AES)
│   ├── src_obfuscated/              # Tigress Flatten generated C sources
│   ├── binaries_baseline/           # Unobfuscated compiled binaries (-O0)
│   ├── binaries_obfuscated/         # Obfuscated compiled binaries (-O0)
│   ├── ground_truth_cfgs/           # angr CFGFast ground-truth JSONs
│   ├── io_tests/                    # Concrete I/O test suites (32 test vectors)
│   └── manifest.json                # Unified dataset metadata manifest
├── pipeline/
│   ├── obfuscate.py                 # Step 1: Obfuscation and I/O generation
│   ├── extract_ground_truth.py      # Step 2: angr CFGFast ground truth extraction
│   ├── angr_deobf.py                # Step 3: angr symbolic dispatcher recovery
│   ├── llm_agent.py                 # Step 4: Tool-augmented LLM-only & Hybrid agent evaluation
│   ├── binary_rewriter.py           # Step 5: ARM64 Mach-O direct branch patching
│   └── evaluate.py                  # Step 6: Statistical analysis & charting
├── results/
│   ├── angr_baseline/               # Intermediate JSON artifacts & recovered C
│   ├── llm_only/                    # LLM-only outputs and evaluation summary
│   ├── hybrid/                      # Hybrid outputs and evaluation summary
│   ├── patched_binaries/            # Deflattened Mach-O binaries with ad-hoc codesigning
│   ├── charts/                      # Publication-grade PNG figures
│   ├── evaluation_summary.json      # Machine-readable aggregate metrics
│   ├── evaluation_table.md          # Master markdown comparison table
│   └── evaluation_table.csv         # Master CSV export
├── reports/                         # Publication-grade research papers & reports (.md)
├── tools/
│   └── tigress/                     # Tigress Obfuscator (v3.3.3) for macOS ARM64
├── run_experiments.py               # Master orchestration runner (Steps 1–6)
├── requirements.txt                 # Python dependencies
└── .env                             # Cloud LLM API configuration (Groq, Gemini)
```
