#!/usr/bin/env python3
"""Authoritative deterministic packer for DIAloga Dense Index Build RC2.
Rebuilds the already-audited RC2 candidate without changing candidate members.
Fails closed on source identity, runtime contract, and final candidate SHA-256.
"""
from __future__ import annotations
import argparse, hashlib, json, platform, zipfile, zlib
from pathlib import Path
EXPECTED_SPEC_SHA256 = "e9bb633ded2c867d9699f61db5002d6ab9173a988c59ef0dc0b35c33f8aa57f0"
def sha256_file(path):
    h=hashlib.sha256()
    with Path(path).open("rb") as f:
        for chunk in iter(lambda:f.read(1024*1024), b""): h.update(chunk)
    return h.hexdigest()
def sha256_bytes(data): return hashlib.sha256(data).hexdigest()
def fail(msg): raise SystemExit("DENSE_RC2_PACKAGING_FAIL:"+msg)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--source-dir",required=True,type=Path); ap.add_argument("--spec",required=True,type=Path); ap.add_argument("--output",required=True,type=Path); a=ap.parse_args()
    if sha256_file(a.spec)!=EXPECTED_SPEC_SHA256: fail("PACKAGING_SPEC_SHA_MISMATCH")
    s=json.loads(a.spec.read_text(encoding="utf-8")); zc=s["zip_contract"]
    if platform.python_implementation()!=zc["python_implementation"]: fail("PYTHON_IMPLEMENTATION_MISMATCH")
    if ".".join(platform.python_version_tuple()[:2])!=zc["python_major_minor"]: fail("PYTHON_MAJOR_MINOR_MISMATCH")
    if zlib.ZLIB_RUNTIME_VERSION!=zc["zlib_runtime_version"]: fail("ZLIB_RUNTIME_VERSION_MISMATCH")
    expected=[m["path"] for m in s["members"]]; actual=sorted(p.relative_to(a.source_dir).as_posix() for p in a.source_dir.rglob("*") if p.is_file())
    if sorted(expected)!=actual: fail("SOURCE_MEMBER_SET_MISMATCH")
    payloads={}
    for m in s["members"]:
        data=(a.source_dir/Path(m["path"])).read_bytes()
        if len(data)!=m["bytes"]: fail("SOURCE_MEMBER_SIZE_MISMATCH:"+m["path"])
        if sha256_bytes(data)!=m["sha256"]: fail("SOURCE_MEMBER_SHA_MISMATCH:"+m["path"])
        payloads[m["path"]]=data
    a.output.parent.mkdir(parents=True,exist_ok=True); tmp=a.output.with_suffix(a.output.suffix+".tmp"); tmp.unlink(missing_ok=True); dt=tuple(zc["timestamp"])
    with zipfile.ZipFile(tmp,"w",compression=zipfile.ZIP_DEFLATED,compresslevel=zc["compresslevel"],strict_timestamps=zc["strict_timestamps"]) as out:
        out.comment=bytes.fromhex(zc["archive_comment_hex"])
        for m in sorted(s["members"],key=lambda x:x["ordinal"]):
            zi=zipfile.ZipInfo(m["path"],date_time=dt); zi.compress_type=zipfile.ZIP_DEFLATED; zi.create_system=zc["create_system"]; zi.create_version=zc["create_version"]; zi.extract_version=zc["extract_version"]; zi.external_attr=zc["external_attr"]; zi.internal_attr=zc["internal_attr"]; zi.flag_bits=zc["flag_bits"]; zi.extra=bytes.fromhex(zc["extra_hex"]); zi.comment=bytes.fromhex(zc["comment_hex"])
            out.writestr(zi,payloads[m["path"]],compress_type=zipfile.ZIP_DEFLATED,compresslevel=zc["compresslevel"])
    actual_sha=sha256_file(tmp); actual_bytes=tmp.stat().st_size
    if actual_sha!=s["expected_candidate_sha256"]: tmp.unlink(missing_ok=True); fail("FINAL_CANDIDATE_SHA_MISMATCH:"+actual_sha)
    if actual_bytes!=s["expected_candidate_bytes"]: tmp.unlink(missing_ok=True); fail("FINAL_CANDIDATE_SIZE_MISMATCH")
    tmp.replace(a.output)
    print(json.dumps({"status":"PASS","candidate_sha256":actual_sha,"candidate_bytes":actual_bytes,"members":len(s["members"]),"python_version":platform.python_version(),"zlib_runtime_version":zlib.ZLIB_RUNTIME_VERSION,"packaging_spec_sha256":EXPECTED_SPEC_SHA256},sort_keys=True))
if __name__=="__main__": main()
