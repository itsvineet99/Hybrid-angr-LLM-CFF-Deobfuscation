# Week 2 Research Report: angr Walking Skeleton & LLM Agent Scaffold

**Project**: Hybrid angr + LLM CFF Deobfuscation (Academic Final Year Project)  
**Date**: September 2026  
**Status**: Week 2 Deliverables Complete  

---

## 1. Executive Summary

Week 2 established the core technical walking skeleton:
1. End-to-end implementation of the **angr symbolic dispatcher-recovery pipeline** against Tigress's Flatten pattern.
2. Serialization of intermediate binary analysis artifacts into a standardized JSON schema (capturing dispatcher address, latch node, per-block state expressions, and concrete I/O pairs).
3. Design and implementation of the **LLM agent binary tool environment** (`get_block`, `get_successors`, `get_xrefs`, `run_with_input`).
4. Smoke-testing of the symbolic execution and agent tools on `sample1_bitmix`.

---

## 2. Reverse Engineering Tigress Flatten Dispatcher Structure

Disassembly of Tigress Flatten binaries on ARM64 revealed a predictable three-component pattern:

### 2.1 Prologue and Initial State Injection
```assembly
0x1000005f8: sub sp, sp, #0x20
0x1000005fc: str w0, [sp, #0x1c]       ; Preserve input argument
0x100000600: mov x8, #3                ; Initial state value = 3
0x100000604: str x8, [sp, #0x10]       ; Store state variable on stack (sp+0x10)
0x100000608: b   #0x10000060c          ; Direct branch to dispatcher cascade
```

### 2.2 Dispatcher Cascade
Rather than a single indirect jump table, Tigress emits a cascade of linear comparison blocks:
```assembly
0x10000060c: ldr  x8, [sp, #0x10]      ; Load state variable
0x100000614: cbz  x8, #0x100000728     ; If state == 0 -> Handler 0
0x10000061c: subs x8, x8, #1
0x100000624: b.eq #0x100000698         ; If state == 1 -> Handler 1
0x10000062c: subs x8, x8, #2
0x100000634: b.eq #0x100000788         ; If state == 2 -> Handler 2
...
```

### 2.3 Handler Execution & Latch Node
Each basic block executes program statements, writes the next state value to `[sp, #0x10]`, and branches to the central **latch node** (`0x1000007bc`), which loops back to `0x10000060c`.

---

## 3. angr Symbolic Execution Algorithm

The dispatcher-recovery algorithm executes as follows:
1. **Dispatcher & Latch Identification**:
   - Compute in-degrees across all nodes in `func.transition_graph`.
   - The latch node $L$ is uniquely identified as $\arg\max_{n} \text{in\_degree}(n)$.
   - The dispatcher $D$ is the unique successor of $L$.
2. **State Variable Tracking**:
   - Trace the prologue write to determine stack offset (`0x10`) and initial state.
3. **Symbolic Exploration per Handler**:
   - Initialize a `blank_state` at the handler entry address with valid stack pointer `regs.sp = 0x7fff0000`.
   - Use `simulation_manager.explore(find=L.addr, num_find=5)`.
   - On reaching latch $L$, evaluate `state.mem[0x7fff0000 + 0x10].uint64_t.resolved`.
   - Use Z3 solver (`s.solver.eval_upto(next_state, 5)`) to recover all reachable next state constants.
   - Detect terminal exit blocks by checking for `ret` instructions.

---

## 4. Intermediate JSON Artifact Schema

The intermediate representation is saved for every function regardless of whether it solves fully, enabling reuse as context in the Hybrid pipeline:

```json
{
  "function": "sample1_bitmix",
  "dispatcher_addr": "0x10000060c",
  "latch_addr": "0x1000007bc",
  "initial_state": 3,
  "blocks": [
    {
      "addr": "0x1000006bc",
      "entry_state": "0x1000006bc",
      "next_state_expr": "state=5",
      "next_states": [5],
      "status": "solved"
    },
    {
      "addr": "0x100000700",
      "entry_state": "0x100000700",
      "next_state_expr": "state=2, state=7",
      "next_states": [2, 7],
      "status": "solved"
    },
    {
      "addr": "0x10000068c",
      "entry_state": "exit",
      "next_state_expr": "EXIT",
      "status": "solved"
    }
  ],
  "concrete_io_pairs": [
    {"input": ["0"], "output": "0x9A921618"},
    {"input": ["1"], "output": "0xAFEBA9FA"}
  ],
  "solve_status": "solved",
  "latency_seconds": 0.065
}
```

---

## 5. LLM Agent Scaffold & Tool Interface

To facilitate autonomous decompilation, an interactive binary environment was built in `pipeline/llm_agent.py` exposing four core reverse engineering tools:

1. `get_block(addr)`: Disassembles the machine instructions at `addr`.
2. `get_successors(addr)`: Queries the CFG transition graph for outgoing edges.
3. `get_xrefs(addr)`: Identifies all incoming branch references / predecessors.
4. `run_with_input(args)`: Executes the compiled binary dynamically with concrete arguments.

Smoke tests verified that the agent environment can successfully query blocks, trace edges through the CFG, and execute concrete test inputs on Apple Silicon.
