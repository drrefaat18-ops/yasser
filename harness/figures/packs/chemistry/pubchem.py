"""PubChem cross-check of a chem.structure (core §7.5). Stdlib only.

Compares the spec's SMILES with PubChem's record for `pubchem_cid`, else for `name`, both sides canonicalised by
RDKit. A spec that states stereochemistry is compared with PubChem's isomeric SMILES, stereo included (an enantiomer
is a mismatch); a spec without stereo is compared by connectivity. Live mode: one request, timeout 10 s, successful
responses cached under the given cache folder. Offline mode, a network failure or an unreadable answer is
`unverified`, never `pass`. Every judged result carries the request URL, `live`/`cached` and the SHA-256 of the
answer it used, so the build report binds the evidence.
"""
import hashlib, json, pathlib, urllib.parse, urllib.request

BASE = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"
TIMEOUT_S = 10
SMILES_KEYS = ("IsomericSMILES", "SMILES", "CanonicalSMILES", "ConnectivitySMILES")   # PubChem renamed them in 2025
ISOMERIC_KEYS = ("IsomericSMILES", "SMILES")   # old and new name of the SMILES with stereo


def _url(spec):
    if spec.get("pubchem_cid"):
        return f"{BASE}/cid/{int(spec['pubchem_cid'])}/property/IsomericSMILES/JSON"
    return f"{BASE}/name/{urllib.parse.quote(spec['name'], safe='')}/property/IsomericSMILES/JSON"


def _canonical(smiles, stereo):
    from rdkit import Chem
    m = Chem.MolFromSmiles(smiles)
    return None if m is None else Chem.MolToSmiles(m, isomericSmiles=stereo)


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
    smiles = spec.get("smiles") or ""
    ours_flat = _canonical(smiles, False)
    if ours_flat is None:
        return {"status": "fail", "detail": "the spec SMILES does not parse"}
    stereo = _canonical(smiles, True) != ours_flat
    url = _url(spec)
    body, how = _fetch(url, cache_dir)
    if body is None:
        return {"status": "unverified", "detail": how, "url": url}
    ev = {"url": url, "how": how,
          "response_sha256": hashlib.sha256(json.dumps(body, sort_keys=True).encode("utf-8")).hexdigest()}
    try:
        props = body["PropertyTable"]["Properties"][0]
        theirs_raw = next(props[k] for k in (ISOMERIC_KEYS if stereo else SMILES_KEYS) if k in props)
    except (KeyError, IndexError, TypeError, StopIteration):
        why = "no isomeric SMILES to compare stereo with" if stereo else "no SMILES"
        return {"status": "unverified", "detail": f"PubChem answer has {why} ({how})", **ev}
    theirs = _canonical(theirs_raw, stereo)
    if theirs is None:
        return {"status": "unverified", "detail": f"PubChem SMILES {theirs_raw!r} does not parse", **ev}
    if theirs != _canonical(smiles, stereo):
        return {"status": "fail", "detail": f"PubChem {theirs_raw} for {spec.get('name')!r} differs from {smiles}"
                                           + (" (stereo compared)" if stereo else ""), **ev}
    return {"status": "pass", "detail": f"matches PubChem ({how}{', stereo compared' if stereo else ''})", **ev}
