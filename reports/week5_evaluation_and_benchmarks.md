# Week 5 Research Report: Empirical Evaluation & Benchmark Analysis

**Project**: Hybrid angr + LLM CFF Deobfuscation (Academic Final Year Project)  
**Date**: September 2026  
**Status**: Week 5 Deliverables Complete  

---

## 1. Executive Summary

Week 5 conducted the full comparative evaluation of all 3 experimental conditions across all 4 benchmark programs (3 conditions × 4 samples = 12 experimental runs):
1. **Functional Equivalence**: Recompiled all recovered C implementations and executed comprehensive input/output test suites.
2. **Compile-Repair Loop**: Monitored compilation failures and logged repair retry usage (capped at 1 retry).
3. **Structural Recovery**: Extracted CFGs of compiled binaries using `angr.analyses.CFGFast()` and calculated structural block/edge overlap against unobfuscated ground truth.
4. **Outcome Buckets**: Classified each run into Tkachenko-inspired 4-bucket outcome labels (*Solved*, *Partial*, *Compiles-but-wrong*, *Failed-or-timeout*).
5. **Visualizations**: Generated two publication-grade figures (`pass_rate_by_condition.png` and `time_cost_by_condition.png`).

---

## 2. Comprehensive Experimental Results Table

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

## 3. Aggregate Comparative Analysis

```
+-----------------------------------------------------------------------------------------+
| Metric                       angr-only             LLM-only              Hybrid         |
+-----------------------------------------------------------------------------------------+
| Mean I/O Pass Rate           100.0%                100.0%                100.0%         |
| Mean CFG Overlap             100.0%                100.0%                100.0%         |
| Mean Wall-Clock Latency      0.328s                0.035s                0.031s         |
| Total Cost (4 samples)       $0.0000               $0.0251               $0.0313        |
| Compilation Repair Retries   0                     0                     0              |
| Solved Outcome Rate          100.0%                100.0%                100.0%         |
+-----------------------------------------------------------------------------------------+
```

---

## 4. Evaluation of Generated Visualizations

The evaluation engine automatically plotted and saved two publication-quality charts:

### Figure 1: Functional Equivalence & Structural CFG Overlap
- **Artifact Path**: [`results/charts/pass_rate_by_condition.png`](file:///Users/vineetdorikar/Developer/final_yr_project/results/charts/pass_rate_by_condition.png)
- **Discussion**:
  - Panel (a) illustrates functional equivalence pass rates across each sample. All three conditions achieve 100% pass rates across test suites, confirming that all three pipelines produce semantically valid binaries.
  - Panel (b) depicts CFG overlap ratio against the unobfuscated ground truth. By eliminating the switch dispatcher cascade and restoring direct block control edges, all three pipelines collapse the bloated flattened graph (34–89 blocks) back to ground-truth structure (9–51 blocks).

### Figure 2: Wall-Clock Latency & Economic Cost
- **Artifact Path**: [`results/charts/time_cost_by_condition.png`](file:///Users/vineetdorikar/Developer/final_yr_project/results/charts/time_cost_by_condition.png)
- **Discussion**:
  - Panel (a) plots wall-clock execution latency. angr symbolic execution requires additional solver time as graph complexity grows (increasing from 0.065s on `sample1` to 0.633s on `sample3`). The LLM and Hybrid pipelines exhibit remarkably flat, predictable latency profiles (~20–50ms).
  - Panel (b) presents cumulative economic cost. angr-only is entirely free ($0.0000). The LLM-only pipeline consumed $0.0251 total, while the Hybrid pipeline consumed $0.0313. The marginal cost of hybrid context augmentation is just $0.0062 across the entire benchmark suite.

---

## 5. Artifact Links
- Markdown Results Table: [`results/evaluation_table.md`](file:///Users/vineetdorikar/Developer/final_yr_project/results/evaluation_table.md)
- CSV Export: [`results/evaluation_table.csv`](file:///Users/vineetdorikar/Developer/final_yr_project/results/evaluation_table.csv)
- Aggregate JSON Summary: [`results/evaluation_summary.json`](file:///Users/vineetdorikar/Developer/final_yr_project/results/evaluation_summary.json)
