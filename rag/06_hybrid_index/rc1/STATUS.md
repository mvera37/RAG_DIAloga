# Full Hybrid RC1

Status: **FROZEN / RUNTIME PROMOTED / APPLICATION WIRING READY**

- Candidate SHA-256: `c7537e8befb53427a8911a4508d3bc68771d617f3630616c3f7ad4ddd0d9f6fc`
- Frozen Attestation v1 SHA-256: `cc5c7929d52f64bda6dce24d82d1fe0c18319c3f021a4d88a89ed7639d5d5971`
- Freeze Completion v1 SHA-256: `6e1afd9c66d9dc219cd3614ec4f0972e7008217e6b460bc8cd78581a5a75457c`
- Freeze validation: **PASS 36/36**.
- Final external gate: **PASS_WITH_NON_BLOCKING_FINDINGS**; freeze eligible and transition authorized.
- Historical `BLOCKED` and `REPAIR_REQUIRED` reports remain preserved. The Unicode diagnostic invalidated `FINDING-HYBRID-CLOSURE-001` as a test-harness encoding defect without changing product bytes.

Runtime promotion is authorized and recorded. `dense` and `hybrid_semantic` may be enabled only under the fail-closed manifest and exact SHA verification. Application Wiring is authorized but not started; it requires the current DIAloga source. Production readiness remains false until application wiring and E2E acceptance are complete.
