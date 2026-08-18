#!/usr/bin/env python3
import collections, hashlib, io, json, math, re, types, unicodedata, zipfile
from pathlib import Path

TRAN=str.maketrans({
    "á":"a","à":"a","ä":"a","â":"a",
    "é":"e","è":"e","ë":"e","ê":"e",
    "í":"i","ì":"i","ï":"i","î":"i",
    "ó":"o","ò":"o","ö":"o","ô":"o",
    "ú":"u","ù":"u","ü":"u","û":"u"
})
TOKEN_RE=re.compile(r"[a-z0-9_ñ]+")
SHA256_RE=re.compile(r"^[0-9a-f]{64}$")

TRUST_MANIFEST_FILENAME="runtime_dependency_trust_manifest_rc2.json"
TRUST_MANIFEST_SHA256="e65a3100353778ad35913a8d46663d7a8ae66c74402c05afe93b74dfb861e8f3"
TRUSTED_DEPENDENCIES={"constraint_engine":{"bytes":15941,"sha256":"39f18c9d8d55d2f40b567d20b63d45007bf6e2dc8b48615cf9ca797c8a175d71"},"intent_lane":{"bytes":6696,"sha256":"a11ad47a526328fedf6cc590b0e639aca3bbfb32ec4da66465921215d34e55bb"},"lexical_frozen_attestation":{"bytes":4280,"sha256":"ce49cbdebe04a11e8ef239f2a9156d1ca2eb52063835794ea26880ea0d4e1df9"},"lexical_index":{"bytes":401289,"sha256":"67edda46bb3e0465921c254ae05df4a1b6a30926b6a26f45574b69f97dd2cdac"},"rc4_zip":{"bytes":76570567,"sha256":"f45eb3a90b73dadb14d9c73bc87fde64f1b1a49d298395e93fe8a8e7555214d1"},"rc9_candidate":{"bytes":708462,"sha256":"e7f9eb8da031a56752e89c0cd357aa3dd6a244fac365743b38574fb80a90e8f5"},"request_schema":{"bytes":1486,"sha256":"36b0419500e076e403f77d7858e555f721863e0bac188abe5d67c136be1342ac"},"semantic_domain":{"bytes":81640,"sha256":"1ee298b8710d2f68aeeaf5b4c26e61e7c9e962221d573ddc20d10e3d2e0e5055"},"structured_state_registry":{"bytes":856439,"sha256":"050e375a175565309447312b0531cd237146205b0b1661146722868091f4df5d"}}
REQUIRED_DEPENDENCY_KEYS=frozenset({
    "rc4_zip","rc9_candidate","lexical_index","lexical_frozen_attestation",
    "constraint_engine","request_schema","intent_lane","semantic_domain",
    "structured_state_registry"
})

def _sha256_file(path):
    h=hashlib.sha256()
    with open(path,"rb") as f:
        for block in iter(lambda:f.read(1024*1024),b""):
            h.update(block)
    return h.hexdigest()

def _tokens(text):
    s=unicodedata.normalize("NFC",text).casefold().translate(TRAN)
    s=re.sub(r"[^a-z0-9_ñ]+"," ",s)
    return TOKEN_RE.findall(s)

def _load_constraint_engine_from_bytes(source_bytes):
    mod=types.ModuleType("dialoga_constraint_engine")
    code=compile(source_bytes.decode("utf-8"),"<verified_constraint_engine>","exec")
    exec(code,mod.__dict__)
    return mod

def _validate_embedded_trust_root():
    if set(TRUSTED_DEPENDENCIES)!=REQUIRED_DEPENDENCY_KEYS:
        raise ValueError("TRUST_ROOT_REQUIRED_KEY_SET_MISMATCH")
    if len(TRUSTED_DEPENDENCIES)!=9:
        raise ValueError("TRUST_ROOT_DEPENDENCY_COUNT_MISMATCH")
    for key in sorted(REQUIRED_DEPENDENCY_KEYS):
        item=TRUSTED_DEPENDENCIES.get(key)
        if not isinstance(item,dict) or set(item)!={"sha256","bytes"}:
            raise ValueError(f"TRUST_ROOT_ENTRY_SCHEMA_MISMATCH:{key}")
        if not isinstance(item["sha256"],str) or not SHA256_RE.fullmatch(item["sha256"]):
            raise ValueError(f"TRUST_ROOT_SHA256_MALFORMED:{key}")
        if type(item["bytes"]) is not int or item["bytes"]<=0:
            raise ValueError(f"TRUST_ROOT_BYTES_MALFORMED:{key}")

