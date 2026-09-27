"""PubChem cross-check of a chem.structure (core §7.5). Stdlib only.

Compares the connectivity (stereo-free canonical SMILES, both sides canonicalised by RDKit) of the spec's SMILES with
PubChem's record for `pubchem_cid`, else for `name`. Live mode: one request, timeout 10 s, successful responses cached
under the given cache folder. Offline mode, a network failure or an unreadable answer is `unverified`, never `pass`.
"""
import hashlib, json, pathlib, urllib.parse, urllib.request

BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"
TIMEOUT_S = 10
SMILES_KEYS = ("CanonicalSMILES", "ConnectivitySMILES", "IsomericSMILES", "SMILES")   # PubChem renamed them in 2025


def _url(spec):
    if spec.get("pubchem_cid"):
        return f"{BASE}/cid/{int(spec['pubchem_cid'])}/property/CanonicalSMILES/JSON"
    return f"{BASE}/name/{urllib.parse.quote(spec['name'], safe='')}/property/CanonicalSMILES/JSON"


def _connectivity(smiles):
    from rdkit import Chem
    m = Chem.MolFromSmiles(smiles)
    return None if m is None else Chem.MolToSmiles(m, isomericSmiles=False)


def _fetch(url, cache_dir):
    """-> (body dict or None, detail). Only a parsed, successful answer is cached."""
    cache = pathlib.Path(cache_dir) / (hashlib.sha256(url.encode("utf-8")).hexdigest() + ".json")
    if cache.is_file():
        try:
            return json.loads(cache.read_text(encoding="utf-8")), "cached"
        except json.JSONDecodeError:
            cache.unlink()
    try:
        with urllib.request.urlopen(url, timeout=TIMEOUT_S) as r:
            body = json.loads(r.read())
    except (OSError, ValueError) as e:   # URLError, timeouts and HTTP errors are OSErrors; bad JSON is a ValueError
        return None, f"PubChem not reached: {type(e).__name__}: {e}"
    cache.parent.mkdir(parents=True, exist_ok=True)
    cache.write_text(json.dumps(body, sort_keys=True), encoding="utf-8", newline="\n")
    return body, "live"


def crosscheck(spec, mode, cache_dir):
    """-> {status: pass | fail | unverified, detail}."""
    if mode not in ("live", "offline"):
        raise ValueError(f"mode must be live or offline, not {mode!r}")
    if mode == "offline":
        return {"status": "unverified", "detail": "offline mode: not checked against PubChem"}
    if not spec.get("pubchem_cid") and not spec.get("name"):
        return {"status": "unverified", "detail": "no name or pubchem_cid to look up"}
    ours = _connectivity(spec.get("smiles") or "")
    if ours is None:
        return {"status": "fail", "detail": "the spec SMILES does not parse"}
    body, how = _fetch(_url(spec), cache_dir)
    if body is None:
        return {"status": "unverified", "detail": how}
    try:
        props = body["PropertyTable"]["Properties"][0]
        theirs_raw = next(props[k] for k in SMILES_KEYS if k in props)
    except (KeyError, IndexError, TypeError, StopIteration):
        return {"status": "unverified", "detail": f"PubChem answer has no SMILES ({how})"}
    theirs = _connectivity(theirs_raw)
    if theirs is None:
        return {"status": "unverified", "detail": f"PubChem SMILES {theirs_raw!r} does not parse"}
    if theirs != ours:
        return {"status": "fail", "detail": f"PubChem {theirs_raw} for {spec.get('name')!r} differs from {spec['smiles']}"}
    return {"status": "pass", "detail": f"matches PubChem ({how})"}
