#!/usr/bin/env python3
import argparse, hashlib, json, zipfile
from pathlib import Path

AUDITED_VECTOR_SHA="89189e573b7f7818b137bd69d00a0acabbaec0c64a2778d22c9244b432262a6e"
AUDITED_CANDIDATE_SHA="67d0804361c2cb594216c5c33de330cc7c22c5f5988372eabd9988ba8f86ae2a"

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

ap=argparse.ArgumentParser()
ap.add_argument("--fresh-candidate",required=True)
ap.add_argument("--output",required=True)
a=ap.parse_args()

p=Path(a.fresh_candidate).resolve()
with zipfile.ZipFile(p) as z:
    if z.testzip() is not None: raise SystemExit("FRESH_CANDIDATE_CRC_FAIL")
    raw=z.read("data/production_embeddings.f32le")
    manifest=json.loads(z.read("production_embedding_candidate_manifest.json"))

fresh_vector_sha=hashlib.sha256(raw).hexdigest()
evidence={
 "schema_version":"dialoga_production_embeddings_rc2_fresh_regeneration_evidence_v1",
 "fresh_candidate_filename":p.name,
 "fresh_candidate_sha256":sha_file(p),
 "fresh_vector_sha256":fresh_vector_sha,
 "audited_vector_sha256":AUDITED_VECTOR_SHA,
 "vector_byte_identical_to_audited":fresh_vector_sha==AUDITED_VECTOR_SHA,
 "fresh_manifest_release":manifest.get("candidate"),
 "fresh_manifest_status":manifest.get("status"),
 "note":"The audited SHA is a post-generation comparison target, not a shortcut acceptance input to generation."
}
Path(a.output).write_text(json.dumps(evidence,indent=2,sort_keys=True)+"\n",encoding="utf-8")
print(json.dumps(evidence,indent=2))
raise SystemExit(0 if evidence["vector_byte_identical_to_audited"] else 2)