class FrozenLexicalIndex:
    def __init__(self,index_bytes):
        with zipfile.ZipFile(io.BytesIO(index_bytes)) as z:
            expected={"lexical_stats.json","lexical_documents.jsonl","lexical_postings.jsonl","lexical_index_manifest.json"}
            if set(z.namelist())!=expected:
                raise ValueError("LEXICAL_INDEX_MEMBER_SET_MISMATCH")
            self.stats=json.loads(z.read("lexical_stats.json"))
            self.documents=[json.loads(x) for x in z.read("lexical_documents.jsonl").decode("utf-8").splitlines()]
            rows=[json.loads(x) for x in z.read("lexical_postings.jsonl").decode("utf-8").splitlines()]
            self.terms={r["term"]:r for r in rows}
        self.record_to_ordinal={d["record_id"]:d["corpus_ordinal"] for d in self.documents}
        self.N=self.stats["bm25"]["N"]
        self.avgdl=self.stats["bm25"]["avgdl_tokens"]
        self.k1=self.stats["bm25"]["k1"]
        self.b=self.stats["bm25"]["b"]
        if self.N!=1466 or len(self.documents)!=1466:
            raise ValueError("LEXICAL_INDEX_CARDINALITY_MISMATCH")
        if self.stats["bm25"]["statistics_scope"]!="GLOBAL_FROZEN_LEXICAL_CORPUS":
            raise ValueError("LEXICAL_STATISTICS_SCOPE_MISMATCH")

    def search(self,query_text,eligible_ordinals,top_k=40):
        qterms=list(dict.fromkeys(_tokens(query_text)))
        if not qterms:
            return []
        eligible=set(eligible_ordinals)
        scores=collections.defaultdict(float)
        matched=collections.defaultdict(int)
        for term in qterms:
            row=self.terms.get(term)
            if row is None:
                continue
            df=row["df"]
            idf=math.log(1+(self.N-df+0.5)/(df+0.5))
            for ordinal,tf in row["postings"]:
                if ordinal not in eligible:
                    continue
                dl=self.documents[ordinal]["document_length"]
                score=idf*(tf*(self.k1+1))/(tf+self.k1*(1-self.b+self.b*dl/self.avgdl))
                scores[ordinal]+=score
                matched[ordinal]+=1
        out=[]
        for ordinal,score in scores.items():
            if matched[ordinal]>=1 and score>0:
                d=self.documents[ordinal]
                out.append({
                    "record_id":d["record_id"],
                    "corpus_ordinal":ordinal,
                    "score":score,
                    "matched_query_terms":matched[ordinal]
                })
        out.sort(key=lambda x:(-x["score"],x["corpus_ordinal"]))
        return out[:top_k]

