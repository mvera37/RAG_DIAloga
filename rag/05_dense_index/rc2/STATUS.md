# Dense Index Build RC2

Status: **FROZEN**

RC2 is a `PARENT_FREEZE_LINEAGE_REBIND_ONLY` rebuild. The frozen Dense core is unchanged: exact search, no ANN, fixed `candidate_k=40`, cosine on L2-normalized vectors, hard filters before top-k, and deterministic tie-break by cosine descending then `corpus_ordinal` ascending.

## Frozen release identity

- Candidate: `DIAloga_Dense_Index_Build_RC2_Candidate.zip`
- Candidate SHA-256: `f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8`
- Dense index SHA-256: `085215053fa3da335d3f557e644ea33c33c678e47012c4c3d2d12cf9b6fe0198`
- Row map SHA-256: `957afabb965ffca781502ab15063f11930950207d771ed42cc5bcec49c6bcada`
- Vector payload SHA-256: `89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e`
- Parent Production Embeddings Frozen Attestation v2: `1ebb82c73abe68b56fc806b05ef2dfe59b547c1775f9821749a2bb0ba5b7c40f`
- Dense RC2 Frozen Attestation v1 SHA-256: `991dc756d0ba513324ba59e2428e211417009f4b46ea6d936790fa0572416ff3`
- Frozen Attestation publication commit: `a0118f9d6d0addf1448fbd734dcbd8a7b957fb8c`
- Freeze Completion SHA-256: `c86aa65e52ed8b62939917ea45ed63e3c9e187fd9c221ce5e33580ceba5b5405`
- Freeze completion validation: PASS 18/18.

## External audit chain

The first two audit reports remain preserved as historical BLOCKED decisions:

- `DIAloga_Dense_Index_Build_RC2_External_Audit_FINAL.md` — SHA-256 `26405462685cad7265ba4d8b716cc9aeed5e1d84bd924fbff0d8d7db96c7de92`.
- `DIAloga_Dense_Index_Build_RC2_Supplemental_External_Audit_FINAL.md` — SHA-256 `fb2a993716826cb93b8f1582dcf2cd90c0b2d9c3453c83aa39c4a57cbea835c4`.

The closure report is the release-closing decision:

- `DIAloga_Dense_Index_Build_RC2_Closure_External_Audit_FINAL.md`
- SHA-256 `f75c5a9374837211c5ebeee42026d3558e339996ca1ee88ac762ea3522c93116`
- `FINAL_VERDICT = PASS_WITH_NON_BLOCKING_FINDINGS`
- `DENSE_PRODUCTION_READY = true`
- `DENSE_RELEASE_FREEZE_ELIGIBLE = true`
- `ALL_PREVIOUS_BLOCKERS_CLOSED = true`.

The closure auditor independently reproduced the candidate twice byte-identically, fetched the Dense external release anchor from the immutable GitHub commit, and verified that the external anchor rejects a coordinated fake release even when bundle-local validation and packaging components are attacker-controlled.

## External release authority

- Commit: `49b1b255cd34ed1db3a5a28fc8deb11576fcb732`
- Path: `rag/05_dense_index/rc2/release_authority/DENSE_RC2_OFFICIAL_RELEASE_ANCHOR.json`
- Anchor SHA-256: `487ead0654711b94366e3e9d56086deecc0de4573a9a7e6670a28491d9b1b07d`
- Policy: unsigned immutable public GitHub commit pin; signed authority is optional hardening and is not a freeze gate.

## Next gate

Dense RC2 is now a frozen dependency authorized for the **next Full Hybrid build**. This does not mean Full Hybrid is already built or frozen. The Dense and `hybrid_semantic` runtime lanes remain disabled until a new Full Hybrid candidate is built and passes its own required validation/release gates.

## Historical guard

Dense RC1 remains `HOLD_DO_NOT_AUDIT_DO_NOT_PROMOTE`; its old audit bundle remains `DO_NOT_SEND`. Any change to the RC2 candidate, Dense index, row map, parent payload, algorithm, metric or row ordering requires a new release identity and new audit decision.
