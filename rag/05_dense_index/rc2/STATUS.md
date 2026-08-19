# Dense Index Build RC2

Status: **READY_FOR_EXTERNAL_AUDIT**

RC2 is a `PARENT_FREEZE_LINEAGE_REBIND_ONLY` rebuild. The functional Dense retrieval design remains unchanged from frozen Hybrid Index V4 Design RC9: exact search, no ANN, fixed `candidate_k=40`, cosine on L2-normalized vectors, hard filters before top-k, and deterministic tie-break by cosine descending then `corpus_ordinal` ascending.

## Candidate

- `DIAloga_Dense_Index_Build_RC2_Candidate.zip`
- SHA-256: `f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8`
- Dense index SHA-256: `085215053fa3da335d3f557e644ea33c33c678e47012c4c3d2d12cf9b6fe0198`
- Row map SHA-256: `957afabb965ffca781502ab15063f11930950207d771ed42cc5bcec49c6bcada`
- Vector payload SHA-256: `89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e`
- Parent Production Embeddings Frozen Attestation v2: `1ebb82c73abe68b56fc806b05ef2dfe59b547c1775f9821749a2bb0ba5b7c40f`

Internal gates: validator 88/88 PASS, adversarial 8/8 rejected, 72 conformance fixtures PASS, self-retrieval 1450/1450, deterministic index and deterministic outer ZIP.

## External audit bundle

- `DIAloga_Dense_Index_Build_RC2_External_Audit_Bundle.zip`
- SHA-256: `8e10f52a8ce63db6129969c2fcaf3e4c3ef43ace3448ba1a76ba1260913df662`
- Internal bundle verifier: 49/49 PASS.

## Guard

Historical Dense RC1 remains `HOLD_DO_NOT_AUDIT_DO_NOT_PROMOTE` and its old External Audit Bundle remains `DO_NOT_SEND`. Full Hybrid remains blocked until RC2 receives an external PASS, is freeze-eligible, and a Dense RC2 frozen attestation is issued.
