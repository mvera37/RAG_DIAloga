#!/usr/bin/env python3
import argparse, hashlib, json, shutil, zipfile
from pathlib import Path

MODEL_ID='ibm-granite/granite-embedding-311m-multilingual-r2'
REVISION='44399559930365213510b1ee2eb15ded83374f0e'
EXPECTED_ROOT='39f3282103fbafccc288ad3ff8b3717d5266d378f3e684a83587506fdc7473ad'
ORDER=['1_Pooling/config.json', 'config.json', 'config_sentence_transformers.json', 'model.safetensors', 'modules.json', 'README.md', 'sentence_bert_config.json', 'special_tokens_map.json', 'tokenizer.json', 'tokenizer_config.json']
EXPECTED={'1_Pooling/config.json': {'bytes': 313, 'sha256': '781299da695e58439d70d491840da22ea0935d1d57d9646eb9725f1f19754e89'}, 'README.md': {'bytes': 21421, 'sha256': '3c47e61d962601a89027f406fe78f32f9bcdd9c73576c5204b3e70defb3e796b'}, 'config.json': {'bytes': 1191, 'sha256': 'e1e3fc842a8e0537e25d6e4c93879698b92ae96722e8c162bef334b57978a3b0'}, 'config_sentence_transformers.json': {'bytes': 283, 'sha256': 'f09adf93fcf868bb2fc3976a435d810b2ecdffa953d1da091d2a91168abab44b'}, 'model.safetensors': {'bytes': 623341952, 'sha256': 'dcb6431bfa6e817fe100a2b0521360cec3383963b03fa966b685de18ca310d31'}, 'modules.json': {'bytes': 349, 'sha256': '84e40c8e006c9b1d6c122e02cba9b02458120b5fb0c87b746c41e0207cf642cf'}, 'sentence_bert_config.json': {'bytes': 60, 'sha256': '967ef958285e4a7a37d8ff1832473d967edd913b4e48572f31c3d3ea361d5327'}, 'special_tokens_map.json': {'bytes': 694, 'sha256': 'cb9e60dcf4d8d314315cb3e761fe4c2e664fda8dbf66d7815372b2639e381182'}, 'tokenizer.json': {'bytes': 33384821, 'sha256': '0087c868b33bad550a78a08d19798cfd7f713cde4f020803b8f51f405503e15f'}, 'tokenizer_config.json': {'bytes': 1155500, 'sha256': '7947bdf0378520e69ca412b8c4dacd1cffa8aef099f851fdd5c65aa27c6b36a0'}}

def sha_file(p):
    h=hashlib.sha256()
    with open(p,"rb") as f:
        for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
    return h.hexdigest()

def canonical_root(files):
    payload="\n".join(f"{p}\0{files[p]['bytes']}\0{files[p]['sha256']}" for p in ORDER)+"\n"
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--source-model-dir",required=True)
    ap.add_argument("--output-dir",required=True)
    a=ap.parse_args()
    src=Path(a.source_model_dir).resolve()
    out=Path(a.output_dir).resolve()
    out.mkdir(parents=True,exist_ok=True)

    actual={}
    for rel in ORDER:
        p=src/rel
        if not p.is_file(): raise SystemExit("MISSING_MODEL_FILE:"+rel)
        actual[rel]={"bytes":p.stat().st_size,"sha256":sha_file(p)}
        if actual[rel]!=EXPECTED[rel]:
            raise SystemExit("MODEL_FILE_AUTH_FAIL:"+rel)

    root=canonical_root(actual)
    if root!=EXPECTED_ROOT: raise SystemExit("MODEL_ROOT_FAIL:"+root)

    manifest={
      "schema_version":"dialoga_granite311_authenticated_snapshot_rc2_v1",
      "status":"AUTHENTICATED",
      "model_id":MODEL_ID,
      "revision":REVISION,
      "canonical_snapshot_root_sha256":root,
      "ordered_allowlist":ORDER,
      "files":[{"path":p,**actual[p]} for p in ORDER]
    }
    mp=out/"DIAloga_Granite311_Authenticated_Snapshot_RC2.manifest.json"
    mp.write_text(json.dumps(manifest,indent=2,sort_keys=True)+"\n",encoding="utf-8")

    zp=out/"DIAloga_Granite311_Authenticated_Snapshot_RC2.zip"
    with zipfile.ZipFile(zp,"w",compression=zipfile.ZIP_STORED) as z:
        for rel in ORDER:
            zi=zipfile.ZipInfo(rel,date_time=(2020,1,1,0,0,0))
            zi.create_system=0; zi.compress_type=zipfile.ZIP_STORED; zi.external_attr=0
            z.writestr(zi,(src/rel).read_bytes())
        zi=zipfile.ZipInfo(mp.name,date_time=(2020,1,1,0,0,0))
        zi.create_system=0; zi.compress_type=zipfile.ZIP_STORED; zi.external_attr=0
        z.writestr(zi,mp.read_bytes())

    zsha=sha_file(zp)
    (out/(zp.name+".sha256")).write_text(f"{zsha}  {zp.name}\n",encoding="utf-8")
    print(json.dumps({
      "status":"AUTHENTICATED_SNAPSHOT_READY",
      "snapshot_zip":str(zp),
      "snapshot_zip_sha256":zsha,
      "canonical_model_root_sha256":root,
      "model_id":MODEL_ID,
      "revision":REVISION
    },indent=2))
    return 0

if __name__=="__main__":
    raise SystemExit(main())
