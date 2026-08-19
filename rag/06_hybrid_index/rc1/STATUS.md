# Full Hybrid RC1

Status: **READY_FOR_EXTERNAL_AUDIT / NOT FROZEN / NOT RUNTIME AUTHORIZED**

## Release identity
- Candidate: `DIAloga_Hybrid_Index_V4_Full_Hybrid_RC1_Candidate.zip`
- Candidate SHA-256: `c7537e8befb53427a8911a4508d3bc68771d617f3630616c3f7ad4ddd0d9f6fc`
- Bytes: `1738458`
- Members: `25`
- Artifact class: `QUERY_TIME_FULL_HYBRID_COMPOSITION`

Full Hybrid RC1 does not materialize a static fused index. It deterministically composes the already-frozen lexical and Dense rankings at query time according to the frozen Hybrid Design contract.

## Frozen fusion contract
- RRF `k=60`.
- Lexical `candidate_k=40`.
- Dense `candidate_k=40`.
- Base fused set: top 20.
- Deterministic order: RRF score DESC, lane presence DESC, best lane rank ASC, `corpus_ordinal` ASC.
- `structured_exact` bypasses RRF and must preserve the complete exact set.
- The 16 lexical-only records are protected when they have a positive lexical match.
- Maximum final set: 36 = top-20 base + up to 16 protected lexical-only records.

## Internal gates
- Candidate validator: **PASS 125/125**.
- Adversarial validation: **PASS 8/8**.
- Physical Dense ↔ Production Embeddings ↔ Full Hybrid validation: **PASS 28/28**.
- Candidate deterministic rebuild: **4/4 byte-identical**, including two packaged and two independently implemented rebuilds.
- Audit bundle verifier: **PASS 30/30** in support mode and **PASS 31/31** when an external anchor file is supplied.

A validator weakness discovered during the first internal iteration was fixed before this candidate identity was finalized: rehashing a modified RRF contract could previously evade a subset of semantic checks. The final validator pins the complete fusion contract and other critical authorities by SHA-256. No earlier candidate is release authority.

## External release authority
- Repository: `mvera37/RAG_DIAloga`
- Immutable commit: `9e6a7a5a745095e4e24404ca99d25647ff73b345`
- Path: `rag/06_hybrid_index/rc1/release_authority/FULL_HYBRID_RC1_OFFICIAL_RELEASE_ANCHOR.json`
- Anchor SHA-256: `034e1b95296ba9f971b6fcf1c7522319bc2f04f67b300907f5cca50474e2214a`

The auditor must obtain that anchor independently from the exact commit. A copy included in the audit bundle is not terminal trust authority.

## External audit bundle
- `DIAloga_Hybrid_Index_V4_Full_Hybrid_RC1_External_Audit_Bundle.zip`
- SHA-256: `257fb9876b2ed4ad9e137317ad7eb8540204e6060a96fafd1bf5a78e6fcae5eb`
- Bytes: `23362489`
- Members: `15`

The bundle includes the Full Hybrid candidate, exact frozen Dense and Production Embeddings parent candidates, prior closure reports, physical cross-parent evidence, deterministic rebuild evidence, adversarial results, auditor instructions and a support verifier.

## Runtime and freeze gate
This release is **not frozen**. `dense` and `hybrid_semantic` must remain disabled. Application Wiring remains blocked. A Full Hybrid Frozen Attestation may be created only after an independent external audit returns an explicit release-freeze decision.
