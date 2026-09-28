"""Chemistry figure pack (core §7.4, §7.5; plan Task 9.2). Optional dependency group: requirements-chemistry.txt.

Spec files (JSON under <paths.figures>/src/):
  chem.structure  {"kind", "smiles", "name", "pubchem_cid"?}
  chem.reaction   {"kind", "smarts", "name", "conditions"?}   (conditions belong in the caption; not drawn)
RDKit is imported lazily, so the harness runs without it; `preflight()` names what is missing and never installs.
Drawings are deterministic: CoordGen 2D layout, fixed bond length and font size, no timestamps; the PNG is drawn
with Cairo and re-encoded through png.write_canonical.
"""
import pathlib, re

KINDS = {"chem.structure", "chem.reaction"}
CROSSCHECK_KINDS = {"chem.structure"}   # a reaction has no single PubChem compound to compare (ruling in step9-rulings)
REQUIREMENTS = pathlib.Path(__file__).resolve().parents[4] / "requirements-chemistry.txt"
BOND_PX_AT_300DPI = 110
FONT_PX_AT_300DPI = 44
HEIGHT = {"chem.structure": 0.42, "chem.reaction": 0.26}   # canvas height / width


def _pinned():
    if not REQUIREMENTS.is_file():
        return None
    m = re.search(r"^rdkit==(\S+)", REQUIREMENTS.read_text(encoding="utf-8"), re.M)
    return m.group(1) if m else None


def preflight():
    try:
        import rdkit
        from rdkit import Chem
    except ImportError:
        return ["missing Python package: rdkit (optional group; install from requirements-chemistry.txt)"]
    probs = []
    pin = _pinned()
    if pin and _norm(rdkit.__version__) != _norm(pin):
        probs.append(f"rdkit {rdkit.__version__} is installed, requirements-chemistry.txt pins {pin} "
                     "(renders are only byte-stable on the pinned version)")
    if Chem.MolFromSmiles("CCO") is None:
        probs.append("rdkit smoke test CCO failed")
    return probs


def _norm(v):
    return ".".join(str(int(x)) for x in v.split("."))


def versions():
    import rdkit
    return {"rdkit": rdkit.__version__}


def _quiet():
    from rdkit import RDLogger
    RDLogger.DisableLog("rdApp.*")


def _mol(smiles):
    """-> (mol, finding or None)."""
    from rdkit import Chem
    if not isinstance(smiles, str) or not smiles.strip():
        return None, {"id": "CHEM-SMILES-INVALID", "message": "smiles is missing"}
    mol = Chem.MolFromSmiles(smiles, sanitize=False)
    if mol is None:
        return None, {"id": "CHEM-SMILES-INVALID", "message": f"SMILES {smiles!r} does not parse"}
    try:
        Chem.SanitizeMol(mol)
    except Exception as e:   # RDKit raises several sanitisation exception types
        return None, {"id": "CHEM-SANITIZE", "message": f"SMILES {smiles!r} fails sanitisation: {e}"}
    return mol, None


def _reaction(smarts):
    """-> (reaction, finding or None). Every reactant and product must sanitise."""
    from rdkit import Chem
    from rdkit.Chem import AllChem
    bad = {"id": "CHEM-SMARTS-INVALID", "message": f"reaction SMARTS {smarts!r} does not parse"}
    if not isinstance(smarts, str) or ">>" not in smarts and smarts.count(">") != 2:
        return None, bad
    try:
        rxn = AllChem.ReactionFromSmarts(smarts, useSmiles=True)
    except ValueError:
        return None, bad
    if rxn is None or rxn.GetNumReactantTemplates() == 0 or rxn.GetNumProductTemplates() == 0:
        return None, bad
    for m in list(rxn.GetReactants()) + list(rxn.GetProducts()):
        try:
            Chem.SanitizeMol(m)
        except Exception as e:
            return None, {"id": "CHEM-SMARTS-INVALID", "message": f"a molecule of {smarts!r} fails sanitisation: {e}"}
    return rxn, None


