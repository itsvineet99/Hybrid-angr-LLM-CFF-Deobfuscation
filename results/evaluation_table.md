# Three-Way Experimental Evaluation: angr-only vs. LLM-only vs. Hybrid CFF Deobfuscation

| Benchmark Sample | Condition | Outcome Bucket | I/O Pass Rate | CFG Overlap | Wall Time (s) | Cost ($ USD) | Retry Used |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **sample1_bitmix** | angr-only | Solved | 100.0% (8/8) | 100.0% | 0.082s | $0.0000 | No |
| | LLM-only | Solved | 100.0% (8/8) | 100.0% | 0.019s | $0.0063 | No |
| | **Hybrid (angr+LLM)** | **Solved** | **100.0% (8/8)** | **100.0%** | **0.016s** | **$0.0078** | No |
| **sample2_xtea** | angr-only | Solved | 100.0% (5/5) | 100.0% | 0.074s | $0.0000 | No |
| | LLM-only | Solved | 100.0% (5/5) | 100.0% | 0.017s | $0.0063 | No |
| | **Hybrid (angr+LLM)** | **Solved** | **100.0% (5/5)** | **100.0%** | **0.027s** | **$0.0078** | No |
| **sample3_parser** | angr-only | Solved | 100.0% (6/6) | 100.0% | 0.700s | $0.0000 | No |
| | LLM-only | Solved | 100.0% (6/6) | 100.0% | 0.044s | $0.0063 | No |
| | **Hybrid (angr+LLM)** | **Solved** | **100.0% (6/6)** | **100.0%** | **0.050s** | **$0.0078** | No |
| **sample4_fsm** | angr-only | Solved | 100.0% (8/8) | 100.0% | 0.559s | $0.0000 | No |
| | LLM-only | Solved | 100.0% (8/8) | 100.0% | 0.043s | $0.0063 | No |
| | **Hybrid (angr+LLM)** | **Solved** | **100.0% (8/8)** | **100.0%** | **0.036s** | **$0.0078** | No |