# Supplemental fresh regeneration procedure

The auditor's FINAL report blocks freeze until a fresh end-to-end regeneration can be independently verified.

Use the already-authenticated Granite311 snapshot matching:
- revision `44399559930365213510b1ee2eb15ded83374f0e`
- canonical root `39f3282103fbafccc288ad3ff8b3717d5266d378f3e684a83587506fdc7473ad`

The auditor should execute the **original RC2 Execution Bundle** and original PREEXECUTION attestation in a clean environment, pointing `SourceModelDir` to the authenticated snapshot.

After the fresh pipeline produces `DIAloga_Production_Embeddings_RC2_Candidate.zip`, run:

```powershell
python .\scripts\verify_fresh_regeneration_result.py `
  --fresh-candidate "C:\PATH\DIAloga_Production_Embeddings_RC2_Candidate.zip" `
  --output ".\fresh_regeneration_evidence.json"
```

The audited vector SHA `89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e` is compared only AFTER generation.

For release unblocking, the auditor should independently record:
1. authenticated snapshot ZIP SHA;
2. canonical model root `39f3282103fbafccc288ad3ff8b3717d5266d378f3e684a83587506fdc7473ad`;
3. fresh candidate SHA;
4. fresh vector SHA;
5. whether fresh vector bytes equal the audited vector bytes;
6. the external publication/signature that anchors `DIAloga_Production_Embeddings_RC2_OFFICIAL_RELEASE_ANCHOR.json`.

RC1 scope invariance is explicitly not a freeze gate for RC2.
