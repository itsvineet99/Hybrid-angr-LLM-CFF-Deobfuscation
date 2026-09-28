#!/usr/bin/env python3
"""
Pipeline Step 6: Evaluation Engine, Comparative Aggregation & Chart Generation
Implements Week 5 deliverables:
- Aggregates results across all 3 conditions (angr-only, LLM-only, Hybrid) x 4 samples
- Computes Functional Equivalence (I/O pass rate), Structural CFG Overlap, Latency, Cost, and Outcome Buckets
- Generates Markdown & CSV comparison tables
- Renders 2 publication-grade charts:
    (1) Pass Rate and CFG Overlap by Condition
    (2) Time (Latency) and Cost by Condition
"""

import os
import sys
import json
import csv
from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np

ROOT_DIR = Path(__file__).resolve().parent.parent

def load_data():
    angr_path = ROOT_DIR / "results" / "angr_baseline" / "angr_results_summary.json"
    llm_path = ROOT_DIR / "results" / "llm_only" / "llm_only_summary.json"
    hybrid_path = ROOT_DIR / "results" / "hybrid" / "hybrid_summary.json"
    
    with open(angr_path) as f:
        angr_data = json.load(f)
    with open(llm_path) as f:
        llm_data = json.load(f)
    with open(hybrid_path) as f:
        hybrid_data = json.load(f)
        
    return angr_data, llm_data, hybrid_data

def generate_markdown_table(samples, angr_data, llm_data, hybrid_data):
    md = []
    md.append("# Three-Way Experimental Evaluation: angr-only vs. LLM-only vs. Hybrid CFF Deobfuscation\n")
    md.append("| Benchmark Sample | Condition | Outcome Bucket | I/O Pass Rate | CFG Overlap | Wall Time (s) | Cost ($ USD) | Retry Used |")
    md.append("| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |")
    
    for s in samples:
        a = angr_data.get(s, {})
        l = llm_data.get(s, {})
        h = hybrid_data.get(s, {})
        
        md.append(f"| **{s}** | angr-only | {a.get('outcome_bucket', 'N/A')} | {a.get('io_pass_rate', 0)*100:.1f}% ({a.get('passed_tests', '0')}) | {a.get('cfg_overlap_ratio', 0)*100:.1f}% | {a.get('latency_seconds', 0):.3f}s | ${a.get('cost_dollars', 0):.4f} | No |")
        md.append(f"| | LLM-only | {l.get('outcome_bucket', 'N/A')} | {l.get('io_pass_rate', 0)*100:.1f}% ({l.get('passed_tests', '0')}) | {l.get('cfg_overlap_ratio', 0)*100:.1f}% | {l.get('latency_seconds', 0):.3f}s | ${l.get('cost_dollars', 0):.4f} | {'Yes' if l.get('repair_attempted') else 'No'} |")
        md.append(f"| | **Hybrid (angr+LLM)** | **{h.get('outcome_bucket', 'N/A')}** | **{h.get('io_pass_rate', 0)*100:.1f}% ({h.get('passed_tests', '0')})** | **{h.get('cfg_overlap_ratio', 0)*100:.1f}%** | **{h.get('latency_seconds', 0):.3f}s** | **${h.get('cost_dollars', 0):.4f}** | {'Yes' if h.get('repair_attempted') else 'No'} |")
        
    return "\n".join(md)

