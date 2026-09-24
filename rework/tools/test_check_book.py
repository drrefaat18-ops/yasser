import pathlib, subprocess, sys, textwrap, tempfile

TOOL = pathlib.Path(__file__).with_name("check_book.py")

GOOD = textwrap.dedent("""\
# Chapter 99: Fixture

## Opening Case
Lina asks a chatbot about a mole. She is worried.

## Learning Objectives
1. [LO1] Explain what a **model** is.
2. [LO2] Calculate positive predictive value.
3. [LO3] Identify one risk of a chatbot.

## Core Idea
A model learns patterns from data [1]. Accuracy can mislead [2, 3].

> **Medical Background in 60 Seconds:** A mole is a skin growth.

> **Through Four Lenses**
> - **Medicine:** Doctors read the output with care.
> - **Pharmacy:** Pharmacists check doses with care.
> - **Physical Therapy:** Therapists check movement with care.
> - **Health Sciences:** Technologists check samples with care.

> **Myth vs Evidence:** Myth. Evidence [1].

> **Safety Alert:** Always confirm.

## Key Takeaways
- One.

## Self-Assessment
{mcqs}
**Case Question.** What would you do?

## Answers and Rationales
{answers}

## References
1. Author A. Title. J. 2020. DOI: 10.1000/x1
2. Author B. Title. J. 2021.
3. Author C. Title. J. 2022.
""")

KEYS = "ABCDABCDAC"


def mcqs(keys=KEYS, extra=""):
    qs = "".join(f"**Q{i+1}.** Stem [LO{1 + i % 3}]\nA) a\nB) b\nC) c\nD) d\n{extra}\n" for i in range(len(keys)))
    ans = "".join(f"**Q{i+1}. {k}** — because.\n" for i, k in enumerate(keys))
    return qs, ans


def run(text, glossary="model"):
    d = pathlib.Path(tempfile.mkdtemp())
    (d / "glossary.md").write_text(f"**{glossary.strip()}** — def\n", encoding="utf-8")
    f = d / "ch99.md"
    f.write_text(text, encoding="utf-8")
    r = subprocess.run([sys.executable, str(TOOL), str(f), "--budget", "0", "--glossary", str(d / "glossary.md")],
                       capture_output=True, text=True, encoding="utf-8")
    return r.returncode, r.stdout


def build(keys=KEYS, extra="", body_sub=None):
    q, a = mcqs(keys, extra)
    t = GOOD.format(mcqs=q, answers=a)
    if body_sub:
        assert body_sub[0] in t, body_sub[0]
        t = t.replace(*body_sub)
    return t


def test_good_passes():
    code, out = run(build())
    assert code == 0, out


def test_key_imbalance_fails():
    code, out = run(build(keys="BBBBBBBBBA"))
    assert code == 1 and "key" in out.lower(), out


def test_option_e_fails():
    code, out = run(build(extra="E) e"))
    assert code == 1 and "option e" in out.lower(), out


def test_missing_option_fails():
    code, out = run(build(body_sub=("**Q1.** Stem [LO1]\nA) a\nB) b\nC) c\nD) d\n", "**Q1.** Stem [LO1]\nA) a\nB) b\nC) c\n")))
    assert code == 1 and "q1" in out.lower(), out


def test_uncited_reference_fails():
    code, out = run(build(body_sub=("[2, 3]", "[2]")))
    assert code == 1 and "uncited" in out.lower(), out


def test_citation_range_resolves():
    code, out = run(build(body_sub=("[2, 3]", "[2–3]")))
    assert code == 0, out


def test_bold_label_not_glossary_term_but_real_term_checked():
    code, out = run(build(), glossary="other")
    assert code == 1 and "model" in out and "Medicine" not in out, out


def test_understand_in_lo_fails():
    code, out = run(build(body_sub=("Explain what", "Understand what")))
    assert code == 1 and "understand" in out.lower(), out


def test_lens_imbalance_fails():
    code, out = run(build(body_sub=("Pharmacists check doses with care.", "Yes.")))
    assert code == 1 and "lens" in out.lower(), out


def test_master_slave_fails():
    code, out = run(build(body_sub=("A model learns", "A master-slave model learns")))
    assert code == 1 and "master" in out.lower(), out


if __name__ == "__main__":
    for name, fn in list(globals().items()):
        if name.startswith("test_"):
            fn()
            print("ok", name)
