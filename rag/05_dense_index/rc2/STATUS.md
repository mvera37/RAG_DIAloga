# Dense Index Build RC2

Status: **READY_FOR_CLOSURE_EXTERNAL_AUDIT / NOT FROZEN**

RC2 is a `PARENT_FREEZE_LINEAGE_REBIND_ONLY` rebuild. The verified Dense core remains unchanged: exact search, no ANN, fixed `candidate_k=40`, cosine on L2-normalized vectors, hard filters before top-k, and deterministic tie-break by cosine descending then `corpus_ordinal` ascending.

## Verified Dense core

- Candidate: `DIAloga_Dense_Index_Build_RC2_Candidate.zip`
- Candidate SHA-256: `f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8`
- Dense index SHA-256: `085215053fa3da335d3f557e644ea33c33c678e47012c4c3d2d12cf9b6fe0198`
- Row map SHA-256: `957afabb965ffca781502ab15063f11930950207d771ed42cc5bcec49c6bcada`
- Vector payload SHA-256: `89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e`
- Parent Production Embeddings Frozen Attestation v2: `1ebb82c73abe68b56fc806b05ef2dfe59b547c1775f9821749a2bb0ba5b7c40f`

External evidence has independently verified the index rebuild byte-identically, row map byte-identically, conformance 72/72, self-retrieval 1450/1450 and auditor-run rejection of the eight declared adversarial manipulations.

## Double external audit result

Both reports remain historical authority and both verdicts are `BLOCKED` for release freeze:

- `DIAloga_Dense_Index_Build_RC2_External_Audit_FINAL.md` SHA-256 `26405462685cad7265ba4d8b716cc9aeed5e1d84bd924fbff0d8d7db96c7de92`.
- `DIAloga_Dense_Index_Build_RC2_Supplemental_External_Audit_FINAL.md` SHA-256 `fb2a993716826cb93b8f1582dcf2cd90c0b2d9c3453c83aa39c4a57cbea835c4`.

The remaining blockers are evidence/trust-chain blockers, not Dense-core defects:

1. deterministic candidate ZIP packaging authority was absent;
2. Dense release authority was not externally pinned, so a coordinated attacker controlling bundle + verifier could construct an internal fake PASS.

## Closure remediation

The original candidate identity was preserved. No new Dense candidate or Dense index was created.

Authoritative deterministic packaging is now recorded under `release_authority/`:

- packaging spec SHA-256: `e9bb633ded2c867d9699f61db5002d6ab9173a988c59ef0dc0b35c33f8aa57f0`;
- authoritative packer SHA-256: `ed7a30bc3936dbc563b0bc88247adcc597be2a24c7a1f612bd76b3d57fdb8370`;
- local closure evidence SHA-256: `85d207ad4f19d8d10dff9b06fcd4e1791a24a72c2f3a4299bafc2a279b3fa005`;
- rebuilt candidate SHA-256: `f45b854796c733affed1811984cdd6ebd061eaf0ec9341e4a4af60bf74df1ea8`, byte-identical to the official candidate.

Dense external release authority is published as a public immutable GitHub commit pin:

- commit: `49b1b255cd34ed1db3a5a28fc8deb11576fcb732`;
- path: `rag/05_dense_index/rc2/release_authority/DENSE_RC2_OFFICIAL_RELEASE_ANCHOR.json`;
- anchor SHA-256: `487ead0654711b94366e3e9d56086deecc0de4573a9a7e6670a28491d9b1b07d`.

The anchor pins the Dense candidate, Dense index, row map, original external audit bundle and deterministic packaging authority. Bundle-local anchor copies are not terminal trust authority; the closure auditor must fetch the anchor independently from the exact commit.

## Closure audit bundle

- `DIAloga_Dense_Index_Build_RC2_Closure_External_Audit_Bundle.zip`
- SHA-256: `d130b209ec45dcbac9e823fd3daf1192f443e9b98844395a7d31a1a29c8786b4`
- Support verifier: PASS 14/14.

Dense remains **NOT FROZEN** and `DENSE_RELEASE_FREEZE_ELIGIBLE=false` until an independent closure audit confirms both blockers are closed. Full Hybrid remains blocked.

## Historical guard

Dense RC1 remains `HOLD_DO_NOT_AUDIT_DO_NOT_PROMOTE`; its old audit bundle remains `DO_NOT_SEND`. Do not modify the verified RC2 Dense index, row map, parent payload or parent frozen attestation to address trust-chain or packaging evidence gaps.
