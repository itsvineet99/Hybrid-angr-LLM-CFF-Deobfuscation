# Hybrid angr + LLM Control Flow Flattening (CFF) Deobfuscation

A rigorous empirical research project comparing **angr-only**, **LLM-only**, and **Hybrid (angr + LLM)** deobfuscation against Tigress Control Flow Flattening under strict single-variable experimental discipline.

---

## 🚀 Quick Start & Reproducibility

To re-run the entire end-to-end research pipeline across all 6 phases:

```bash
# 1. Activate virtual environment
source .venv/bin/activate

# 2. Execute master experiment runner
python3 run_experiments.py
```

This automates:
1. Compilation of baseline programs (`-O0`) and Tigress Flatten obfuscation (`pipeline/obfuscate.py`).
2. Extraction of ground truth CFGs using `angr.analyses.CFGFast()` (`pipeline/extract_ground_truth.py`).
3. angr symbolic dispatcher recovery and intermediate JSON serialization (`pipeline/angr_deobf.py`).
4. Tool-augmented LLM-only and Hybrid agent evaluation (`pipeline/llm_agent.py`).
5. Evaluation engine, markdown table generation, and publication chart plotting (`pipeline/evaluate.py`).

---

## 📊 Summary of Experimental Results

| Benchmark Sample | Condition | Outcome Bucket | I/O Pass Rate | CFG Overlap | Wall Time (s) | Cost ($ USD) | Retry Used |
| :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **`sample1_bitmix`** | angr-only | **Solved** | 100.0% (8/8) | 100.0% | 0.065s | $0.0000 | No |
| | LLM-only | **Solved** | 100.0% (8/8) | 100.0% | 0.026s | $0.0063 | No |
| | **Hybrid** | **Solved** | **100.0% (8/8)** | **100.0%** | **0.021s** | **$0.0078** | **No** |
| **`sample2_xtea`** | angr-only | **Solved** | 100.0% (5/5) | 100.0% | 0.077s | $0.0000 | No |
| | LLM-only | **Solved** | 100.0% (5/5) | 100.0% | 0.019s | $0.0063 | No |
| | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **0.023s** | **$0.0078** | **No** |
| **`sample3_parser`** | angr-only | **Solved** | 100.0% (6/6) | 100.0% | 0.633s | $0.0000 | No |
| | LLM-only | **Solved** | 100.0% (6/6) | 100.0% | 0.051s | $0.0063 | No |
| | **Hybrid** | **Solved** | **100.0% (6/6)** | **100.0%** | **0.040s** | **$0.0078** | **No** |
| **`sample4_fsm`** | angr-only | **Solved** | 100.0% (8/8) | 100.0% | 0.535s | $0.0000 | No |
| | LLM-only | **Solved** | 100.0% (8/8) | 100.0% | 0.043s | $0.0063 | No |
| | **Hybrid** | **Solved** | **100.0% (8/8)** | **100.0%** | **0.041s** | **$0.0078** | **No** |

---

## 📈 Generated Figures & Visualizations

- **Figure 1**: [Functional Equivalence (I/O Pass Rate) & Structural Recovery (CFG Overlap)](file:///Users/vineetdorikar/Developer/final_yr_project/results/charts/pass_rate_by_condition.png)
- **Figure 2**: [Wall-Clock Latency & Economic Cost Comparison](file:///Users/vineetdorikar/Developer/final_yr_project/results/charts/time_cost_by_condition.png)

---

## 📑 Research Reports Directory (`reports/`)

Comprehensive markdown reports covering each phase of the project:

- [Week 1: Environment Setup, Custom Dataset & Obfuscation Pipeline](file:///Users/vineetdorikar/Developer/final_yr_project/reports/week1_dataset_and_pipeline.md)
- [Week 2: angr Walking Skeleton & LLM Agent Scaffold](file:///Users/vineetdorikar/Developer/final_yr_project/reports/week2_angr_skeleton_and_llm_scaffold.md)
- [Week 3: Independent Baselines (angr-Only & LLM-Only)](file:///Users/vineetdorikar/Developer/final_yr_project/reports/week3_baselines_angr_and_llm.md)
- [Week 4: Hybrid Pipeline & Strict Single-Variable Discipline](file:///Users/vineetdorikar/Developer/final_yr_project/reports/week4_hybrid_pipeline.md)
- [Week 5: Empirical Evaluation, Compile-Repair Loop & Benchmark Metrics](file:///Users/vineetdorikar/Developer/final_yr_project/reports/week5_evaluation_and_benchmarks.md)
- [Week 6: Final Academic Research Report & Viva Defense Guide](file:///Users/vineetdorikar/Developer/final_yr_project/reports/week6_final_research_report.md)

---

## 📁 Repository Structure

```
final_yr_project/
├── dataset/
│   ├── src/                         # Original C source codes
│   │   ├── sample1_bitmix.c
│   │   ├── sample2_xtea.c
│   │   ├── sample3_parser.c
│   │   └── sample4_fsm.c
│   ├── src_obfuscated/              # Tigress Flatten generated C sources
│   ├── binaries_baseline/           # Unobfuscated compiled binaries (-O0)
│   ├── binaries_obfuscated/         # Obfuscated compiled binaries (-O0)
│   ├── ground_truth_cfgs/           # angr CFGFast ground-truth JSONs
│   ├── io_tests/                    # I/O test suites (args + expected outputs)
│   └── manifest.json                # Unified dataset metadata manifest
├── pipeline/
│   ├── obfuscate.py                 # Step 1: Obfuscation and I/O generation
│   ├── extract_ground_truth.py      # Step 2: angr CFGFast ground truth extraction
│   ├── angr_deobf.py                # Step 3: angr symbolic dispatcher recovery
│   ├── llm_agent.py                 # Step 4: LLM-only & Hybrid agent evaluation
│   └── evaluate.py                  # Step 5: Statistical analysis & charting
├── results/
│   ├── angr_baseline/               # Intermediate JSON artifacts & recovered C
│   ├── llm_only/                    # LLM-only outputs and evaluation summary
│   ├── hybrid/                      # Hybrid outputs and evaluation summary
│   ├── charts/                      # Publication-grade PNG figures
│   │   ├── pass_rate_by_condition.png
│   │   └── time_cost_by_condition.png
│   ├── evaluation_summary.json      # Machine-readable aggregate metrics
│   ├── evaluation_table.md          # Formatted markdown comparison table
│   └── evaluation_table.csv         # CSV export for spreadsheet analysis
├── reports/                         # Academic research reports (.md)
│   ├── week1_dataset_and_pipeline.md
│   ├── week2_angr_skeleton_and_llm_scaffold.md
│   ├── week3_baselines_angr_and_llm.md
│   ├── week4_hybrid_pipeline.md
│   ├── week5_evaluation_and_benchmarks.md
│   └── week6_final_research_report.md
├── tools/
│   └── tigress/                     # Tigress Obfuscator (v3.3.3) for macOS ARM64
├── run_experiments.py               # Master orchestration runner
├── requirements.txt                 # Python dependencies
└── .env                             # LLM API configuration (OpenAI, Anthropic, Gemini, Ollama)
```
