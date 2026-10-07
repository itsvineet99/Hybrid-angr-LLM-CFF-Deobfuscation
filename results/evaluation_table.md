# Master Evaluation: angr-only vs. LLM-only vs. Hybrid CFF Deobfuscation

Empirical comparison across 7 benchmarks (Core Custom + GNU Coreutils + OpenSSL AES Primitive):

| Benchmark Sample | Category | Condition | Outcome Bucket | I/O Pass Rate | CFG Overlap | Complexity Reduction | Wall Time (s) | Cost ($ USD) |
| :--- | :--- | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **sample1_bitmix** | Custom | angr-only | **Solved** | 100.0% (8/8) | 100.0% | - | 0.075s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/8) | 0.0% | -0.0% (13→0) | 1.223s | $0.0000 |
| | | **Hybrid** | **Partial** | **25.0% (2/8)** | **100.0%** | **-69.2% (13→4)** | **1.239s** | **$0.0000** |
| **sample2_xtea** | Custom | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.068s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/5) | 0.0% | -0.0% (13→0) | 0.548s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-69.2% (13→4)** | **8.183s** | **$0.0000** |
| **sample3_parser** | Custom | angr-only | **Solved** | 100.0% (6/6) | 100.0% | - | 0.627s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/6) | 0.0% | -0.0% (37→0) | 9.403s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (6/6)** | **100.0%** | **-62.2% (37→14)** | **37.028s** | **$0.0000** |
| **sample4_fsm** | Custom | angr-only | **Solved** | 100.0% (8/8) | 100.0% | - | 0.516s | $0.0000 |
| | | LLM-only | **Partial** | 25.0% (2/8) | 45.1% | -77.3% (44→10) | 9.107s | $0.0000 |
| | | **Hybrid** | **Failed-or-timeout** | **0.0% (0/8)** | **0.0%** | **-68.2% (44→14)** | **57.661s** | **$0.0000** |
| **sample5_coreutils_base64** | Coreutils | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.884s | $0.0000 |
| | | LLM-only | **Compiles-but-wrong** | 0.0% (0/5) | 72.0% | -77.4% (31→7) | 17.723s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-71.0% (31→9)** | **32.895s** | **$0.0000** |
| **sample6_coreutils_md5** | Coreutils | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.266s | $0.0000 |
| | | LLM-only | **Solved** | 100.0% (5/5) | 92.9% | -62.5% (16→6) | 11.676s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-68.8% (16→5)** | **32.955s** | **$0.0000** |
| **sample7_crypto_aes** | Crypto | angr-only | **Solved** | 100.0% (5/5) | 100.0% | - | 0.042s | $0.0000 |
| | | LLM-only | **Failed-or-timeout** | 0.0% (0/5) | 0.0% | -0.0% (13→0) | 10.023s | $0.0000 |
| | | **Hybrid** | **Solved** | **100.0% (5/5)** | **100.0%** | **-69.2% (13→4)** | **23.650s** | **$0.0000** |