def validate(spec):
    """-> [{id, message}] (core §7.5 IDs); empty means the spec can be drawn."""
    _quiet()
    kind = spec.get("kind")
    if kind not in KINDS:
        return [{"id": "CHEM-SMILES-INVALID", "message": f"kind {kind!r} is not a chemistry kind"}]
    name = spec.get("name")
    out = [] if isinstance(name, str) and name.strip() else [
        {"id": "CHEM-SMILES-INVALID" if kind == "chem.structure" else "CHEM-SMARTS-INVALID", "message": "name is missing"}]
    finding = _mol(spec.get("smiles"))[1] if kind == "chem.structure" else _reaction(spec.get("smarts"))[1]
    return out + ([finding] if finding else [])


class ChemistryError(ValueError):
    """Invalid chemistry input at render time (validate() names the check ID)."""


def render(spec, out_svg, out_png, width_cm=14, dpi=300):
    """Deterministic SVG and PNG of a structure or reaction, drawn at the placed width."""
    _quiet()
    from PIL import Image
    import io
    from rdkit.Chem import rdDepictor
    from rdkit.Chem.Draw import rdMolDraw2D
    from harness.figures import png
    problems = validate(spec)
    if problems:
        raise ChemistryError("; ".join(f"{p['id']}: {p['message']}" for p in problems))
    rdDepictor.SetPreferCoordGen(True)
    w = png.width_px(width_cm, dpi)
    h = round(w * HEIGHT[spec["kind"]])
    k = dpi / 300
    if spec["kind"] == "chem.structure":
        target = _mol(spec["smiles"])[0]
        rdDepictor.Compute2DCoords(target)
    else:
        target = _reaction(spec["smarts"])[0]
        for m in list(target.GetReactants()) + list(target.GetProducts()):
            rdDepictor.Compute2DCoords(m)

    def draw(drawer):
        o = drawer.drawOptions()
        o.fixedBondLength = BOND_PX_AT_300DPI * k
        o.fixedFontSize = round(FONT_PX_AT_300DPI * k)
        o.bondLineWidth = max(2, round(4 * k))
        o.clearBackground = True
        if spec["kind"] == "chem.structure":
            drawer.DrawMolecule(target)
        else:
            drawer.DrawReaction(target)
        drawer.FinishDrawing()
        return drawer.GetDrawingText()

    svg = draw(rdMolDraw2D.MolDraw2DSVG(w, h))
    pathlib.Path(out_svg).parent.mkdir(parents=True, exist_ok=True)
    pathlib.Path(out_svg).write_text(svg, encoding="utf-8", newline="\n")
    raw = draw(rdMolDraw2D.MolDraw2DCairo(w, h))
    with Image.open(io.BytesIO(raw)) as im:
        im.load()
        png.write_canonical(im, out_png, dpi)


from harness.figures.packs.chemistry.pubchem import crosscheck  # noqa: E402,F401  (pack interface member)


# ---------- chapter text (plan Task 9b.5): formulas must carry real subscripts ----------

TEXT_IDS = ["CHEM-FORMULA-PLAIN"]
ELEMENTS = set("""H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni Cu Zn Ga Ge As Se Br Kr Rb
Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir
Pt Au Hg Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr""".split())
FORMULA = re.compile(r"(?<![\w~^/.#-])((?:\(?(?:[A-Z][a-z]?\d*)+\)?\d*){1,})(?![\w~^])")
PART = re.compile(r"([A-Z][a-z]?)(\d*)")
DIATOMIC = {"H2", "N2", "O2", "O3", "F2", "Cl2", "Br2", "I2"}


def plain_formulas(text):
    """Formulas written with bare digits (CO2, H2SO4, (NH4)2SO4): every symbol an element, a digit right after one,
    and two or more elements (or a common diatomic). Written CO~2~ they are skipped.
    ponytail: one element with a number (a vitamin 'B12', an ion 'Ca2+') is not flagged; add ions if books need it."""
    out = []
    for m in FORMULA.finditer(text):
        tok = m.group(1)
        body = tok.replace("(", "").replace(")", "")
        parts = PART.findall(body)
        if not all(s in ELEMENTS for s, _ in parts) or not re.search(r"[A-Za-z)]\d", tok):
            continue
        if len(parts) >= 2 or tok in DIATOMIC:
            out.append(tok)
    return out


def check_text(text):
    found = sorted(set(plain_formulas(text)))
    return {"CHEM-FORMULA-PLAIN": [f"formula without subscripts: {f} (write it with ~n~, e.g. CO~2~)" for f in found[:15]]}
