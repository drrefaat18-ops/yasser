"""Receipt hashing rules (core §2.3)."""
import hashlib, json, pathlib

TEXT_SUFFIXES = {".md", ".txt", ".svg", ".py"}


def canonical_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False).encode("utf-8")


def hash_bytes(data):
    return hashlib.sha256(data).hexdigest()


def hash_file(path):
    path = pathlib.Path(path)
    data = path.read_bytes()
    if path.suffix == ".json":
        return hash_bytes(canonical_json(json.loads(data.decode("utf-8"))))
    if path.suffix in TEXT_SUFFIXES:
        return hash_bytes(data.replace(b"\r\n", b"\n"))
    return hash_bytes(data)