class LexicalRuntimeRetrieverRC2:
    def __init__(self,*,rc4_zip,rc9_candidate,lexical_index_zip,lexical_frozen_attestation,
                 constraint_engine_path,request_schema_path,intent_lane_path,semantic_domain_path,
                 structured_state_registry_path):
        _validate_embedded_trust_root()

        runtime_root=Path(__file__).resolve().parent.parent
        trust_manifest_path=runtime_root/TRUST_MANIFEST_FILENAME
        if not trust_manifest_path.is_file():
            raise ValueError("TRUST_MANIFEST_MISSING")
        try:
            trust_manifest_bytes=trust_manifest_path.read_bytes()
        except Exception as exc:
            raise ValueError("TRUST_MANIFEST_READ_FAILED") from exc
        if hashlib.sha256(trust_manifest_bytes).hexdigest()!=TRUST_MANIFEST_SHA256:
            raise ValueError("TRUST_MANIFEST_SHA256_MISMATCH")
        try:
            trust_manifest=json.loads(trust_manifest_bytes.decode("utf-8"))
        except Exception as exc:
            raise ValueError("TRUST_MANIFEST_INVALID_JSON") from exc
        if trust_manifest.get("required_dependency_count")!=9:
            raise ValueError("TRUST_MANIFEST_DEPENDENCY_COUNT_MISMATCH")
        if set(trust_manifest.get("required_keys",[]))!=REQUIRED_DEPENDENCY_KEYS:
            raise ValueError("TRUST_MANIFEST_REQUIRED_KEY_SET_MISMATCH")
        if trust_manifest.get("dependencies")!=TRUSTED_DEPENDENCIES:
            raise ValueError("TRUST_MANIFEST_EMBEDDED_ROOT_MISMATCH")

        self.rc4_zip=Path(rc4_zip).resolve()
        self.rc9_candidate=Path(rc9_candidate).resolve()
        self.lexical_frozen_attestation=Path(lexical_frozen_attestation).resolve()

        paths={
            "rc4_zip":self.rc4_zip,
            "rc9_candidate":self.rc9_candidate,
            "lexical_index":Path(lexical_index_zip).resolve(),
            "lexical_frozen_attestation":self.lexical_frozen_attestation,
            "constraint_engine":Path(constraint_engine_path).resolve(),
            "request_schema":Path(request_schema_path).resolve(),
            "intent_lane":Path(intent_lane_path).resolve(),
            "semantic_domain":Path(semantic_domain_path).resolve(),
            "structured_state_registry":Path(structured_state_registry_path).resolve(),
        }
        if set(paths)!=REQUIRED_DEPENDENCY_KEYS:
            raise ValueError("RUNTIME_DEPENDENCY_PATH_SET_MISMATCH")

        verified_bytes={}
        for key in sorted(REQUIRED_DEPENDENCY_KEYS):
            path=paths[key]
            if not path.is_file():
                raise ValueError(f"DEPENDENCY_MISSING:{key}")
            expected=TRUSTED_DEPENDENCIES[key]
            try:
                data=path.read_bytes()
            except Exception as exc:
                raise ValueError(f"DEPENDENCY_READ_FAILED:{key}") from exc
            if len(data)!=expected["bytes"]:
                raise ValueError(f"DEPENDENCY_BYTES_MISMATCH:{key}")
            if hashlib.sha256(data).hexdigest()!=expected["sha256"]:
                raise ValueError(f"DEPENDENCY_SHA256_MISMATCH:{key}")
            verified_bytes[key]=data

        att=json.loads(verified_bytes["lexical_frozen_attestation"].decode("utf-8"))
        if att.get("freeze_status")!="FROZEN":
            raise ValueError("LEXICAL_INDEX_NOT_FROZEN")
        if att["frozen_index"]["sha256"]!=TRUSTED_DEPENDENCIES["lexical_index"]["sha256"]:
            raise ValueError("LEXICAL_ATTESTATION_INDEX_BINDING_MISMATCH")
        if att["parent_design_binding"]["design_candidate_sha256"]!=TRUSTED_DEPENDENCIES["rc9_candidate"]["sha256"]:
            raise ValueError("LEXICAL_ATTESTATION_RC9_BINDING_MISMATCH")
        if att["freeze_transition"]["ready_for_runtime_integration"] is not True:
            raise ValueError("RUNTIME_INTEGRATION_NOT_AUTHORIZED")

        self.engine=_load_constraint_engine_from_bytes(verified_bytes["constraint_engine"])
        self.schema=json.loads(verified_bytes["request_schema"].decode("utf-8"))
        self.matrix=json.loads(verified_bytes["intent_lane"].decode("utf-8"))
        self.domain=json.loads(verified_bytes["semantic_domain"].decode("utf-8"))
        self.states=json.loads(verified_bytes["structured_state_registry"].decode("utf-8"))

        with zipfile.ZipFile(io.BytesIO(verified_bytes["rc4_zip"])) as z:
            corpus=z.read("corpus/integrated_canonical_v4_rc1.jsonl")
        self.records=[json.loads(x) for x in corpus.decode("utf-8").splitlines()]
        if len(self.records)!=1466:
            raise ValueError("RC4_CORPUS_CARDINALITY_MISMATCH")
        self.by_id={r["record_id"]:r for r in self.records}

        self.index=FrozenLexicalIndex(verified_bytes["lexical_index"])
        if set(self.by_id)!=set(self.index.record_to_ordinal):
            raise ValueError("INDEX_CORPUS_RECORD_ID_SET_MISMATCH")

    def retrieve(self,query_text,canonical_request,top_k=40):
        if not isinstance(query_text,str) or not query_text.strip():
            return {"status":"INVALID_RUNTIME_REQUEST","errors":["query_text_must_be_nonempty_string"]}
        if type(top_k) is not int or isinstance(top_k,bool) or not (1<=top_k<=40):
            return {"status":"INVALID_RUNTIME_REQUEST","errors":["top_k_must_be_integer_1_to_40"]}

        resolved=self.engine.safe_execute(
            canonical_request,self.schema,self.matrix,self.domain,self.states,self.records
        )
        if resolved.get("status")!="VALID":
            return {
                "status":"NO_RETRIEVAL",
                "constraint_status":resolved.get("status"),
                "errors":resolved.get("errors",[]),
                "lane":resolved.get("lane")
            }

        lane=resolved["lane"]
        candidate_rows=resolved["records"]
        candidate_ids=[r["record_id"] for r in candidate_rows]
        candidate_ordinals=[self.index.record_to_ordinal[rid] for rid in candidate_ids]

        if lane=="structured_exact":
            ordered=sorted(candidate_rows,key=lambda r:self.index.record_to_ordinal[r["record_id"]])
            return {
                "status":"PASS",
                "mode":"STRUCTURED_BYPASS_BM25",
                "lane":lane,
                "candidate_count":len(ordered),
                "result_count":len(ordered),
                "results":[
                    {"record_id":r["record_id"],"corpus_ordinal":self.index.record_to_ordinal[r["record_id"]]}
                    for r in ordered
                ]
            }

        lexical=self.index.search(query_text,candidate_ordinals,top_k=top_k)
        if not lexical:
            return {
                "status":"EMPTY_LEXICAL_LANE",
                "mode":"BM25_WITH_PRE_RANKING_CANDIDATE_UNIVERSE",
                "lane":lane,
                "candidate_count":len(candidate_ordinals),
                "result_count":0,
                "results":[]
            }

        return {
            "status":"PASS",
            "mode":"BM25_WITH_PRE_RANKING_CANDIDATE_UNIVERSE",
            "lane":lane,
            "candidate_count":len(candidate_ordinals),
            "result_count":len(lexical),
            "results":lexical
        }
