# Full Hybrid RC1

Status: **BLOCKED BY INITIAL EXTERNAL AUDIT / SUPPLEMENTAL CLOSURE READY FOR EXTERNAL AUDIT / NOT FROZEN / NOT RUNTIME AUTHORIZED**

## Immutable release identity
- Candidate: `DIAloga_Hybrid_Index_V4_Full_Hybrid_RC1_Candidate.zip`
- Candidate SHA-256: `c7537e8befb53427a8911a4508d3bc68771d617f3630616c3f7ad4ddd0d9f6fc`
- Bytes: `1738458`
- Members: `25`
- Artifact class: `QUERY_TIME_FULL_HYBRID_COMPOSITION`

The candidate remains byte-identical. No candidate change is required or authorized to close the current findings.

## Initial external audit
- Report: `DIAloga_Hybrid_Index_V4_Full_Hybrid_RC1_External_Audit_FINAL.md`
- SHA-256: `449eb7a5076fc523b2fee015987ab75490f00553e5ea5825940b8e08aaf78cbf`
- Verdict: **BLOCKED**
- `FULL_HYBRID_BUILD_READY = true`
- `FULL_HYBRID_PRODUCTION_READY = false`
- `FULL_HYBRID_RELEASE_FREEZE_ELIGIBLE = false`

The auditor independently confirmed the Full Hybrid composition boundary, RRF k=60, 41/41 fusion recomputations, deterministic candidate rebuilds, Dense parent, lexical-only preservation at the fusion boundary, and rejection of a coordinated fake PASS. The two blocking findings were release/evidence scope, not a demonstrated fusion defect:

1. `FINDING-HYBRID-001`: physical Lexical Index RC1 and Lexical Runtime RC2 ZIPs were not supplied in the first audit bundle.
2. `FINDING-HYBRID-002`: the original candidate anchor intentionally withheld runtime/freeze authorization before external audit.

`FINDING-HYBRID-003` (unsigned public commit authority) is LOW/non-blocking under the current release contract.

## Supplemental closure package
- Bundle: `DIAloga_Hybrid_Index_V4_Full_Hybrid_RC1_Supplemental_Closure_External_Audit_Bundle.zip`
- SHA-256: `98a9a8742487c6c07fe98e86e3f27e518a84f1a5f2e3641cae3bbb3b2b6569fc`
- Bytes: `105321856`
- Deterministic rebuild: **PASS / byte-identical**
- Closure-bundle verifier: **PASS 88/88** with independently supplied authority and live lexical runtime execution.
- Lexical Runtime RC2 validator re-execution: **PASS 9246/9246**.
- Lexical Runtime RC2 adversarial re-execution: **PASS 36/36**.

The bundle supplies the exact physical Lexical Index RC1 candidate/frozen bundle and Lexical Runtime RC2 candidate/frozen bundle. The Runtime frozen chain contains its original external audit bundle with physical RC4, Design RC9, Lexical Index RC1 and Runtime RC2 evidence.

## Conditional external closure authority
- Repository: `mvera37/RAG_DIAloga`
- Immutable commit: `91b0b691e4efe7668f73b7f8efd9f9b13db63f67`
- Path: `rag/06_hybrid_index/rc1/release_authority/FULL_HYBRID_RC1_CLOSURE_AUTHORIZATION.json`
- Raw-file SHA-256: `b67f6e33a97041ae3329a462e12b2ed9000bc890202961be3e9ced9aad12e2e2`

The auditor must fetch this authority independently from the exact commit. It authorizes a **conditional** release transition: the auditor may return `FULL_HYBRID_PRODUCTION_READY=true` and `FULL_HYBRID_RELEASE_FREEZE_ELIGIBLE=true` only if all blocking findings are closed and no new blocker exists. It does not itself freeze or enable runtime.

## Runtime and freeze gate
`dense` and `hybrid_semantic` remain disabled. Application Wiring remains blocked. A Full Hybrid Frozen Attestation may be issued only after the supplemental external closure audit returns an explicit PASS/freeze-eligible decision.

See `audits/AUDIT_CHAIN.json` for the machine-readable audit history.