def generate_csv_table(samples, angr_data, llm_data, hybrid_data, out_path):
    rows = [["Sample", "Condition", "OutcomeBucket", "IOPassRate", "PassedTests", "CFGOverlap", "WallTimeSec", "CostUSD", "RetryUsed"]]
    for s in samples:
        for cond_name, cdata in [("angr-only", angr_data), ("LLM-only", llm_data), ("Hybrid", hybrid_data)]:
            d = cdata.get(s, {})
            rows.append([
                s,
                cond_name,
                d.get("outcome_bucket", ""),
                f"{d.get('io_pass_rate', 0)*100:.1f}%",
                d.get("passed_tests", ""),
                f"{d.get('cfg_overlap_ratio', 0)*100:.1f}%",
                f"{d.get('latency_seconds', 0):.3f}",
                f"{d.get('cost_dollars', 0):.4f}",
                "Yes" if d.get("repair_attempted") else "No"
            ])
    with open(out_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(rows)

def plot_charts(samples, angr_data, llm_data, hybrid_data, chart_dir):
    os.makedirs(chart_dir, exist_ok=True)
    
    # -------------------------------------------------------------
    # Chart 1: Pass Rate & CFG Overlap by Condition
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    sample_labels = [s.replace("sample", "S").replace("_", "\n") for s in samples]
    x = np.arange(len(samples))
    width = 0.25
    
    # I/O Pass Rates
    angr_pass = [angr_data[s]["io_pass_rate"] * 100 for s in samples]
    llm_pass = [llm_data[s]["io_pass_rate"] * 100 for s in samples]
    hybrid_pass = [hybrid_data[s]["io_pass_rate"] * 100 for s in samples]
    
    ax1.bar(x - width, angr_pass, width, label='angr-only', color='#4575b4', alpha=0.9)
    ax1.bar(x, llm_pass, width, label='LLM-only', color='#fdae61', alpha=0.9)
    ax1.bar(x + width, hybrid_pass, width, label='Hybrid', color='#2ca25f', alpha=0.9)
    
    ax1.set_ylabel('Functional Equivalence Pass Rate (%)', fontsize=12, fontweight='bold')
    ax1.set_title('(a) Functional Equivalence (I/O Pass Rate)', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(sample_labels, fontsize=10)
    ax1.set_ylim(0, 115)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(loc='lower right', frameon=True)
    
    # CFG Overlap
    angr_cfg = [angr_data[s]["cfg_overlap_ratio"] * 100 for s in samples]
    llm_cfg = [llm_data[s]["cfg_overlap_ratio"] * 100 for s in samples]
    hybrid_cfg = [hybrid_data[s]["cfg_overlap_ratio"] * 100 for s in samples]
    
    ax2.bar(x - width, angr_cfg, width, label='angr-only', color='#4575b4', alpha=0.9)
    ax2.bar(x, llm_cfg, width, label='LLM-only', color='#fdae61', alpha=0.9)
    ax2.bar(x + width, hybrid_cfg, width, label='Hybrid', color='#2ca25f', alpha=0.9)
    
    ax2.set_ylabel('Structural CFG Overlap Ratio (%)', fontsize=12, fontweight='bold')
    ax2.set_title('(b) Structural Recovery (CFG Overlap)', fontsize=13, fontweight='bold')
    ax2.set_xticks(x)
    ax2.set_xticklabels(sample_labels, fontsize=10)
    ax2.set_ylim(0, 115)
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    ax2.legend(loc='lower right', frameon=True)
    
    plt.tight_layout()
    chart1_path = chart_dir / "pass_rate_by_condition.png"
    plt.savefig(chart1_path, dpi=300)
    plt.close()
    print(f"  ✓ Saved Chart 1: {chart1_path}")
    
    # -------------------------------------------------------------
    # Chart 2: Time (Latency) & Cost by Condition
    # -------------------------------------------------------------
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    angr_time = [angr_data[s]["latency_seconds"] for s in samples]
    llm_time = [llm_data[s]["latency_seconds"] for s in samples]
    hybrid_time = [hybrid_data[s]["latency_seconds"] for s in samples]
    
    ax1.bar(x - width, angr_time, width, label='angr-only', color='#4575b4', alpha=0.9)
    ax1.bar(x, llm_time, width, label='LLM-only', color='#fdae61', alpha=0.9)
    ax1.bar(x + width, hybrid_time, width, label='Hybrid', color='#2ca25f', alpha=0.9)
    
    ax1.set_ylabel('Execution Latency (seconds)', fontsize=12, fontweight='bold')
    ax1.set_title('(a) Wall-Clock Latency per Sample', fontsize=13, fontweight='bold')
    ax1.set_xticks(x)
    ax1.set_xticklabels(sample_labels, fontsize=10)
    ax1.grid(axis='y', linestyle='--', alpha=0.5)
    ax1.legend(loc='upper right', frameon=True)
    
    # Cumulative Cost Comparison
    conditions = ['angr-only', 'LLM-only', 'Hybrid']
    total_costs = [
        sum(angr_data[s]["cost_dollars"] for s in samples),
        sum(llm_data[s]["cost_dollars"] for s in samples),
        sum(hybrid_data[s]["cost_dollars"] for s in samples)
    ]
    colors = ['#4575b4', '#fdae61', '#2ca25f']
    
    bars = ax2.bar(conditions, total_costs, color=colors, width=0.5, alpha=0.9)
    ax2.set_ylabel('Total Cost ($ USD)', fontsize=12, fontweight='bold')
    ax2.set_title('(b) Total Economic Cost across Dataset', fontsize=13, fontweight='bold')
    ax2.grid(axis='y', linestyle='--', alpha=0.5)
    
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2.0, yval + 0.0005, f"${yval:.4f}", ha='center', va='bottom', fontweight='bold')
        
    plt.tight_layout()
    chart2_path = chart_dir / "time_cost_by_condition.png"
    plt.savefig(chart2_path, dpi=300)
    plt.close()
    print(f"  ✓ Saved Chart 2: {chart2_path}")

def main():
    print("=" * 60)
    print("Step 6: Evaluation Engine & Publication Chart Generation")
    print("=" * 60)
    
    angr_data, llm_data, hybrid_data = load_data()
    samples = list(angr_data.keys())
    
    # 1. Generate Markdown Table
    md_content = generate_markdown_table(samples, angr_data, llm_data, hybrid_data)
    md_path = ROOT_DIR / "results" / "evaluation_table.md"
    with open(md_path, "w") as f:
        f.write(md_content)
    print(f"  ✓ Saved Markdown Table: {md_path}")
    
    # 2. Generate CSV Table
    csv_path = ROOT_DIR / "results" / "evaluation_table.csv"
    generate_csv_table(samples, angr_data, llm_data, hybrid_data, csv_path)
    print(f"  ✓ Saved CSV Table: {csv_path}")
    
    # 3. Generate Charts
    chart_dir = ROOT_DIR / "results" / "charts"
    plot_charts(samples, angr_data, llm_data, hybrid_data, chart_dir)
    
    # 4. Save JSON Summary
    summary = {
        "num_samples": len(samples),
        "conditions": ["angr-only", "llm-only", "hybrid"],
        "mean_io_pass_rate": {
            "angr-only": float(np.mean([angr_data[s]["io_pass_rate"] for s in samples])),
            "llm-only": float(np.mean([llm_data[s]["io_pass_rate"] for s in samples])),
            "hybrid": float(np.mean([hybrid_data[s]["io_pass_rate"] for s in samples]))
        },
        "mean_cfg_overlap": {
            "angr-only": float(np.mean([angr_data[s]["cfg_overlap_ratio"] for s in samples])),
            "llm-only": float(np.mean([llm_data[s]["cfg_overlap_ratio"] for s in samples])),
            "hybrid": float(np.mean([hybrid_data[s]["cfg_overlap_ratio"] for s in samples]))
        },
        "mean_latency_seconds": {
            "angr-only": float(np.mean([angr_data[s]["latency_seconds"] for s in samples])),
            "llm-only": float(np.mean([llm_data[s]["latency_seconds"] for s in samples])),
            "hybrid": float(np.mean([hybrid_data[s]["latency_seconds"] for s in samples]))
        },
        "total_cost_dollars": {
            "angr-only": float(np.sum([angr_data[s]["cost_dollars"] for s in samples])),
            "llm-only": float(np.sum([llm_data[s]["cost_dollars"] for s in samples])),
            "hybrid": float(np.sum([hybrid_data[s]["cost_dollars"] for s in samples]))
        }
    }
    
    summary_path = ROOT_DIR / "results" / "evaluation_summary.json"
    with open(summary_path, "w") as f:
        json.dump(summary, f, indent=2)
    print(f"  ✓ Saved Evaluation Summary: {summary_path}")
    
    print("\n" + "=" * 60)
    print("Aggregate Benchmark Metrics:")
    print(f"  I/O Pass Rate:  angr={summary['mean_io_pass_rate']['angr-only']*100:.1f}% | LLM={summary['mean_io_pass_rate']['llm-only']*100:.1f}% | Hybrid={summary['mean_io_pass_rate']['hybrid']*100:.1f}%")
    print(f"  CFG Overlap:    angr={summary['mean_cfg_overlap']['angr-only']*100:.1f}% | LLM={summary['mean_cfg_overlap']['llm-only']*100:.1f}% | Hybrid={summary['mean_cfg_overlap']['hybrid']*100:.1f}%")
    print(f"  Mean Latency:   angr={summary['mean_latency_seconds']['angr-only']:.3f}s | LLM={summary['mean_latency_seconds']['llm-only']:.3f}s | Hybrid={summary['mean_latency_seconds']['hybrid']:.3f}s")
    print("=" * 60)

if __name__ == "__main__":
    main()
